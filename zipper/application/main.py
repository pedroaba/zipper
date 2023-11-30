import sys

from PySide6.QtWidgets import QMainWindow, QApplication

from zipper.application.settings import MINIMUM_SIZE_OF_APPLICATION
from zipper.application.screens.main_screen import MainScreen


class Application(QMainWindow):
    def __init__(self, parent=None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        self.setWindowTitle("Zipper")
        self.setMinimumSize(MINIMUM_SIZE_OF_APPLICATION["width"], MINIMUM_SIZE_OF_APPLICATION["height"])

        self.showMaximized()

        screen = MainScreen()
        self.setCentralWidget(screen)

        self._config_styles()

    def _config_styles(self):
        self.setStyleSheet("""
        background-color: #18181b;
        """)


if __name__ == "__main__":
    import ctypes

    app_id = "13.remove_bg_rbg"  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

    # application to open as window
    application = QApplication(sys.argv)

    # main screen
    main_application = Application()
    main_application.show()

    application.exec()