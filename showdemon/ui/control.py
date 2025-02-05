from PySide6.QtWidgets import (QWidget, QPushButton, QMessageBox, QVBoxLayout, QLabel, QHBoxLayout, QComboBox, QSlider, QGroupBox,
    QTableWidget, QTableWidgetItem, QLineEdit, QTabWidget, QDialog, QFrame, QAbstractItemView, QCheckBox, QMainWindow)

from PySide6.QtCore import Qt
from devices.interfaces import DMXInterface
from devices.models import Device, Channel, ChannelParameter, DeviceFeature, LibraryChannel, LibraryDevice

from devices.signals import dmx_signal
import uuid
from django.dispatch import Signal, receiver
from static.style import resources_rc
from devices.models import Color


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
        self.device = Device.objects.get(pk=self.device_id)
        self.dmx = DMXInterface()
        self.uuid = uuid.uuid4()

        dmx_signal.connect(self.receive_dmx_signal)
        self.setWindowTitle("Control")
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.layout = QVBoxLayout(main_widget)
        
        self.slide_ctl_frame = QFrame()
        self.slide_ctl_frame.setMinimumHeight(300)

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
        self.device_record = Device.objects.get(pk=device_id)
       
        
        self.setWindowTitle('Feature Control')
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.layout = QVBoxLayout(main_widget)
        
        horz_layout = QHBoxLayout()

        feat_v_layout = QVBoxLayout()
        
        device_layout = QHBoxLayout()
        # device_lbl = QLabel('Device')
        # device_lbl.setMinimumWidth(100)
        device_val_lbl = QLabel(self.device_record.name)
        device_val_lbl.setStyleSheet('font-weight: bold; font-size: 16px;')
        #device_layout.addWidget(device_lbl)
        device_layout.addWidget(device_val_lbl)
        device_layout.addStretch()
        feat_v_layout.addLayout(device_layout)
        
        self.feat_h_layout = QHBoxLayout()
        
        self.create_feature_widgets()
        
        feat_v_layout.addLayout(self.feat_h_layout)
        self.feat_h_layout.addStretch()
        
        horz_layout.addLayout(feat_v_layout)
        horz_layout.addStretch()
        self.layout.addLayout(horz_layout)
        self.layout.addStretch()

        
    def create_feature_widgets(self):
        libdev_record = self.device_record.device_library
        feature_qs = DeviceFeature.objects.filter(library_device=libdev_record).order_by('sort_order')

        for feature in feature_qs:
            if feature.feature_class == 'DMX_DIMM':
                self.feat_h_layout.addWidget(DMXDimmerWidget(device_id=self.device_id, feature_id=feature.pk))
            elif feature.feature_class == 'DMX_SELECT':
                self.feat_h_layout.addWidget(DMXSelectorWidget(device_id=self.device_id, feature_id=feature.pk))
            elif feature.feature_class == 'DMX_RGB':
                self.feat_h_layout.addWidget(DMXRGBWidget(device_id=self.device_id, feature_id=feature.pk))           

class DMXSelectorWidget(QGroupBox):
    def __init__(self, device_id, feature_id):
        super().__init__()
        self.device_id = device_id
        self.feature_id = feature_id
        device_record = Device.objects.get(pk=device_id)
        feature_record = DeviceFeature.objects.get(pk=feature_id)
        lib_channel_qs = LibraryChannel.objects.filter(device_feature=feature_record)
        
        lib_channel = lib_channel_qs[0] #should only be one
        self.parm_qs = ChannelParameter.objects.filter(library_channel=lib_channel).order_by('int_min')
        channel_qs = Channel.objects.filter(library_channel=lib_channel, device=device_record)
        self.channel = channel_qs[0] #should only be one
        self.current_value = self.channel.int_value
        
        dmx_signal.connect(self.receive_dmx_signal)
        self.dmx = DMXInterface()
        self.uuid = uuid.uuid4()
        
        self.setTitle(feature_record.name)
        main_layout = QVBoxLayout()
        
        value_layout = QHBoxLayout()
        self.value_lbl = QLabel('Value')
        self.value_lbl.setAlignment(Qt.AlignCenter)
        value_layout.addWidget(self.value_lbl)
        value_layout.setAlignment(self.value_lbl, Qt.AlignCenter)
        
        
        
        slider_layout = QVBoxLayout()
        self.feat_slider = QSlider()
        self.feat_slider.setFixedHeight(220)
        self.feat_slider.setDisabled(True)
        slider_layout.addWidget(self.feat_slider)
        slider_layout.setAlignment(self.feat_slider, Qt.AlignCenter)
        
        
        set_btn_layout = QHBoxLayout()
        self.btn_set = QPushButton('Set')
        self.btn_set.clicked.connect(self.send_update)
        set_btn_layout.addWidget(self.btn_set)
        set_btn_layout.setAlignment(self.btn_set, Qt.AlignCenter)

        combo_layout = QVBoxLayout()
        self.feat_combo = QComboBox()
        self.feat_combo.addItem('', 0)
        for parm in self.parm_qs:
            self.feat_combo.addItem(parm.name, parm.pk)
        self.feat_combo.currentIndexChanged.connect(self.combo_changed)
        combo_layout.addWidget(self.feat_combo)

       
        main_layout.addLayout(value_layout)
        main_layout.addLayout(slider_layout)
        main_layout.addLayout(combo_layout)
        main_layout.addLayout(set_btn_layout)
        main_layout.addStretch()
        
        self.setLayout(main_layout)
        
        self.setMinimumWidth(100)
    

    def combo_changed(self):
        if self.feat_combo.currentData() != 0:
            parm_qs = ChannelParameter.objects.get(pk=self.feat_combo.currentData())
            self.value_lbl.setText(parm_qs.name)
            if parm_qs.allow_fading:
                self.feat_slider.setDisabled(False)
                self.feat_slider.setRange(parm_qs.int_min, parm_qs.int_max)
                self.feat_slider.setValue(parm_qs.int_min)
            else:
                self.feat_slider.setDisabled(True)
                self.feat_slider.setRange(parm_qs.int_min, parm_qs.int_max)
                self.feat_slider.setValue(parm_qs.int_min)
            

    def set_slider(self):
        pass

    def set_current_value(self, value):
        index = 0
        for parm in self.parm_qs:
            if value >= parm.int_min and value <= parm.int_max:
                self.value_lbl.setText(parm.name)
                if parm.allow_fading:
                    self.feat_slider.setDisabled(False)
                    self.feat_slider.setRange(parm.int_min, parm.int_max)
                    self.feat_slider.setValue(value)
                else:
                    self.feat_slider.setDisabled(True)
                    self.feat_slider.setRange(parm.int_min, parm.int_max)
                    self.feat_slider.setValue(value)
                    
                break
            index += 1

    def send_update(self):
        send_dict = {'channel': self.channel.system_channel, 'value': self.feat_slider.value(), 'requester': self.uuid}
        dmx_signal.send(sender=self.uuid, data_dict=send_dict)

    def receive_dmx_signal(self, sender, **kwargs):
        if sender == 'DMX-INTERFACE':
            data = kwargs.get('data_dict')
            if data['requester'] != self.uuid:
                if data['channel'] == self.channel.system_channel:
                    value = data['value']
                    self.set_current_value(value)
                    self.current_value = value
        
        
class DMXDimmerWidget(QGroupBox):
    def __init__(self, device_id, feature_id):
        super().__init__()
        self.device_id = device_id
        self.feature_id = feature_id
        device_record = Device.objects.get(pk=device_id)
        feature_record = DeviceFeature.objects.get(pk=feature_id)
        lib_channel_qs = LibraryChannel.objects.filter(device_feature=feature_record)
        lib_channel = lib_channel_qs[0] #should only be one
        channel_qs = Channel.objects.filter(library_channel=lib_channel, device=device_record)
        self.channel = channel_qs[0] #should only be one
        self.current_value = self.channel.int_value

        dmx_signal.connect(self.receive_dmx_signal)
        self.dmx = DMXInterface()
        self.uuid = uuid.uuid4()
        


        main_layout = QVBoxLayout()
        
        self.setTitle(feature_record.name)

       
        ctrl_layout = QVBoxLayout()
        self.feat_slider = QSlider()
        self.feat_slider.setFixedHeight(250)
        self.feat_slider.setRange(0, 255)
        ctrl_layout.addWidget(self.feat_slider)
        ctrl_layout.setAlignment(Qt.AlignCenter)
        ctrl_layout.addStretch()

        set_btn_layout = QHBoxLayout()
        self.btn_set = QPushButton('Set')
        self.btn_set.clicked.connect(self.send_update)
        set_btn_layout.addWidget(self.btn_set)
        set_btn_layout.addStretch()
        set_btn_layout.setAlignment(self.btn_set, Qt.AlignCenter)
       
        main_layout.addLayout(ctrl_layout)
        main_layout.addLayout(set_btn_layout)
        main_layout.addStretch()
        self.setLayout(main_layout)
        self.setMinimumWidth(100)

        self.set_current_value(self.current_value)


    def set_current_value(self, value):
        self.feat_slider.setValue(value)

    def send_update(self):
        send_dict = {'channel': self.channel.system_channel, 'value': self.feat_slider.value(), 'requester': self.uuid}
        dmx_signal.send(sender=self.uuid, data_dict=send_dict)

    def receive_dmx_signal(self, sender, **kwargs):
        if sender == 'DMX-INTERFACE':
            data = kwargs.get('data_dict')
            if data['requester'] != self.uuid:
                if data['channel'] == self.channel.system_channel:
                    value = data['value']
                    self.set_current_value(value)
                    self.current_value = value


        
class DMXRGBWidget(QGroupBox):
    def __init__(self, parent=None, device_id=None, feature_id=None):
        super().__init__(parent)
        self.device_id = device_id
        self.feature_id = feature_id
        device_record = Device.objects.get(pk=device_id)
        feature_record = DeviceFeature.objects.get(pk=feature_id)
        lib_channel_qs = LibraryChannel.objects.filter(device_feature=feature_record).order_by('sort_order')
        self.red_channel = Channel.objects.get(library_channel=lib_channel_qs[0], device=device_record)
        self.green_channel = Channel.objects.get(library_channel=lib_channel_qs[1], device=device_record)
        self.blue_channel = Channel.objects.get(library_channel=lib_channel_qs[2], device=device_record)
        self.red_current_value = self.red_channel.int_value
        self.green_current_value = self.green_channel.int_value
        self.blue_current_value = self.blue_channel.int_value  
        
        dmx_signal.connect(self.receive_dmx_signal)
        self.dmx = DMXInterface()
        self.uuid = uuid.uuid4()

        colors = Color.objects.all()
        main_layout = QVBoxLayout()
        
        self.setTitle(feature_record.name)  
        
    
        combo_layout = QVBoxLayout()
        self.color_combo = QComboBox()
        self.color_combo.currentIndexChanged.connect(self.color_combo_changed)
        self.color_combo.addItem('', 0)
        colors = Color.objects.all()
        for color in colors:
            self.color_combo.addItem(color.name, color.pk)
        self.color_combo.setMinimumWidth(50)
        combo_layout.addWidget(self.color_combo)
        
        slider_layout = QHBoxLayout()
        
        red_layout = QVBoxLayout()
        red_lbl = QLabel('Red')
        red_lbl.setAlignment(Qt.AlignCenter)       
        red_layout.addWidget(red_lbl)
        self.red_slider = QSlider()
        self.red_slider.setRange(0, 255)
        self.red_slider.setFixedHeight(200)
        self.red_slider.valueChanged.connect(self.red_changed)
        red_layout.addWidget(self.red_slider)
        red_layout.setAlignment(self.red_slider, Qt.AlignCenter)
        
        green_layout = QVBoxLayout()
        green_lbl = QLabel('Green')
        green_layout.setAlignment(Qt.AlignCenter)
        green_layout.addWidget(green_lbl)
        self.green_slider = QSlider()
        self.green_slider.setRange(0, 255)
        self.green_slider.setFixedHeight(200)
        self.green_slider.valueChanged.connect(self.green_changed)
        green_layout.addWidget(self.green_slider)
        green_layout.setAlignment(self.green_slider, Qt.AlignCenter)

        blue_layout = QVBoxLayout()
        blue_lbl = QLabel('Blue')
        blue_layout.setAlignment(Qt.AlignCenter)
        blue_layout.addWidget(blue_lbl)
        self.blue_slider = QSlider()
        self.blue_slider.setRange(0, 255)
        self.blue_slider.setFixedHeight(200)
        blue_layout.addWidget(self.blue_slider)
        blue_layout.setAlignment(self.blue_slider, Qt.AlignCenter)

        slider_layout.addLayout(red_layout)
        slider_layout.addLayout(green_layout)
        slider_layout.addLayout(blue_layout)

        set_btn_layout = QHBoxLayout()
        self.btn_set = QPushButton('Set')
        self.btn_set.clicked.connect(self.send_update)
        set_btn_layout.addWidget(self.btn_set)
        set_btn_layout.addStretch()
        set_btn_layout.setAlignment(self.btn_set, Qt.AlignCenter)

        main_layout.addLayout(combo_layout)
        main_layout.addLayout(slider_layout)
        main_layout.addLayout(set_btn_layout)
        main_layout.addStretch()
        self.setLayout(main_layout)

        self.set_current_values(self.red_current_value, self.green_current_value, self.blue_current_value)

    def set_current_values(self, red, green, blue):
        self.red_slider.setValue(red)
        self.green_slider.setValue(green)
        self.blue_slider.setValue(blue)

    def color_combo_changed(self):
        color_id = self.color_combo.currentData()
        color_record = Color.objects.get(pk=color_id)
        if color_id != 0:
            self.red_slider.setValue(color_record.red)
            self.green_slider.setValue(color_record.green)
            self.blue_slider.setValue(color_record.blue)  
        
    def red_changed(self, value):
        pass

    def green_changed(self, value):
        pass

    def blue_changed(self, value):
        pass
    
    def send_update(self):
        send_dict = {'channel': self.red_channel.system_channel, 'value': self.red_slider.value(), 'requester': self.uuid}
        dmx_signal.send(sender=self.uuid, data_dict=send_dict)
        send_dict = {'channel': self.green_channel.system_channel, 'value': self.green_slider.value(), 'requester': self.uuid}
        dmx_signal.send(sender=self.uuid, data_dict=send_dict)
        send_dict = {'channel': self.blue_channel.system_channel, 'value': self.blue_slider.value(), 'requester': self.uuid}

    def receive_dmx_signal(self, sender, **kwargs):
        if sender == 'DMX-INTERFACE':
            data = kwargs.get('data_dict')
            if data['requester'] != self.uuid:
                if data['channel'] == self.red_channel.system_channel:
                    value = data['value']
                    self.red_slider.setValue(value)
                    self.red_current_value = value
                elif data['channel'] == self.green_channel.system_channel:
                    value = data['value']
                    self.green_slider.setValue(value)
                    self.green_current_value = value
                elif data['channel'] == self.blue_channel.system_channel:
                    value = data['value']
                    self.blue_slider.setValue(value)
                    self.blue_current_value = value

