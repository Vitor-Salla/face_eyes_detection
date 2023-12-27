import sys
import back_end
from PySide6.QtWidgets import QApplication
from front_end.main_window import MainWindow


if __name__ == "__main__":
    # aplicação
    app = QApplication([])
    main_window = MainWindow()

    main_window.show()

    sys.exit(app.exec())
