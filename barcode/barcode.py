from . import cv2
from . import decode, ZBarSymbol
from . import np
from . import cfg


class barcode:
    def __init__(self):
        self.new_book_codes = None
        self.detected_codes = set()
        self.no_detection_limit = None
        self.no_detection_frames = None
        self.limit_numer = None
        self.frame_number = None
        self.loaded_params = None
        self.intrinsic_matrix = None
        self.distortion_parameters = None
    
    def set_camera_params(self,file_path):
        self.loaded_params = np.load(cfg.CAMERA_PARAM_FILE)
        self.intrinsic_matrix = self.loaded_params['Intrinsic']
        self.distortion_parameters = self.loaded_params['Distortion']

    def set_no_detection_frames(self, number):
        self.no_detection_frames = int(number)
        self.frame_number = int(number)
    
    def set_no_detection_limit(self, number):
        self.no_detection_limit = int(number)
        self.limit_numer = int(number)

    def undistort_frame(self,frame):
        h, w = frame.shape[:2]
        new_mtx, roi = cv2.getOptimalNewCameraMatrix(self.intrinsic_matrix, self.distortion_parameters, (w, h), 1, (w, h))
        undistorted_frame = cv2.undistort(frame, self.intrinsic_matrix, self.distortion_parameters, None, new_mtx)
        
        # Optionally crop the image based on the ROI
        x, y, w, h = roi
        undistorted_frame = undistorted_frame[y:y+h, x:x+w]
        
        return undistorted_frame

    
    def rotate_image(self, image, angle):
        h, w = image.shape[:2]
        center = (w // 2, h // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated_image = cv2.warpAffine(image, rotation_matrix, (w, h))
        return rotated_image

    def preprocess_image_for_barcode(self, image):
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply CLAHE to enhance contrast
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced_gray = clahe.apply(gray)
        
        # Apply adaptive thresholding to emphasize the barcode
        adaptive_thresh = cv2.adaptiveThreshold(
            enhanced_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 9, 10
        )

        return adaptive_thresh
    
    def detect_and_decode_barcode(self, image, detected_codes, allowed_types=[ZBarSymbol.I25]):
        image = self.preprocess_image_for_barcode(image)
        barcodes = decode(image, symbols= allowed_types)

        self.new_book_codes = []

        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")
            final_barcode_data = f"ESE{barcode_data}"

            if final_barcode_data not in detected_codes:
                detected_codes.add(final_barcode_data)
                self.new_book_codes.append(final_barcode_data)
        
        return self.new_book_codes
    
    def detect_bookcodes(self, cap):
        if None in (self.no_detection_frames, self.no_detection_limit):
            print("[INFO] Set the no detection limit")
            return
        
        if None in self.loaded_params:
            print("[INFO] Set the Camera Parameters")
            return
        
        self.set_no_detection_frames(self.frame_number)
        self.set_no_detection_limit(self.limit_numer)

        self.detected_codes = set()

        while True:
            ret, frame = cap.read()
            if not ret:
                print("[INFO] Error: Could not open frame")
                break
            
            frame = self.undistort_frame(frame)

            self.new_book_codes = self.detect_and_decode_barcode(frame,self.detected_codes)

            if not self.new_book_codes:
                for angle in range(45,315,45):
                    rotated_frame = self.rotate_image(frame, angle)
                    rotated_code = self.detect_and_decode_barcode(rotated_frame, self.detected_codes)
                    if rotated_code:
                        self.new_book_codes +=rotated_code
                        break
            
            frame = cv2.flip(frame,1)
            frame = cv2.putText(frame,f"{self.detected_codes}",(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 2)
            cv2.namedWindow("Registering Books", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Registering Books", cfg.CAMERA_WIDTH, cfg.CAMERA_HEIGHT)
            cv2.moveWindow("Registering Books", cfg.REGISTER_X, cfg.REGISTER_Y)
            cv2.imshow("Registering Books", frame)

            if not self.new_book_codes:
                self.no_detection_frames +=1
            else:
                self.no_detection_frames = 0

            
            if self.no_detection_frames >= self.no_detection_limit:
                break
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cv2.destroyWindow("Registering Books")

        return list(self.detected_codes)

        

if __name__ == "__main__":
    try:
        bookcode = barcode()
        bookcode.set_no_detection_frames(0)
        bookcode.set_no_detection_limit(1000)
        cap = cv2.VideoCapture(1)
        books = bookcode.detect_bookcodes(cap)
        print(books)

    except Exception as e:
        print("Exception: ", e)
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
