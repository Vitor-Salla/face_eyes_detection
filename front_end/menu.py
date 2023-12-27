import time
import cv2
from PySide6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QSlider,
    QSizePolicy,
    QFileDialog,
    QSpacerItem,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

# ----- buttons -----
class MenuButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setFixedHeight(35)
        self.setStyleSheet(
            """
            QPushButton {
                background-color: #E0E0E0;
                border: 2px solid #FFFFFF;
                border-radius: 6px;
                color: #505050;
                font-size: 14px;
                font-weight: 500;
                margin: 0;
                max-height: 20px;
            }

            QPushButton:hover {
                background-color: #A0A0FF;
            }
        """
        )


class OpenImageButton(MenuButton):
    def __init__(self, text, display, update_image_thread):
        super().__init__(text)
        self.clicked.connect(self.select_image)
        self.display = display
        self.update_image_thread = update_image_thread

    def select_image(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Images (*.png *.jpg *.bmp)")

        if file_dialog.exec_() == QFileDialog.Accepted:
            selected_file = file_dialog.selectedFiles()[0]
            self.update_image_thread.requestInterruption()
            time.sleep(1)
            self.update_image_thread.frameCaptured.connect(self.update_image_display)
            self.update_image_thread.acquisition_local = "filesystem"
            self.update_image_thread.file_path = selected_file
            self.update_image_thread.start()

    def update_image_display(self, n, q_image):
        pixmap = QPixmap.fromImage(q_image)
        if self.update_image_thread.image_processing.model == "faces":
            self.display.info_display.info_label.setText(f"Number of Faces: {n}")
        elif self.update_image_thread.image_processing.model == "eyes":
            self.display.info_display.info_label.setText(f"Number of Eyes: {n}")

        self.display.image_display.image_label.setPixmap(pixmap)


class OpenWebCamButton(MenuButton):
    def __init__(self, text, display, update_image_thread):
        super().__init__(text)
        self.update_image_thread = update_image_thread
        self.display = display

        self.clicked.connect(self.start_webcam)

    def start_webcam(self):
        self.update_image_thread.requestInterruption()
        time.sleep(1)
        self.update_image_thread.acquisition_local = "webcam"
        self.update_image_thread.frameCaptured.connect(self.update_image_display)
        self.update_image_thread.start()

    def update_image_display(self, n, q_image):
        pixmap = QPixmap.fromImage(q_image)
        if self.update_image_thread.image_processing.model == "faces":
            self.display.info_display.info_label.setText(f"Number of Faces: {n}")
        elif self.update_image_thread.image_processing.model == "eyes":
            self.display.info_display.info_label.setText(f"Number of Eyes: {n}")

        self.display.image_display.image_label.setPixmap(pixmap)


class ColouredImageButton(MenuButton):
    def __init__(self, text, update_image_thread):
        super().__init__(text)
        self.update_image_thread = update_image_thread
        self.clicked.connect(self.set_image_color_to_rgb)

    def set_image_color_to_rgb(self):
        self.update_image_thread.image_processing.set_image_color("rgb")


class GrayScaleImageButton(MenuButton):
    def __init__(self, text, update_image_thread):
        super().__init__(text)
        self.update_image_thread = update_image_thread
        self.clicked.connect(self.set_image_color_to_gray)

    def set_image_color_to_gray(self):
        self.update_image_thread.image_processing.set_image_color("gray")


class FaceDetectionButton(MenuButton):
    def __init__(self, text, update_image_thread):
        super().__init__(text)
        self.update_image_thread = update_image_thread
        self.clicked.connect(self.set_model_to_faces)

    def set_model_to_faces(self):
        self.update_image_thread.image_processing.set_model("faces")


class EyeDetectionButton(MenuButton):
    def __init__(self, text, update_image_thread):
        super().__init__(text)
        self.update_image_thread = update_image_thread
        self.clicked.connect(self.set_model_to_eyes)

    def set_model_to_eyes(self):
        self.update_image_thread.image_processing.set_model("eyes")


# ----- sliders -----
class MenuSlider(QSlider):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(35)
        self.setOrientation(Qt.Horizontal)


class ScaleFactorSlider(QWidget):
    def __init__(self, update_image_thread):
        super().__init__()
        self.update_image_thread = update_image_thread

        main_layout = QVBoxLayout(self)
        title_layout = QHBoxLayout()

        self.title_label = QLabel("Scale Factor")
        self.title_label.setStyleSheet(
            """
            QLabel {
                color: #FFFFFF;
                font-size: 14px;
                font-weight: 500;
            }
        """
        )
        self.info_label = QLabel("(1.5)")
        self.info_label.setStyleSheet(
            """
            QLabel {
                color: #FFFFFF;
                font-size: 12px;
                font-weight: 500;
            }
        """
        )
        self.slider = MenuSlider()
        self.slider.setMinimum(101)
        self.slider.setMaximum(200)
        self.slider.setValue(150)
        self.slider.setSingleStep(1)
        self.slider.valueChanged.connect(self.set_scale_factor)

        vertical_spacer = QSpacerItem(
            20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding
        )
        horizontal_spacer = QSpacerItem(
            20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        title_layout.addWidget(self.title_label, alignment=Qt.AlignLeft)
        title_layout.addWidget(self.info_label, alignment=Qt.AlignLeft)
        title_layout.addItem(horizontal_spacer)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_widget = QWidget()
        title_widget.setLayout(title_layout)

        main_layout.addItem(vertical_spacer)
        main_layout.addWidget(title_widget)
        main_layout.addWidget(self.slider)
        main_layout.addItem(vertical_spacer)

    def set_scale_factor(self):
        value = self.slider.value() / 100
        self.info_label.setText(f"({round(value, 2)})")
        self.update_image_thread.image_processing.set_scale_factor(value)


class MinNeighborsSlider(QWidget):
    def __init__(self, update_image_thread):
        super().__init__()
        self.update_image_thread = update_image_thread

        main_layout = QVBoxLayout(self)
        title_layout = QHBoxLayout()

        self.title_label = QLabel("Min Neighbors")
        self.title_label.setStyleSheet(
            """
            QLabel {
                color: #FFFFFF;
                font-size: 14px;
                font-weight: 500;
            }
        """
        )
        self.info_label = QLabel("(5)")
        self.info_label.setStyleSheet(
            """
            QLabel {
                color: #FFFFFF;
                font-size: 12px;
                font-weight: 500;
            }
        """
        )
        self.slider = MenuSlider()
        self.slider.setMinimum(1)
        self.slider.setMaximum(10)
        self.slider.setValue(5)
        self.slider.setSingleStep(1)
        self.slider.valueChanged.connect(self.set_min_neighbors)

        vertical_spacer = QSpacerItem(
            20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding
        )
        horizontal_spacer = QSpacerItem(
            20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        title_layout.addWidget(self.title_label, alignment=Qt.AlignLeft)
        title_layout.addWidget(self.info_label, alignment=Qt.AlignLeft)
        title_layout.addItem(horizontal_spacer)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_widget = QWidget()
        title_widget.setLayout(title_layout)

        main_layout.addItem(vertical_spacer)
        main_layout.addWidget(title_widget)
        main_layout.addWidget(self.slider)
        main_layout.addItem(vertical_spacer)

    def set_min_neighbors(self):
        value = self.slider.value()
        self.info_label.setText(f"({round(value, 2)})")
        self.update_image_thread.image_processing.set_min_neighbors(value)


# ---- button menu ----
class ButtonsMenu(QWidget):
    def __init__(self, display, update_image_thread):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.button1 = OpenImageButton("Open Image", display, update_image_thread)
        self.button2 = OpenWebCamButton("Open Webcam", display, update_image_thread)
        self.button3 = ColouredImageButton("Coloured Image", update_image_thread)
        self.button4 = GrayScaleImageButton("Gray Scale Image", update_image_thread)
        self.button5 = FaceDetectionButton("Detect Faces", update_image_thread)
        self.button6 = EyeDetectionButton("Detect Eyes", update_image_thread)
        self.button7 = MenuButton("Connect Serial")

        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.button3)
        self.layout.addWidget(self.button4)
        self.layout.addWidget(self.button5)
        self.layout.addWidget(self.button6)
        self.layout.addWidget(self.button7)

        self.setStyleSheet(
            """
            QWidget {
                background-color: none;
            }
        """
        )

        self.setFixedHeight(350)


# ---- slider menu ----
class SlidersMenu(QWidget):
    def __init__(self, update_image_thread):
        super().__init__()

        self.layout = QVBoxLayout(self)

        slider1 = ScaleFactorSlider(update_image_thread)
        slider2 = MinNeighborsSlider(update_image_thread)

        self.layout.addWidget(slider1)
        self.layout.addWidget(slider2)

        self.setFixedHeight(300)
        self.setStyleSheet(
            """
            QWidget {
                background-color: none;
            }
        """
        )


# ---- menu ----
class Menu(QWidget):
    def __init__(self, display, screen_geometry, update_image_thread):
        super().__init__()

        self.buttons_menu = ButtonsMenu(display, update_image_thread)
        self.sliders_menu = SlidersMenu(update_image_thread)
        self.layout = QVBoxLayout(self)

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(
            """
            QWidget {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(70,70,70,1), stop:0.69 rgba(97,96,122,1), stop:1 rgba(110,120,159,1));
                border-radius: 15px;
            }
            """
        )

        self.layout.addWidget(self.buttons_menu)
        self.layout.addWidget(self.sliders_menu)

        self.setFixedWidth(300)
        self.setFixedHeight(screen_geometry.height() - 50)
