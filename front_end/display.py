from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QSizePolicy,
    QSpacerItem,
)
from PySide6.QtCore import Qt


class InfoDisplay(QWidget):
    def __init__(self, screen_geometry):
        super().__init__()
        self.layout = QHBoxLayout(self)

        self.info_label = QLabel()

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.info_label.setAttribute(Qt.WA_StyledBackground, True)
        
        self.info_label.setStyleSheet(
            """
                QLabel {
                    background-color: none;
                    color: white;
                    font-size: 20px;
                    font-weight: 600;
                }
            """
        )

        self.setStyleSheet(
            """
            QWidget {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(70,70,70,1), stop:0.69 rgba(97,96,122,1), stop:1 rgba(110,120,159,1));
                border-radius: 15px;
            }
        """
        )

        horizontal_spacer = QSpacerItem(
            20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.layout.addItem(horizontal_spacer)
        self.layout.addWidget(self.info_label)
        self.layout.addItem(horizontal_spacer)

        self.setFixedHeight((screen_geometry.height() - 50) * 0.19)


class ImageDisplay(QWidget):
    def __init__(self, screen_geometry):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(
            """
                QWidget {
                    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(70,70,70,1), stop:0.69 rgba(97,96,122,1), stop:1 rgba(110,120,159,1));
                    border-radius: 15px;
                }
            """
        )

        self.image_label = QLabel()
        self.image_label.setAttribute(Qt.WA_StyledBackground, True)
        self.image_label.setStyleSheet(
            """
                QWidget {
                    background: none;w
                }
            """
        )
        self.layout.addWidget(self.image_label)
        self.setFixedHeight((screen_geometry.height() - 50) * 0.8)


class Display(QWidget):
    def __init__(self, screen_geometry):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 32)
        self.layout.setSpacing(0)

        self.info_display = InfoDisplay(screen_geometry)
        self.image_display = ImageDisplay(screen_geometry)

        vertical_spacer = QSpacerItem(
            20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.layout.addWidget(self.info_display)
        self.layout.addItem(vertical_spacer)
        self.layout.addWidget(self.image_display)
