from . import cv2
from . import np
from . import os
from . import pickle
from . import tk
from . import simpledialog

class face_recog:
    def __init__(self):
        # Constraints
        self.DATA_PATH = None
        self.SIMILARITY_THRESHOLD = None
        self.REGISTRATION_THRESHOLD = None
        self.label_map = None
        self.label_map_pkl_path = None
        # Face Recognizer using LBPH
        self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.trained = False

        # Haar Cascade
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    def set_face_data_path(self, data_path:str):
        self.DATA_PATH = data_path

    def set_similarity_threshold(self, similarity_threshold):
        self.SIMILARITY_THRESHOLD = similarity_threshold

    def set_registration_threshold(self, registration_threshold):
        self.REGISTRATION_THRESHOLD = registration_threshold

    def set_label_pckl_file_path(self,pickle_path:str):
        self.label_map_pkl_path = pickle_path

    def load_label_map(self):
        if self.label_map_pkl_path is None:
            print("[INFO] Enter path for label map pkl file.")
            return
        
        with open(self.label_map_pkl_path,"rb") as f:
            self.label_map = pickle.load(f)

    def create_face_directory(self):
        if self.DATA_PATH is not None:
            os.makedirs(self.DATA_PATH,exist_ok=True)
        else:
            print("[INFO] Please set the data path")

    def register_face(self, frame):
        if self.REGISTRATION_THRESHOLD is None:
            print("[INFO] Set Registeration Threshold")
            return
        
        if self.DATA_PATH is None:
            print("[INFO] Set DATA Path first")
            return
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60,60))
        if len(faces) == 0:
            print("[WARNING] No faces detected during registration")
            return False

        x, y, w, h = faces[0]
        face = gray[y:y+h,x:x+w]
        face_resized = cv2.resize(face,(200,200))

        if self.trained:
            label_id, confidence = self.face_recognizer.predict(face_resized)
            if confidence < self.REGISTRATION_THRESHOLD:
                print("[WARNING] This face is already registered.")
                return False
            
        # Save image for training
        label = self.get_sr_number_from_gui()
        
        if label:
            face_path = os.path.join(self.DATA_PATH, f"{label}.png")
            cv2.imwrite(face_path,face_resized)
            cv2.imshow("Registered Face", face_resized)
            print(f"[INFO] New Face Registered as '{label}'")
            cv2.waitKey(2000) #wait for 200 ms
            cv2.destroyWindow("Registered Face")
            return True
        else:
            print(f"[INFO] No input for label given")
            return False

    def get_sr_number_from_gui(self):
        # Function to create the Tkinter GUI and return the input value
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        # Use a simple dialog to ask for the SR Number
        label = simpledialog.askstring("SR Number", "Please enter the SR Number:", parent=root)
        
        root.destroy()  # Close the Tkinter window after input
        return label

    
    def train_recognizer(self):
        if self.DATA_PATH is None:
            print("[INFO] Set the data path first")
            return
        if self.label_map_pkl_path is None:
            print("[INFO] Enter path for label map pkl file.")
            return
        
        images, labels = [], []
        label_map = {}

        # Get all the labels and images for training
        for idx, filename in enumerate(os.listdir(self.DATA_PATH)):
            if filename.endswith(".png"):
                filepath = os.path.join(self.DATA_PATH,filename)
                label = os.path.splitext(filename)[0]
                img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
                images.append(img)
                labels.append(idx)
                label_map[idx] = label

        # Train the recognizer with labels if available

        if images and labels:
            self.face_recognizer.train(images,np.array(labels))
            with open(self.label_map_pkl_path,"wb") as f:
                pickle.dump(label_map,f)
            
            self.trained = True
            self.load_label_map()
            print("[INFO] Training Complete with labels:", label_map)
        
        else:
            self.trained = False
            print("[INFO] No images to train on")

    def recognize_face(self, frame):
        if not self.trained:
            # print("[DEBUG] Model has not been trained yet")
            return "Unkown", None
        if self.SIMILARITY_THRESHOLD is None:
            print("[INFO] Set similarity threshold")
            return
        
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60,60))

            if len(faces) == 0:
                return "Unkown", None
            
            for (x,y,w,h) in faces:
                face = gray[y:y+h, x:x+w]
                face_resized = cv2.resize(face, (200,200))

                # Predict using the recognizer
                label_id, confidence = self.face_recognizer.predict(face_resized)

                if confidence<self.SIMILARITY_THRESHOLD:
                    label = self.label_map.get(label_id, "Unkown")
                    # print("[DEBUG] Recognized label '{label}' with confidence '{confidence}'")

                    # Draw a bound box
                    cv2.rectangle(frame,(x,y),(x+w,y+h), (255,0,0),2)
                    cv2.putText(frame, f"{label} ({confidence:.2f})",(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,0,0),2)

                    return label, confidence
                
                else:
                    # print("[DEBUG] Recognized confidence too low: '{confidence}'")

                    cv2. rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
                    cv2.putText(frame, "Unkown", (x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)

                    return "Unkown", None
        except cv2.error as e:
            print("[ERROR] Face Recognition failed: ",e)
            return "Unkown", None