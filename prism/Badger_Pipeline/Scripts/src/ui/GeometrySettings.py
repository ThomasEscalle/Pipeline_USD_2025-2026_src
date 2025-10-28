from qtpy.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QHBoxLayout, QPushButton, QMessageBox, QCheckBox


import logging
import sys

class GeometrySettingsDialog(QDialog):
    def __init__(self, parent=None):
        super(GeometrySettingsDialog, self).__init__(parent)

        self.setWindowTitle("Geometry Settings")
        self.resize(600, 400)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Quatmull Clark
        self.cb_quatmullclark = QCheckBox("Catmull-Clark Subdivision")
        layout.addWidget(self.cb_quatmullclark)

        # Watertight
        self.cb_watertight = QCheckBox("Watertight Geometry")
        layout.addWidget(self.cb_watertight)

        # Activation du displace



        # spacer
        layout.addStretch()

        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.save_button.clicked.connect(self.save_settings)
        self.cancel_button.clicked.connect(self.reject)


    def save_settings(self):
        pass

        