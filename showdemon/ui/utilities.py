from PySide6.QtGui import QIcon, QPixmap

def get_icon_obj(icon):
    path = 'C:\\Dev\\showdemon\\showdemon\\static\\fugue-2x-icons\\icons-2x\\' + icon + '.png'
    return QIcon(QPixmap(path))
    