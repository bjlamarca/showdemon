import sys
import librosa
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class WaveformWidget(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)

    def plot_waveform(self, filename):
        y, sr = librosa.load(filename)
        self.axes.clear()
        self.axes.plot(y, color='black')
        self.draw()

class AudioPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.player = QMediaPlayer()
        self.waveform = WaveformWidget(self)

        layout = QVBoxLayout()
        layout.addWidget(self.waveform)

        controls_layout = QHBoxLayout()
        # Add play/pause, stop, etc. buttons here
        layout.addLayout(controls_layout)

        self.setLayout(layout)

        self.player.setMedia(QMediaContent(QUrl.fromLocalFile("showgui/media/haunted_house.wav")))
        self.waveform.plot_waveform("showgui/media/haunted_house.wav")

def run_gui():
    app = QApplication(sys.argv)
    player = AudioPlayer()
    player.show()
    sys.exit(app.exec_())