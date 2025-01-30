from PySide6.QtWidgets import (QWidget, QPushButton, QMessageBox, QVBoxLayout, QLabel, QHBoxLayout, QComboBox,
    QTableWidget, QTableWidgetItem, QLineEdit, QTabWidget, QDialog, QDialogButtonBox, QAbstractItemView,)

from PySide6.QtCore import QSize

from devices.models import Manufacture, LibraryDevice, DeviceFeature, LibraryChannel
from devices.constants import SystemType, Interfaces, FeatureList, ChannelType
from devices.features import Feature
from .utilities import get_icon_obj
from pprint import pprint

class DevLibWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Device Library")
       

        self.layout = QVBoxLayout(self)
      
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
            if dlg.exec():
                self.fill_manuf_table()
            else:    
                pass
           
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
            self.accept()
        else:
            self.msg_label.setText("Name cannot be empty")
            self.msg_label.setStyleSheet("color: red")
            # self.msg_label.adjustSize()
            # self.msg_label.show()
            

    def edit_manuf(self):
        name = self.txt_name.text()
        if name != "":
            self.manuf_qs.name = name
            self.manuf_qs.comments = self.txt_comm.text()
            self.manuf_qs.save()
            self.accept()
        else:
            self.msg_label.setText("Name cannot be empty")
            self.msg_label.setStyleSheet("color: red")
            # self.msg_label.adjustSize()
            # self.msg_label.show()

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
                print('Add Device', self.manuf_list.currentData(), self.system_list.currentData())
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
        layout.addLayout(channel_table_layout)
        layout.addStretch()


        self.setLayout(layout)

    
    
    def fill_feature_tables(self):
        libdev_qs = LibraryDevice.objects.get(pk=self.device_id)
        feature_qs = DeviceFeature.objects.filter(library_device=libdev_qs).order_by('sort_order')
        feature_count = feature_qs.count()
    
    
        #print('Fill Feature Table', self.feature_channel_list)
        self.feature_table.clear()
        self.feature_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.feature_table.setSelectionMode
        self.feature_table.setColumnCount(4)
        self.feature_table.setHorizontalHeaderLabels(['Name', 'Type', 'Order', 'ID'])
        self.feature_table.setRowCount(feature_count)
        self.feature_table.resize(100, 200)
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
        self.channel_table.setColumnCount(4)
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
            feature.add_feature(self.type_list.currentData(), self.txt_name.text(), self.devlib_id)
            self.accept()
        else:
            self.msg_label.setText("Name cannot be empty")
            self.msg_label.setStyleSheet("color: red")

    def edit_feature(self):
        if self.txt_name.text() != "":
            self.feature_qs.name = self.txt_name.text()
            self.feature_qs.save()
            self.accept()
        else:
            self.msg_label.setText("Name cannot be empty")
            self.msg_label.setStyleSheet("color: red")
        

       