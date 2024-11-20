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

BROKER_IP = 'test.mosquitto.org'
USERNAME = 'username'
PASSWORD = 'password'
PORT = 1884
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

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_PARAM_FILE = 'barcode/camera_params.npz'

PERSON_WIDTH = 20
PERSON_HEIGHT = 20

LIBRARY_X = 10
LIBRARY_Y = 10

PERSON_X = LIBRARY_X + CAMERA_WIDTH
PERSON_Y = LIBRARY_Y

REGISTER_X = LIBRARY_X
REGISTER_Y = LIBRARY_Y + CAMERA_HEIGHT

CAMERA_DEVICE = 0

# ---------------------------------------------------------------------