from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import shutil
import PrismInit

from PySide6 import QtCore, QtGui, QtWidgets

import sys
import os

import maya.OpenMayaUI as omui

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.cmds as cmds
from maya.OpenMayaUI import MQtUtil


from SaveAs.DlgAskVariation import DlgAskVariation
from SaveAs.DlgAskAnimSettings import DlgAskAnimSettings
from SaveAs.DlgAskCharacterName import DlgAskCharacterName

def saveUSDOverrideEdits(product_name, file_name):
    """
    This function saves the current USD override edits for Maya USD stages to new versioned USD files.
    It checks if the override layer is dirty and saves it to a new file in the usd_overrides directory.
    This function could be added to Maya's kBeforeSave callback to automatically save the overrides when the scene is saved.

    import maya.OpenMaya as api
    api.MSceneMessage.addCallback(api.MSceneMessage.kBeforeSave, saveUSDOverrideEdits)
    """
    #import this at runtime because otherwise maya crashes on startup
    import mayaUsd.ufe as mayaUsdUfe 


    for n in cmds.ls(type="mayaUsdProxyShape"):
        stage = mayaUsdUfe.getStage(cmds.ls(n, long=True)[0])
        overrideLayer = stage.GetRootLayer()

        # if(overrideLayer.dirty ):

        pcore = PrismInit.pcore
        current_file_name = pcore.getCurrentFileName()
        current_entity = pcore.entities.getScenefileData(current_file_name , getEntityFromPath=True)         
        product = pcore.products.createProduct(current_entity , product_name,location="global" )  # <-- Make sure the product exists
        version = pcore.products.ingestProductVersion(files=[], entity=current_entity,product=product_name, location="global") # <-- Create a new version

        save_path_edit_setD = version["versionPath"]
        save_path_edit_setD = save_path_edit_setD.replace("\\", "/")

        versionInfo = pcore.getConfig(configPath=save_path_edit_setD + "/versioninfo.json") or {}
        versionInfo["extension"] = ".usda"
        pcore.setConfig(data=versionInfo, configPath=save_path_edit_setD + "/versioninfo.json")

        save_path_edit_setD = os.path.join(save_path_edit_setD, file_name)
        save_path_edit_setD = save_path_edit_setD.replace("\\", "/")

        override_path = save_path_edit_setD
        overrideLayer.Export(override_path)
        cmds.setAttr(n + ".filePath", override_path, type="string")
        print(n + " USD layer was dirty - saved new version of overrides")

        pcore.products.updateMasterVersion(save_path_edit_setD)

            
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
        anim_dlg = DlgAskAnimSettings()
        result = anim_dlg.exec_()

        if result == QtWidgets.QDialog.Rejected:
            return
        
        user_selection = anim_dlg.getResult()

        # Based on user selection, perform different export actions

        ################################
        #### CAMERAS PUBLISH ###########
        ################################
        if user_selection == "cameras":
            # Export the current camera as ".ma"
            print("Exporting cameras...")
            
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
            name = "RLO_Cam_Publish"
            
            # Set the state UI elements
            state.ui.l_taskName.setText(name)
            state.ui.cb_outType.setCurrentText(outputType)
            state.ui.typeChanged(state.ui.getOutputType())
            
            # Run the export
            try:
                pcore.getPlugin("Maya").onShelfClickedExport()
            except:
                self.showPrismWarningMessage()





        ################################
        #### CHARACTER PUBLISH #########
        ################################
        if user_selection == "characters":
            # Avec des options (mode combobox disponible)
            data = []  # Todo: fetch characters from scene
            dialog = DlgAskCharacterName(data)
            if dialog.exec() == QtWidgets.QDialog.Rejected:
                return
            
            user_choice = dialog.getResult()
            print("User choice:", user_choice)

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
            outputType = ".usd"

            # The name is : "<department>_Publish"
            name = "RLO_Char_" + user_choice + "_Publish"
            
            # Set the state UI elements
            state.ui.l_taskName.setText(name)
            state.ui.cb_outType.setCurrentText(outputType)
            state.ui.typeChanged(state.ui.getOutputType())
            
            # Run the export
            try:
                pcore.getPlugin("Maya").onShelfClickedExport()
            except:
                self.showPrismWarningMessage()

        ################################
        #### SET DRESS EDITS PUBLISH ###
        ################################
        if user_selection == "setDressEdits":
            saveUSDOverrideEdits(product_name="RLO_Edit_SetD_Publish", file_name = "RLO_Edit_SetD_Publish.usda")
        

        pass

    def export(self, pcore):
        
        # Show a message box to say that this function is not implemented yet
        QMessageBox.information(None, "Info", "Export function is not implemented yet.")
        return

# Execute department for FLO (final layout)
class ExecuteDepartment_FLO(ExecuteDepartment):
    def publish(self, pcore):
        anim_dlg = DlgAskAnimSettings()
        result = anim_dlg.exec_()

        if result == QtWidgets.QDialog.Rejected:
            return
        
        user_selection = anim_dlg.getResult()

        # Based on user selection, perform different export actions

        ################################
        #### CAMERAS PUBLISH ###########
        ################################
        if user_selection == "cameras":
            # Export the current camera as ".ma"
            print("Exporting cameras...")
            
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
            name = "FLO_Cam_Publish"
            
            # Set the state UI elements
            state.ui.l_taskName.setText(name)
            state.ui.cb_outType.setCurrentText(outputType)
            state.ui.typeChanged(state.ui.getOutputType())
            
            # Run the export
            try:
                pcore.getPlugin("Maya").onShelfClickedExport()
            except:
                self.showPrismWarningMessage()





        ################################
        #### CHARACTER PUBLISH #########
        ################################
        if user_selection == "characters":
            # Avec des options (mode combobox disponible)
            data = []  # Todo: fetch characters from scene
            dialog = DlgAskCharacterName(data)
            if dialog.exec() == QtWidgets.QDialog.Rejected:
                return
            
            user_choice = dialog.getResult()
            print("User choice:", user_choice)

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
            outputType = ".usd"

            # The name is : "<department>_Publish"
            name = "FLO_Char_" + user_choice + "_Publish"
            
            # Set the state UI elements
            state.ui.l_taskName.setText(name)
            state.ui.cb_outType.setCurrentText(outputType)
            state.ui.typeChanged(state.ui.getOutputType())
            
            # Run the export
            try:
                pcore.getPlugin("Maya").onShelfClickedExport()
            except:
                self.showPrismWarningMessage()

        ################################
        #### SET DRESS EDITS PUBLISH ###
        ################################
        if user_selection == "setDressEdits":
            saveUSDOverrideEdits(product_name="FLO_Edit_SetD_Publish", file_name = "FLO_Edit_SetD_Publish.usda")
        

        pass
        

    def export(self, pcore):
        # Show a message box to say that this function is not implemented yet
        QMessageBox.information(None, "Info", "Export function is not implemented yet.")
        return
            
        
        

# Execute department for Animation
class ExecuteDepartment_Animation(ExecuteDepartment):
    def publish(self, pcore):
        anim_dlg = DlgAskAnimSettings()
        result = anim_dlg.exec_()

        if result == QtWidgets.QDialog.Rejected:
            return
        
        user_selection = anim_dlg.getResult()

        # Based on user selection, perform different export actions

        ################################
        #### CAMERAS PUBLISH ###########
        ################################
        if user_selection == "cameras":
            # Export the current camera as ".ma"
            print("Exporting cameras...")
            
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
            outputType = ".usd"

            # The name is : "<department>_Publish"
            name = "Anim_Cam_Publish"
            
            # Set the state UI elements
            state.ui.l_taskName.setText(name)
            state.ui.cb_outType.setCurrentText(outputType)
            state.ui.typeChanged(state.ui.getOutputType())
            
            # Run the export
            try:
                pcore.getPlugin("Maya").onShelfClickedExport()
            except:
                self.showPrismWarningMessage()





        ################################
        #### CHARACTER PUBLISH #########
        ################################
        if user_selection == "characters":
            # Avec des options (mode combobox disponible)
            data = []  # Todo: fetch characters from scene
            dialog = DlgAskCharacterName(data)
            if dialog.exec() == QtWidgets.QDialog.Rejected:
                return
            
            user_choice = dialog.getResult()
            print("User choice:", user_choice)

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
            outputType = ".usd"

            # The name is : "<department>_Publish"
            name = "Anim_Char_" + user_choice + "_Publish"
            
            # Set the state UI elements
            state.ui.l_taskName.setText(name)
            state.ui.cb_outType.setCurrentText(outputType)
            state.ui.typeChanged(state.ui.getOutputType())
            
            # Run the export
            try:
                pcore.getPlugin("Maya").onShelfClickedExport()
            except:
                self.showPrismWarningMessage()

        ################################
        #### SET DRESS EDITS PUBLISH ###
        ################################
        if user_selection == "setDressEdits":
            saveUSDOverrideEdits(product_name="Anim_Edit_SetD_Publish", file_name = "Anim_Edit_SetD_Publish.usda")
        

        pass

    def export(self, pcore):
        # Show a message box to say that this function is not implemented yet
        QMessageBox.information(None, "Info", "Export function is not implemented yet.")
        return