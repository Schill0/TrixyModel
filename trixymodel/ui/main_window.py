from PyQt6.QtWidgets import (
    QMainWindow, QMenuBar, QMenu, QFileDialog, QDialog,
    QVBoxLayout, QLabel, QPushButton, QLineEdit, QWidget,
    QFormLayout, QListWidget, QDockWidget, QMenu
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from ui.viewport_widget import ViewportWidget

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        layout = QVBoxLayout()

        form = QFormLayout()
        self.shortcut_inputs = {}

        shortcuts = {
            "Toggle Edit Mode": "Tab",
            "Add Cube": "Ctrl+1",
            "Add Sphere": "Ctrl+2",
            "Add Plane": "Ctrl+3"
        }

        for action, default in shortcuts.items():
            input_box = QLineEdit(default)
            self.shortcut_inputs[action] = input_box
            form.addRow(QLabel(action), input_box)

        layout.addLayout(form)
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.accept)
        layout.addWidget(save_button)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TrixyModel v0.1")
        self.setGeometry(100, 100, 1280, 720)

        self.viewport = ViewportWidget(self)
        self.setCentralWidget(self.viewport)

        self._create_menus()
        self._create_object_dock()

    def _create_menus(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        file_menu.addAction(QAction("Import .obj", self, triggered=self.import_obj))
        file_menu.addAction(QAction("Save .trixym", self, triggered=self.save_trixym))
        file_menu.addAction(QAction("Export .obj", self, triggered=self.export_obj))

        view_menu = menu_bar.addMenu("View Mode")
        for mode in ["Shaded", "Wireframe", "Vertices", "Edit Mode"]:
            action = QAction(mode, self)
            action.triggered.connect(lambda checked, m=mode: self.viewport.set_display_mode(m))
            view_menu.addAction(action)

        tools_menu = menu_bar.addMenu("Tools")
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings)
        tools_menu.addAction(settings_action)

        menu_bar.addMenu("Windows")

    def _create_object_dock(self):
        self.object_list = QListWidget()
        self.object_list.itemClicked.connect(self.object_selected)

        dock = QDockWidget("Scene Objects", self)
        dock.setWidget(self.object_list)
        dock.setFloating(False)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
        self.viewport.set_object_list_widget(self.object_list)

    def object_selected(self, item):
        obj_name = item.text()
        self.viewport.select_object_by_name(obj_name)

    def open_settings(self):
        dlg = SettingsDialog(self)
        if dlg.exec():
            print("Settings saved:")
            for action, input_box in dlg.shortcut_inputs.items():
                print(f"{action}: {input_box.text()}")

    def import_obj(self):
        file, _ = QFileDialog.getOpenFileName(self, "Import OBJ", "", "OBJ Files (*.obj)")
        if file:
            self.viewport.import_obj(file)

    def save_trixym(self):
        file, _ = QFileDialog.getSaveFileName(self, "Save Project", "", "Trixy Files (*.trixym)")
        if file:
            self.viewport.save_trixym(file)

    def export_obj(self):
        file, _ = QFileDialog.getSaveFileName(self, "Export OBJ", "", "OBJ Files (*.obj)")
        if file:
            self.viewport.export_obj(file)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        cube_action = menu.addAction("Add Cube")
        sphere_action = menu.addAction("Add Sphere")
        plane_action = menu.addAction("Add Plane")

        action = menu.exec(event.globalPos())

        if action == cube_action:
            self.viewport.add_primitive("cube")
        elif action == sphere_action:
            self.viewport.add_primitive("sphere")
        elif action == plane_action:
            self.viewport.add_primitive("plane")
