import os
import shutil
from typing import Literal

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QTextEdit, QSizePolicy

from zipper.application.components.alert import Alert
from zipper.application.components.button import Button
from zipper.application.settings import TEMP_FOLDER
from zipper.application.utils.ui import UIUtils
from zipper.application.utils.file import is_our_compression_extention
from zipper.core.compresser import LZWCompresser
from zipper.core.decompresser import LZWDecompresser


class MainScreen(QFrame):
    def __init__(self):
        super(MainScreen, self).__init__()

        self.layout = QVBoxLayout()

        self._config_styles()
        self._config_layout()

    def _config_layout(self):
        self._imported_file_view = QTextEdit()
        self._imported_file_view.setStyleSheet("color: white; font-size: 12pt;")
        self._imported_file_view.setReadOnly(True)
        self._imported_file_view.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self._imported_file_view.setTextInteractionFlags(
            self._imported_file_view.textInteractionFlags() | Qt.TextSelectableByMouse
        )
        self._imported_file_view.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

        self.layout.addWidget(
            self._imported_file_view
        )

        self._button_container_widget = QWidget()
        self._button_container_layout = QHBoxLayout()

        self._import_file_button: Button = UIUtils.remove_margins(Button("Import File"))
        self._import_file_button.set_button_action(self._import_file)
        self._button_container_layout.addWidget(self._import_file_button,
                                                alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        self._save_compact_file_button: Button = UIUtils.remove_margins(Button("Compact File & Save"))
        self._save_compact_file_button.set_button_action(self._compact_file)
        self._button_container_layout.addWidget(self._save_compact_file_button,
                                                alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        self._save_decompact_file_button: Button = UIUtils.remove_margins(Button("Decompact File & Save"))
        self._save_decompact_file_button.set_button_action(self._decompact_file)
        self._button_container_layout.addWidget(self._save_decompact_file_button,
                                                alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        self._clear_text_area_button: Button = UIUtils.remove_margins(Button("Clear File View"))
        self._clear_text_area_button.set_button_action(self._clear_text_area)
        self._button_container_layout.addWidget(self._clear_text_area_button,
                                                alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        self._button_container_widget.setLayout(self._button_container_layout)
        self.layout.addWidget(self._button_container_widget,
                              alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)

        self.setLayout(self.layout)

    def _decompact_file(self):
        folder = self._get_folder()
        if folder is None:
            return

        compresser = LZWDecompresser()
        destiny, text_on_file = compresser.decompress(self._txt_original_path, folder)
        self._imported_file_view.setPlainText(text_on_file)

        self._alert_box("Success", f"File has saved on {destiny}")

    def _clear_text_area(self):
        self._imported_file_view.setPlainText("")

        self._alert_box("Success", "File content view was cleared")

    def _compact_file(self):
        folder = self._get_folder()
        if folder is None:
            return

        compresser = LZWCompresser()
        destiny = compresser.compress(self._txt_original_path, folder)

        self._alert_box("Success", f"File has saved on {destiny}")

    def _get_folder(self) -> str | None:
        if not hasattr(self, "_txt_original_path"):
            self._alert_box("Warning", "No file to save, please import an file")
            return

        path_to_open = os.path.join(
            os.path.expanduser("~"),
            "Downloads"
        )

        folder = str(
            QFileDialog.getExistingDirectory(
                self,
                "Select directory to export template",
                dir=path_to_open,
            )
        )

        if folder == "":
            self._alert_box("Warning", "No folder selected")
            return

        return folder

    def _import_file(self):
        txt_path, _ = QFileDialog.getOpenFileName(
            self,
            "Upload a text file",
            "filename",
            "TXT (*.txt *.marcelo)"
        )

        if txt_path is None or not txt_path:
            self._alert_box("Warning", "No path selected")
            return

        temp_file = os.path.join(
            TEMP_FOLDER,
            os.path.basename(txt_path)
        )

        if not os.path.exists(temp_file):
            shutil.copy(
                txt_path,
                temp_file
            )

        self._txt_original_path = temp_file

        is_marcelo_extention = is_our_compression_extention(temp_file)
        if not is_marcelo_extention:
            with open(temp_file, 'r') as file:
                content = file.read()
                self._imported_file_view.setPlainText(content)
        self._toggle_disable_between_compact_and_decompact_button(
            is_marcelo_extention
        )

        self._alert_box("Success", "File imported with success")

    def _toggle_disable_between_compact_and_decompact_button(self, disabled: bool):
        self._save_compact_file_button.setDisabled(disabled)
        self._save_decompact_file_button.setDisabled(not disabled)

    def _config_styles(self):
        self.setStyleSheet("""
          QFrame: {
            background-color: #18181b;
          }
        """)

    @staticmethod
    def _alert_box(
        title: str,
        message: str,
        message_type: Literal["warning", "info", "error", "question"] = "error",
    ):
        alert = Alert(title, message, message_type)
        alert.exec()
