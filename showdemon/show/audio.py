import sys
import librosa
import numpy as np
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt

class WaveformWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.audio_file = 'C:\\Dev\\showdemon\\showdemon\\static\\audio\\HauntedHouse.mp3'
        self.y, self.sr = librosa.load(self.audio_file, sr=None)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()

        # Normalize the waveform
        y_norm = self.y / np.max(np.abs(self.y))

        # Calculate the number of samples per pixel
        samples_per_pixel = len(self.y) // width

        for x in range(width):
            start_sample = x * samples_per_pixel
            end_sample = start_sample + samples_per_pixel
            sample_values = y_norm[start_sample:end_sample]
            y_value = np.mean(sample_values) * height / 2 + height / 2

            painter.setPen(QPen(QColor(0, 0, 0), 1))
            painter.drawLine(x, height / 2, x, y_value)