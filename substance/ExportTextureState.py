# ExportTextureState.py

name = "ExportTextureState"
classname = "ExportTextureState"


import os

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from PrismUtils.Decorators import err_catcher


class ExportTextureState:
    def __init__(self, core):
        self.core = core
        self.version = "v1.0.0"

        self.core.registerCallback("onStateManagerOpen", self.onStateManagerOpen, plugin=self)

    def onStateManagerOpen(self, origin):
        origin.loadState(ExportTextureClass)


class ExportTextureClass(QWidget):
    className = "ExportTexture"
    listType = "Export"

    def setup(self, state, core, stateManager, stateData=None):
        self.core = core
        self.state = state
        self.stateManager = stateManager
        self.canSetVersion = True
        self.setupUi()
        self.connectEvents()

        if stateData is not None:
            self.loadData(stateData)

    @err_catcher(name=__name__)
    def loadData(self, data):
        if "statename" in data:
            self.e_name.setText(data["statename"])
        if "option1" in data:
            self.chb_option1.setChecked(data["option1"])
        if "fileFormat" in data:
            idx = self.cb_format.find(data["fileFormat"])
            if idx != -1:
                self.cb_format.setCurrentIndex(idx)
        if "stateenabled" in data and self.listType == "Export":
            self.state.setCheckState(
                0,
                eval(
                    data["stateenabled"]
                    .replace("PySide.QtCore.", "")
                    .replace("PySide2.QtCore.", "")
                ),
            )

        self.core.callback("onStateSettingsLoaded", self, data)

    @err_catcher(name=__name__)
    def setupUi(self):
        self.lo_main = QVBoxLayout(self)
        self.w_name = QWidget()
        self.lo_name = QHBoxLayout(self.w_name)
        self.l_name = QLabel("Name:")
        self.e_name = QLineEdit()
        self.e_name.setText(self.state.text(0))
        self.l_name.setVisible(False)
        self.e_name.setVisible(False)
        self.lo_name.addWidget(self.l_name)
        self.lo_name.addWidget(self.e_name)

        self.gb_general = QGroupBox("General")
        self.lo_general = QVBoxLayout(self.gb_general)

        self.w_option1 = QWidget()
        self.lo_option1 = QHBoxLayout(self.w_option1)
        self.l_option1 = QLabel("Option1:")
        self.chb_option1 = QCheckBox()
        self.lo_option1.addWidget(self.l_option1)
        self.lo_option1.addStretch()
        self.lo_option1.addWidget(self.chb_option1)

        self.w_format = QWidget()
        self.lo_format = QHBoxLayout(self.w_format)
        self.l_format = QLabel("Format:")
        self.cb_format = QComboBox()
        self.cb_format.addItems([".f1", "f2"])
        self.lo_format.addWidget(self.l_format)
        self.lo_format.addStretch()
        self.lo_format.addWidget(self.cb_format)

        self.lo_general.addWidget(self.w_option1)
        self.lo_general.addWidget(self.w_format)

        self.lo_main.addWidget(self.w_name)
        self.lo_main.addWidget(self.gb_general)

    @err_catcher(name=__name__)
    def connectEvents(self):
        self.e_name.textChanged.connect(self.nameChanged)
        self.e_name.editingFinished.connect(self.stateManager.saveStatesToScene)
        self.chb_option1.toggled.connect(self.stateManager.saveStatesToScene)
        self.cb_format.currentIndexChanged.connect(self.stateManager.saveStatesToScene)

    @err_catcher(name=__name__)
    def nameChanged(self, text):
        self.state.setText(0, text)

    @err_catcher(name=__name__)
    def updateUi(self):
        return True

    @err_catcher(name=__name__)
    def preExecuteState(self):
        warnings = []

        if not self.chb_option1.isChecked():
            warnings.append(["Option1 not checked.", "", 2])

        return [self.state.text(0), warnings]

    @err_catcher(name=__name__)
    def executeState(self, parent, useVersion="next"):
        fileName = self.core.getCurrentFileName()
        context = self.core.getScenefileData(fileName)
        outputPath = self.core.products.generateProductPath(
            entity=context,
            task="myProduct",
            extension=self.cb_format.currentText(),
        )

        if not os.path.exists(os.path.dirname(outputPath)):
            os.makedirs(os.path.dirname(outputPath))

        with open(outputPath, "w") as f:
            f.write("custom export")

        self.core.popup("Custom export to: %s" % outputPath, severity="info")
        result = {"result": "success"}
        if result["result"] == "success":
            return [self.state.text(0) + " - success"]
        else:
            return [
                self.state.text(0)
                + " - error - %s" % result["error"]
            ]

    @err_catcher(name=__name__)
    def getStateProps(self):
        stateProps = {}
        stateProps.update(
            {
                "statename": self.e_name.text(),
                "option1": self.chb_option1.isChecked(),
                "cb_format": self.cb_format.currentText(),
                "stateenabled": str(self.state.checkState(0)),
            }
        )
        return stateProps