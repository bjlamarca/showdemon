from PySide6.QtWidgets import (QWidget, QPushButton, QMessageBox, QVBoxLayout, QLabel, QHBoxLayout, QComboBox,
    QTableWidget, QTableWidgetItem, QLineEdit, QTabWidget, QDialog, QFrame, QAbstractItemView, QCheckBox, QMainWindow)

from PySide6.QtCore import QSize

from devices.models import Manufacture, LibraryDevice, DeviceFeature, LibraryChannel, ChannelParameter, Color
from devices.constants import SystemType, Interfaces, FeatureList, ChannelType
from devices.features import Feature
from .utilities import get_icon_obj
from pprint import pprint

class DevLibWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Device Library")
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        self.layout = QVBoxLayout(main_widget)
      
        self.tab_widget = QTabWidget()
        self.tab_manuf = QWidget()
        self.tab_device = QWidget()
        self.tab3 = QWidget()

        self.tab_widget.addTab(self.tab_device, "Devices")
        self.tab_widget.addTab(self.tab_manuf, "Manufacture")
        
        
        msg_layout = QHBoxLayout()
        self.msg_label = QLabel('')
        msg_layout.addWidget(self.msg_label)
        msg_layout.addStretch()
        
        self.layout.addWidget(self.tab_widget)
        self.layout.addLayout(msg_layout)

        self.init_tab_manuf()
        self.init_tab_device()
        

    def init_tab_manuf(self):
        m_m_layout = QVBoxLayout(self.tab_manuf)
        m_h_layout = QHBoxLayout()
        m_layout = QVBoxLayout()
        
        m_btn_layout = QHBoxLayout()
        btn_add_manuf = QPushButton('Add')
        btn_add_manuf.clicked.connect(self.show_add_manuf_dlg)
        btn_add_manuf.setIcon(get_icon_obj('plus-circle'))
        btn_edit_manuf = QPushButton('Edit')
        btn_edit_manuf.clicked.connect(self.show_edit_manuf_dlg)
        btn_edit_manuf.setIcon(get_icon_obj('pencil'))
        btn_del_manuf = QPushButton('Delete')
        btn_del_manuf.clicked.connect(self.show_del_manuf_dlg)
        btn_del_manuf.setIcon(get_icon_obj('cross-circle'))
        m_btn_layout.addWidget(btn_add_manuf)
        m_btn_layout.addWidget(btn_edit_manuf)
        m_btn_layout.addWidget(btn_del_manuf)
        m_btn_layout.addStretch()

        m_tbl_layout = QHBoxLayout()
        self.manuf_table = QTableWidget()
        self.fill_manuf_table()
        m_tbl_layout.addWidget(self.manuf_table)
        m_tbl_layout.addStretch()

        m_layout.addLayout(m_btn_layout)
        m_layout.addLayout(m_tbl_layout)
        m_layout.addStretch()
        
        m_h_layout.addLayout(m_layout)
        m_h_layout.addStretch()
        m_m_layout.addLayout(m_h_layout)

    def init_tab_device(self):
        d_m_layout = QVBoxLayout(self.tab_device)
        d_h_layout = QHBoxLayout()
        d_layout = QVBoxLayout()
        
        d_btn_layout = QHBoxLayout()
        btn_add_device = QPushButton('Add')
        btn_add_device.setIcon(get_icon_obj('plus-circle'))
        btn_add_device.clicked.connect(self.show_add_device_dlg)
        btn_edit_device = QPushButton('Edit')
        btn_edit_device.setIcon(get_icon_obj('pencil'))
        btn_edit_device.clicked.connect(self.show_edit_device_dlg)
        btn_del_device = QPushButton('Delete')
        btn_del_device.setIcon(get_icon_obj('cross-circle'))
        btn_del_device.clicked.connect(self.show_del_device_dlg)
        btn_edit_device_features = QPushButton('Edit Features')
        btn_edit_device_features.setIcon(get_icon_obj('traffic-light--pencil'))
        btn_edit_device_features.clicked.connect(self.show_edit_device_feature_dlg)
        d_btn_layout.addWidget(btn_add_device)
        d_btn_layout.addWidget(btn_edit_device)
        d_btn_layout.addWidget(btn_del_device)
        d_btn_layout.addWidget(btn_edit_device_features)
        d_btn_layout.addStretch()

        d_tbl_layout = QHBoxLayout()
        self.device_table = QTableWidget()
        self.device_table.setMinimumWidth(550)
        self.fill_device_table()
        d_tbl_layout.addWidget(self.device_table)
        d_tbl_layout.addStretch()

        

        d_layout.addLayout(d_btn_layout)
        d_layout.addLayout(d_tbl_layout)
        
        d_layout.addStretch()
        
        d_h_layout.addLayout(d_layout)
        d_h_layout.addStretch()
        d_m_layout.addLayout(d_h_layout)

    

    def fill_manuf_table(self):
        self.manuf_table.clear()
        self.manuf_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.manuf_table.setSelectionMode
        self.manuf_table.setColumnCount(3)
        self.manuf_table.setHorizontalHeaderLabels(['Name', 'Comments', 'ID'])
        self.manuf_table.setRowCount(Manufacture.objects.count())
        for i, manuf in enumerate(Manufacture.objects.all()):
            self.manuf_table.setItem(i, 0, QTableWidgetItem(manuf.name))
            self.manuf_table.setItem(i, 1, QTableWidgetItem(manuf.comments))
            self.manuf_table.setItem(i, 2, QTableWidgetItem(str(manuf.pk)))
        #self.manuf_table.itemSelectionChanged.connect(self.manuf_table_clicked)

    def show_add_manuf_dlg(self, type):
        dlg = ManufDialog(self, 'add')
        dlg.resize(400, 200)
        if dlg.exec():
            self.fill_manuf_table()
        else:    
            pass

    def show_edit_manuf_dlg(self):
        if self.manuf_table.currentRow() != -1:
            manuf_id = int(self.manuf_table.item(self.manuf_table.currentRow(), 2).text())
            dlg = ManufDialog(self, 'edit', manuf_id)
            dlg.resize(400, 200)
            # if dlg.exec():
            #     self.fill_manuf_table()
            # else:    
            #     pass
            dlg.show()
    def show_del_manuf_dlg(self):
        if self.manuf_table.currentRow() != -1:
            del_diag = QMessageBox.warning(
                self,
                'Delete Manufacture',
                'Do you want to delete this manufacture?',
                QMessageBox.Yes | QMessageBox.No
            )
            if del_diag == QMessageBox.Yes:
                try:
                    manuf_id = int(self.manuf_table.item(self.manuf_table.currentRow(), 2).text())
                    manuf_qs = Manufacture.objects.get(pk=manuf_id)
                    manuf_qs.delete()
                except Exception as e:
                    if type(e).__name__ == 'ProtectedError':
                        self.msg_label.setText("Device is in use and cannot be deleted")
                        self.msg_label.setStyleSheet("color: red")
                else:
                    self.fill_manuf_table()

    def fill_device_table(self):
        self.device_table.clear()
        self.device_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.device_table.setSelectionMode
        self.device_table.setColumnCount(5)
        self.device_table.setHorizontalHeaderLabels(['Name', 'Manufacture', 'System', 'Description', 'ID'])
        self.device_table.setRowCount(LibraryDevice.objects.count())
        sys_type = SystemType()
        for i, device in enumerate(LibraryDevice.objects.all()):
            self.device_table.setItem(i, 0, QTableWidgetItem(device.name))
            self.device_table.setItem(i, 1, QTableWidgetItem(device.manufacture.name))
            self.device_table.setItem(i, 2, QTableWidgetItem(sys_type.get_display(device.system)))
            self.device_table.setItem(i, 3, QTableWidgetItem(device.description))
            self.device_table.setItem(i, 4, QTableWidgetItem(str(device.pk)))

    def show_add_device_dlg(self):
        dlg_add_dev = DeviceAddEditDialog(self, 'add')
        dlg_add_dev.resize(400, 200)
        if dlg_add_dev.exec():
            self.fill_device_table()
            
    def show_edit_device_dlg(self):
        if self.device_table.currentRow() != -1:
            device_id = int(self.device_table.item(self.device_table.currentRow(), 4).text())
            dlg_edit_dev = DeviceAddEditDialog(self, 'edit', device_id)
            dlg_edit_dev.resize(400, 200)
            if dlg_edit_dev.exec():
                self.fill_device_table()

    def show_edit_device_feature_dlg(self):
        if self.device_table.currentRow() != -1:
            device_id = int(self.device_table.item(self.device_table.currentRow(), 4).text())
            dlg_edit_dev = DeviceEditFeatureDialog(self, device_id)
            dlg_edit_dev.resize(600, 800)
            if dlg_edit_dev.exec():
                self.fill_device_table()
    
    

    def show_del_device_dlg(self):
        if self.device_table.currentRow() != -1:
            del_diag = QMessageBox.warning(
                self,
                'Delete Device',
                'Are you sure you want to delete this device?',
                QMessageBox.Yes | QMessageBox.No
            )
            if del_diag == QMessageBox.Yes:
                try:
                    device_id = int(self.device_table.item(self.device_table.currentRow(), 4).text())
                    device_qs = LibraryDevice.objects.get(pk=device_id)
                    device_qs.delete()
                except Exception as e:
                    if type(e).__name__ == 'ProtectedError':
                        self.msg_label.setText("Device is in use and cannot be deleted")
                        self.msg_label.setStyleSheet("color: red")
                else:
                    self.fill_device_table()

class ManufDialog(QDialog):
    def __init__(self, parent=None, type=None, manuf_id=None):
        super().__init__(parent)
        if type == 'add':
            self.setWindowTitle("Add Manufacture")
           
        elif type == 'edit':
            self.setWindowTitle("Edit Manufacture")
        
        layout = QVBoxLayout()
        
        n_layout = QHBoxLayout()
        lbl_name = QLabel("Name")
        self.txt_name = QLineEdit()
        n_layout.addWidget(lbl_name)
        n_layout.addWidget(self.txt_name)
        n_layout.addStretch()

        c_layout = QHBoxLayout()
        lbl_comm = QLabel("Comments")
        self.txt_comm = QLineEdit()
        c_layout.addWidget(lbl_comm)
        c_layout.addWidget(self.txt_comm)
        c_layout.addStretch()

        b_layout = QHBoxLayout()
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.reject)
        b_layout.addWidget(btn_cancel)
        if type == 'add':
            btn_add = QPushButton("Add")
            btn_add.clicked.connect(self.add_manuf)
            b_layout.addWidget(btn_add)
        elif type == 'edit':
            btn_edit = QPushButton("Save")
            btn_edit.clicked.connect(self.edit_manuf)
            b_layout.addWidget(btn_edit)
            self.manuf_qs = Manufacture.objects.get(pk=manuf_id)
            self.txt_name.setText(self.manuf_qs.name)
            self.txt_comm.setText(self.manuf_qs.comments)
        b_layout.addStretch()

        msg_layout = QHBoxLayout()
        self.msg_label = QLabel('')
        msg_layout.addWidget(self.msg_label)
        msg_layout.addStretch()

        layout.addLayout(n_layout)
        layout.addLayout(c_layout)
        layout.addLayout(b_layout)
        layout.addLayout(msg_layout)
        layout.addStretch()

        self.setLayout(layout)

    def add_manuf(self):
        name = self.txt_name.text()
        if name != "":
            new_manuf = Manufacture()
            new_manuf.name = name
            new_manuf.comments = self.txt_comm.text()
            new_manuf.save()
            self.parent().fill_manuf_table()
            self.close()
        else:
            self.msg_label.setText("Name cannot be empty")
            self.msg_label.setStyleSheet("color: red")
                   

    def edit_manuf(self):
        name = self.txt_name.text()
        if name != "":
            self.manuf_qs.name = name
            self.manuf_qs.comments = self.txt_comm.text()
            self.manuf_qs.save()
            self.parent().fill_manuf_table()
            self.close()
        else:
            self.msg_label.setText("Name cannot be empty")
            self.msg_label.setStyleSheet("color: red")
         

class DeviceAddEditDialog(QDialog):
    def __init__(self, parent=None, dlg_type=None, device_id=None):
        super().__init__(parent)
        if dlg_type == 'add':
            self.setWindowTitle("Add Device")
        elif dlg_type == 'edit':
            self.setWindowTitle("Edit Device")
            device_qs = LibraryDevice.objects.get(pk=device_id)
            self.device_id = device_id
                
        layout = QVBoxLayout()
        
        n_layout = QHBoxLayout()
        lbl_name = QLabel("Name")
        lbl_name.setMinimumWidth(100)
        self.txt_name = QLineEdit()
        if dlg_type == 'edit':
            self.txt_name.setText(device_qs.name)
        n_layout.addWidget(lbl_name)
        n_layout.addWidget(self.txt_name)
        n_layout.addStretch()

        m_layout = QHBoxLayout()
        lbl_manuf = QLabel("Manufacture")
        lbl_manuf.setMinimumWidth(100)
        self.manuf_list = QComboBox()
        mauf_qs = Manufacture.objects.all()
        for manuf in mauf_qs:
            self.manuf_list.addItem(manuf.name, manuf.pk)
        m_layout.addWidget(lbl_manuf)
        m_layout.addWidget(self.manuf_list)
        m_layout.addStretch()

        s_layout = QHBoxLayout()
        lbl_system = QLabel("System")
        lbl_system.setMinimumWidth(100)
        s_layout.addWidget(lbl_system)
        if dlg_type == 'add':
            self.system_list = QComboBox()
            for system in SystemType():
                self.system_list.addItem(system[1], system[0])
            s_layout.addWidget(self.system_list)
        elif dlg_type == 'edit':
            self.lbl_system_name = QLabel(device_qs.system)
            s_layout.addWidget(self.lbl_system_name)
        
        
        s_layout.addStretch()

        des_layout = QHBoxLayout()
        lbl_des = QLabel("Desription")
        lbl_des.setMinimumWidth(100)
        self.txt_des = QLineEdit()
        if dlg_type == 'edit':
            self.txt_des.setText(device_qs.description)
        des_layout.addWidget(lbl_des)
        des_layout.addWidget(self.txt_des)
        des_layout.addStretch()

        btn_layout = QHBoxLayout()
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancel)
        if dlg_type == 'add':
            btn_add = QPushButton("Add")
            btn_add.clicked.connect(self.add_device)
            btn_layout.addWidget(btn_add)
        elif dlg_type == 'edit':
            btn_edit = QPushButton("Save")
            btn_edit.clicked.connect(self.save_device)
            btn_layout.addWidget(btn_edit)
        btn_layout.addStretch()

        msg_layout = QHBoxLayout()
        self.msg_label = QLabel('')
        msg_layout.addWidget(self.msg_label)
        msg_layout.addStretch()

        layout.addLayout(n_layout)
        layout.addLayout(m_layout)
        layout.addLayout(s_layout)
        layout.addLayout(des_layout)
        layout.addSpacing(20)
        layout.addLayout(btn_layout)
        layout.addLayout(msg_layout)
        
        layout.addStretch()
        self.setLayout(layout)

    def add_device(self):
            
            name = self.txt_name.text()
            if name != "":
                manuf_qs = Manufacture.objects.get(pk=int(self.manuf_list.currentData()))
                new_device = LibraryDevice()
                new_device.name = name
                new_device.manufacture = manuf_qs
                new_device.system = self.system_list.currentData()
                new_device.description = self.txt_des.text()
                new_device.save()
                self.accept()
            else:
                self.msg_label.setText("Name cannot be empty")
                self.msg_label.setStyleSheet("color: red")

    def save_device(self):
        if self.txt_name.text() != "":
            device_qs = LibraryDevice.objects.get(pk=self.device_id)
            device_qs.name = self.txt_name.text()
            device_qs.manufacture = Manufacture.objects.get(pk=int(self.manuf_list.currentData()))
            device_qs.description = self.txt_des.text()
            device_qs.save()
            self.accept()
        else:
            self.msg_label.setText("Name cannot be empty")
            self.msg_label.setStyleSheet("color: red")
    


class DeviceEditFeatureDialog(QDialog):
    def __init__(self, parent=None, device_id=None):
        super().__init__(parent)
        
        self.feature_channel_list = []
        self.device_id = device_id
        device_qs = LibraryDevice.objects.get(pk=device_id)
        

        self.setWindowTitle("Edit Device")
                
        layout = QVBoxLayout()
        
        dev_title_layout = QHBoxLayout()
        lbl_title = QLabel("Device")
        lbl_title.setStyleSheet("font-weight: bold; color: blue; font-size: 16px;")
        dev_title_layout.addWidget(lbl_title)
        dev_title_layout.addStretch()

        n_layout = QHBoxLayout()
        lbl_name = QLabel("Name")
        lbl_name.setMinimumWidth(100)
        lbl_name_text = QLabel(device_qs.name)
        n_layout.addWidget(lbl_name)
        n_layout.addWidget(lbl_name_text)
        n_layout.addStretch()

        m_layout = QHBoxLayout()
        lbl_manuf = QLabel("Manufacture")
        lbl_manuf.setMinimumWidth(100)
        lbl_manuf_name = QLabel(device_qs.manufacture.name)
        m_layout.addWidget(lbl_manuf)
        m_layout.addWidget(lbl_manuf_name)
        m_layout.addStretch()


        s_layout = QHBoxLayout()
        lbl_system = QLabel("System")
        lbl_system.setMinimumWidth(100)
        self.lbl_system_name = QLabel("System Name")
        self.lbl_system_name.setText(SystemType().get_display(device_qs.system))
        self.lbl_system_name.setMinimumWidth(100)
        s_layout.addWidget(lbl_system)
        s_layout.addWidget(self.lbl_system_name)
        s_layout.addStretch()

        des_layout = QHBoxLayout()
        lbl_des = QLabel("Desription")
        lbl_des.setMinimumWidth(100)
        lbl_des_text = QLabel(device_qs.description)
        des_layout.addWidget(lbl_des)
        des_layout.addWidget(lbl_des_text)
        des_layout.addStretch()
        
        feature_layout = QHBoxLayout()
        lbl_feature = QLabel("Features")
        lbl_feature.setMinimumWidth(100)
        lbl_feature.setStyleSheet("font-weight: bold; color: blue; font-size: 16px;")
        feature_layout.addWidget(lbl_feature)
        feature_layout.addStretch()

        feature_btn_layout = QHBoxLayout()
        btn_add_feature = QPushButton("Add")
        btn_add_feature.setIcon(get_icon_obj('plus-circle'))
        btn_add_feature.clicked.connect(self.add_feature)
        btn_edit_feature = QPushButton("Edit")
        btn_edit_feature.setIcon(get_icon_obj('pencil'))
        btn_edit_feature.clicked.connect(self.edit_feature)
        btn_del_feature = QPushButton("Delete")
        btn_del_feature.setIcon(get_icon_obj('cross-circle'))
        btn_del_feature.clicked.connect(self.del_feature)
        btn_move_up = QPushButton()
        btn_move_up.clicked.connect(self.move_up)
        btn_move_up.setIcon(get_icon_obj('arrow-turn-090-left'))
        btn_move_down = QPushButton()
        btn_move_down.clicked.connect(self.move_down)
        btn_move_down.setIcon(get_icon_obj('arrow-turn-270-left'))

        feature_btn_layout.addWidget(btn_add_feature)
        feature_btn_layout.addWidget(btn_edit_feature)
        feature_btn_layout.addWidget(btn_del_feature)
        feature_btn_layout.addWidget(btn_move_up)
        feature_btn_layout.addWidget(btn_move_down)
        feature_btn_layout.addStretch()

        feature_table_label_layout = QHBoxLayout()
        lbl_feature_table = QLabel("Features")
        lbl_feature_table.setMinimumWidth(100)
        feature_table_label_layout.addWidget(lbl_feature_table)
        feature_table_label_layout.addStretch()

        channel_btn_layout = QHBoxLayout()
        btn_edit_feature = QPushButton("Edit")
        btn_edit_feature.setIcon(get_icon_obj('pencil'))
        btn_edit_feature.clicked.connect(self.edit_channel)
        channel_btn_layout.addWidget(btn_edit_feature)
        channel_btn_layout.addStretch()

        feature_table_layout = QVBoxLayout()
        self.feature_table = QTableWidget()
        feature_table_layout.addWidget(self.feature_table)
        feature_table_layout.addStretch()

        channel_table_label_layout = QHBoxLayout()
        lbl_channel_table = QLabel("Channels")
        lbl_channel_table.setMinimumWidth(100)
        channel_table_label_layout.addWidget(lbl_channel_table)
        channel_table_label_layout.addStretch()

        channel_table_layout = QVBoxLayout()
        self.channel_table = QTableWidget()
        
        channel_table_layout.addWidget(self.channel_table)
        channel_table_layout.addStretch()

        self.fill_feature_tables()
        
        layout.addLayout(dev_title_layout)
        layout.addLayout(n_layout)
        layout.addLayout(m_layout)
        layout.addLayout(s_layout)
        layout.addLayout(des_layout)
        layout.addSpacing(30)
        layout.addLayout(feature_layout)
        layout.addLayout(feature_btn_layout)
        layout.addLayout(feature_table_label_layout)
        layout.addLayout(feature_table_layout)
        layout.addLayout(channel_table_label_layout)
        layout.addLayout(channel_btn_layout)
        layout.addLayout(channel_table_layout)
        layout.addStretch()

        self.setLayout(layout)

    
    
    def fill_feature_tables(self):
        libdev_qs = LibraryDevice.objects.get(pk=self.device_id)
        feature_qs = DeviceFeature.objects.filter(library_device=libdev_qs).order_by('sort_order')
        feature_count = feature_qs.count()
    
        self.feature_table.clear()
        self.feature_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.feature_table.setSelectionMode
        self.feature_table.setColumnCount(4)
        self.feature_table.setHorizontalHeaderLabels(['Name', 'Type', 'Order', 'ID'])
        self.feature_table.setRowCount(feature_count)
        i = 0
        for feature in feature_qs:
            self.feature_table.setItem(i, 0, QTableWidgetItem(feature.name))
            self.feature_table.setItem(i, 1, QTableWidgetItem(feature.feature_class))
            self.feature_table.setItem(i, 2, QTableWidgetItem(str(feature.sort_order)))
            self.feature_table.setItem(i, 3, QTableWidgetItem(str(feature.pk)))
            i += 1

        self.channel_table.clear()
        self.channel_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.channel_table.setSelectionMode
        self.channel_table.setColumnCount(5)
        self.channel_table.setHorizontalHeaderLabels(['Name', 'Feature', 'Type', 'Order', 'ID'])

        channel_count  = 0
        for feature in feature_qs:
            channel_qs = LibraryChannel.objects.filter(device_feature=feature).order_by('sort_order')
            channel_count += channel_qs.count()
        self.channel_table.setRowCount(channel_count)
        self.channel_table.setMinimumHeight(300)
        i = 0
        for feature in feature_qs:
            channel_qs = LibraryChannel.objects.filter(device_feature=feature).order_by('sort_order')
            for channel in channel_qs:
                self.channel_table.setItem(i, 0, QTableWidgetItem(channel.name))
                self.channel_table.setItem(i, 1, QTableWidgetItem(feature.name))
                self.channel_table.setItem(i, 2, QTableWidgetItem(channel.channel_type))
                self.channel_table.setItem(i, 3, QTableWidgetItem(str(channel.sort_order)))
                self.channel_table.setItem(i, 4, QTableWidgetItem(str(channel.pk)))
                i += 1    
            
    def add_feature(self):
        dlg = FeatureDialog(self, dlg_type='add', devlib_id=self.device_id)
        dlg.resize(400, 200)
        if dlg.exec():
            self.fill_feature_tables()
            

    def edit_feature(self):
        if self.feature_table.currentRow() != -1:
            feature_id = int(self.feature_table.item(self.feature_table.currentRow(), 3).text())
            dlg = FeatureDialog(self, 'edit', feature_id)
            dlg.resize(400, 200)
            if dlg.exec():
                self.fill_feature_tables()
                

    def del_feature(self):
        if self.feature_table.currentRow() != -1:
            del_diag = QMessageBox.warning(
                self,
                'Delete Feature',
                'Are you sure you want to delete this feature?',
                QMessageBox.Yes | QMessageBox.No
            )
            if del_diag == QMessageBox.Yes:
                feature = Feature()
                feature.delete_feature(int(self.feature_table.item(self.feature_table.currentRow(), 3).text()))
                self.fill_feature_tables()

    def move_up(self):
        if self.feature_table.currentRow() != -1:
            feature = Feature()
            if feature.move_feature(int(self.feature_table.item(self.feature_table.currentRow(), 3).text()), 'up'):
                self.fill_feature_tables()

    def move_down(self):
        if self.feature_table.currentRow() != -1:
            feature = Feature()
            if feature.move_feature(int(self.feature_table.item(self.feature_table.currentRow(), 3).text()), 'down'):
                self.fill_feature_tables()

    def edit_channel(self):
        if self.channel_table.currentRow() != -1:
            channel_id = int(self.channel_table.item(self.channel_table.currentRow(), 4).text())
            dlg = ChannelDialog(self, channel_id)
            dlg.resize(400, 200)
            if dlg.exec():
                self.fill_feature_tables()

class FeatureDialog(QDialog):
    def __init__(self, parent=None, dlg_type=None, feature_id=None, devlib_id=None):
        super().__init__(parent)
        self.dlg_type = dlg_type
        self.devlib_id = devlib_id
        if dlg_type == 'add':
            self.setWindowTitle("Add Feature")
        elif dlg_type == 'edit':
            self.setWindowTitle("Edit Feature")
            self.feature_qs = DeviceFeature.objects.get(pk=feature_id)
                
        layout = QVBoxLayout()
        
        type_layout = QHBoxLayout()
        lbl_type = QLabel("Type")
        self.type_list = QComboBox()
        for feature in FeatureList():
            self.type_list.addItem(feature[1], feature[0])
        self.type_list.currentIndexChanged.connect(self.feature_combo_changed)
        if dlg_type=='edit':
            self.type_list.setEnabled(False)
        type_layout.addWidget(lbl_type)
        type_layout.addWidget(self.type_list)
        type_layout.addStretch()

        name_layout = QHBoxLayout()
        lbl_name = QLabel("Name")
        self.txt_name = QLineEdit()
        if dlg_type == 'edit':
            self.txt_name.setText(self.feature_qs.name)
        name_layout.addWidget(lbl_name)
        name_layout.addWidget(self.txt_name)
        name_layout.addStretch()

        hide_layout = QHBoxLayout()
        lbl_hide = QLabel("Hide")
        self.chk_hide = QCheckBox()
        if dlg_type == 'edit':
            self.chk_hide.setChecked(self.feature_qs.hide)
        else:
            self.chk_hide.setChecked(False)
        hide_layout.addWidget(lbl_hide)
        hide_layout.addWidget(self.chk_hide)
        hide_layout.addStretch()
        
        btn_layout = QHBoxLayout()
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancel)
        if dlg_type == 'add':
            btn_add = QPushButton("Add")
            btn_add.clicked.connect(self.add_feature)
            btn_layout.addWidget(btn_add)
            self.txt_name.setText(self.type_list.currentText())
        elif dlg_type == 'edit':
            btn_edit = QPushButton("Save")
            btn_edit.clicked.connect(self.edit_feature)
            btn_layout.addWidget(btn_edit)
           
        msg_layout = QHBoxLayout()
        self.msg_label = QLabel('')
        msg_layout.addWidget(self.msg_label)
        msg_layout.addStretch()

        layout.addLayout(type_layout)
        layout.addLayout(name_layout)
        layout.addLayout(hide_layout)
        layout.addLayout(btn_layout)
        layout.addLayout(msg_layout)
        layout.addStretch()
        self.setLayout(layout)

    def feature_combo_changed(self):
        if self.dlg_type=='add':
            self.txt_name.setText(self.type_list.currentText())

    def add_feature(self):
        if self.txt_name.text() != "":
            feature = Feature()
            feature.add_feature(self.type_list.currentData(), self.txt_name.text(), self.chk_hide.isChecked(), self.devlib_id)
            self.accept()
        else:
            self.msg_label.setText("Name cannot be empty")
            self.msg_label.setStyleSheet("color: red")

    def edit_feature(self):
        if self.txt_name.text() != "":
            self.feature_qs.name = self.txt_name.text()
            self.feature_qs.hide = self.chk_hide.isChecked()
            self.feature_qs.save()
            self.accept()
        else:
            self.msg_label.setText("Name cannot be empty")
            self.msg_label.setStyleSheet("color: red")

class ChannelDialog(QDialog):

    def __init__(self, parent=None, channel_id=None):
        super().__init__(parent)
             
        self.setWindowTitle("Edit Channel")
        self.channel_qs = LibraryChannel.objects.get(pk=channel_id)
        self.has_parameters = False
                
        
        self.top_frame = QFrame()
        top_layout = QVBoxLayout()

        type_layout = QHBoxLayout()
        lbl_type = QLabel("Type:")
        lbl_type.setMinimumWidth(100)
        chnl_type = ChannelType()
        lbl_type_display = QLabel(chnl_type.get_display(self.channel_qs.channel_type))
        type_layout.addWidget(lbl_type)
        type_layout.addWidget(lbl_type_display)
        type_layout.addStretch()

        name_layout = QHBoxLayout()
        lbl_name = QLabel("Name")
        lbl_name.setMinimumWidth(100)
        self.txt_name = QLineEdit()
        self.txt_name.setText(self.channel_qs.name)
        name_layout.addWidget(lbl_name)
        name_layout.addWidget(self.txt_name)
        name_layout.addStretch()

        startup_layout = QHBoxLayout()
        lbl_startup = QLabel("Startup Value")
        lbl_startup.setMinimumWidth(100)
        self.txt_startup = QLineEdit()
        self.txt_startup.setFixedWidth(30)
        self.txt_startup.setText(str(self.channel_qs.startup_int))
        startup_layout.addWidget(lbl_startup)
        startup_layout.addWidget(self.txt_startup)
        startup_layout.addStretch()


        btn_layout = QHBoxLayout()
        btn_edit = QPushButton("Save")
        btn_edit.clicked.connect(self.edit_channel)
        btn_layout.addWidget(btn_edit)
        btn_layout.addStretch()

        

        top_layout.addLayout(type_layout)
        top_layout.addLayout(name_layout)
        top_layout.addLayout(startup_layout)
        top_layout.addLayout(btn_layout)
        top_layout.addStretch()
        self.top_frame.setLayout(top_layout)
        
        self.parm_frame = QFrame()
        parm_layout = QVBoxLayout()

        parm_btn_layout = QHBoxLayout()
        btn_add_parm = QPushButton("Add")
        btn_add_parm.setIcon(get_icon_obj('plus-circle'))
        btn_add_parm.clicked.connect(self.add_parm)
        btn_edit_parm = QPushButton("Edit")
        btn_edit_parm.setIcon(get_icon_obj('pencil'))
        btn_edit_parm.clicked.connect(self.edit_parm)
        btn_del_parm = QPushButton("Delete")
        btn_del_parm.setIcon(get_icon_obj('cross-circle'))
        btn_del_parm.clicked.connect(self.del_parm)
        parm_btn_layout.addWidget(btn_add_parm)
        parm_btn_layout.addWidget(btn_edit_parm) 
        parm_btn_layout.addWidget(btn_del_parm)
        parm_btn_layout.addStretch()   
        
        
        parm_table_layout = QHBoxLayout()
        self.parm_table = QTableWidget()
        self.parm_table.setMinimumWidth(500)
        self.parm_table.setMinimumHeight(300)
        parm_table_layout.addWidget(self.parm_table)
        parm_table_layout.addStretch()

        parm_layout.addLayout(parm_btn_layout)
        parm_layout.addLayout(parm_table_layout)
        parm_layout.addStretch()
        self.parm_frame.setLayout(parm_layout)

        self.bottom_frame = QFrame()
        bottom_layout = QVBoxLayout()

        
           
        msg_layout = QHBoxLayout()
        self.msg_label = QLabel('')
        msg_layout.addWidget(self.msg_label)
        msg_layout.addStretch()

        bottom_layout.addLayout(msg_layout)
        bottom_layout.addStretch()
        self.bottom_frame.setLayout(bottom_layout)


        layout = QVBoxLayout()
        layout.addWidget(self.top_frame)
        layout.addWidget(self.parm_frame)
        layout.addWidget(self.bottom_frame)
        self.setLayout(layout)

        self.fill_parm_table()

    def fill_parm_table(self):
        feature = Feature()
        feature_cls = feature.get_feature_class(self.channel_qs.device_feature.feature_class)
        if feature_cls.has_parameters():
            self.has_parameters = True
            self.parm_frame.show()
            
            feature_fields = feature_cls.get_parameter_fields()
            self.parm_table.clear()
            self.parm_table.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.parm_table.setSelectionMode
            self.parm_table.setColumnCount(len(feature_fields)+2)
            header_list = []
            header_list.append('Name')
            for field in feature_fields:
                header_list.append(feature.get_parameter_field_display(field))
            header_list.append('ID')
            self.parm_table.setHorizontalHeaderLabels(header_list)
            chnl_parms = ChannelParameter.objects.filter(library_channel=self.channel_qs)
            self.parm_table.setRowCount(chnl_parms.count())
            row = 0
            for parm in chnl_parms:
                self.parm_table.setItem(row, 0, QTableWidgetItem(parm.name))
                column = 1
                for field in feature_fields:
                    self.parm_table.setItem(row, column, QTableWidgetItem(str(getattr(parm, field))))
                    column += 1
                self.parm_table.setItem(row, column, QTableWidgetItem(str(parm.pk)))
                row += 1      
                

        else:
            self.has_parameters = False
            self.parm_frame.hide()
            

    def edit_channel(self):
        
        save_record = False
        
        if self.txt_name.text() != "":
            try:
                statup_val = int(self.txt_startup.text())
            except:
                    self.msg_label.setText("Startup value must be an integer")
                    self.msg_label.setStyleSheet("color: red")
            else:
                save_record = True
        else:
            self.msg_label.setText("Name cannot be empty")
            self.msg_label.setStyleSheet("color: red")

        if save_record == True:
            self.channel_qs.name = self.txt_name.text()
            self.channel_qs.startup_int = statup_val
            self.channel_qs.save()
            self.accept()

        
    def add_parm(self):
        dlg_parm = ParmWindows(self, self.channel_qs, 'add')
        dlg_parm.resize(400, 600)
        if dlg_parm.exec():
            self.fill_parm_table()
        else:
            self.fill_parm_table()

    def edit_parm(self):
        if self.parm_table.currentRow() != -1:
            parm_id = int(self.parm_table.item(self.parm_table.currentRow(), 5).text())
            dlg_parm = ParmWindows(self, self.channel_qs, 'edit', parm_id)
            dlg_parm.resize(400, 600)
            if dlg_parm.exec():
                self.fill_parm_table()
            else:
                self.fill_parm_table    

    def del_parm(self):
        if self.parm_table.currentRow() != -1:
            del_diag = QMessageBox.warning(
                self,
                'Delete Parameter',
                'Are you sure you want to delete this parameter?',
                QMessageBox.Yes | QMessageBox.No
            )
            if del_diag == QMessageBox.Yes:
                try:
                    parm_id = int(self.parm_table.item(self.parm_table.currentRow(), 5).text())
                    parm_qs = ChannelParameter.objects.get(pk=parm_id)
                    parm_qs.delete()
                except Exception as e:
                    if type(e).__name__ == 'ProtectedError':
                        self.msg_label.setText("Parameter is in use and cannot be deleted")
                        self.msg_label.setStyleSheet("color: red")
                else:
                    self.fill_parm_table()
       

class ParmWindows(QDialog):
    def __init__(self, parent=None, channel_qs=None, dlg_type=None, channel_id=None):
        super().__init__(parent)
        self.channel_qs = channel_qs
        self.dlg_type = dlg_type
        layout = QVBoxLayout()

        if dlg_type == 'add':
            self.setWindowTitle("Add Parameter")
        elif dlg_type == 'edit':
            self.setWindowTitle("Edit Parameter")
            self.parm_qs = ChannelParameter.objects.get(pk=channel_id)


        color_layout = QHBoxLayout()
        lbl_color = QLabel("Color")
        lbl_color.setMinimumWidth(100)
        self.color_combo = QComboBox()
        self.color_combo.addItem('', 0)
        colors = Color.objects.all()
        for color in colors:
            self.color_combo.addItem(color.name, color.pk)
        self.color_combo.setMinimumWidth(50)
        self.color_combo.currentIndexChanged.connect(self.color_combo_changed)
        color_layout.addWidget(lbl_color)
        color_layout.addWidget(self.color_combo)
        color_layout.addStretch()

        name_layout = QHBoxLayout()
        lbl_name = QLabel("Name")
        lbl_name.setMinimumWidth(100)
        self.txt_name = QLineEdit()
        if dlg_type == 'edit':
            self.txt_name.setText(self.parm_qs.name)
        name_layout.addWidget(lbl_name)
        name_layout.addWidget(self.txt_name)
        name_layout.addStretch()

        allow_fading_layout = QHBoxLayout()
        lbl_fading = QLabel("Allow Fading")
        lbl_fading.setMinimumWidth(100)
        self.chk_fading = QCheckBox()
        if dlg_type == 'edit':
            self.chk_fading.setChecked(self.parm_qs.allow_fading)
        allow_fading_layout.addWidget(lbl_fading)
        allow_fading_layout.addWidget(self.chk_fading)
        allow_fading_layout.addStretch()

        min_layout = QHBoxLayout()
        lbl_min = QLabel("Min")
        lbl_min.setMinimumWidth(100)
        self.txt_min = QLineEdit()
        if dlg_type == 'edit':
            self.txt_min.setText(str(self.parm_qs.int_min))
        min_layout.addWidget(lbl_min)
        min_layout.addWidget(self.txt_min)
        min_layout.addStretch()

        max_layout = QHBoxLayout()
        lbl_max = QLabel("Max")
        lbl_max.setMinimumWidth(100)
        self.txt_max = QLineEdit()
        if dlg_type == 'edit':
            self.txt_max.setText(str(self.parm_qs.int_max))
        max_layout.addWidget(lbl_max)
        max_layout.addWidget(self.txt_max)
        max_layout.addStretch()

        value_layout = QHBoxLayout()
        lbl_value = QLabel("Value")
        lbl_value.setMinimumWidth(100)
        self.txt_value = QLineEdit()
        if dlg_type == 'edit':
            self.txt_value.setText(str(self.parm_qs.int_value))
        value_layout.addWidget(lbl_value)
        value_layout.addWidget(self.txt_value)

        str_layout = QHBoxLayout()
        lbl_str = QLabel("String Value")
        lbl_str.setMinimumWidth(100)
        self.txt_str = QLineEdit()
        if dlg_type == 'edit':
            self.txt_str.setText(self.parm_qs.str_value)
        str_layout.addWidget(lbl_str)
        str_layout.addWidget(self.txt_str)

        
        btn_layout = QHBoxLayout()
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancel)
        if dlg_type == 'add':
            btn_add = QPushButton("Add")
            btn_add.clicked.connect(self.add_parm)
            btn_layout.addWidget(btn_add)
        elif dlg_type == 'edit':
            btn_edit = QPushButton("Save")
            btn_edit.clicked.connect(self.edit_parm)
            btn_layout.addWidget(btn_edit)
        btn_layout.addStretch()


       
        feature = Feature()
        self.feature_cls = feature.get_feature_class(self.channel_qs.device_feature.feature_class)
        feature_fields = self.feature_cls.get_parameter_fields()
        if 'color' in feature_fields:
            layout.addLayout(color_layout)
        layout.addLayout(name_layout)
        if 'int_min' in feature_fields:
            layout.addLayout(min_layout)
        if 'int_max' in feature_fields:
            layout.addLayout(max_layout)
        if 'str_value' in feature_fields:
            layout.addLayout(value_layout)
        if 'allow_fading' in feature_fields:
            layout.addLayout(allow_fading_layout)
        if 'int_value' in feature_fields:
            layout.addLayout(value_layout)
        
        layout.addLayout(btn_layout) 

        msg_layout = QHBoxLayout()
        self.msg_label = QLabel('')
        msg_layout.addWidget(self.msg_label)
        msg_layout.addStretch()
        layout.addLayout(msg_layout)

        self.setLayout(layout)

        self.set_color()


    def set_color(self):
        if self.dlg_type == 'edit':
            if self.parm_qs.color:
                self.color_combo.setCurrentIndex(self.color_combo.findData(self.parm_qs.color.pk))
                self.chk_fading.setEnabled(False)
            else:
                self.chk_fading.setEnabled(True)

    def color_combo_changed(self):
        if self.color_combo.currentData() != 0:
            self.chk_fading.setChecked(False)
            self.chk_fading.setEnabled(False)
            self.txt_name.setText(self.color_combo.currentText())
        else:
            self.chk_fading.setEnabled(True)

    def add_parm(self):
        value_dict = {}
        value_dict['name'] = self.txt_name.text()
        value_dict['int_min'] = self.txt_min.text()
        value_dict['int_max'] = self.txt_max.text()
        value_dict['str_value'] = self.txt_value.text()
        value_dict['allow_fading'] = self.chk_fading.isChecked()
        value_dict['int_value'] = self.txt_value.text()
        value_dict['color'] = self.color_combo.currentData()
        result = self.feature_cls.add_parameter(self.channel_qs.pk, value_dict)
        if result['result']:
            self.msg_label.setText(result['message'])
            self.accept()
        else:
            self.msg_label.setText(result['message'])
            self.msg_label.setStyleSheet('color: red')



    def edit_parm(self):
        value_dict = {}
        value_dict['name'] = self.txt_name.text()
        value_dict['int_min'] = self.txt_min.text()
        value_dict['int_max'] = self.txt_max.text()
        value_dict['str_value'] = self.txt_value.text()
        value_dict['allow_fading'] = self.chk_fading.isChecked()
        value_dict['int_value'] = self.txt_value.text()
        value_dict['color'] = self.color_combo.currentData()
        result = self.feature_cls.edit_parameter(self.parm_qs.pk, value_dict)
        if result['result']:
            self.msg_label.setText(result['message'])
            self.accept()
        else:
            self.msg_label.setText(result['message'])
            self.msg_label.setStyleSheet('color: red')

