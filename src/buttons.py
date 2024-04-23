from PySide6.QtWidgets import QPushButton, QGridLayout
from PySide6.QtCore import Slot
from variables import MEDIUM_FONT_SIZE
from utils import isEmpty, isNumOrDot, isValidNumber, isSignal
from display import Display


class ButtonsGrid(QGridLayout):
    def __init__(self, display: Display, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._gridMask = [['%', 'CE', 'C', '←'],
                          ['⅟ⅹ', 'x²', '√2', '÷'],
                          ['7', '8', '9', '⨉'],
                          ['4', '5', '6', '-'],
                          ['1', '2', '3', '+'],
                          ['+/-', '0', '.', '=']]
        self._makeGrid()
        self.display = display

    def _makeGrid(self):
        for rowNumber, row_data in enumerate(self._gridMask):
            for columnNumber, buttonText in enumerate(row_data):
                button = Button(buttonText)
                if (not isNumOrDot(buttonText) and
                    not isEmpty(buttonText) and
                        not isSignal(buttonText)):
                    button.setProperty('cssClass', 'specialButton')
                else:
                    button.setProperty('cssClass', 'numbersButton')
                self.addWidget(button, rowNumber, columnNumber)
                buttonSlot = self._makeButtonDisplaySlot(
                    self._insertButtonTextToDisplay,
                    button
                )
                button.clicked.connect(buttonSlot)

    def _makeButtonDisplaySlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot():
            func(*args, **kwargs)
        return realSlot

    def _insertButtonTextToDisplay(self, button):
        buttonText = button.text()
        newDisplayValue = self.display.text() + buttonText
        if not isValidNumber(newDisplayValue):
            return

        self.display.insert(buttonText)


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(50, 50)
        self.setProperty('cssClass', 'specialButton')
