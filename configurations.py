# --------------------------------------------------------------------
# CONTRAINTS FOR IMAGE PROCESSING AND FACE RECOGNITION
# --------------------------------------------------------------------

FACE_DATA_PATH = "/home/iot/Desktop/Library_management_system/identify_face/face_data"
SIMILARITY_THRESHOLD = 50
REGISTRATION_THRESHOLD = 50

LABEL_PICKLE_FILE ="database/label_map.pkl"

# ---------------------------------------------------------------------



# --------------------------------------------------------------------
# CONTRAINTS FOR MQTT
# --------------------------------------------------------------------

BROKER_IP = '10.114.241.13'
USERNAME = 'username'
PASSWORD = 'password'
PORT = 1883
BOOK_LIMIT = 3

MAIN_TOPIC = 'library'

DUMMY_BOOK_PAYLOAD = ["ESE000086","ESE000087"]
# ---------------------------------------------------------------------

# --------------------------------------------------------------------
# CONTRAINTS FOR BOOKCODE READING
# --------------------------------------------------------------------

NO_DETECTION_LIMIT = 100
NO_DETECTION_FRAMES = 0


# ---------------------------------------------------------------------
# --------------------------------------------------------------------
# CAMERA SPECIFICATIONS
# --------------------------------------------------------------------

CAMERA_WIDTH = int(640)
CAMERA_HEIGHT = int(480)
CAMERA_PARAM_FILE = 'barcode/camera_params.npz'

PERSON_WIDTH = int(20)
PERSON_HEIGHT = int(20)

LIBRARY_X = int(10)
LIBRARY_Y = int(50)

PERSON_X = LIBRARY_X + CAMERA_WIDTH
PERSON_Y = LIBRARY_Y

REGISTER_X = int(10)
REGISTER_Y = int(LIBRARY_X+CAMERA_HEIGHT)

CAMERA_DEVICE = 0

# ---------------------------------------------------------------------