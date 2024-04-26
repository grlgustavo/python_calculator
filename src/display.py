from PySide6.QtWidgets import QLineEdit, QLabel, QWidget
from PySide6.QtCore import Qt
import variables as var


class Display(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        self.setStyleSheet(f'font-size: {var.BIG_FONT_SIZE}px;')
        self.setMinimumSize(var.MIN_WIDTH, var.BIG_FONT_SIZE * 2)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*[var.TEXT_MARGIN for _ in range(4)])


class Info(QLabel):
    def __init__(self, text: str, parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.configStyle()

    def configStyle(self):
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
    #     self.setStyleSheet(f'font-size: {var.SMALL_FONT_SIZE}px;')
