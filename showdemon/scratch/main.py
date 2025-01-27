import sys, time
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QVBoxLayout
from demondmx.interface import DMXInterface

class Window(QWidget):

     def __init__(self):
        super().__init__()
        self.setGeometry(200,200,800,800)
        self.setWindowTitle("Show Demon")
        self.label1 = QLabel(self)
        layout = QVBoxLayout()
        layout.addWidget(self.label1)
        self.setLayout(layout)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    

    dmx = DMXInterface()
    dmx.start_dmx_process()
    #while True:
    time.sleep(1)
    print("Red")
    dmx.update(5,255)
    dmx.update(1,255)
    dmx.update(2,0)
    dmx.update(3,0)
    
    time.sleep(1)
    print("Green")
    dmx.update(1,0)
    dmx.update(2,255)
    dmx.update(3,0)
    
    time.sleep(1)
    print("Blue")
    dmx.update(1,0)
    dmx.update(2,0)
    dmx.update(3,255)

    sys.exit(app.exec())