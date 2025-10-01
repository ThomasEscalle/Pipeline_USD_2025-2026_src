
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

from SaveAs.IconLoader import loadIcon


# A dialog to ask the user for the animation settings
class DlgAskAnimSettings(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("C quoi q'tu sors ?")
        self.setMinimumWidth(300)

        # Create a vertical layout
        layout = QtWidgets.QHBoxLayout(self)

        self.result = ""

        # Add a button to export the camera
        self.btn_export_cam = QtWidgets.QPushButton("Cameras", self)
        self.btn_export_cam.setIcon(loadIcon("camera.png"))
        self.btn_export_cam.setIconSize(QtCore.QSize(24, 24))
        self.btn_export_cam.clicked.connect(lambda: self.setResult("cameras"))
        layout.addWidget(self.btn_export_cam)

        # Add a button to export a character
        self.btn_export_char = QtWidgets.QPushButton("Anims", self)
        self.btn_export_char.setIcon(loadIcon("person.png"))
        self.btn_export_char.clicked.connect(lambda: self.setResult("characters"))
        self.btn_export_char.setIconSize(QtCore.QSize(24, 24))
        layout.addWidget(self.btn_export_char)

        # Add a button to export an edit of the setDress
        self.btn_export_setDress = QtWidgets.QPushButton("Set Dress Edit", self)
        self.btn_export_setDress.setIcon(loadIcon("edit.png"))
        self.btn_export_setDress.clicked.connect(lambda: self.setResult("setDressEdits"))
        self.btn_export_setDress.setIconSize(QtCore.QSize(24, 24))
        layout.addWidget(self.btn_export_setDress)

        # Set the layout
        self.setLayout(layout)

    def getResult(self):
        return self.result

    def setResult(self, result):
        self.result = result
        self.accept()

    def getDefaultVariation(self):
        return "default"
