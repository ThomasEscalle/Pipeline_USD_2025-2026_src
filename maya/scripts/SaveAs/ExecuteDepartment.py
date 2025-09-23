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


from SaveAs.DlgAskVariation import DlgAskVariation
from SaveAs.DlgAskAnimSettings import DlgAskAnimSettings


# Base class for execute department
class ExecuteDepartment():
    def publish(self, pcore):
        raise NotImplementedError("Subclasses must implement publish method")
    def export(self, pcore):
        raise NotImplementedError("Subclasses must implement export method")

    # Get the state manager
    def getState(self, pcore):
        # Get the state manager
        sm = pcore.getStateManager()
        if not pcore.fileInPipeline():
            pcore.showFileNotInProjectWarning(title="Warning")
            return False

        for state in sm.states:
            if state.ui.className == "Export" and state.ui.e_name.text() == "Default Export ({product})":
                break
        else:
            parent = self.getDftStateParent(pcore=pcore)
            state = sm.createState("Export", stateData={"stateName": "Default Export ({product})"}, parent=parent)
            if not state:
                msg = "Failed to create export state. Please contact the support."
                pcore.popup(msg)
                return

            state.ui.initializeContextBasedSettings()
        return state
    
    def getDftStateParent(self, create=True, pcore = None):
        sm = pcore.getStateManager()
        if not sm:
            return

        for state in sm.states:
            if state.ui.listType != "Export" or state.ui.className != "Folder":
                continue

            if state.ui.e_name.text() != "Default States":
                continue

            return state

        if create:
            stateData = {
                "statename": "Default States",
                "listtype": "Export",
                "stateenabled": 2,
                "stateexpanded": False,
            }
            state = sm.createState("Folder", stateData=stateData)
            return state
        
    def __init__(self):
        pass




# Execute department for Modelisation Low
class ExecuteDepartment_ModL(ExecuteDepartment):
    def __init__(self):
        super(ExecuteDepartment_ModL, self).__init__()

    # Publish the file as usd
    def publish(self, pcore):
        """
        dialog = DlgAskAnimSettings()
        result = dialog.exec_()
        if result == QtWidgets.QDialog.Rejected:
            return
        return
        """
        # Get the state manager
        state = self.getState(pcore)

        if not state or state == None:
            msg = "Failed to create publish state. Please contact the support."
            pcore.popup(msg)
            return
        
        # Ask for variation
        dialog = DlgAskVariation()
        result = dialog.exec_()
        if result == QtWidgets.QDialog.Rejected:
            return
        variation = dialog.getSelectedVariation()

        # Get the current file path and split it
        filePath = pcore.getCurrentFileName()
        filePath = filePath.replace("\\", "/")
        splitedPath = filePath.split("/")

        # Prepare the name
        department = splitedPath[-3]
        taskName = splitedPath[-2]
        outputType = ".usd"

        if variation == dialog.getDefaultVariation():
            # The name is : "<department>_Publish"
            name = department + "_Publish"
        else:
            name = department + "_Publish_" + variation
        
        # Set the state UI elements
        state.ui.l_taskName.setText(name)
        state.ui.cb_outType.setCurrentText(outputType)
        state.ui.typeChanged(state.ui.getOutputType())
        
        # Run the export
        try:
            pcore.getPlugin("Maya").onShelfClickedExport()
        except:
            self.showPrismWarningMessage()

        
    # Export the file as usd
    def export(self, pcore):
        # Get the state manager
        state = self.getState(pcore)

        if not state:
            msg = "Failed to create publish state. Please contact the support."
            pcore.popup(msg)
            return

        # Ask for variation
        dialog = DlgAskVariation()
        result = dialog.exec_()
        if result == QtWidgets.QDialog.Rejected:
            return
        variation = dialog.getSelectedVariation()

        # Get the current file path and split it
        filePath = pcore.getCurrentFileName()
        filePath = filePath.replace("\\", "/")
        splitedPath = filePath.split("/")

        # Prepare the name
        department = splitedPath[-3]
        taskName = splitedPath[-2]
        outputType = ".usd"

        if variation == dialog.getDefaultVariation():
            name = department + "_Export_" + taskName
        else:
            name = department + "_Export_" + taskName + "_" + variation

        state.ui.l_taskName.setText(name)
        state.ui.cb_outType.setCurrentText(outputType)
        state.ui.typeChanged(state.ui.getOutputType())

        try:
            pcore.getPlugin("Maya").onShelfClickedExport()
        except:
            self.showPrismWarningMessage()



# Execute department for Modelisation High
class ExecuteDepartment_ModH(ExecuteDepartment):

    # Publish the file as usd
    def publish(self, pcore):
        # Get the state manager
        state = self.getState(pcore)

        if not state or state == None:
            msg = "Failed to create publish state. Please contact the support."
            pcore.popup(msg)
            return
        
        # Ask for variation
        dialog = DlgAskVariation()
        result = dialog.exec_()
        if result == QtWidgets.QDialog.Rejected:
            return
        variation = dialog.getSelectedVariation()

        # Get the current file path and split it
        filePath = pcore.getCurrentFileName()
        filePath = filePath.replace("\\", "/")
        splitedPath = filePath.split("/")

        # Prepare the name
        department = splitedPath[-3]
        taskName = splitedPath[-2]
        outputType = ".usd"

        if variation == dialog.getDefaultVariation():
            # The name is : "<department>_Publish"
            name = department + "_Publish"
        else:
            name = department + "_Publish_" + variation
        
        # Set the state UI elements
        state.ui.l_taskName.setText(name)
        state.ui.cb_outType.setCurrentText(outputType)
        state.ui.typeChanged(state.ui.getOutputType())
        
        # Run the export
        try:
            pcore.getPlugin("Maya").onShelfClickedExport()
        except:
            self.showPrismWarningMessage()

        
    # Export the file as usd
    def export(self, pcore):
        # Get the state manager
        state = self.getState(pcore)

        if not state:
            msg = "Failed to create publish state. Please contact the support."
            pcore.popup(msg)
            return

        # Ask for variation
        dialog = DlgAskVariation()
        result = dialog.exec_()
        if result == QtWidgets.QDialog.Rejected:
            return
        variation = dialog.getSelectedVariation()

        # Get the current file path and split it
        filePath = pcore.getCurrentFileName()
        filePath = filePath.replace("\\", "/")
        splitedPath = filePath.split("/")

        # Prepare the name
        department = splitedPath[-3]
        taskName = splitedPath[-2]
        outputType = ".usd"

        if variation == dialog.getDefaultVariation():
            name = department + "_Export_" + taskName
        else:
            name = department + "_Export_" + taskName + "_" + variation

        state.ui.l_taskName.setText(name)
        state.ui.cb_outType.setCurrentText(outputType)
        state.ui.typeChanged(state.ui.getOutputType())

        try:
            pcore.getPlugin("Maya").onShelfClickedExport()
        except:
            self.showPrismWarningMessage()



# Execute department for Rig Low
class ExecuteDepartment_RigL(ExecuteDepartment):

    # Publish the file as .ma
    def publish(self, pcore):
        # Get the state manager
        state = self.getState(pcore)

        if not state or state == None:
            msg = "Failed to create publish state. Please contact the support."
            pcore.popup(msg)
            return
        
        # Get the current file path and split it
        filePath = pcore.getCurrentFileName()
        filePath = filePath.replace("\\", "/")
        splitedPath = filePath.split("/")

        # Prepare the name
        department = splitedPath[-3]
        taskName = splitedPath[-2]
        outputType = ".ma"

        # The name is : "<department>_Publish"
        name = department + "_Publish"
        
        # Set the state UI elements
        state.ui.l_taskName.setText(name)
        state.ui.cb_outType.setCurrentText(outputType)
        state.ui.typeChanged(state.ui.getOutputType())
        
        # Run the export
        try:
            pcore.getPlugin("Maya").onShelfClickedExport()
        except:
            self.showPrismWarningMessage()

    def export(self, pcore):
        # Get the state manager
        state = self.getState(pcore)

        if not state:
            msg = "Failed to create publish state. Please contact the support."
            pcore.popup(msg)
            return

        # Get the current file path and split it
        filePath = pcore.getCurrentFileName()
        filePath = filePath.replace("\\", "/")
        splitedPath = filePath.split("/")

        # Prepare the name
        department = splitedPath[-3]
        taskName = splitedPath[-2]
        outputType = ".ma"

        name = department + "_Export_" + taskName

        state.ui.l_taskName.setText(name)
        state.ui.cb_outType.setCurrentText(outputType)
        state.ui.typeChanged(state.ui.getOutputType())

        try:
            pcore.getPlugin("Maya").onShelfClickedExport()
        except:
            self.showPrismWarningMessage()


# Execute department for Rig High
class ExecuteDepartment_RigH(ExecuteDepartment):
    def publish(self, pcore):
        # Get the state manager
        state = self.getState(pcore)

        if not state or state == None:
            msg = "Failed to create publish state. Please contact the support."
            pcore.popup(msg)
            return
        
        # Get the current file path and split it
        filePath = pcore.getCurrentFileName()
        filePath = filePath.replace("\\", "/")
        splitedPath = filePath.split("/")

        # Prepare the name
        department = splitedPath[-3]
        taskName = splitedPath[-2]
        outputType = ".ma"

        # The name is : "<department>_Publish"
        name = department + "_Publish"
        
        # Set the state UI elements
        state.ui.l_taskName.setText(name)
        state.ui.cb_outType.setCurrentText(outputType)
        state.ui.typeChanged(state.ui.getOutputType())
        
        # Run the export
        try:
            pcore.getPlugin("Maya").onShelfClickedExport()
        except:
            self.showPrismWarningMessage()

    def export(self, pcore):
        # Get the state manager
        state = self.getState(pcore)

        if not state:
            msg = "Failed to create publish state. Please contact the support."
            pcore.popup(msg)
            return

        # Get the current file path and split it
        filePath = pcore.getCurrentFileName()
        filePath = filePath.replace("\\", "/")
        splitedPath = filePath.split("/")

        # Prepare the name
        department = splitedPath[-3]
        taskName = splitedPath[-2]
        outputType = ".ma"

        name = department + "_Export_" + taskName

        state.ui.l_taskName.setText(name)
        state.ui.cb_outType.setCurrentText(outputType)
        state.ui.typeChanged(state.ui.getOutputType())

        try:
            pcore.getPlugin("Maya").onShelfClickedExport()
        except:
            self.showPrismWarningMessage()



# Execute department for RLO (rough layout)
class ExecuteDepartment_RLO(ExecuteDepartment):
    def publish(self, pcore):
        pass

    def export(self, pcore):
        pass

# Execute department for FLO (final layout)
class ExecuteDepartment_FLO(ExecuteDepartment):
    def publish(self, pcore):
        pass

    def export(self):
        pass

# Execute department for Animation
class ExecuteDepartment_Animation(ExecuteDepartment):
    def publish(self, pcore):
        pass

    def export(self, pcores):
        pass