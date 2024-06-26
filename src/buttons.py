from typing import TYPE_CHECKING
from PySide6.QtWidgets import QPushButton, QGridLayout
from PySide6.QtCore import Slot
import math
from utils import (isEmpty, isNumOrDot, isValidNumber, isInverseSignal, isZero,
                   isDot)

if TYPE_CHECKING:  # Evita erros de circular import
    from main_window import MainWindow
    from display import Display, Info


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ButtonsGrid(QGridLayout):
    def __init__(self, display: 'Display', info: 'Info', window: 'MainWindow',
                 *args, **kwargs
                 ) -> None:
        super().__init__(*args, **kwargs)
        self._gridMask = [['%', 'CE', 'C', '←'],
                          ['⅟ⅹ', 'x²', '√2', '÷'],
                          ['7', '8', '9', 'x'],
                          ['4', '5', '6', '-'],
                          ['1', '2', '3', '+'],
                          ['+/-', '0', '.', '=']]
        self.display = display
        self.info = info
        self.window = window
        self._equation = ''
        self._left = None
        self._right = None
        self._operator = None
        self._makeGrid()

    @property
    def equation(self):
        return self._equation

    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

    def _makeGrid(self):

        self.display.eqPressed.connect(self._solve)
        self.display.clearPressed.connect(self._clear)
        self.display.delPressed.connect(self.display.backspace)
        self.display.numbersPressed.connect(self._insertToDisplay)
        self.display.operatorPressed.connect(self._operation)

        for rowNumber, row_data in enumerate(self._gridMask):
            for columnNumber, buttonText in enumerate(row_data):
                button = Button(buttonText)
                if (not isNumOrDot(buttonText) and
                    not isEmpty(buttonText) and
                        not isInverseSignal(buttonText)):
                    button.setProperty('cssClass', 'specialButton')
                else:
                    button.setProperty('cssClass', 'numbersButton')
                self._configButton(button)
                self.addWidget(button, rowNumber, columnNumber)

    def _connectButtonClicked(self, button, slot):
        button.clicked.connect(slot)

    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot():
            func(*args, **kwargs)
        return realSlot

    def _insertToDisplay(self, text):
        newDisplayValue = self.display.text() + text
        if isDot(newDisplayValue):
            text = '0'
        if not isValidNumber(newDisplayValue):
            return

        self.display.insert(text)
        self.display.setFocus()

    def _inverseNumber(self):
        displayText = self.display.text()
        if isZero(displayText) or isEmpty(displayText) or isDot(displayText):
            return
        try:
            displayValue = round(1/float(displayText), 4)
        except ValueError:
            self.display.setText('Entrada inválida')
        self.display.setText(str(displayValue))
        self.display.setFocus()

    def _changeDisplaySignal(self):
        displayText = self.display.text()
        if isZero(displayText) or isEmpty(displayText):
            return
        try:
            displayValue = -1 * float(displayText)
        except ValueError:
            self.display.setText('Entrada inválida')
        self.display.setText(str(displayValue))
        self.display.setFocus()

    def _squareRoot(self):
        displayText = self.display.text()
        try:
            displayValue = round(math.sqrt(float(displayText)), 4)
        except ValueError:
            self.display.setText('Entrada inválida')
            return
        self.display.setText(str(displayValue))
        self.display.setFocus()

    def _exponation(self):
        displayText = self.display.text()
        try:
            displayValue = float(displayText) ** 2
        except ValueError:
            self.display.setText('Entrada inválida')
            return
        self.display.setText(str(displayValue))
        self.display.setFocus()

    def _operation(self, text):
        buttonText = text
        if buttonText == '÷':
            buttonText = '/'
        elif buttonText == 'x':
            buttonText = '*'
        displayText = self.display.text()
        self.display.clear()

        if not isValidNumber(displayText) and self._left is None:
            self._showError('Você não digitou nada.')
            return
        elif self._left is None:
            self._left = float(displayText)

        self._operator = buttonText
        self.equation = f'{self._left} {self._operator} ??'
        self.display.setFocus()

    def _solve(self):
        displayText = self.display.text()

        if not isValidNumber(displayText):
            return

        self._right = float(displayText)
        if isZero(str(self._right)) or isEmpty(str(self._left)):
            return
        self.equation = f'{self._left} {self._operator} {self._right}'
        result = round(eval(self.equation), 4)
        self.display.setText(str(result))
        self._left = result
        self._operator = None
        self.equation = f'{self.equation} = {result}'
        self.display.setFocus()

    def _percentage(self):

        if not isValidNumber(str(self._left)) or isEmpty(str(self._operator)):
            return

        displayText = self.display.text()

        if not isValidNumber(displayText):
            return

        self._right = float(displayText)/100
        self.equation = f'{self._left} {self._operator} {self._right}'
        result = round(eval(self.equation), 4)
        self._left = result
        self._operator = None
        self.equation = f'{self.equation} = {result}'
        self.display.setText(str(result))
        self.display.setFocus()

    def _clear(self):
        self._left = None
        self._right = None
        self._operator = None
        self.info.clear()
        self.display.clear()
        self.display.setFocus()

    def _configButton(self, button):
        text = button.text()
        slot = self._makeSlot(self._clear)
        if text == 'C':
            slot = self._makeSlot(self._clear)
        elif text in '+-÷x':
            slot = self._makeSlot(self._operation, text)
        elif text == '=':
            slot = self._makeSlot(self._solve)
        elif text == '←':
            self._connectButtonClicked(button, self.display.backspace)
            return
        elif text == '⅟ⅹ':
            slot = self._makeSlot(self._inverseNumber)
        elif text == '√2':
            slot = self._makeSlot(self._squareRoot)
        elif text == 'x²':
            slot = self._makeSlot(self._exponation)
        elif text == '%':
            slot = self._makeSlot(self._percentage)
        elif text == '+/-':
            slot = self._makeSlot(self._changeDisplaySignal)
        else:
            slot = self._makeSlot(self._insertToDisplay, text)

        self._connectButtonClicked(button, slot)

    def _showError(self, text):
        msgBox = self.window.makeMessageBox()
        msgBox.setText(text)
        msgBox.setIcon(msgBox.Icon.Critical)

        msgBox.setStandardButtons(
            msgBox.StandardButton.Cancel |
            msgBox.StandardButton.Close
        )
        msgBox.button(msgBox.StandardButton.Close).setText('Fechar')
        msgBox.button(msgBox.StandardButton.Cancel).setText('Voltar')

        result = msgBox.exec()
        self.display.setFocus()

        if result == msgBox.StandardButton.Close:
            exit()
