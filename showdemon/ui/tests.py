from django.test import TestCase

from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QLayout, QLayoutItem, QTextBrowser, QWidget, QWidgetItem, QTextEdit,
    QDialog, QDialogButtonBox, QGridLayout, QGroupBox, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox,
    QTextEdit, QVBoxLayout, QComboBox, QSlider, QProgressBar, QDial)





class TestDialog(QDialog):
    num_grid_rows = 3
    num_buttons = 4

    def __init__(self):
        super().__init__()

        #self.create_menu()
        self.create_horizontal_group_box()
        self.create_grid_group_box()
        self.create_form_group_box()

        big_editor = QTextEdit()
        big_editor.setPlainText("This widget takes up all the remaining space "
                                "in the top-level layout.")

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok
                                      | QDialogButtonBox.StandardButton.Cancel)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        main_layout = QVBoxLayout()
        #main_layout.setMenuBar(self._menu_bar)
        main_layout.addWidget(self._horizontal_group_box)
        main_layout.addWidget(self._grid_group_box)
        main_layout.addWidget(self._form_group_box)
        main_layout.addWidget(big_editor)
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)

        self.setWindowTitle("Basic Layouts")

    # def create_menu(self):
    #     self._menu_bar = QMenuBar()

    #     self._file_menu = QMenu("&File", self)
    #     self._exit_action = self._file_menu.addAction("E&xit")
    #     self._menu_bar.addMenu(self._file_menu)

    #     self._exit_action.triggered.connect(self.accept)

    def create_horizontal_group_box(self):
        self._horizontal_group_box = QGroupBox("Horizontal layout")
        layout = QHBoxLayout()

        for i in range(TestDialog.num_buttons):
            button = QPushButton(f"Button {i + 1}")
            layout.addWidget(button)

        self._horizontal_group_box.setLayout(layout)

    def create_grid_group_box(self):
        self._grid_group_box = QGroupBox("Grid layout")
        layout = QGridLayout()

        for i in range(TestDialog.num_grid_rows):
            label = QLabel(f"Line {i + 1}:")
            line_edit = QLineEdit()
            layout.addWidget(label, i + 1, 0)
            layout.addWidget(line_edit, i + 1, 1)

        self._small_editor = QTextEdit()
        self._small_editor.setPlainText("This widget takes up about two thirds of the grid layout.")

        layout.addWidget(self._small_editor, 0, 2, 4, 1)

        layout.setColumnStretch(1, 10)
        layout.setColumnStretch(2, 20)
        self._grid_group_box.setLayout(layout)

    def create_form_group_box(self):
        self._form_group_box = QGroupBox("Form layout")
        layout = QFormLayout()
        layout.addRow(QLabel("Line 1:"), QLineEdit())
        layout.addRow(QLabel("Line 2, long text:"), QComboBox())
        layout.addRow(QLabel("Line 3:"), QSpinBox())
        self._form_group_box.setLayout(layout)


class TestDynDialog(QDialog):
    def __init__(self):
        super().__init__()

        self._rotable_widgets = []

        self.create_rotable_group_box()
        self.create_options_group_box()
        self.create_button_box()

        main_layout = QGridLayout()
        main_layout.addWidget(self._rotable_group_box, 0, 0)
        main_layout.addWidget(self._options_group_box, 1, 0)
        main_layout.addWidget(self._button_box, 2, 0)
        main_layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)

        self._main_layout = main_layout
        self.setLayout(self._main_layout)

        self.setWindowTitle("Dynamic Layouts")

    def rotate_widgets(self):
        count = len(self._rotable_widgets)
        if count % 2 == 1:
            raise AssertionError("Number of widgets must be even")

        for widget in self._rotable_widgets:
            self._rotable_layout.removeWidget(widget)

        self._rotable_widgets.append(self._rotable_widgets.pop(0))

        for i in range(count // 2):
            self._rotable_layout.addWidget(self._rotable_widgets[count - i - 1], 0, i)
            self._rotable_layout.addWidget(self._rotable_widgets[i], 1, i)

    def buttons_orientation_changed(self, index):
        self._main_layout.setSizeConstraint(QLayout.SetNoConstraint)
        self.setMinimumSize(0, 0)

        orientation = Qt.Orientation(self._buttons_orientation_combo_box.itemData(index))

        if orientation == self._button_box.orientation():
            return

        self._main_layout.removeWidget(self._button_box)

        spacing = self._main_layout.spacing()

        old_size_hint = self._button_box.sizeHint() + QSize(spacing, spacing)
        self._button_box.setOrientation(orientation)
        new_size_hint = self._button_box.sizeHint() + QSize(spacing, spacing)

        if orientation == Qt.Orientation.Horizontal:
            self._main_layout.addWidget(self._button_box, 2, 0)
            self.resize(self.size() + QSize(-old_size_hint.width(), new_size_hint.height()))
        else:
            self._main_layout.addWidget(self._button_box, 0, 3, 2, 1)
            self.resize(self.size() + QSize(new_size_hint.width(), -old_size_hint.height()))

        self._main_layout.setSizeConstraint(QLayout.SetDefaultConstraint)

    def show_help(self):
        QMessageBox.information(self, "Dynamic Layouts Help",
                                "This example shows how to change layouts "
                                "dynamically.")

    def create_rotable_group_box(self):
        self._rotable_group_box = QGroupBox("Rotable Widgets")

        self._rotable_widgets.append(QSpinBox())
        self._rotable_widgets.append(QSlider())
        self._rotable_widgets.append(QDial())
        self._rotable_widgets.append(QProgressBar())
        count = len(self._rotable_widgets)
        for i in range(count):
            element = self._rotable_widgets[(i + 1) % count]
            self._rotable_widgets[i].valueChanged[int].connect(element.setValue)

        self._rotable_layout = QGridLayout()
        self._rotable_group_box.setLayout(self._rotable_layout)

        self.rotate_widgets()

    def create_options_group_box(self):
        self._options_group_box = QGroupBox("Options")

        buttons_orientation_label = QLabel("Orientation of buttons:")

        buttons_orientation_combo_box = QComboBox()
        buttons_orientation_combo_box.addItem("Horizontal", Qt.Orientation.Horizontal)
        buttons_orientation_combo_box.addItem("Vertical", Qt.Orientation.Vertical)
        buttons_orientation_combo_box.currentIndexChanged[int].connect(
            self.buttons_orientation_changed)

        self._buttons_orientation_combo_box = buttons_orientation_combo_box

        options_layout = QGridLayout()
        options_layout.addWidget(buttons_orientation_label, 0, 0)
        options_layout.addWidget(self._buttons_orientation_combo_box, 0, 1)
        options_layout.setColumnStretch(2, 1)
        self._options_group_box.setLayout(options_layout)

    def create_button_box(self):
        self._button_box = QDialogButtonBox()

        close_button = self._button_box.addButton(QDialogButtonBox.StandardButton.Close)
        help_button = self._button_box.addButton(QDialogButtonBox.StandardButton.Help)
        rotate_widgets_button = self._button_box.addButton(
            "Rotate &Widgets", QDialogButtonBox.ButtonRole.ActionRole)

        rotate_widgets_button.clicked.connect(self.rotate_widgets)
        close_button.clicked.connect(self.close)
        help_button.clicked.connect(self.show_help)

### Border Layout

from dataclasses import dataclass
from enum import IntEnum, auto

class Position(IntEnum):
    West = auto()
    North = auto()
    South = auto()
    East = auto()
    Center = auto()


class SizeType(IntEnum):
    MinimumSize = auto()
    SizeHint = auto()


@dataclass
class ItemWrapper:
    item: QLayoutItem
    position: Position


class BorderLayout(QLayout):
    def __init__(self, parent=None, spacing: int = -1):
        super().__init__(parent)

        self._list: list[ItemWrapper] = []

        self.setSpacing(spacing)

        if parent is not None:
            self.setParent(parent)

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item: QLayoutItem):
        self.add(item, Position.West)

    def addWidget(self, widget: QWidget, position: Position):
        self.add(QWidgetItem(widget), position)

    def expandingDirections(self) -> Qt.Orientations:
        return Qt.Orientation.Horizontal | Qt.Orientation.Vertical

    def hasHeightForWidth(self) -> bool:
        return False

    def count(self) -> int:
        return len(self._list)

    def itemAt(self, index: int) -> QLayoutItem:
        if index < len(self._list):
            wrapper: ItemWrapper = self._list[index]
            return wrapper.item
        return None

    def minimumSize(self) -> QSize:
        return self.calculate_size(SizeType.MinimumSize)

    def setGeometry(self, rect: QRect):
        center: ItemWrapper = None
        east_width = 0
        west_width = 0
        north_height = 0
        south_height = 0

        super().setGeometry(rect)

        for wrapper in self._list:
            item: QLayoutItem = wrapper.item
            position: Position = wrapper.position

            if position == Position.North:
                item.setGeometry(
                    QRect(
                        rect.x(), north_height, rect.width(), item.sizeHint().height()
                    )
                )

                north_height += item.geometry().height() + self.spacing()

            elif position == Position.South:
                item.setGeometry(
                    QRect(
                        item.geometry().x(),
                        item.geometry().y(),
                        rect.width(),
                        item.sizeHint().height(),
                    )
                )

                south_height += item.geometry().height() + self.spacing()

                item.setGeometry(
                    QRect(
                        rect.x(),
                        rect.y() + rect.height() - south_height + self.spacing(),
                        item.geometry().width(),
                        item.geometry().height(),
                    )
                )
            elif position == Position.Center:
                center = wrapper

        center_height = rect.height() - north_height - south_height

        for wrapper in self._list:
            item: QLayoutItem = wrapper.item
            position: Position = wrapper.position

            if position == Position.West:
                item.setGeometry(
                    QRect(
                        rect.x() + west_width,
                        north_height,
                        item.sizeHint().width(),
                        center_height,
                    )
                )

                west_width += item.geometry().width() + self.spacing()

            elif position == Position.East:
                item.setGeometry(
                    QRect(
                        item.geometry().x(),
                        item.geometry().y(),
                        item.sizeHint().width(),
                        center_height,
                    )
                )

                east_width += item.geometry().width() + self.spacing()

                item.setGeometry(
                    QRect(
                        rect.x() + rect.width() - east_width + self.spacing(),
                        north_height,
                        item.geometry().width(),
                        item.geometry().height(),
                    )
                )

        if center:
            center.item.setGeometry(
                QRect(
                    west_width,
                    north_height,
                    rect.width() - east_width - west_width,
                    center_height,
                )
            )

    def sizeHint(self) -> QSize:
        return self.calculate_size(SizeType.SizeHint)

    def takeAt(self, index: int):
        if 0 <= index < len(self._list):
            layout_struct: ItemWrapper = self._list.pop(index)
            return layout_struct.item
        return None

    def add(self, item: QLayoutItem, position: Position):
        self._list.append(ItemWrapper(item, position))

    def calculate_size(self, size_type: SizeType):
        total_size = QSize()

        for wrapper in self._list:
            position = wrapper.position

            item_size: QSize
            if size_type == SizeType.MinimumSize:
                item_size = wrapper.item.minimumSize()
            else:
                item_size = wrapper.item.sizeHint()

            if position in (Position.North, Position.South, Position.Center):
                total_size.setHeight(total_size.height() + item_size.height())

            if position in (Position.West, Position.East, Position.Center):
                total_size.setWidth(total_size.width() + item_size.width())

        return total_size


class BorderWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.central_widget = QTextBrowser()
        self.central_widget.setPlainText("Central widget")

        border_layout = BorderLayout()
        border_layout.addWidget(self.central_widget, Position.Center)

        label_north = self.create_label("North")
        border_layout.addWidget(label_north, Position.North)

        label_west = self.create_label("West")
        border_layout.addWidget(label_west, Position.West)

        label_east1 = self.create_label("East 1")
        border_layout.addWidget(label_east1, Position.East)

        label_east2 = self.create_label("East 2")
        border_layout.addWidget(label_east2, Position.East)

        label_south = self.create_label("South")
        border_layout.addWidget(label_south, Position.South)

        self.setLayout(border_layout)

        self.setWindowTitle("Border Layout")

    @staticmethod
    def create_label(text: str):
        label = QLabel(text)
        label.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        return label