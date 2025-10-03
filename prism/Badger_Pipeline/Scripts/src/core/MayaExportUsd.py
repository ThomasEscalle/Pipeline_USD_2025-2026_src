# Class to allow usd export in maya
import os

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

class MayaExportUsd:
    
    def __init__(self, core):
        self.core = core
        self.state = None

    def onStateStartup(self, state):
        # this function is used to create the GUI widgets every time a state gets created
        self.state = state

        # only for export states
        if state.className == "Export":

            # create the "Setting1" widgets only in Maya
            if self.core.appPlugin.pluginName == "Maya":

                # get the layout of the state settings, which the new widgets will be added to
                state.cb_outType.addItems([".usd"] )
                state.cb_outType.currentIndexChanged.connect(self.onCbOutTypeValueChanged)


                # Add a combobox to know if we want Ascii or binary
                self.exportFormat = QComboBox()
                self.exportFormat.addItems(["ASCII", "Binary"])
                state.verticalLayout_2.addWidget(self.exportFormat)

                # Add a checkbox for the "exportNamespace" setting
                self.exportNamespace = QCheckBox("Export Namespaces")
                state.verticalLayout_2.addWidget(self.exportNamespace)

                # Add a checkbox for the "Export materials" setting
                self.exportMaterials = QCheckBox("Export Materials")
                state.verticalLayout_2.addWidget(self.exportMaterials)

                # Add a checkbox for the "Export UVs" setting
                self.exportUVs = QCheckBox("Export UVs")
                self.exportUVs.setChecked(True)  # Default to checked
                state.verticalLayout_2.addWidget(self.exportUVs)

                # Add a checkbox for "catmull_clark subdivision"
                self.exportCatmullClark = QCheckBox("Catmull-clark Subdivision")
                state.verticalLayout_2.addWidget(self.exportCatmullClark)

                # Add a line edit for the "Create Usd Parent Scope"
                self.createUsdParentScope = QLineEdit()
                state.verticalLayout_2.addWidget(self.createUsdParentScope)
                self.createUsdParentScope.setPlaceholderText("Enter USD Parent Scope")



                self.onCbOutTypeValueChanged()

    def onStateGetSettings(self, state, settings):
        # this function collects the currents settings from the GUI widgets in order to save the settings
        pass

    def onStateSettingsLoaded(self, state, settings):
        # this function loads the state settings from a dict to the GUI widgets
        pass

    def onCbOutTypeValueChanged(self):
        # If the new value is ".usda" or ".usdc", update the UI accordingly
        if self.state.cb_outType.currentText() == ".usd":
            self.exportFormat.setVisible(True)
            self.exportNamespace.setVisible(True)
            self.exportMaterials.setVisible(True)
            self.exportUVs.setVisible(True)
            self.exportCatmullClark.setVisible(True)
            self.createUsdParentScope.setVisible(True)
        else:
            self.exportFormat.setVisible(False)
            self.exportNamespace.setVisible(False)
            self.exportMaterials.setVisible(False)
            self.exportUVs.setVisible(False)
            self.exportCatmullClark.setVisible(False)
            self.createUsdParentScope.setVisible(False)

    def preExport(self, **kwargs):
        


        #kwargs = {
        #       "state": self,
        #       "scenefile": fileName,
        #       "startframe": startFrame,
        #       "endframe": endFrame,
        #       "outputpath": outputName,
        #   }
        # {
        #     "state": "<StateManager.ExportClass(0x1f529e76270, name="wg_Export") at 0x000001F51A43FD00>",
        #     "scenefile": "E:/3D/Projects/06_Ouyang/03_Production/01_Assets/Chars/TEST/Scenefiles/ModL/Modeling/TEST_Modeling_v0001.ma",
        #     "startframe": 1,
        #     "endframe": 1,
        #     "outputpath": "E:/3D/Projects/06_Ouyang/03_Production/01_Assets/Chars/TEST/Export/ModL_Publish/v0003/TEST_ModL_Publish_v0003.usda"
        # }


        # create the "Setting1" widgets only in Maya
        if self.core.appPlugin.pluginName == "Maya":

            # Import cmds
            import maya.cmds as cmds

            if self.state.cb_outType.currentText() != ".usd":
                return
            
            # this function will be executed before the export started
            print("Pre Export called")

            output_path = kwargs["outputpath"]
            output_path = output_path.replace("\\", "/")  # Ensure the path is in the correct format

            # Get the nodes and select them
            cmds.select(clear=True)
            nodes = kwargs["state"].nodes
            cmds.select(nodes, replace=True)

            # Get the "wholeScene" setting
            whole_scene = kwargs["state"].chb_wholeScene.isChecked()

            # Get the "exportFormat" setting
            export_format = self.exportFormat.currentText()
            export_format = "usda" if export_format == "ASCII" else "usdc"

            # Get the "exportNamespace" setting
            export_namespace = self.exportNamespace.isChecked()

            # Get the "exportMaterials" setting
            export_materials = self.exportMaterials.isChecked()

            # Get the "exportUVs" setting
            export_uvs = self.exportUVs.isChecked()

            # Get the "exportQuads" setting
            export_catmull_clark = self.exportCatmullClark.isChecked()

            # Get the "createUsdParentScope" setting
            create_usd_parent_scope = self.createUsdParentScope.text()






            self.exportAsUsd(
                outputName=output_path,
                startFrame=kwargs["startframe"],
                endFrame=kwargs["endframe"],
                nodes=nodes,
                wholeScene=whole_scene,
                namespaces=export_namespace,
                materials=export_materials,
                catmull_clark=export_catmull_clark,
                exportUVs=export_uvs,
                parentPrim=create_usd_parent_scope
            )


    def postExport(self, **kwargs):
        # create the "Setting1" widgets only in Maya
        if self.core.appPlugin.pluginName == "Maya":
            print("Post Export called")


    # file -force -options ";exportUVs=1;exportSkels=none;exportSkin=none;exportBlendShapes=0;exportDisplayColor=0;;exportColorSets=1;exportComponentTags=1;defaultMeshScheme=catmullClark;animation=1;eulerFilter=0;staticSingleSample=0;startTime=1;endTime=3;frameStride=1;frameSample=0.0;defaultUSDFormat=usda;parentScope=PRIM;shadingMode=useRegistry;convertMaterialsTo=[];exportRelativeTextures=automatic;exportInstances=1;exportVisibility=1;mergeTransformAndShape=1;stripNamespaces=0;worldspace=0" -type "USD Export" -es "C:/Users/Thomas/OneDrive/Bureau/abdqzd.usd";

    # file -force -options ";exportUVs=1;exportSkels=none;exportSkin=none;exportBlendShapes=0;exportDisplayColor=0;;exportColorSets=1;exportComponentTags=1;defaultMeshScheme=catmullClark;animation=1;eulerFilter=0;staticSingleSample=0;startTime=1;endTime=3;
    # frameStride=1;frameSample=0.0;defaultUSDFormat=usda;parentScope=PRIM;shadingMode=useRegistry;convertMaterialsTo=[];exportRelativeTextures=automatic;exportInstances=1;exportVisibility=1;mergeTransformAndShape=1;stripNamespaces=0;worldspace=0" -type "USD Export" -ea "C:/Users/Thomas/OneDrive/Bureau/qzdqzdqzdqzqzd.usd";
    # Difference : -ea (export all)


    def exportAsUsd(self, outputName, startFrame, endFrame, nodes=None, wholeScene=False, namespaces=False, materials=False, catmull_clark=False, parentPrim = "", exportUVs=True , exportFormat = "usda"):

        # Import mel
        import maya.mel as mel

        # Create the file's directory if it doesn't exist
        os.makedirs(os.path.dirname(outputName), exist_ok=True)

        command = "file -force -options \";"
        if exportUVs:
            command += "exportUVs=1;"
        else:
            command += "exportUVs=0;"
        command += "exportSkels=none;"
        command += "exportSkin=none;"
        command += "exportBlendShapes=0;"
        command += "exportDisplayColor=0;;"
        command += "exportColorSets=1;"
        command += "exportComponentTags=1;"
        if catmull_clark:
            command += "defaultMeshScheme=catmullClark;"
        else:
            command += "defaultMeshScheme=none;"
        command += "animation=1;"
        command += "eulerFilter=0;"
        command += "staticSingleSample=0;"
        command += f"startTime={startFrame};"
        command += f"endTime={endFrame};"
        command += "frameStride=1;"
        command += "frameSample=0.0;"
        command += f"defaultUSDFormat={exportFormat};"
        if parentPrim == "":
            command += "parentScope=;"
        else:
            command += f"parentScope={parentPrim};"
        command += "shadingMode=useRegistry;"
        command += "convertMaterialsTo=[];"
        command += "exportRelativeTextures=automatic;"
        command += "exportInstances=1;"
        command += "exportVisibility=1;"
        command += "mergeTransformAndShape=1;"
        if namespaces:
            command += "stripNamespaces=0;"
        else:
            command += "stripNamespaces=1;"
        command += "worldspace=0;"
        command += "\" -type \"USD Export\" "

        if wholeScene:
            command += f"-ea \"{outputName}\";"
        else:
            command += f"-es \"{outputName}\";"

        print(f"Executing MEL command: {command}")

        # Execute the mel command
        mel.eval(command)
