from PySide6.QtWidgets import (QWidget, QPushButton, QMessageBox, QVBoxLayout, QLabel, QHBoxLayout, QComboBox,
    QTableWidget, QTableWidgetItem, QLineEdit, QTabWidget, QDialog, QDialogButtonBox, QAbstractItemView, QFrame)
from .utilities import get_icon_obj
from devices.models import LibraryDevice, Device
from devices.constants import SystemType
from devices.systems import DMX

class DeviceWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Devices")
        dev_layout = QVBoxLayout()
        self.setLayout(dev_layout)

        dev_horz_layout = QHBoxLayout()
        dev_vert_layout = QVBoxLayout()

        dev_btn_layout = QHBoxLayout()
        btn_add_device = QPushButton('Add Device')
        btn_add_device.clicked.connect(self.add_device)
        btn_add_device.setIcon(get_icon_obj('plus-circle'))
        btn_edit_device = QPushButton('Edit Device')
        btn_edit_device.clicked.connect(self.edit_device)
        btn_edit_device.setIcon(get_icon_obj('pencil'))
        btn_del_device = QPushButton('Delete Device')
        btn_del_device.clicked.connect(self.del_device)
        btn_del_device.setIcon(get_icon_obj('cross-circle'))
        dev_btn_layout.addWidget(btn_add_device)
        dev_btn_layout.addWidget(btn_edit_device)
        dev_btn_layout.addWidget(btn_del_device)
        dev_btn_layout.addStretch()

        dev_tbl_layout = QHBoxLayout()
        self.device_table = QTableWidget()
        self.device_table.setMinimumWidth(500)
        dev_tbl_layout.addWidget(self.device_table)
        dev_tbl_layout.addStretch()

        msg_layout = QHBoxLayout()
        self.msg_label = QLabel('')
        msg_layout.addWidget(self.msg_label)
        msg_layout.addStretch()

        dev_vert_layout.addLayout(dev_btn_layout)
        dev_vert_layout.addLayout(dev_tbl_layout)
        dev_vert_layout.addLayout(msg_layout)
        dev_vert_layout.addStretch()
        dev_horz_layout.addLayout(dev_vert_layout)
        dev_horz_layout.addStretch()
        dev_layout.addLayout(dev_horz_layout)

        self.fill_dev_table()


    def fill_dev_table(self):
        self.device_table.clear()
        self.device_table.setColumnCount(4)
        self.device_table.setHorizontalHeaderLabels(['Name', 'System', 'Type', 'ID'])
        self.device_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.device_table.setSelectionMode(QAbstractItemView.SingleSelection)
        dev_qs = Device.objects.all()
        self.device_table.setRowCount(dev_qs.count())
        row = 0
        for dev in dev_qs:
            self.device_table.setItem(row, 0, QTableWidgetItem(dev.name))
            self.device_table.setItem(row, 1, QTableWidgetItem(dev.device_library.system))
            self.device_table.setItem(row, 2, QTableWidgetItem(dev.device_library.name))
            self.device_table.setItem(row, 3, QTableWidgetItem(str(dev.pk)))
            row += 1
        
        

    def add_device(self):
        dlg_add_device = DeviceAddEditDialog(dlg_type='add')
        dlg_add_device.resize(400, 200)
        if dlg_add_device.exec_():
            self.fill_dev_table()

    def edit_device(self):
        
        if not self.device_table.currentRow() == -1:
            device_id = int(self.device_table.item(self.device_table.currentRow(), 3).text())
            dlg_edit_device = DeviceAddEditDialog(dlg_type='edit', dev_id=device_id)
            dlg_edit_device.resize(400, 200)
            if dlg_edit_device.exec_():
                self.fill_dev_table()

    def del_device(self):
        if not self.device_table.currentRow() == -1:
            dlg_diag = QMessageBox(
                QMessageBox.Question,
                'Delete Device',
                'Are you sure you want to delete this device?',
                QMessageBox.Yes | QMessageBox.No
            )
            if dlg_diag.exec_() == QMessageBox.Yes:
                dmx = DMX()
                device_id = int(self.device_table.item(self.device_table.currentRow(), 3).text())
                result = dmx.delete_device(device_id)
                if result['result']:
                    self.fill_dev_table()
                    self.msg_label.setText(result['message'])
                else:
                    self.msg_label.setText(result['message'])
                    self.msg_label.setStyleSheet('color: red')
        else:
            self.msg_label.setText('No Device Selected')


class DeviceAddEditDialog(QDialog):
    def __init__(self, dlg_type=None, dev_id=None):
        super().__init__()
        if dlg_type == 'add':
            self.setWindowTitle("Add Device")
        else:
            self.setWindowTitle("Edit Device")

        self.dlg_type = dlg_type
        self.dev_id = dev_id
        self.system = ''
        self.dmx_start_channel = 0
        dev_layout = QVBoxLayout()

        system_frame = QFrame()
        system_layout = QHBoxLayout()
        system_label = QLabel('System:')
        system_label.setMinimumWidth(100)
        self.system_combo = QComboBox()
        self.system_combo.addItem('Choose System', '') 
        for system in SystemType():
            self.system_combo.addItem(system[1], system[0])
        self.system_combo.currentIndexChanged.connect(self.system_changed)
           
        system_layout.addWidget(system_label)
        system_layout.addWidget(self.system_combo)
        system_layout.addStretch()
        system_frame.setLayout(system_layout)


        name_layout = QHBoxLayout()
        name_label = QLabel('Name:')
        name_label.setMinimumWidth(100)
        self.name_txt = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_txt)
        name_layout.addStretch()

        type_layout = QHBoxLayout()
        type_label = QLabel('Device Type:')
        type_label.setMinimumWidth(100)
        self.type_combo = QComboBox()
        self.type_combo.addItem('Choose Type', '')
                  
        self.type_combo.currentIndexChanged.connect(self.dev_type_changed)
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type_combo)
        type_layout.addStretch()



        
        dmx_chnl_layout = QVBoxLayout()
        
        dmx_chnl_count_layout = QHBoxLayout()
        dmx_chnl_count_label = QLabel('Channels:')
        dmx_chnl_count_label.setMinimumWidth(100)
        self.dmx_chnl_count = QLabel('0')
        dmx_chnl_count_layout.addWidget(dmx_chnl_count_label)
        dmx_chnl_count_layout.addWidget(self.dmx_chnl_count)
        dmx_chnl_count_layout.addStretch()

        dmx_chnl_pos_layout = QHBoxLayout()
        dmx_chnl_pos_start_label = QLabel('Start:')
        dmx_chnl_pos_start_label.setMinimumWidth(100)
        self.dmx_chnl_pos_start = QLineEdit()
        self.dmx_chnl_pos_start.setFixedWidth(50)
        #dmx_chml_pos_end_label = QLabel('End:')
        #self.dmx_chnl_pos_end = QLineEdit()
        dmx_chnl_pos_layout.addWidget(dmx_chnl_pos_start_label)
        dmx_chnl_pos_layout.addWidget(self.dmx_chnl_pos_start)
        #dmx_chnl_pos_layout.addWidget(dmx_chml_pos_end_label)
        #dmx_chnl_pos_layout.addWidget(self.dmx_chnl_pos_end)
        dmx_chnl_pos_layout.addStretch()

        dmx_chnl_layout.addLayout(dmx_chnl_count_layout)
        dmx_chnl_layout.addLayout(dmx_chnl_pos_layout)
        dmx_chnl_layout.addStretch()
        


        btn_layout = QHBoxLayout()
        btn_cancel = QPushButton('Cancel')
        btn_cancel.clicked.connect(self.reject)
        if self.dlg_type == 'add':
            self.btn_add_edit = QPushButton('Add')
            self.btn_add_edit.clicked.connect(self.add_device)
        else:
            self.btn_add_edit = QPushButton('Edit')
            self.btn_add_edit.clicked.connect(self.edit_device)
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(self.btn_add_edit)
        btn_layout.addStretch()

        msg_layout = QHBoxLayout()
        self.msg_label = QLabel('')
        msg_layout.addWidget(self.msg_label)
        msg_layout.addStretch()

        self.dmx_frame = QFrame()
        dmx_frame_layout = QVBoxLayout()
        dmx_frame_layout.addLayout(type_layout)
        dmx_frame_layout.addLayout(name_layout)
        dmx_frame_layout.addLayout(dmx_chnl_layout)
        dmx_frame_layout.addLayout(btn_layout)
        dmx_frame_layout.addLayout(msg_layout)
        self.dmx_frame.setLayout(dmx_frame_layout)

        # dev_layout.addLayout(name_layout)
        # dev_layout.addLayout(type_layout)
        # dev_layout.addWidget(dmx_frame) 
        # dev_layout.addLayout(btn_layout)
        # dev_layout.addLayout(msg_layout)
        dev_layout.addWidget(system_frame)
        dev_layout.addWidget(self.dmx_frame)
        dev_layout.addStretch()

        self.dmx_frame.hide()
        self.setLayout(dev_layout)

        if self.dlg_type == 'edit':
            dev_qs = Device.objects.get(pk=self.dev_id)
            self.name_txt.setText(dev_qs.name)
            self.system_combo.setCurrentText(dev_qs.device_library.system)
            self.system_combo.setEnabled(False)
            self.type_combo.setCurrentText(dev_qs.device_library.name)
            self.type_combo.setEnabled(False)
            dmx = DMX()
            self.dmx_start_channel = dmx.get_start_channel(self.dev_id)
            self.dmx_chnl_pos_start.setText(str(self.dmx_start_channel))
            
            
            

    def system_changed(self):
        self.system = self.system_combo.currentData()
        if self.system == 'DMX':
            dev_lib_qs = LibraryDevice.objects.filter(system='DMX')
            for dev in dev_lib_qs:
                self.type_combo.addItem(dev.name, dev.pk)
            self.dmx_frame.show()
        else:
            self.dmx_frame.hide()

    def dev_type_changed(self):
        if self.system == 'DMX':
            dmx_sys = DMX()
            chnl_count = dmx_sys.get_lib_dev_channel_count(self.type_combo.currentData())
            self.dmx_chnl_count.setText(str(chnl_count))
            if self.dlg_type == 'add':
                self.name_txt.setText(self.type_combo.currentText())
                self.dmx_chnl_pos_start.setText(str(dmx_sys.next_start_channel(chnl_count)))
    
    def add_device(self):
        if self.system == 'DMX':
            dmx_sys = DMX()
            
            result = dmx_sys.add_device(int(self.type_combo.currentData()), self.name_txt.text(), int(self.dmx_chnl_pos_start.text()))
            if result['result']:
                self.accept()
            else:
                self.msg_label.setText(result['message'])
                self.msg_label.setStyleSheet('color: red')

    def edit_device(self):
        if self.system == 'DMX':
            dmx_sys = DMX()
            result = dmx_sys.edit_device(self.dev_id, self.name_txt.text(), int(self.dmx_chnl_pos_start.text()))
            if result['result']:
                self.accept()
            else:
                self.msg_label.setText(result['message'])
                self.msg_label.setStyleSheet('color: red')
            


    