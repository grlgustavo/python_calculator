# QSS - Estilos do QT for Python
# https://doc.qt.io/qtforpython/tutorials/basictutorial/widgetstyling.html
# Dark Theme
# https://pyqtdarktheme.readthedocs.io/en/latest/how_to_use.html


from PySide6.QtGui import QIcon
import qdarktheme
import variables as var

temp = QIcon()

qss = f'''
    PushButton[cssClass="specialButton"] {{
    QPushButton[cssClass="specialButton"] {{
        color: #fff;
        background: {var.PRIMARY_COLOR};
    }}
    PushButton[cssClass="specialButton"]:hover {{
    QPushButton[cssClass="specialButton"]:hover {{
        color: #fff;
        background: {var.DARKER_PRIMARY_COLOR};
    }}
    PushButton[cssClass="specialButton"]:pressed {{
    QPushButton[cssClass="specialButton"]:pressed {{
        color: #fff;
        background: {var.DARKEST_PRIMARY_COLOR};
    }}
'''


def setupTheme(typeTheme: str = 'dark'):
    qdarktheme.load_stylesheet(typeTheme)  # ou dark
    # dark_stylesheet = qdarktheme.load_stylesheet('light')  # ou dark
