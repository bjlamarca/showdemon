from PySide6.QtWidgets import (QWidget, QPushButton, QMessageBox, QVBoxLayout, QLabel, QHBoxLayout, QComboBox,
    QTableWidget, QTableWidgetItem, QLineEdit, QTabWidget, QDialog, QDialogButtonBox, QAbstractItemView, QFrame)
from .utilities import get_icon_obj
from devices.models import LibraryDevice

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
        dev_tbl_layout.addWidget(self.device_table)
        dev_tbl_layout.addStretch()

        dev_vert_layout.addLayout(dev_btn_layout)
        dev_vert_layout.addLayout(dev_tbl_layout)
        dev_vert_layout.addStretch()
        dev_horz_layout.addLayout(dev_vert_layout)
        dev_horz_layout.addStretch()
        dev_layout.addLayout(dev_horz_layout)




    def add_device(self):
        dlg_add_device = DeviceAddEditDialog(dlg_type='add')
        dlg_add_device.resize(400, 200)
        dlg_add_device.exec_()

    def edit_device(self):
        pass

    def del_device(self):
        pass


class DeviceAddEditDialog(QDialog):
    def __init__(self, dlg_type=None, dev_id=None):
        super().__init__()
        self.setWindowTitle("Add/Edit Device")
        dev_layout = QVBoxLayout()

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
        dev_lib_qs = LibraryDevice.objects.all()
        for dev in dev_lib_qs:
            self.type_combo.addItem(dev.name, dev.pk)
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type_combo)
        type_layout.addStretch()

        dmx_frame = QFrame()
        dmx_layout = QHBoxLayout()
        dmx_label = QLabel('DMX Start Channel:')
        dmx_label.setMinimumWidth(100)
        self.dmx_start = QLineEdit()
        dmx_layout.addWidget(dmx_label)
        dmx_layout.addWidget(self.dmx_start)
        dmx_layout.addStretch()
        dmx_frame.setLayout(dmx_layout)


        btn_layout = QHBoxLayout()
        btn_cancel = QPushButton('Cancel')
        btn_cancel.clicked.connect(self.reject)
        btn_add = QPushButton('Add')
        btn_add.clicked.connect(self.add_device)
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_add)
        btn_layout.addStretch()

        msg_layout = QHBoxLayout()
        self.msg_label = QLabel('')
        msg_layout.addWidget(self.msg_label)
        msg_layout.addStretch()


        dev_layout.addLayout(name_layout)
        dev_layout.addLayout(type_layout)
        dev_layout.addWidget(dmx_frame) 
        dev_layout.addLayout(btn_layout)
        dev_layout.addLayout(msg_layout)
        dev_layout.addStretch()

       

        self.setLayout(dev_layout)

    def add_device(self):
        pass


    