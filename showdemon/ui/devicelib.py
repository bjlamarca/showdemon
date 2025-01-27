from PySide6.QtWidgets import QWidget, QPushButton, QBoxLayout, QVBoxLayout, QLabel, QHBoxLayout, QComboBox, QCheckBox, QRadioButton, QTextEdit
from PySide6.QtWidgets import   QTableWidget, QTableWidgetItem, QLineEdit, QTabWidget, QDialog, QDialogButtonBox
from devices.models import Manufacture

class DevLibWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Show Demon - Device Library")
       

        self.layout = QVBoxLayout(self)
      
        self.tab_widget = QTabWidget()
        self.tab_manuf = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.tab_widget.addTab(self.tab_manuf, "Manufacture")
        self.tab_widget.addTab(self.tab2, "Tab 2")
        self.tab_widget.addTab(self.tab3, "Tab 3")

        self.layout.addWidget(self.tab_widget)

        self.init_tab_manuf()
        self.initTab2()
        self.initTab3()

    def init_tab_manuf(self):
        layout = QVBoxLayout(self.tab_manuf)
        h_layout = QHBoxLayout()
        m_layout = QVBoxLayout()
        

        btn_add_manuf = QPushButton("Add Manufacture")
        btn_add_manuf.clicked.connect(self.show_add_manuf_dlg)
        
        m_layout.addWidget(btn_add_manuf)
        m_layout.addStretch()
        
        


        h_layout.addLayout(m_layout)
        h_layout.addStretch()
        
        layout.addLayout(h_layout)

    def initTab2(self):
        layout = QVBoxLayout(self.tab2)
        label = QLabel("Content of Tab 2")
        layout.addWidget(label)

    def initTab3(self):
        layout = QVBoxLayout(self.tab3)
        label = QLabel("Content of Tab 3")
        layout.addWidget(label)

    def add_manuf_dlg(self):
        dgl = QDialog(self)


    def show_add_manuf_dlg(self, type):
        dlg = ManufDialog(self, 'add')
        dlg.resize(400, 200)
        if dlg.exec():
            print("Accepted")
        else:    
            print("Rejected")

def add_manufacture():
    new_manuf = Manufacture()
    new_manuf.name = "New Manufacture"


class ManufDialog(QDialog):
    def __init__(self, parent=None, type=None):
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
        n_layout.addWidget(txt_name)
        n_layout.addStretch()

        c_layout = QHBoxLayout()
        lbl_comm = QLabel("Comments")
        self.txt_comm = QLineEdit()
        c_layout.addWidget(lbl_comm)
        c_layout.addWidget(txt_comm)

        b_layout = QHBoxLayout()
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.reject)
        b_layout.addWidget(btn_cancel)
        if type == 'add':
            btn_add = QPushButton("Add")
            btn_add.clicked.connect(self.add_manuf)
            b_layout.addWidget(btn_add)
        elif type == 'edit':
            btn_edit = QPushButton("Edit")
            btn_edit.clicked.connect(self.edit_manuf)
            b_layout.addWidget(btn_edit)
        b_layout.addStretch()
        

        
        layout.addLayout(n_layout)
        layout.addLayout(c_layout)
        layout.addLayout(b_layout)
        layout.addStretch()

             
       
        self.setLayout(layout)

    def add_manuf(self):
        name = self.txt_name.text()
        if name != "":
            new_manuf = Manufacture()
            new_manuf.name = self.txt_name.text()
            new_manuf.comments = name
            new_manuf.save()
            self.accept()
            

    def edit_manuf(self):
        pass