# The QDockWidget class provides a widget that can be 
# docked inside a QMainWindow or floated 
# as a top-level window on the desktop

import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon, QTextCharFormat, QFont
from PySide6.QtWidgets import (QApplication, QMainWindow,
    QTextEdit, QLabel, QMessageBox, QVBoxLayout, QPushButton,
    QSpinBox, QDockWidget, QWidget)


class QEditor(QMainWindow):
    
    def __init__(self):

        super().__init__()

        self.text_edit = QTextEdit()        
        self.setCentralWidget(self.text_edit)

        self.label = QLabel()
        self.statusBar().addWidget(self.label)
        
        self.text_edit.textChanged.connect(self.on_text_changed)
        
        menu_bar = self.menuBar()
        
        file_menu = menu_bar.addMenu('&File')
        
        exit_action = QAction(self)
        exit_action.setText('&Exit')
        #exit_action.setIcon(QIcon('./icons/exit.png'))
        exit_action.triggered.connect(QApplication.quit)
        
        file_menu.addAction(exit_action)
          
        help_menu = menu_bar.addMenu('&Help')
        
        about_action = QAction(self)
        about_action.setText('&About')
        #about_action.setIcon(QIcon('./icons/about.png'))
        about_action.triggered.connect(self.show_messagebox)
        
        help_menu.addAction(about_action)
        
        file_toolbar = self.addToolBar('File')
        file_toolbar.addAction(exit_action)
        file_toolbar.addAction(about_action)
        file_toolbar.setToolButtonStyle(
            Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        
        # 1. Create the dock widget
            
        dock_widget = QDockWidget()
        dock_widget.setMaximumWidth(50)
        dock_widget.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
            
        vbox = QVBoxLayout()
        
        button_bold = QPushButton()
        #button_bold.setIcon(QIcon('./icons/bold.png'))
        button_bold.setCheckable(True)
        button_bold.toggled.connect(self.on_button_bold_toggled)
        
        button_italic = QPushButton()
        #button_italic.setIcon(QIcon('./icons/italic.png'))
        button_italic.setCheckable(True)
        button_italic.toggled.connect(self.on_button_italic_toggled)
        
        font_size_spinbox = QSpinBox()
        font_size_spinbox.setMinimum(1)
        font_size_spinbox.setMaximum(24)
        font_size_spinbox.valueChanged.connect(self.on_value_changed)
        
        vbox.addWidget(button_bold)
        vbox.addWidget(button_italic)
        vbox.addWidget(font_size_spinbox)
        vbox.addStretch()
        
        container = QWidget()
        container.setLayout(vbox)
        
        dock_widget.setWidget(container)
        
        # 2. Add the dock widget to the main window
        
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock_widget)
    
    def on_text_changed(self):

        cursor = self.text_edit.textCursor()
        
        size = len(self.text_edit.toPlainText())
        x = str(cursor.blockNumber() + 1)
        y = str(cursor.columnNumber() + 1)
        
        self.label.setText('Chars: {}, Ln: {}, Col: {}'.format(size, x, y))
        
    def show_messagebox(self):
        
        messagebox = QMessageBox()
        messagebox.setText('PyQt menu example')
        messagebox.exec()
    
    # 3. Handle the dock widget children signals
    
    def on_button_bold_toggled(self, checked):

        format = QTextCharFormat()
        
        if checked:
            format.setFontWeight(QFont.Weight.Bold)
        else:
            format.setFontWeight(QFont.Weight.Normal)
        
        cursor = self.text_edit.textCursor()
        self.text_edit.mergeCurrentCharFormat(format)
        self.text_edit.setFocus(Qt.FocusReason.OtherFocusReason)
        
    def on_button_italic_toggled(self, checked):
        
        format = QTextCharFormat()
        
        if checked:
            format.setFontItalic(True)
        else:
            format.setFontItalic(False)
            
        cursor = self.text_edit.textCursor()
        self.text_edit.mergeCurrentCharFormat(format)
        self.text_edit.setFocus(Qt.FocusReason.OtherFocusReason)
        
    def on_value_changed(self, i):
        
        format = QTextCharFormat()
        format.setFontPointSize(i)
        
        cursor = self.text_edit.textCursor()
        self.text_edit.mergeCurrentCharFormat(format)

class DemoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Show Demon")
        self.setFixedSize(QSize(1600, 1200))
        # Main Widget and Layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Function to add widget with label
        def add_widget_with_label(layout, widget, label_text):
            hbox = QHBoxLayout()
            label = QLabel(label_text)
            hbox.addWidget(label)
            hbox.addWidget(widget)
            layout.addLayout(hbox)

        # QLabel
        self.label = QLabel('Hello PySide6!')
        add_widget_with_label(main_layout, self.label, 'QLabel:')

        # QPushButton
        self.button = QPushButton('Click Me')
        self.button.clicked.connect(self.on_button_clicked)
        add_widget_with_label(main_layout, self.button, 'QPushButton:')

        # QLineEdit
        self.line_edit = QLineEdit()
        add_widget_with_label(main_layout, self.line_edit, 'QLineEdit:')

        # QComboBox
        self.combo_box = QComboBox()
        self.combo_box.addItems(['Option 1', 'Option 2', 'Option 3'])
        add_widget_with_label(main_layout, self.combo_box, 'QComboBox:')

        # QCheckBox
        self.check_box = QCheckBox('Check Me')
        add_widget_with_label(main_layout, self.check_box, 'QCheckBox:')

        # QRadioButton
        self.radio_button = QRadioButton('Radio Button')
        add_widget_with_label(main_layout, self.radio_button, 'QRadioButton:')

        # QTextEdit
        self.text_edit = QTextEdit()
        add_widget_with_label(main_layout, self.text_edit, 'QTextEdit:')

        # QSlider
        self.slider = QSlider()
        add_widget_with_label(main_layout, self.slider, 'QSlider:')

        # QSpinBox
        self.spin_box = QSpinBox()
        add_widget_with_label(main_layout, self.spin_box, 'QSpinBox:')

        # QProgressBar
        self.progress_bar = QProgressBar()
        add_widget_with_label(main_layout, self.progress_bar, 'QProgressBar:')

        # QTableWidget
        self.table_widget = QTableWidget(5, 3) 
        for i in range(5):
            for j in range(3):
                item = QTableWidgetItem(f"Cell {i+1},{j+1}")
                self.table_widget.setItem(i, j, item)
        add_widget_with_label(main_layout, self.table_widget, 'QTableWidget:')

    def on_button_clicked(self):
        self.label.setText('Button Clicked!')


def example1():

    app = QApplication(sys.argv)

    editor = QEditor()
    editor.show()

    sys.exit(app.exec())

#  def add_dock():
#             dock_widget = QDockWidget()
#             #dock_widget.setMinimumWidth(200)
#             dock_widget.setAllowedAreas(
#                 Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea | Qt.DockWidgetArea.TopDockWidgetArea | Qt.DockWidgetArea.BottomDockWidgetArea)
                
#             vbox = QVBoxLayout()
            
#             button_bold = QPushButton()
#             #button_bold.setIcon(QIcon('./icons/bold.png'))
#             button_bold.text = "Bold"
#             button_bold.setCheckable(True)
#             #button_bold.toggled.connect(self.on_button_bold_toggled)
            
#             button_italic = QPushButton()
#             #button_italic.setIcon(QIcon('./icons/italic.png'))
#             button_italic.setCheckable(True)
#             #button_italic.toggled.connect(self.on_button_italic_toggled)
            
#             font_size_spinbox = QSpinBox()
#             font_size_spinbox.setMinimum(1)
#             font_size_spinbox.setMaximum(24)
#             #font_size_spinbox.valueChanged.connect(self.on_value_changed)
            
#             vbox.addWidget(button_bold)
#             vbox.addWidget(button_italic)
#             vbox.addWidget(font_size_spinbox)
#             vbox.addStretch()
            
#             container = QWidget()
#             container.setLayout(vbox)
            
#             dock_widget.setWidget(container)
            
#             # 2. Add the dock widget to the main window
            
#             self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock_widget)

