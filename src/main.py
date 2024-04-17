import sys
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtGui import QIcon
from main_window import MainWindow
from variables import WINDOWS_ICO_PATH

if __name__ == '__main__':
    # Cria a aplicação
    app = QApplication(sys.argv)
    window = MainWindow()

    lbl_1 = QLabel('O meu texto é grande')
    lbl_1.setStyleSheet('font-size: 40px')

    # Defini o ícone
    icon = QIcon(str(WINDOWS_ICO_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    if sys.platform.startswith('win'):
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            u'CompanyName.ProductName.SubProduct.VersionInformation')

    # Executa tudo
    window.adjustFixedSize()
    window.show()
    app.exec()
