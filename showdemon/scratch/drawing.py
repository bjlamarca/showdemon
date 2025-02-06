import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QGraphicsView, QGraphicsScene
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QPixmap
from PySide6.QtCore import Qt, QTimer

class TimelineTest(QWidget):
    def __init__(self):
        super().__init__()
        self.events = {
        "2023": "Event 1",
        "2024": "Event 2",
        "2025": "Event 3"
    }
        self.initUI()

    def initUI(self):
        #self.setWindowTitle('Timeline')
        self.setGeometry(100, 100, 800, 200)
        #self.show()

    #def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawTimeline(qp)
        qp.end()

    def drawTimeline(self, qp):
        pen = QPen(Qt.white, 2, Qt.SolidLine)
        qp.setPen(pen)

        # Draw the main line
        qp.drawLine(20, 100, 780, 100)

        # Draw and label the events
        for i, (date, event) in enumerate(self.events.items()):
            x = 20 + (i * (760 / len(self.events)))
            qp.drawLine(x, 90, x, 110)

            font = QFont("Arial", 10)
            qp.setFont(font)
            qp.drawText(x - 20, 130, 40, 20, Qt.AlignCenter, date)
            qp.drawText(x - 20, 150, 40, 20, Qt.AlignCenter, event)




class MovingLine(QWidget):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_line)
        self.timer.start(10)
        print('init')
        main_layout = QVBoxLayout()
        self.lbl = QLabel()
        canvas = QPixmap(400, 300)
        #canvas.fill(Qt.white)
        self.lbl.setPixmap(canvas)
        main_layout.addWidget(self.lbl)
        self.setLayout(main_layout)
    
    # def paintEvent(self, event):
    #     print('paintEvent')
    #     painter = QPainter(self)
    #     painter.setPen(QPen(QColor(255, 0, 0), 3))
    #     painter.drawRect(self.rect().adjusted(10, 10, -10, -10))
    

    def paintEvent(self, event):
        print('paintEvent')
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 2))
        painter.drawLine(self.x, 20, self.x, self.height() - 20)

    def update_line(self):
        self.x += 1
        if self.x > self.width():
            self.x = 0
        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MovingLine()
    widget.show()
    sys.exit(app.exec())

class MyView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # Create a line
        pen = QPen(QColor("red"))
        pen.setWidth(3)
        self.line = self.scene.addLine(10, 10, 10, 100, pen)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Get the position of the mouse click
            pos = event.pos()
            # Move the line
            self.line.setLine(pos.x(), pos.y(), pos.x() + 90, pos.y() + 90)