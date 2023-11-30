from typing import Any
from abc import ABC, abstractmethod
from PySide6.QtWidgets import QWidget


class UIUtils(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @staticmethod
    def remove_margins(widget: QWidget) -> Any:
        widget.setContentsMargins(0, 0, 0, 0)

        return widget
