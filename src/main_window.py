from PySide6.QtWidgets import (QMainWindow, QVBoxLayout,
                               QWidget)


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        # Configurações da janela
        self.setWindowTitle('Calculadora')

        # Configurando o layout básico
        self.cw = QWidget()
        self.v_layout = QVBoxLayout()
        self.cw.setLayout(self.v_layout)
        self.setCentralWidget(self.cw)

    def adjustFixedSize(self):
        # Última coisa a ser feita!
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())
