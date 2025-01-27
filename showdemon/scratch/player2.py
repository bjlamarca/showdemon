import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

class AudioTimeline(QWidget):
    def __init__(self):
        super().__init__()

        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)

        self.timeline = QSlider(Qt.Orientation.Horizontal)
        self.timeline.setRange(0, 0)  # Set the range when the media is loaded
        self.timeline.sliderMoved.connect(self.seek)

        layout = QVBoxLayout()
        layout.addWidget(self.timeline)
        self.setLayout(layout)

    def load_audio(self, file_path):
        self.player.setSource(file_path)
        self.player.durationChanged.connect(self.set_timeline_range)
        self.player.play()

    def set_timeline_range(self, duration):
        self.timeline.setRange(0, duration)

    def seek(self, position):
        self.player.setPosition(position)

def run_gui():
    app = QApplication(sys.argv)
    window = AudioTimeline()
    window.show()
    window.load_audio("showgui/media/haunted_house.wav")  # Replace with your audio file
    sys.exit(app.exec())