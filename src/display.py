from PySide6.QtWidgets import QLineEdit, QLabel, QWidget
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeyEvent
from utils import isEmpty, isNumOrDot
import variables as var


class Display(QLineEdit):

    eqPressed = Signal()
    delPressed = Signal()
    clearPressed = Signal()
    numbersPressed = Signal(str)
    operatorPressed = Signal(str)

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

        isEnter = key in [KEYS.Key_Enter, KEYS.Key_Return, KEYS.Key_Equal]
        isDelete = key in [KEYS.Key_Backspace, KEYS.Key_Delete]
        isEsc = key in [KEYS.Key_Escape]
        isOperator = key in [KEYS.Key_Plus, KEYS.Key_Minus,
                             KEYS.Key_division, KEYS.Key_multiply,
                             KEYS.Key_Slash, KEYS.Key_Asterisk]

        if isEnter:
            self.eqPressed.emit()
        elif isDelete:
            self.delPressed.emit()
        elif isEsc:
            self.clearPressed.emit()
        elif isEmpty(text):
            return event.ignore()
        elif isNumOrDot(text):
            self.numbersPressed.emit(text)
        elif isOperator:
            self.operatorPressed.emit(text)

        return event.ignore()
        # return super().keyPressEvent(event)


class Info(QLabel):
    def __init__(self, text: str, parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.configStyle()

    def configStyle(self):
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
