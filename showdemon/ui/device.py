from PySide6.QtWidgets import (QWidget, QPushButton, QMessageBox, QVBoxLayout, QLabel, QHBoxLayout, QComboBox,
    QTableWidget, QTableWidgetItem, QLineEdit, QTabWidget, QDialog, QDialogButtonBox, QAbstractItemView,)


class DeviceWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Devices")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

      