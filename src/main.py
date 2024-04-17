import sys
import variables as var
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from main_window import MainWindow
from display import Display
from info import Info
import qdarktheme

if __name__ == '__main__':
    # Cria a aplicação
    app = QApplication(sys.argv)
    dark_stylesheet = qdarktheme.load_stylesheet('dark')  # light ou dark
    app.setStyleSheet(str(dark_stylesheet))
    window = MainWindow()

    # Defini o ícone
    icon = QIcon(str(var.WINDOWS_ICO_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    if sys.platform.startswith('win'):
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            u'CompanyName.ProductName.SubProduct.VersionInformation')

    info = Info('2.0 ^ 10.0 = 1024')
    window.addToVLayout(info)

    # Display
    display = Display('0')

    window.addToVLayout(display)

    # Executa tudo
    window.adjustFixedSize()
    window.show()
    app.exec()
