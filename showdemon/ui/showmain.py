from PySide6.QtWidgets import (QWidget, QPushButton, QMessageBox, QVBoxLayout, QLabel, QHBoxLayout, QComboBox,
    QTableWidget, QTableWidgetItem, QLineEdit, QTabWidget, QDialog, QFrame, QAbstractItemView, QCheckBox, QMainWindow,
    QGraphicsScene, QGraphicsView, QGraphicsItem)
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QPen, QColor, QBrush, QWindow, QPainter, QPalette


class ShowMainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Show")
        self.setFixedSize(QSize(800, 600))
        self.setWindowTitle("Window with Custom Title Bar Color")
       
        # palette = self.palette()
        # palette.setColor(QPalette.Window, QColor("#4CAF50"))
        # self.setPalette(palette)
        
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        track1 = TrackWidget()
        track2 = TrackWidget()
        btn_test = QPushButton("Test")
        self.layout.addWidget(track1)
        self.layout.addWidget(track2)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(CustomButton("Test"))
        btn_layout.addStretch()
        
        self.layout.addLayout(btn_layout)
        lbl = QLabel("Show Main Window")
        self.layout.addWidget(lbl)
    
        



class TrackWidget(QWidget):
    def __init__(self):
        super().__init__()
        #self.setFixedSize(QSize(600, 600))

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.view.setBackgroundBrush(QBrush(QColor(47, 79, 79)))
        self.view.setFixedSize(QSize(600, 200))
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

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

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.view)


class CustomButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFixedSize(100, 50)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.isDown():
            color = QColor(100, 100, 100)
        else:
            color = QColor(200, 200, 200)

        painter.setBrush(QBrush(color))
        painter.setPen(QPen(Qt.NoPen))
        painter.drawRoundedRect(self.rect(), 10, 10)

        painter.setPen(QPen(Qt.black))
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())
        


        