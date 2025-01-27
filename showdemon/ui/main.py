import threading
import sys, time

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QBoxLayout, QVBoxLayout, QLabel, QHBoxLayout, QComboBox, QCheckBox, QRadioButton, QTextEdit
from PySide6.QtWidgets import   QSlider, QSpinBox, QProgressBar, QTableWidget, QTableWidgetItem, QLineEdit, QDockWidget, QSizePolicy, QSpacerItem, QLayout, QMenu 
from PySide6.QtGui import  QAction

from devices.interfaces import DMXInterface
from .devicelib import DevLibWindow



        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ShowDemon")
        
        # Main Widget and Layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        menu_bar = self.menuBar()
        
        file_menu = QMenu("File", self)
        exit_action = QAction("Exit", self)
        exit_action.setStatusTip("Exit the application")
        exit_action.triggered.connect(self.close)  # Connect to the close method
        file_menu.addAction(exit_action)
        menu_bar.addMenu(file_menu)

        win_menu = QMenu('Window', self)
        dev_liv_action = QAction('Device Library', self)
        dev_liv_action.triggered.connect(self.show_devlib_window)
        win_menu.addAction(dev_liv_action)
        menu_bar.addMenu(win_menu)




        label_dmx_status = QLabel('DMX Status')
        button_start_dmx = QPushButton('Start')
        button_stop_dmx = QPushButton('Stop')
        button_test_dmx = QPushButton('Test')
        
        
        second_layout = QVBoxLayout()
        second_layout.addWidget(label_dmx_status)
        second_layout.addWidget(button_start_dmx)
        second_layout.addWidget(button_stop_dmx)
        second_layout.addWidget(button_test_dmx)
        second_layout.addStretch()

        a_label = QLabel("Hello World")
        
        third_layout = QVBoxLayout()
        
        third_layout.addWidget(a_label)
        third_layout.addStretch()
        #third_layout.sizeConstraint = QLayout.SetFixedSize

       
        h_layout = QHBoxLayout()
        h_layout.addLayout(second_layout)
        h_layout.addLayout(third_layout)
        h_layout.addStretch()
        
        main_layout.addLayout(h_layout)
        
        label = QLabel("Hello World")
       

          
        # Function to add widget with label
        def add_widget_with_label(layout, widget, label_text):
            hbox = QHBoxLayout()
            
            label = QLabel(label_text)
            hbox.addWidget(label)
            hbox.addWidget(widget)
            layout.addLayout(hbox)

              

        self.show_devlib_window(True)
        
        # # QLabel
        # self.label_dmx_status = QLabel('DMX Status')
        # add_widget_with_label(main_layout, self.label_dmx_status, 'QLabel:')

        # # QPushButton
        # self.button_start_dmx = QPushButton('Start')
        # #self.button_start_dmx.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # self.button_start_dmx.clicked.connect(self.on_button_start_dmx_clicked)
        # add_widget_with_label(main_layout, self.button_start_dmx, 'QPushButton:')

        # # QPushButton
        # self.button_stop_dmx = QPushButton('Stop')
        # self.button_stop_dmx.clicked.connect(self.on_button_stop_dmx_clicked)
        # add_widget_with_label(main_layout, self.button_stop_dmx, 'QPushButton:')

        # self.button_test_dmx = QPushButton('Test')
        # self.button_test_dmx.clicked.connect(self.on_button_test_dmx_clicked)
        # add_widget_with_label(main_layout, self.button_test_dmx, 'QPushButton:')
    
    def show_devlib_window(self, checked):
        print('Checked:', checked)
        self.dev_lib_win = DevLibWindow()
        self.dev_lib_win.resize(QSize(400, 200))
        self.dev_lib_win.show()
   
    def on_button_start_dmx_clicked(self):
        dmx = DMXInterface()
        result = dmx.start_dmx()
        self.label_dmx_status.setText(result)

    def on_button_stop_dmx_clicked(self):
        dmx = DMXInterface()
        result = dmx.stop_dmx()
        self.label_dmx_status.setText(result)

    def on_button_test_dmx_clicked(self):
        dmx = DMXInterface()
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



def app_thread():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    app.exec_()
    

def start_app():
    process = threading.Thread(target=app_thread)
    process.daemon = True
    process.start()


    







