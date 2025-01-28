from PySide6.QtWidgets import QWidget, QPushButton, QMessageBox, QVBoxLayout, QLabel, QHBoxLayout, QComboBox, QCheckBox, QRadioButton, QTextEdit
from PySide6.QtWidgets import   QTableWidget, QTableWidgetItem, QLineEdit, QTabWidget, QDialog, QDialogButtonBox, QAbstractItemView
from devices.models import Manufacture, Device, DeviceLibrary
from devices.constants import SystemType, Interfaces

class DevLibWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Show Demon - Device Library")
       

        self.layout = QVBoxLayout(self)
      
        self.tab_widget = QTabWidget()
        self.tab_manuf = QWidget()
        self.tab_device = QWidget()
        self.tab3 = QWidget()

        self.tab_widget.addTab(self.tab_device, "Devices")
        self.tab_widget.addTab(self.tab_manuf, "Manufacture")
        
        self.tab_widget.addTab(self.tab3, "Tab 3")

        self.layout.addWidget(self.tab_widget)

        self.init_tab_manuf()
        self.init_tab_device()
        self.initTab3()

    def init_tab_manuf(self):
        m_m_layout = QVBoxLayout(self.tab_manuf)
        m_h_layout = QHBoxLayout()
        m_layout = QVBoxLayout()
        
        m_btn_layout = QHBoxLayout()
        btn_add_manuf = QPushButton('Add')
        btn_add_manuf.clicked.connect(self.show_add_manuf_dlg)
        btn_edit_manuf = QPushButton('Edit')
        btn_edit_manuf.clicked.connect(self.show_edit_manuf_dlg)
        btn_del_manuf = QPushButton('Delete')
        btn_del_manuf.clicked.connect(self.show_del_manuf_dlg)
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
        btn_add_device.clicked.connect(self.show_add_device_dlg)
        btn_edit_device = QPushButton('Edit')
        btn_edit_device.clicked.connect(self.show_edit_device_dlg)
        btn_del_device = QPushButton('Delete')
        btn_del_device.clicked.connect(self.show_del_device_dlg)
        d_btn_layout.addWidget(btn_add_device)
        d_btn_layout.addWidget(btn_edit_device)
        d_btn_layout.addWidget(btn_del_device)
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

    def initTab3(self):
        layout = QVBoxLayout(self.tab3)
        label = QLabel("Content of Tab 3")
        layout.addWidget(label)

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
                manuf_id = int(self.manuf_table.item(self.manuf_table.currentRow(), 2).text())
                manuf_qs = Manufacture.objects.get(pk=manuf_id)
                manuf_qs.delete()
                self.fill_manuf_table()

    def fill_device_table(self):
        self.device_table.clear()
        self.device_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.device_table.setSelectionMode
        self.device_table.setColumnCount(4)
        self.device_table.setHorizontalHeaderLabels(['Name', 'Manufacture', 'System', 'Description'])
        self.device_table.setRowCount(DeviceLibrary.objects.count())
        sys_type = SystemType()
        for i, device in enumerate(DeviceLibrary.objects.all()):
            self.device_table.setItem(i, 0, QTableWidgetItem(device.name))
            self.device_table.setItem(i, 1, QTableWidgetItem(device.manufacture.name))
            self.device_table.setItem(i, 2, QTableWidgetItem(sys_type.get_display(device.system)))
            self.device_table.setItem(i, 3, QTableWidgetItem(device.description))

    def show_add_device_dlg(self):
        dlg_add_dev = DeviceAddDialog(self)
        dlg_add_dev.resize(400, 200)
        if dlg_add_dev.exec():
            self.fill_device_table()

    def show_edit_device_dlg(self):
        pass

    def show_del_device_dlg(self):
        pass

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

class DeviceAddDialog(QDialog):
    def __init__(self, parent=None, device_id=None):
        super().__init__(parent)
        self.setWindowTitle("Add Device")
                
        layout = QVBoxLayout()
        
        n_layout = QHBoxLayout()
        lbl_name = QLabel("Name")
        self.txt_name = QLineEdit()
        n_layout.addWidget(lbl_name)
        n_layout.addWidget(self.txt_name)
        n_layout.addStretch()

        m_layout = QHBoxLayout()
        lbl_manuf = QLabel("Manufacture")
        self.manuf_list = QComboBox()
        mauf_qs = Manufacture.objects.all()
        for manuf in mauf_qs:
            self.manuf_list.addItem(manuf.name, manuf.pk)
        m_layout.addWidget(lbl_manuf)
        m_layout.addWidget(self.manuf_list)
        m_layout.addStretch()

        s_layout = QHBoxLayout()
        lbl_system = QLabel("System")
        self.system_list = QComboBox()
        for system in SystemType():
            self.system_list.addItem(system[1], system[0])
        s_layout.addWidget(lbl_system)
        s_layout.addWidget(self.system_list)
        s_layout.addStretch()

        des_layout = QHBoxLayout()
        lbl_des = QLabel("Desription")
        self.txt_des = QLineEdit()
        des_layout.addWidget(lbl_des)
        des_layout.addWidget(self.txt_des)
        des_layout.addStretch()

        b_layout = QHBoxLayout()
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.reject)
        b_layout.addWidget(btn_cancel)
        btn_add = QPushButton("Add")
        btn_add.clicked.connect(self.add_device)
        b_layout.addWidget(btn_add)
        b_layout.addStretch()

        msg_layout = QHBoxLayout()
        self.msg_label = QLabel('')
        msg_layout.addWidget(self.msg_label)
        msg_layout.addStretch()

        layout.addLayout(n_layout)
        layout.addLayout(m_layout)
        layout.addLayout(s_layout)
        layout.addLayout(des_layout)
        layout.addSpacing(20)
        layout.addLayout(b_layout)
        layout.addLayout(msg_layout)
        
        layout.addStretch()
        self.setLayout(layout)

    def add_device(self):
            
            name = self.txt_name.text()
            if name != "":
                print('Add Device', self.manuf_list.currentData(), self.system_list.currentData())
                manuf_qs = Manufacture.objects.get(pk=int(self.manuf_list.currentData()))
                new_device = DeviceLibrary()
                new_device.name = name
                new_device.manufacture = manuf_qs
                new_device.system = self.system_list.currentData()
                new_device.description = self.txt_des.text()
                new_device.save()
                self.accept()
            else:
                self.msg_label.setText("Name cannot be empty")
                self.msg_label.setStyleSheet("color: red")


class DeviceEditDialog(QDialog):
    def __init__(self, parent=None, device_id=None):
        super().__init__(parent)
        
        
        self.setWindowTitle("Edit Device")
                
        layout = QVBoxLayout()
        
        n_layout = QHBoxLayout()
        lbl_name = QLabel("Name")
        self.txt_name = QLineEdit()
        n_layout.addWidget(lbl_name)
        n_layout.addWidget(self.txt_name)
        n_layout.addStretch()

        m_layout = QHBoxLayout()
        lbl_manuf = QLabel("Manufacture")
        self.manuf_list = QComboBox()
        mauf_qs = Manufacture.objects.all()
        for manuf in mauf_qs:
            self.manuf_list.addItem(manuf.name, manuf.pk)
        m_layout.addWidget(lbl_manuf)
        m_layout.addWidget(self.manuf_list)
        m_layout.addStretch()
