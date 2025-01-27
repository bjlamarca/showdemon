from PyQt6.QtCore import Qt, QTimeLine, QSize, QUrl
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QPushButton, QVBoxLayout, QFileDialog, QSlider, QProgressBar, QLabel
from PyQt6.QtGui import QIcon
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
import sys

from charset_normalizer import from_path, detect, from_bytes

def example1():
    app = QApplication(sys.argv)

    window = QMainWindow()
    window.statusBar().showMessage("Hello World!")
    window.menuBar().addMenu("File")
    window.show()

    sys.exit(app.exec())


class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.player = QMediaPlayer()
        self.audio = QAudioOutput()
        self.player.setAudioOutput(self.audio)
        self.audio.setVolume(50)

        #self.player.setSource(QUrl.fromLocalFile('/example_wave.wav'))
        
        
        
       
        self.setGeometry(200,200,800,800)
        self.setWindowTitle("Show Demon")
        
        open_button = QPushButton("Open File")
        open_button.clicked.connect(self.open_file)

        play_button = QPushButton("Play", self)
        play_button.clicked.connect(self.playfile)

        stop_button = QPushButton("Stop", self)
        stop_button.clicked.connect(self.stopfile)



        progressBar = QProgressBar(self)

        self.label1 = QLabel(self)
        self.label2 = QLabel(self)
        self.label3 = QLabel(self)
        self.label4 = QLabel(self)
        
        #self.timeline = QSlider(Qt.Orientation.Horizontal)
        self.timeline = QTimeLine(5000, self)
        self.timeline.setFrameRange(0, 100)
        self.timeline.frameChanged.connect(self.timeChanged)
        #self.timeline.sliderMoved.connect(self.set_position)

        #progressBar.setValue

        layout = QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.label2)
        layout.addWidget(open_button)
        layout.addWidget(play_button)
        layout.addWidget(open_button)
        layout.addWidget(stop_button)
        layout.addWidget(progressBar)
        

        self.setLayout(layout)

        #self.timeline = QTimeLine(10000, self) # Duration: 1000 ms
       
        #self.timeline.valueChanged.connect(self.update_player_position)
    
    def timeChanged(self):
        self.label1.setNum(self.timeline.currentTime())
        self.label2.setNum(self.timeline.currentFrame())

    def startAnimation(self):
        self.timeline.start()

    def playfile(self):
        print("Start")
        #self.player.play()
        self.timeline.start()

    def stopfile(self):
        print("Stop")
        #self.player.stop()
        file_path = 'C:/Users/blamarca/OneDrive/Documents/VenueMagic/Projects/HalloweenProject1.vmp' 
        #results = from_path(file_path)
        #print(str(results.best()))
        with open(file_path, 'rb') as file:
            content = file.read()
            print(str(from_bytes(content).best()))
            #print(content.decode('cp1252'))
            result = detect(content)
            if result['encoding'] is not None:
                print('got', result['encoding'], 'as detected encoding')
            else:
                print('None!')
            #     
            #     print(content)
            #     #print(str(file, encoding='utf-8'))
    
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Audio File", "", )
        if file_path:
            self.player.setSource(QUrl.fromLocalFile(file_path))
            print("Media", file_path, str(self.player.errorString()))
           
            
    
    def set_position(self, position):
        self.player.setPosition(position)

    # def updateButtonSize(self, frame):
    #     size = QSize(100 + frame, 50)
    #     print('Size:', size)
    #     self.button.setFixedSize(size)

   

def example2():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    example2()


#layout.addWidget(self.button)

#self.setWindowIcon(QIcon('showgui/media/demon.png'))
#self.setStyleSheet('background-color:blue')
#self.setWindowOpacity(0.5)
#self.timeline.setFrameRange(0, 100)
#self.timeline.frameChanged.connect(self.updateButtonSize)
#self.button = QPushButton("Start Animation")
#self.button.clicked.connect(self.startAnimation)

 # def update_player_position(self, value):
    #     # Map timeline value (0-1) to audio duration
    #     position = int(value * self.player.duration())
    #     self.player.setPosition(position)
 # def update_player_position(self, value):
    #     # Map timeline value (0-1) to audio duration
    #     position = int(value * self.player.duration())
    #     self.player.setPosition(position)