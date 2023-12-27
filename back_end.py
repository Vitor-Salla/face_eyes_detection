import cv2
from PySide6.QtGui import QImage
from PySide6.QtCore import Qt, Signal, QThread, QTimer
import serial


class ImageProcessing:
    def __init__(self) -> None:
        self.face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
        self.model = "faces"
        self.image_color = "rgb"
        self.scale_factor = 1.5
        self.min_neighbors = 5

    def set_image_color(self, image_color):
        self.image_color = image_color

    def set_model(self, model):
        self.model = model

    def set_scale_factor(self, scale_factor):
        self.scale_factor = scale_factor

    def set_min_neighbors(self, min_neighbors):
        self.min_neighbors = min_neighbors

    def cv_to_qt_image(self, cv_image):
        height, width = cv_image.shape[:2]

        if len(cv_image.shape) == 2:  # Grayscale image
            bytes_per_line = width
            q_image = QImage(
                cv_image.data, width, height, bytes_per_line, QImage.Format_Grayscale8
            )
        elif len(cv_image.shape) == 3:  # RGB image
            bytes_per_line = 3 * width
            q_image = QImage(
                cv_image.data, width, height, bytes_per_line, QImage.Format_BGR888
            )
        else:
            raise ValueError("Unsupported image format")

        return q_image

    def detect_faces(self, cv_image):
        faces = self.face_cascade.detectMultiScale(
            cv_image, self.scale_factor, self.min_neighbors
        )
        for x, y, w, h in faces:
            cv2.rectangle(cv_image, (x, y), (x + w, y + h), (255, 0, 0), 2)

        return len(faces), self.cv_to_qt_image(cv_image)

    def detect_eyes(self, cv_image):
        eyes = self.eye_cascade.detectMultiScale(
            cv_image, self.scale_factor, self.min_neighbors
        )
        for x, y, w, h in eyes:
            cv2.rectangle(cv_image, (x, y), (x + w, y + h), (255, 0, 0), 2)

        return len(eyes), self.cv_to_qt_image(cv_image)

    def process_image(self, cv_image):
        if self.image_color == "gray":
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        elif self.image_color != "rgb":
            print(
                f"Warning: Unrecognized color format {self.image_color}. Using default (RGB)."
            )

        if self.model == "faces":
            return self.detect_faces(cv_image)
        elif self.model == "eyes":
            return self.detect_eyes(cv_image)
        else:
            print(
                f"Warning: Unrecognized model type {self.model}. Using default (faces)."
            )
            return 0, self.cv_to_qt_image(cv_image)


class UpdateImageThread(QThread):
    frameCaptured = Signal(int, QImage)

    def __init__(self):
        super().__init__()
        self.image_processing = ImageProcessing()
        self.acquisition_local = None
        self.file_path = None
        self.n = 0
        self.serial_timer = QTimer(self)
        self.serial_timer.timeout.connect(self.send_serial_data)
        self.serial_timer.start(1500)
        try:
            self.serial = serial.Serial("COM10", 57600)
        except:
            self.serial = None
            print("erro ao abrir portal serial")

    def stop(self):
        self.requestInterruption()
        self.wait()

    def run(self):
        web_cam = cv2.VideoCapture(0)
        while not self.isInterruptionRequested():
            if self.acquisition_local == "webcam":
                _, frame = web_cam.read()
            elif self.acquisition_local == "filesystem":
                frame = cv2.imread(self.file_path)
            if frame is not None:
                self.n, processed_image = self.image_processing.process_image(frame)
                self.frameCaptured.emit(
                    self.n, processed_image.scaled(1000, 800, Qt.KeepAspectRatio)
                )

    def send_serial_data(self):
        if self.serial:
            data_to_send = f"N {self.image_processing.model}: {self.n}"
            self.serial.write(data_to_send.encode())
