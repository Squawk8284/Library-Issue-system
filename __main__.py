from identify_face import *
from mqtt import *
from barcode import *
import configurations as cfg


def clean_screen():
    os.system('clear')


def print_issued_books(mqtt_object, label):
    book_code = []
    sub_msg = mqtt_object.subscribe_to_topic(topic_name=f"{cfg.MAIN_TOPIC}/{label}")
    if sub_msg != None:
        book_code, _, return_date = mqtt_object.extract_book_details(sub_msg)
        if book_code:
            print("*************")
            print(f"{label}")
            print(f"Issued Books: {book_code}")
            print(f"Return dates: {return_date}")
            print("*************\n\n")


def face_setup(face_recognition_object):
    face_recognition_object.set_face_data_path(cfg.FACE_DATA_PATH)
    face_recognition_object.set_registration_threshold(cfg.REGISTRATION_THRESHOLD)
    face_recognition_object.set_similarity_threshold(cfg.SIMILARITY_THRESHOLD)
    face_recognition_object.set_label_pckl_file_path(cfg.LABEL_PICKLE_FILE)

    face_recognition_object.create_face_directory()


def mqtt_setup(mqtt_object):
    mqtt_object.set_mqtt_broker(cfg.BROKER_IP)
    mqtt_object.set_mqtt_password(cfg.PASSWORD)
    mqtt_object.set_mqtt_port(cfg.PORT)
    mqtt_object.set_mqtt_username(cfg.USERNAME)
    mqtt_object.connect_mqtt()

def barcode_setup(barcode_object):
    barcode_object.set_no_detection_frames(cfg.NO_DETECTION_FRAMES)
    barcode_object.set_no_detection_limit(cfg.NO_DETECTION_LIMIT)
    barcode_object.set_camera_params(cfg.CAMERA_PARAM_FILE)




def main(cap):
    face_recognition_object = face_recog()
    mqtt_object = mqtt_paho()
    barcode_object = barcode()

    face_setup(face_recognition_object)
    mqtt_setup(mqtt_object)
    barcode_setup(barcode_object)

    
    if not cap.isOpened():
        print("[ERROR] Unable to open video")
        return
    
    face_recognition_object.train_recognizer()
    print("[INFO] Press 'r' to register a new face")

    prev_label =None
    run = True

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame,1)
        label, _ =face_recognition_object.recognize_face(frame)
        
        cv2.namedWindow("Library system", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Library system", cfg.CAMERA_WIDTH, cfg.CAMERA_HEIGHT)
        cv2.moveWindow("Library system",cfg.LIBRARY_X, cfg.LIBRARY_Y)
        cv2.imshow("Library system", frame)

        if label != "Unkown" and label!=prev_label and run:

            person = cv2.imread(os.path.join(cfg.FACE_DATA_PATH, f"{label}.png"))
            cv2.resizeWindow("Person", cfg.PERSON_WIDTH, cfg.PERSON_HEIGHT)
            cv2.moveWindow("Person",cfg.PERSON_X, cfg.PERSON_Y)
            cv2.imshow("Person", person)
            
            clean_screen()
            print_issued_books(mqtt_object, label)

            time.sleep(1)
            detected_codes = barcode_object.detect_bookcodes(cap)

            book_code = []
            issue_date = []
            return_date = []
            return_book = []

            if detected_codes != []:
                issuing_date = datetime.now().strftime("%d-%m-%Y %H:%M:%s")  # Current date as Issue Date
                returning_date = (datetime.now() + timedelta(days=5)).strftime("%d-%m-%Y %H:%M:%s")  # Return Date = 5 days after Issue Date

                sub_msg = mqtt_object.subscribe_to_topic(topic_name=f"{cfg.MAIN_TOPIC}/{label}")
                if sub_msg != None:
                    book_code, issue_date, return_date = mqtt_object.extract_book_details(sub_msg)
                    if book_code:
                        for code in detected_codes:
                            for book in book_code:
                                if book == code:
                                    index = book_code.index(book)
                                    return_book.append(book)
                                    book_code.pop(index)
                                    issue_date.pop(index)
                                    return_date.pop(index)
                                    break
                
                for code in return_book:
                    index = detected_codes.index(code)
                    detected_codes.pop(index)
                
                for code in detected_codes:
                    if code not in book_code:
                        book_code.append(code)
                        issue_date.append(issuing_date)
                        return_date.append(returning_date)
                               
                

                if len(book_code)>cfg.BOOK_LIMIT:
                    print("[INFO] Limit of books Crossed")
                    label = "Unkown"
                    continue

                msg = mqtt_object.message_book_code(book_code,issue_date,return_date)
                mqtt_object.publish_message(topic=f"{cfg.MAIN_TOPIC}/{label}",message=str(msg))

                clean_screen()
                print("*************")
                print("Person issued: ", f"{label}")
                print("*************")
                print("Issued books: ", book_code)
                print("Return Dates: ", return_date)
                print("*************")
                print("Returned books: ", return_book)
                print("*************")
            
            cv2.destroyWindow("Person")
            time.sleep(1)

        
        # Capture Events
        key = cv2.waitKey(1) & 0xFF

        if key == ord('r'):
            # Register a new face
            if face_recognition_object.register_face(frame):
                face_recognition_object.train_recognizer()
        elif key == ord('q'):
            break
        elif key == ord('u'):
            run = not run
        


if __name__ == "__main__":
    try:
        cap = cv2.VideoCapture(cfg.CAMERA_DEVICE, cv2.CAP_V4L2)
        main(cap)
    
    except Exception as e:
        print("Exception occured: ",e)
    
    except KeyboardInterrupt:
        print("Keyboard Interrupt Occured")

    finally:
        print("Shutting down the server....")
        cap.release()
        cv2.destroyAllWindows()
        