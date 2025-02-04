from PySide6.QtWidgets import (QWidget, QPushButton, QMessageBox, QVBoxLayout, QLabel, QHBoxLayout, QComboBox, QSlider,
    QTableWidget, QTableWidgetItem, QLineEdit, QTabWidget, QDialog, QFrame, QAbstractItemView, QCheckBox, QMainWindow)

from PySide6.QtCore import Qt
from devices.interfaces import DMXInterface
from devices.models import Device, Channel, ChannelParameter, DeviceFeature

from devices.signals import dmx_signal
import uuid
from django.dispatch import Signal, receiver

@receiver(dmx_signal)
def handle_device_signal(sender, **kwargs):
    pass


class MainControlWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Device Control")
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.layout = QVBoxLayout(main_widget)

        self.dev_frame = QFrame()
        #self.dev_frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        dev_layout = QVBoxLayout()

        dev_choice_layout = QHBoxLayout()
        lbl_dev_choice = QLabel("Device")
        lbl_dev_choice.setMinimumWidth(100)
        self.device_list = QComboBox()
        #self.device_list.currentIndexChanged.connect(self.device_selected)
        device_qs = Device.objects.all()
        self.device_list.addItem("Select Device", 0)
        for device in device_qs:
            self.device_list.addItem(device.name, device.pk)
        dev_choice_layout.addWidget(lbl_dev_choice)
        dev_choice_layout.addWidget(self.device_list)
        dev_choice_layout.addStretch()

        dev_btn_layout = QHBoxLayout()
        self.btn_dev_channel = QPushButton('Channel Control')
        self.btn_dev_channel.clicked.connect(self.show_channel_window)
        dev_btn_layout.addWidget(self.btn_dev_channel)
        self.btn_dev_feature = QPushButton('Feature Control')
        self.btn_dev_feature.clicked.connect(self.show_feature_window)
        dev_btn_layout.addWidget(self.btn_dev_feature)
        dev_btn_layout.addStretch()


        dev_layout.addLayout(dev_choice_layout)
        dev_layout.addLayout(dev_btn_layout)
        dev_layout.addStretch()
        self.dev_frame.setLayout(dev_layout)

        self.layout.addWidget(self.dev_frame)
        self.layout.addStretch()
       

    def show_channel_window(self):
        if self.device_list.currentData() != 0:
            device_id = self.device_list.currentData()
            self.channel_window = DMXChannelWindow(device_id=device_id)
            self.channel_window.show()

    def show_feature_window(self):
        if self.device_list.currentData() != 0:
            device_id = self.device_list.currentData()
            self.feature_window = DMXFeatureWindow(device_id=device_id)
            self.feature_window.show()

class DMXChannelWindow(QMainWindow):
    def __init__(self, parent=None, device_id=None):
        super().__init__(parent)
        self.device_id = device_id

        dmx_signal.connect(self.receive_dmx_signal)
        self.setWindowTitle("Control")
        self.dmx = DMXInterface()
        self.uuid = uuid.uuid4()
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.layout = QVBoxLayout(main_widget)


       
        self.slide_ctl_frame = QFrame()
        self.slide_ctl_frame.setMinimumHeight(300)

        self.device = Device.objects.get(pk=self.device_id)
            
        slide_v_layout = QVBoxLayout()
        
        dev_name_layout = QHBoxLayout()
        lbl_dev_name = QLabel('Device:')
        lbl_dev_name.setMinimumWidth(100)
        lbl_dev_name_val = QLabel(self.device.name)
        dev_name_layout.addWidget(lbl_dev_name)
        dev_name_layout.addWidget(lbl_dev_name_val)
        dev_name_layout.addStretch()
        slide_v_layout.addLayout(dev_name_layout)

        self.slide_ctl_layout = QHBoxLayout()
        
        self.create_sliders()

        self.slide_ctl_layout.addStretch()
        slide_v_layout.addLayout(self.slide_ctl_layout)
        #slide_v_layout.addStretch()

        self.slide_ctl_frame.setLayout(slide_v_layout)
        
        self.layout.addWidget(self.slide_ctl_frame)
        
    def create_sliders(self):
        
        channel_qs = Channel.objects.filter(device=self.device).order_by('channel_number')
        if channel_qs:
            for channel in channel_qs:
                    slide_layout = QVBoxLayout()
                    slide_lbl = QLabel(channel.library_channel.name + ' ' + str(channel.system_channel))
                    slide_slider = QSlider()
                    slide_slider.setObjectName(f'slide_{channel.system_channel}')
                    slide_slider.setFixedHeight(250)
                    slide_slider.setOrientation(Qt.Vertical)
                    slide_slider.setRange(0, 255)
                    slide_slider.setMinimumWidth(75)
                    slide_slider.valueChanged.connect(lambda value, index=channel.system_channel: self.slider_changed(value, index))
                    slide_slider.setValue(channel.int_value)
                    slide_layout.addWidget(slide_lbl)
                    slide_layout.addWidget(slide_slider)
                    slide_layout.addStretch()
                    self.slide_ctl_layout.addLayout(slide_layout)
                    self.slide_ctl_layout.addSpacing(20)
      
    
    def receive_dmx_signal(self, sender, **kwargs):
        if sender == 'DMX-INTERFACE':
            data = kwargs.get('data_dict')
            #print('Sender', sender, 'Data', data)
            if data['requester'] != self.uuid:
                channel = data['channel']
                value = data['value']
                slider = self.slide_ctl_frame.findChild(QSlider, f'slide_{channel}')
                slider.setValue(value)
                      
        

    def slider_changed(self, value, index):
        send_dict = {'channel': index, 'value': value, 'requester': ''}
        dmx_signal.send(sender=self.uuid, data_dict=send_dict)
       
class DMXFeatureWindow(QMainWindow):
    def __init__(self, parent=None, device_id=None):
        super().__init__(parent)
        self.device_id = device_id
        self.device = Device.objects.get(pk=device_id)
        
        self.setWindowTitle("Feature Control")
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.layout = QVBoxLayout(main_widget)
        
        self.frame1 = QFrame()
        self.frame1.setMinimumHeight(300)

        layout1_layout = QVBoxLayout()
        layout1_lbl = QLabel('Features')
        layout1_layout.addWidget(layout1_lbl)
        layout1_layout.addWidget(SelectorWidget(device_id=self.device_id, feature_id=0))
        self.frame1.setLayout(layout1_layout)
        self.layout.addWidget(self.frame1)

        
                 

class SelectorWidget(QWidget):
    def __init__(self, device_id, feature_id):
        super().__init__()
        self.device_id = device_id
        self.feature_id = feature_id
        #device_qs = Device.objects.get(pk=device_id)
        #feature_qs = DeviceFeature.objects.get(pk=feature_id)


        self.layout = QVBoxLayout()
        
        layout_main = QHBoxLayout()
        main_lbl = QLabel('Main')
        layout_main.addWidget(main_lbl)
        layout_main.addStretch()

        self.layout.addLayout(layout_main)
        
        
        
        self.setLayout(self.layout)
        
        
        
        self.device_list = QComboBox()
        




