import sys
from PySide6.QtWidgets import QApplication, QLabel
from main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    lbl_1 = QLabel('O meu texto é grande')
    lbl_1.setStyleSheet('font-size: 40px')
    window.v_layout.addWidget(lbl_1)

    window.adjustFixedSize()
    window.show()
    app.exec()
