# QSS - Estilos do QT for Python
# https://doc.qt.io/qtforpython/tutorials/basictutorial/widgetstyling.html
# Dark Theme
# https://pyqtdarktheme.readthedocs.io/en/latest/how_to_use.html


from PySide6.QtGui import QIcon
import qdarktheme


def setupTheme(typeTheme: str = 'dark'):
    qdarktheme.load_stylesheet(typeTheme)  # ou dark
    # dark_stylesheet = qdarktheme.load_stylesheet('light')  # ou dark
