from PySide6.QtWidgets import QLineEdit, QLabel, QWidget
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeyEvent
from utils import isEmpty
import variables as var


class Display(QLineEdit):

    eqPressed = Signal()
    delPressed = Signal()
    clearPressed = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        self.setStyleSheet(f'font-size: {var.BIG_FONT_SIZE}px;')
        self.setMinimumSize(var.MIN_WIDTH, var.BIG_FONT_SIZE * 2)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*[var.TEXT_MARGIN for _ in range(4)])

    def keyPressEvent(self, event: QKeyEvent) -> None:
        text = event.text().strip()
        KEYS = Qt.Key
        key = event.key()

        isEnter = key in [KEYS.Key_Enter, KEYS.Key_Return]
        isDelete = key in [KEYS.Key_Backspace, KEYS.Key_Delete]
        isEsc = key in [KEYS.Key_Escape]

        if isEnter:
            print('Enter Pressionado, sinal emitido', type(self).__name__)
            self.eqPressed.emit()
            return event.ignore()
        if isDelete:
            print('Delete Pressionado, sinal emitido', type(self).__name__)
            self.delPressed.emit()
            return event.ignore()
        if isEsc:
            print('Escape Pressionado, sinal emitido', type(self).__name__)
            self.clearPressed.emit()
            return event.ignore()

        if isEmpty(text):
            return event.ignore()


class Info(QLabel):
    def __init__(self, text: str, parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.configStyle()

    def configStyle(self):
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
