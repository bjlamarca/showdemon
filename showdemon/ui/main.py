import threading
import sys, time

from PySide6.QtCore import QSize, QThread, QObject, Signal, Slot
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QBoxLayout, QVBoxLayout, QLabel, QHBoxLayout, QComboBox, QCheckBox, QRadioButton, QTextEdit
from PySide6.QtWidgets import   QSlider, QSpinBox, QProgressBar, QTableWidget, QTableWidgetItem, QLineEdit, QDockWidget, QSizePolicy, QSpacerItem, QLayout, QMenu 
from PySide6.QtGui import  QAction

from devices.interfaces import DMXInterface
from .devicelib import DevLibWindow
from .device import DeviceWindow
from .control import MainControlWindow
from devices.midi import Midi
from showdemon.threads import ThreadTracker
from showdemon.threads import ThreadTracker
from .utilities import get_icon_obj, load_stylesheet


from devices.colors import colors_db_sync, color_sort

        

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

        setup_menu = QMenu('Setup', self)
        
        dev_liv_action = QAction('Device Library', self)
        dev_liv_action.triggered.connect(self.show_devlib_window)
        setup_menu.addAction(dev_liv_action)
        
        device_action = QAction('Device', self)
        device_action.triggered.connect(self.show_device_window)
        setup_menu.addAction(device_action)
        
        
        menu_bar.addMenu(setup_menu)

        control_menu = QMenu('Control', self)
        channel_action = QAction('Control Window', self)
        channel_action.triggered.connect(self.show_control_channel_window)
        control_menu.addAction(channel_action)
        menu_bar.addMenu(control_menu)

        self.label_dmx_status = QLabel('DMX Status')
        button_start_dmx = QPushButton('Start')
        button_start_dmx.clicked.connect(self.start_dmx)
        button_stop_dmx = QPushButton('Stop')
        button_stop_dmx.clicked.connect(self.stop_dmx)
        button_test_dmx = QPushButton('Start DMX Process')
        button_test_dmx.clicked.connect(self.start_dmx_process)
        

        
        
        second_layout = QVBoxLayout()
        second_layout.addWidget(self.label_dmx_status)
        second_layout.addWidget(button_start_dmx)
        second_layout.addWidget(button_stop_dmx)
        second_layout.addWidget(button_test_dmx)
        second_layout.addStretch()

        
        
        midi_layout = QVBoxLayout()
        midi_label = QLabel("Midi")
        btn_start_midi = QPushButton("Start")
        btn_start_midi.clicked.connect(self.start_midi)
        btn_listen_midi = QPushButton("Listen")
        btn_listen_midi.clicked.connect(self.listen_midi)
        btn_stop_midi = QPushButton("Stop")
        btn_stop_midi.clicked.connect(self.stop_midi)
        btn_test = QPushButton("Test")
        btn_test.clicked.connect(self.test)

        midi_layout.addWidget(midi_label)
        midi_layout.addWidget(btn_start_midi)
        midi_layout.addWidget(btn_listen_midi)
        midi_layout.addWidget(btn_stop_midi)
        midi_layout.addWidget(btn_test)
        midi_layout.addStretch()

        thread_layout = QVBoxLayout()
        thread_label = QLabel("Threads")
        btn_get_thread = QPushButton("Get Threads")
        btn_get_thread.clicked.connect(self.thread_get)
        thread_msg_label = QLabel("Message")
        self.thread_msg = QLabel("No Message")
        thread_layout.addWidget(thread_label)
        thread_layout.addWidget(btn_get_thread)
        thread_layout.addWidget(thread_msg_label)
        thread_layout.addWidget(self.thread_msg)
        thread_layout.addStretch()
        

       
        h_layout = QHBoxLayout()
        h_layout.addLayout(second_layout)
        h_layout.addSpacing(30) 
        h_layout.addLayout(midi_layout)
        h_layout.addSpacing(30)
        h_layout.addLayout(thread_layout)
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

    

    def start_midi(self):
        print("Start Midi")
        midi = Midi()
        midi.connect()

    def listen_midi(self):
        print("Listen Midi")
        midi = Midi()
        midi.start_listen()
    
    def stop_midi(self):
        print("Stop Midi")
        midi = Midi()
        midi.stop_listen()

    def thread_get(self):
        print("Get Threads")
        tracker = ThreadTracker()
        threads = tracker.get_all_thread_info()
        self.thread_msg.setText(str(threads))

    
   
    def start_dmx(self):
        dmx = DMXInterface()
        result = dmx.start_dmx()
        self.label_dmx_status.setText(result)

    def stop_dmx(self):
        dmx = DMXInterface()
        result = dmx.stop_dmx()
        self.label_dmx_status.setText(result)

    def start_dmx_process(self):
        dmx = DMXInterface()
        dmx.start_process_lookup()
    
    def test(self):
        colors_db_sync()
        color_sort()
        pass

    def show_devlib_window(self, checked):
        self.new_window = DevLibWindow()
        self.new_window.resize(QSize(600, 900))
        self.new_window.show()
        
    def show_device_window(self, checked):
        self.device_win = DeviceWindow()
        self.device_win.resize(QSize(600, 900))
        self.device_win.show()

    def show_control_channel_window(self, checked):
        self.control_win = MainControlWindow()
        self.control_win.resize(QSize(600, 600))
        self.control_win.show()

   

        

def app_thread():
    app = QApplication(sys.argv)
    window = MainWindow()
    #app.setStyleSheet(load_stylesheet())
    window.setGeometry(200, 200, 800, 600)
    window.show()
    app.exec_()
    

def start_app():
    thread_tracker = ThreadTracker()
    thread_tracker.start_thread(app_thread, 'UI_MAIN')
    
    # process = threading.Thread(target=app_thread)
    # process.daemon = True
    # process.start()


    







