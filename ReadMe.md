
# Library Management System with Face Recognition and MQTT Integration

This project is a library management system that uses face recognition for identifying users, MQTT for communication, and barcode detection for managing book issuances and returns. The system provides a user-friendly interface to register faces, issue books, and monitor return dates.

## Features
- **Face Recognition**: Identify users using face recognition with OpenCV's LBPH face recognizer.
- **Barcode Scanning**: Detect and track barcode IDs for books.
- **MQTT Integration**: Use MQTT protocol to publish and subscribe to topics for issuing books and tracking return dates.
- **Real-time Alerts**: Display issued books and their return dates on the screen.

## Requirements

### Software Dependencies
- **Python**: v3.7 or higher
- **OpenCV**: For face detection and recognition
- **paho-mqtt**: For MQTT client functionality
- **numpy**: For handling image data
- **pickle**: For saving and loading the face label map
- **datetime**: For managing issue and return dates

You can install the necessary Python libraries using the following command:

```bash
pip install opencv-python numpy paho-mqtt
```

### Hardware Requirements
- **Camera**: A webcam for face and barcode detection.
- **Barcode Scanner** (optional): If you're using a physical scanner to read book barcodes.

---

## Configuration

### Configuration File (`configurations.py`)
This file contains various configuration settings that control the behavior of the system.

1. **Face Recognition Settings**:
   - `FACE_DATA_PATH`: Path to store face data for training the recognizer.
   - `SIMILARITY_THRESHOLD`: Threshold for face similarity during recognition.
   - `REGISTRATION_THRESHOLD`: Threshold to determine if a new face should be registered.
   - `LABEL_PICKLE_FILE`: Path to save the label map of registered users.

2. **MQTT Settings**:
   - `BROKER_IP`: IP address of the MQTT broker.
   - `USERNAME` and `PASSWORD`: MQTT credentials.
   - `PORT`: Port for MQTT communication.
   - `BOOK_LIMIT`: Maximum number of books a user can issue at once.
   - `MAIN_TOPIC`: The base MQTT topic for the library.
   - `DUMMY_BOOK_PAYLOAD`: List of dummy book codes to simulate book data.

3. **Barcode Reading Settings**:
   - `NO_DETECTION_LIMIT`: Maximum number of frames before barcode detection is considered unsuccessful.
   - `NO_DETECTION_FRAMES`: Number of frames without barcode detection before triggering an action.

4. **Camera Settings**:
   - `CAMERA_WIDTH` and `CAMERA_HEIGHT`: Resolution of the camera feed.
   - `CAMERA_PARAM_FILE`: Path to the camera parameters file.
   - `PERSON_WIDTH` and `PERSON_HEIGHT`: Dimensions for displaying the person's image on the window.
   - `LIBRARY_X` and `LIBRARY_Y`: Position to place the library video window on the screen.
   - `PERSON_X` and `PERSON_Y`: Position for the person window displaying the recognized face.
   - `REGISTER_X` and `REGISTER_Y`: Position for the registration window.
   - `CAMERA_DEVICE`: The device index for the camera.

### Example Configuration:
```python
# --------------------------------------------------------------------
# CONTRAINTS FOR IMAGE PROCESSING AND FACE RECOGNITION
# --------------------------------------------------------------------
FACE_DATA_PATH = "/home/iot/Desktop/Library_management_system/identify_face/face_data"
SIMILARITY_THRESHOLD = 50
REGISTRATION_THRESHOLD = 50
LABEL_PICKLE_FILE = "database/label_map.pkl"

# ---------------------------------------------------------------------
# CONTRAINTS FOR MQTT
# ---------------------------------------------------------------------
BROKER_IP = '10.114.241.13'
USERNAME = 'username'
PASSWORD = 'password'
PORT = 1883
BOOK_LIMIT = 3
MAIN_TOPIC = 'library'
DUMMY_BOOK_PAYLOAD = ["ESE000086", "ESE000087"]

# ---------------------------------------------------------------------
# CONTRAINTS FOR BOOKCODE READING
# ---------------------------------------------------------------------
NO_DETECTION_LIMIT = 100
NO_DETECTION_FRAMES = 0

# ---------------------------------------------------------------------
# CAMERA SPECIFICATIONS
# ---------------------------------------------------------------------
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_PARAM_FILE = 'barcode/camera_params.npz'

PERSON_WIDTH = 20
PERSON_HEIGHT = 20
LIBRARY_X = 10
LIBRARY_Y = 50
PERSON_X = LIBRARY_X + CAMERA_WIDTH
PERSON_Y = LIBRARY_Y

REGISTER_X = 10
REGISTER_Y = LIBRARY_X + CAMERA_HEIGHT

CAMERA_DEVICE = 0
```

---

## Setup & Implementation Steps

### Step 1: Prepare the Environment
- Install dependencies using pip:
  ```bash
  pip install opencv-python numpy paho-mqtt
  ```
- Ensure you have a **webcam** connected for capturing faces and barcodes.

### Step 2: Configuration
- Update the `configurations.py` file with your MQTT details, camera settings, and other parameters.
- Set the paths for face data and the label pickle file.

### Step 3: Run the Script
1. **Face Registration**: 
   - On the first run, the system will ask you to register faces. Press `r` to register a new face.
   - Enter the SR Number when prompted by the GUI.

2. **Main Operation**:
   - Once faces are registered, the system will continuously check for faces and issue books.
   - When a face is recognized, the system will subscribe to the MQTT topic related to that user and show their issued books with return dates.
   - Barcode scanning is done in real-time to track books being issued or returned.
   - Press `q` to quit the application, or `u` to toggle the system’s operation.

### Step 4: Start the Application
Run the main script using:
```bash
python __main__.py
```

---

## How the System Works

1. **Face Recognition**:
   - The system captures the face and compares it with the registered faces in the database.
   - If a match is found, it fetches the user’s issued book details from the MQTT topic.

2. **MQTT Communication**:
   - The system subscribes to a user-specific MQTT topic (based on the SR number) to retrieve issued book information.
   - Books are issued and returned based on barcode detection.
   - Book details (book code, issue date, and return date) are published to the MQTT broker.

3. **Barcode Detection**:
   - The system uses a camera to detect book barcodes and match them with the issued books.
   - Upon detection, the book’s status is updated (issued/returned).

---

## File Structure

- `identify_face/`: Contains face recognition-related classes and methods.
  - `face_recog.py`: Handles face recognition using LBPH.
  - `__init__.py`: Initialization for the face recognition module.

- `mqtt/`: Contains MQTT communication code.
  - `mqtt_paho.py`: Handles MQTT connection, publishing, and subscribing.
  - `__init__.py`: Initialization for the MQTT module.

- `barcode/`: Handles barcode detection and related functionality.

- `configurations.py`: Contains configuration settings such as camera parameters, MQTT details, and paths.

- `__main__.py`: The entry point for the library management system.

---

## Troubleshooting

- **Face Recognition not working**:
  - Make sure that your camera is properly connected and configured in the `configurations.py` file.
  - Ensure the lighting conditions are good for face detection.
  
- **MQTT Connection Issues**:
  - Verify that the MQTT broker is running and accessible from the machine.
  - Check that the credentials (username/password) and port are correctly configured in `configurations.py`.

- **Barcode Detection Problems**:
  - If the barcode scanner is not detecting codes correctly, try adjusting the camera settings (e.g., focus, lighting) or check for issues with the barcode scanner itself.


