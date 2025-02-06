
from PySide6.QtCore import QSize, Qt

from PySide6.QtGui import QPen, QBrush

from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsItem, QWidget


class GraphicsWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(600, 600))

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)

        green_pen = QPen(Qt.green)
        red_pen = QPen(Qt.red)
        black_pen = QPen(Qt.black)
        green_pen.setWidth(3)
        
        green_pen.setWidth(3)
        red_pen.setWidth(3)
        black_pen.setWidth(3)
        blue_brush = QBrush(Qt.blue)

        rect1 = self.scene.addRect(50, 50, 100, 100, green_pen)
        rect2 = self.scene.addRect(100, 100, 100, 100, red_pen)
        rect3 = self.scene.addRect(150, 150, 100, 100, black_pen, blue_brush)

        rect1.setFlag(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        rect2.setFlag(QGraphicsItem.ItemIsMovable)
        rect3.setFlag(QGraphicsItem.ItemIsMovable)

        self.setCentralWidget(self.view)

        

        




