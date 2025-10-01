
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from PySide6 import QtCore, QtGui, QtWidgets

import sys
import os

import maya.OpenMayaUI as omui

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.cmds as cmds
from maya.OpenMayaUI import MQtUtil



# A dialog to ask the user for the variation name
class DlgAskVariation(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enter Variation Name")
        self.setMinimumWidth(300)

        # Create a vertical layout
        layout = QtWidgets.QVBoxLayout(self)

        # Create a label
        label = QtWidgets.QLabel("Select a variation for your publish:")
        layout.addWidget(label)

        # Create a combo box
        self.combo_box = QtWidgets.QComboBox(self)
        self.combo_box.addItems(["default","var001", "var002", "var003", "var004", "var005", "var006", "var007", "var008", "var009", "var010",
                                 "var011", "var012", "var013", "var014", "var015", "var016", "var017", "var018", "var019", "var020"])
        layout.addWidget(self.combo_box)
        
        # Add a spacer
        spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        layout.addItem(spacer)
        
        # Create a button box
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        # Set the layout
        self.setLayout(layout)

    def getSelectedVariation(self):
        return self.combo_box.currentText()

    def getDefaultVariation(self):
        return "default"
