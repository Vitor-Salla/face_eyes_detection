from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QWidget
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt
from front_end.display import Display
from front_end.menu import Menu
from back_end import UpdateImageThread, ImageProcessing


class MainWidget(QWidget):
    def __init__(self, screen_geometry):
        super().__init__()
        self.layout = QHBoxLayout(self)
        self.update_image_thread = UpdateImageThread()
        self.display = Display(screen_geometry)
        self.menu = Menu(self.display, screen_geometry, self.update_image_thread)
        self.layout.addWidget(self.menu, alignment=Qt.AlignTop)
        self.layout.addWidget(self.display)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(
            """
            QWidget {
                background: #0F0F0F;
            }
            """
        )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("T3 - Vitor Salla e Matteus")
        self.screen_geometry = QGuiApplication.primaryScreen().availableGeometry()

        # Set the window size explicitly
        self.resize(self.screen_geometry.width(), self.screen_geometry.height())

        # centralizing the window
        self.center_point = self.screen_geometry.center()
        self.window_frame = self.frameGeometry()
        self.window_frame.moveCenter(self.center_point)
        self.move(self.window_frame.topLeft())

        # including the screen elements
        self.main_widget = MainWidget(self.screen_geometry)
        self.setCentralWidget(self.main_widget)
