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


# A dialog to ask the user for a character name
class DlgAskCharacterName(QtWidgets.QDialog):
    def __init__(self, character_options=None):
        super().__init__()
        
        self.charcter_options = character_options

        # Par défaut en mode auto, sauf si pas d'options disponibles
        self.mode = "auto"
        if not (self.charcter_options and len(self.charcter_options) > 0):
            self.mode = "manual"

        self.setupUi()


    def setupUi(self):
        self.setWindowTitle("c'est qui ?") 
        self.layout = QtWidgets.QVBoxLayout(self)

        self.cb_mode = QtWidgets.QCheckBox("Mode auto", self)
        self.cb_mode.setChecked(self.mode == "auto")
        self.cb_mode.stateChanged.connect(self.onModeChanged)
        
        # Désactiver la checkbox si pas d'options disponibles
        if not (self.charcter_options and len(self.charcter_options) > 0):
            self.cb_mode.setEnabled(False)
            self.cb_mode.setToolTip("Mode auto non disponible - aucune option de personnage fournie")
        
        self.layout.addWidget(self.cb_mode)

        self.combo_characters = QtWidgets.QComboBox(self)
        if(self.charcter_options and len(self.charcter_options) > 0):
            self.combo_characters.addItems(self.charcter_options)
        self.layout.addWidget(self.combo_characters)

        self.lineEdit_character_name = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.lineEdit_character_name)
        self.lineEdit_character_name.setPlaceholderText("Character Name")
        self.lineEdit_character_name.setText("")

        # Add OK and Cancel buttons
        self.button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

        # Set initial visibility based on mode
        self.onModeChanged(QtCore.Qt.CheckState.Checked.value if self.mode == "auto" else QtCore.Qt.CheckState.Unchecked.value)



    def onModeChanged(self, state):
        print("Mode changed to : ", state)
        if state == QtCore.Qt.CheckState.Checked.value or state == 2:
            self.mode = "auto"
            self.lineEdit_character_name.setVisible(False)
            self.combo_characters.setVisible(True)
        else:
            self.mode = "manual"
            self.lineEdit_character_name.setVisible(True)
            self.combo_characters.setVisible(False)

    def getResult(self):
        if self.mode == "auto":
            return self.combo_characters.currentText()
        else:
            return self.lineEdit_character_name.text()  


