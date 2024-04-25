from typing import TYPE_CHECKING
from PySide6.QtWidgets import QPushButton, QGridLayout
from PySide6.QtCore import Slot
from utils import isEmpty, isNumOrDot, isValidNumber, isSignal

if TYPE_CHECKING:  # Evita erros de circular import
    from display import Display, Info


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ButtonsGrid(QGridLayout):
    def __init__(self, display: 'Display', info: 'Info', *args, **kwargs
                 ) -> None:
        super().__init__(*args, **kwargs)
        self._gridMask = [['%', 'CE', 'C', '←'],
                          ['⅟ⅹ', 'x²', '√2', '÷'],
                          ['7', '8', '9', '⨉'],
                          ['4', '5', '6', '-'],
                          ['1', '2', '3', '+'],
                          ['+/-', '0', '.', '=']]
        self.display = display
        self.info = info
        self._equation = ''
        self._makeGrid()

    @property
    def equation(self):
        return self._equation

    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText = value

    def _makeGrid(self):
        for rowNumber, row_data in enumerate(self._gridMask):
            for columnNumber, buttonText in enumerate(row_data):
                button = Button(buttonText)
                if (not isNumOrDot(buttonText) and
                    not isEmpty(buttonText) and
                        not isSignal(buttonText)):
                    button.setProperty('cssClass', 'specialButton')
                    self._configSpecialButton(button)
                else:
                    button.setProperty('cssClass', 'numbersButton')
                    self._configNumbersButton(button)
                self.addWidget(button, rowNumber, columnNumber)

                # slot = self._makeSlot(self._insertButtonTextToDisplay,button)
                # self._connectButtonClicked(button, slot)

    def _connectButtonClicked(self, button, slot):
        button.clicked.connect(slot)

    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot():
            func(*args, **kwargs)
        return realSlot

    def _insertButtonTextToDisplay(self, button):
        buttonText = button.text()
        displayValue = self.display.text()
        if displayValue == '0' or displayValue == '-0.0':
            self.display.clear()
        newDisplayValue = self.display.text() + buttonText
        if not isValidNumber(newDisplayValue):
            return

        self.display.insert(buttonText)

    def _changeDisplaySignal(self):
        displayText = self.display.text()
        if not isValidNumber(displayText):
            return
        displayValue = -1 * float(displayText)
        self.display.setText(str(displayValue))

    def _clear(self):
        self.display.clear()

    def _configSpecialButton(self, button):
        text = button.text()

        if text == 'C':
            slot = self._makeSlot(self._clear)
            self._connectButtonClicked(button, slot)

        print('Texto do botão especial:', text)

    def _configNumbersButton(self, button):
        text = button.text()

        if text == '+/-':
            slot = self._makeSlot(self._changeDisplaySignal)
            self._connectButtonClicked(button, slot)
        else:
            slot = self._makeSlot(self._insertButtonTextToDisplay, button)
            self._connectButtonClicked(button, slot)
