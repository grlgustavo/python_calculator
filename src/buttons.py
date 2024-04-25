from typing import TYPE_CHECKING
from PySide6.QtWidgets import QPushButton, QGridLayout
from PySide6.QtCore import Slot
import math
from utils import (isEmpty, isNumOrDot, isValidNumber, isInverseSignal, isZero,
                   isDot)

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
                        not isInverseSignal(buttonText)):
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
        newDisplayValue = self.display.text() + buttonText
        if isDot(newDisplayValue):
            newDisplayValue = '0'
        if not isValidNumber(newDisplayValue):
            return

        self.display.insert(buttonText)

    def _popString(self):
        displayText = self.display.text()
        try:
            newDisplayValue = float(displayText[0:len(displayText)-1])
        except ValueError:
            return
        self.display.setText(str(newDisplayValue))

    def _inverseNumber(self):
        displayText = self.display.text()
        if isZero(displayText) or isEmpty(displayText) or isDot(displayText):
            return
        try:
            displayValue = round(1/float(displayText), 4)
        except ValueError:
            self.display.setText('Entrada inválida')
        self.display.setText(str(displayValue))

    def _changeDisplaySignal(self):
        displayText = self.display.text()
        if isZero(displayText) or isEmpty(displayText):
            return
        try:
            displayValue = -1 * float(displayText)
        except ValueError:
            self.display.setText('Entrada inválida')
        self.display.setText(str(displayValue))

    def _squareRoot(self):
        displayText = self.display.text()
        try:
            displayValue = round(math.sqrt(float(displayText)), 4)
        except ValueError:
            self.display.setText('Entrada inválida')
            return
        self.display.setText(str(displayValue))

    def _exponation(self):
        displayText = self.display.text()
        try:
            displayValue = float(displayText) ** 2
        except ValueError:
            self.display.setText('Entrada inválida')
            return
        self.display.setText(str(displayValue))

    def _clear(self):
        self.display.clear()

    def _configSpecialButton(self, button):
        text = button.text()
        slot = self._makeSlot(self._clear)
        if text == 'C':
            slot = self._makeSlot(self._clear)
            # self._connectButtonClicked(button, slot)
        elif text == '←':
            slot = self._makeSlot(self._popString)
            # self._connectButtonClicked(button, slot)
        elif text == '⅟ⅹ':
            slot = self._makeSlot(self._inverseNumber)
        elif text == '√2':
            slot = self._makeSlot(self._squareRoot)
        elif text == 'x²':
            slot = self._makeSlot(self._exponation)

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
