from PySide6.QtWidgets import (QWidget, QPushButton, QMessageBox, QVBoxLayout, QLabel, QHBoxLayout, QComboBox, QSlider,
    QTableWidget, QTableWidgetItem, QLineEdit, QTabWidget, QDialog, QFrame, QAbstractItemView, QCheckBox, QMainWindow)

from PySide6.QtCore import Qt
from devices.interfaces import DMXInterface
from devices.models import Device, Channel, ChannelParameter, DeviceFeature, LibraryChannel

from devices.signals import dmx_signal
import uuid
from django.dispatch import Signal, receiver
from static.style import resources_rc

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
        #self.device_list.setStyleSheet("QComboBox::down-arrow {image: url('C:/Dev/showdemon/showdemon/static/fugue-2x-icons/icons-2x/arrow-down.png');}")
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
        self.channel_list = []

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
                    self.channel_list.append(channel.system_channel)
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
            if data['requester'] != self.uuid:
                if data['channel'] in self.channel_list:
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
        
        horz_layout = QHBoxLayout()

        self.frame1 = QFrame()
        self.frame1.setMinimumHeight(300)

        layout1_layout = QVBoxLayout()
        layout1_lbl = QLabel('Features')
        layout1_layout.addWidget(layout1_lbl)
        layout1_layout.addWidget(DMXSelectorWidget(device_id=self.device_id, feature_id=6))
        self.frame1.setLayout(layout1_layout)
        horz_layout.addWidget(self.frame1)
        
        self.frame2 = QFrame()
        self.frame2.setMinimumHeight(300)

        layout2_layout = QVBoxLayout()
        layout2_lbl = QLabel('Features')
        layout2_layout.addWidget(layout2_lbl)
        layout2_layout.addWidget(DMXDimmerWidget(device_id=self.device_id, feature_id=4))
        self.frame2.setLayout(layout2_layout)
        horz_layout.addWidget(self.frame2)
        


        self.layout.addLayout(horz_layout)

        
                 

class DMXSelectorWidget(QWidget):
    def __init__(self, device_id, feature_id):
        super().__init__()
        self.device_id = device_id
        self.feature_id = feature_id
        device_qs = Device.objects.get(pk=device_id)
        feature_qs = DeviceFeature.objects.get(pk=feature_id)
        lib_channel_qs = LibraryChannel.objects.filter(device_feature=feature_qs)
        
        lib_channel = lib_channel_qs[0]
        self.parm_qs = ChannelParameter.objects.filter(library_channel=lib_channel).order_by('int_min')
        channel_qs = Channel.objects.filter(library_channel=lib_channel, device=device_qs)
        self.channel = channel_qs[0]
        self.current_value = self.channel.int_value
        

                
        dmx_signal.connect(self.receive_dmx_signal)
        self.dmx = DMXInterface()
        self.uuid = uuid.uuid4()
        self.layout = QVBoxLayout()
        horz_layout = QHBoxLayout() 
        title_layout = QHBoxLayout()
        title_feat_txt_lbl = QLabel(feature_qs.name)
        title_feat_txt_lbl.setStyleSheet('font-weight: bold;')
        title_layout.addWidget(title_feat_txt_lbl)
        title_layout.addStretch()
        self.layout.addLayout(title_layout)


        ctrl_layout = QVBoxLayout()
        self.feat_combo = QComboBox()
        for parm in self.parm_qs:
            self.feat_combo.addItem(parm.name, parm.pk)
        self.feat_combo.currentIndexChanged.connect(self.combo_changed)
        ctrl_layout.addWidget(self.feat_combo)
        self.feat_slider = QSlider()
        self.feat_slider.setFixedHeight(250)
        self.feat_slider.setDisabled(True)
        ctrl_layout.addWidget(self.feat_slider)
        ctrl_layout.addStretch()

        
        horz_layout.addLayout(ctrl_layout)
        
        horz_layout.addStretch()
        self.layout.addLayout(horz_layout)
        self.layout.addStretch()
        self.setLayout(self.layout)

        self.set_current_value(self.current_value)

    def combo_changed(self):
        parm_qs = ChannelParameter.objects.get(pk=self.feat_combo.currentData())
        if parm_qs.allow_fading:
            self.feat_slider.setDisabled(False)
            self.feat_slider.setRange(parm_qs.int_min, parm_qs.int_max)
            self.feat_slider.setValue(parm_qs.int_min)
        else:
            self.feat_slider.setValue(0)
            self.feat_slider.setDisabled

    def set_slider(self):
        pass

    def set_current_value(self, value):
        index = 0
        for parm in self.parm_qs:
            if value >= parm.int_min and value <= parm.int_max:
                self.feat_combo.setCurrentIndex(index)
                if parm.allow_fading:
                    self.feat_slider.setDisabled(False)
                    self.feat_slider.setRange(parm.int_min, parm.int_max)
                    self.feat_slider.setValue(value)
                else:
                    self.feat_slider.setValue(0)
                    self.feat_slider.setDisabled(True)
                break
            index += 1

    def receive_dmx_signal(self, sender, **kwargs):
        if sender == 'DMX-INTERFACE':
            data = kwargs.get('data_dict')
            if data['requester'] != self.uuid:
                if data['channel'] == self.channel.system_channel:
                    channel = data['channel']
                    value = data['value']
                    self.set_current_value(value)
                    self.current_value = value
        
        
class DMXDimmerWidget(QWidget):
    def __init__(self, device_id, feature_id):
        super().__init__()
        self.device_id = device_id
        self.feature_id = feature_id
        device_qs = Device.objects.get(pk=device_id)
        feature_qs = DeviceFeature.objects.get(pk=feature_id)
        lib_channel_qs = LibraryChannel.objects.filter(device_feature=feature_qs)
        lib_channel = lib_channel_qs[0]
        channel_qs = Channel.objects.filter(library_channel=lib_channel, device=device_qs)
        self.channel = channel_qs[0]
        self.current_value = self.channel.int_value

        


        dmx_signal.connect(self.receive_dmx_signal)
        self.dmx = DMXInterface()
        self.uuid = uuid.uuid4()
        self.layout = QVBoxLayout()
        horz_layout = QHBoxLayout() 
        title_layout = QHBoxLayout()
        title_feat_txt_lbl = QLabel(feature_qs.name)
        title_feat_txt_lbl.setStyleSheet('font-weight: bold;')
        title_layout.addWidget(title_feat_txt_lbl)
        title_layout.addStretch()
        self.layout.addLayout(title_layout)

        ctrl_layout = QVBoxLayout()
        self.feat_slider = QSlider()
        self.feat_slider.setFixedHeight(250)
        self.feat_slider.setDisabled(True)
        ctrl_layout.addWidget(self.feat_slider)
        ctrl_layout.addStretch()


        horz_layout.addLayout(ctrl_layout)
        
        horz_layout.addStretch()
        self.layout.addLayout(horz_layout)
        self.layout.addStretch()
        self.setLayout(self.layout)

        self.set_current_value(self.current_value)


    def set_current_value(self, value):
        self.feat_slider.setValue(value)

    def receive_dmx_signal(self, sender, **kwargs):
        if sender == 'DMX-INTERFACE':
            data = kwargs.get('data_dict')
            if data['requester'] != self.uuid:
                if data['channel'] == self.channel.system_channel:
                    channel = data['channel']
                    value = data['value']
                    self.set_current_value(value)
                    self.current_value = value


        




