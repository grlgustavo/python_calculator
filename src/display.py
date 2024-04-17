from PySide6.QtWidgets import QLineEdit
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
