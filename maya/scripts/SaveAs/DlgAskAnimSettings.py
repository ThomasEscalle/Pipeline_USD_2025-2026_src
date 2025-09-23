
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from PySide2 import QtCore, QtGui, QtWidgets

import sys
import os

import maya.OpenMayaUI as omui
import shiboken2
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.cmds as cmds
from maya.OpenMayaUI import MQtUtil

from SaveAs.IconLoader import loadIcon


# A dialog to ask the user for the animation settings
class DlgAskAnimSettings(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enter Animation Settings")
        self.setMinimumWidth(300)

        # Create a vertical layout
        layout = QtWidgets.QHBoxLayout(self)

        # Add a button to export the camera
        self.btn_export_cam = QtWidgets.QPushButton("", self)
        self.btn_export_cam.setIcon(loadIcon("camera.png"))
        self.btn_export_cam.setIconSize(QtCore.QSize(38, 38))
        layout.addWidget(self.btn_export_cam)

        # Add a button to export a character
        self.btn_export_char = QtWidgets.QPushButton("", self)
        self.btn_export_char.setIcon(loadIcon("person.png"))
        self.btn_export_char.setIconSize(QtCore.QSize(38, 38))
        layout.addWidget(self.btn_export_char)

        # Add a button to export an edit of the setDress
        self.btn_export_setDress = QtWidgets.QPushButton("", self)
        self.btn_export_setDress.setIcon(loadIcon("edit.png"))
        self.btn_export_setDress.setIconSize(QtCore.QSize(38, 38))
        layout.addWidget(self.btn_export_setDress)

        # Set the layout
        self.setLayout(layout)

    def getSelectedVariation(self):
        return self.combo_box.currentText()

    def getDefaultVariation(self):
        return "default"
