from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from PySide6.QtCore import Qt

from Prism_SubstancePainter_ExportTextureUI import TextureExportUI
import substance_painter.export
import substance_painter.resource
import substance_painter.ui

import json
import os
import logging
import platform
import shutil

logger = logging.getLogger(__name__)

class TextureExportController(TextureExportUI):
    def __init__(self, core, parent):
        super().__init__(parent, core)
        self.core = core
        self.edit_preset_btn.clicked.connect(self.on_edit_preset)
        self.preset_combo.currentIndexChanged.connect(self.on_preset_combo_toggled)
        # Use the toggled(bool) signal so the handler always receives a boolean
        # (stateChanged(int) emits an int which previously caused a mismatch
        # when the UI also connected to toggled and passed a bool).
        self.preset_check.toggled.connect(self.on_preset_toggled)

        self.export_btn.clicked.connect(self.on_export_btn_clicked)
        self.use_next_version.stateChanged.connect(self.createVersion)
        self.identifier_edit.currentIndexChanged.connect(self.createVersion)

        # Ensure parent/child checkboxes stay in sync
        self.texture_tree.itemChanged.connect(self.on_texture_tree_item_changed)

    def on_texture_tree_item_changed(self, item, column):
        # If parent is checked/unchecked, set all children to same state
        if item.childCount() > 0:
            state = item.checkState(0)
            for i in range(item.childCount()):
                child = item.child(i)
                # Only update if different to avoid recursion
                if child.checkState(0) != state:
                    child.setCheckState(0, state)

    def on_edit_preset(self):
        pass

    def on_preset_toggled(self, state: bool):
        checked = bool(state)
        self.preset_combo.setEnabled(checked)
        # Keep the edit button in sync as well
        try:
            self.edit_preset_btn.setEnabled(checked)
        except Exception:
            pass
    
    def on_preset_combo_toggled(self):
        preset_name = self.preset_combo.currentText()
        resource_presets = substance_painter.export.list_resource_export_presets()
        predefined_presets = substance_painter.export.list_predefined_export_presets()
        selected_preset = None
        for preset in resource_presets:
            if preset.resource_id.name == preset_name:
                selected_preset = preset
                break
        for preset in predefined_presets:
            if preset.name == preset_name:
                selected_preset = preset
                break
        if selected_preset:
            self.texture_tree.clear()
            self.populate_texture_tree(selected_preset)
    
    def on_export_btn_clicked(self):
        #self.state = self.sm.createState("Export", setActive=True)
        #self.core.appPlugin.currentState = getattr(self.state, "state", None)

        #get the context
        contextPath = self.core.getCurrentFileName()[:-4] + "versioninfo.json"
        #context = self.core.getScenefileData(fileName=self.core.getCurrentFileName(path=False))
        if os.path.exists(contextPath):
            with open(contextPath, 'r') as file:
                context = json.load(file)

        #get the task and comment
        product = self.identifier_edit.currentText()

        comment=""
        try :
            comment = self.comment_edit.text()
        except:
            print("No comment commited")

        #get the extensions
        extensions = self.get_texture_tree_format_bit()

        #get the export path 
        version = self.core.products.getNextAvailableVersion(context, product)
        if not self.use_next_version.isChecked():
            version = self.version_comboBox.currentText()

        exportPathFile = self.core.products.generateProductPath(
            task=product,
            entity=context,
            extension=".exr",
            comment=comment,
            version=version
        )
        exportPath = exportPathFile.replace("\\", "/")
        exportPath = exportPath.split("/")
        exportPath.pop(-1)
        exportPath = '/'.join(exportPath)

        # save the texture in a temp folder before moving them to the exportPath because substance doesn't like network
        tempPath = os.path.dirname(os.path.abspath(__file__)) + os.sep + "tempTextureExport"

        #export the texture

        #prepare the export config 
        exportConfig = self.build_export_config(export_path=tempPath, product=product, asset=context["asset"])

        if not os.path.exists(exportPath) :
            os.makedirs(exportPath)

        exportResultState = substance_painter.export.export_project_textures(exportConfig)
        exportResult = substance_painter.export.list_project_textures(exportConfig)

        #move the texture to the final location
        for file in os.listdir(tempPath):
            shutil.move(os.path.join(tempPath, file), os.path.join(exportPath, file))

        #customise the data to have match product's data
        productContext = context
        productContext["product"] = product
        productContext["version"] = version
        productContext["type"] = "asset"
        productContext["comment"] = comment
        productContext["product"] = self.identifier_edit.currentText()
        productContext["sourceScene"] = self.core.getCurrentFileName()

        
        #save the json file
        self.core.saveVersionInfo(exportPath, productContext)
        material_names = []
        for i in range(self.texture_tree.topLevelItemCount()):
            material_item = self.texture_tree.topLevelItem(i)
            material_name = material_item.text(0)
            material_names.append(material_name)
        allTextures = []
        for name in material_names :
            allTextures += exportResult[(name,"")]

        #before updating the master version, relocate the current master to its original folder
        masterDataPath = exportPath.replace("\\", "/")
        masterDataPath = masterDataPath.split("/")
        masterDataPath.pop(-1)
        productPath = '/'.join(masterDataPath)

        masterDataPath.append("master")
        masterPath = '/'.join(masterDataPath)

        masterDataPath.append("versioninfo.json")
        masterDataPath = '/'.join(masterDataPath)
        if os.path.exists(masterDataPath):
            with open(masterDataPath, 'r') as file:
                masterData = json.load(file)
            originalMasterDataVersion = masterData["version"]
            #move the files
            for file in os.listdir(masterPath):
                shutil.move(os.path.join(masterPath, file), os.path.join(productPath, originalMasterDataVersion, file))
        
        #Update the master version
        self.updateMasterVersion(path=exportPathFile, data=productContext)

        #remove file of the version folder that is currently in master to avoid double files
        if os.path.exists(masterDataPath):
            with open(masterDataPath, 'r') as file:
                masterData = json.load(file)
            newMasterVersion = masterData["version"]
            versionPath = productPath + os.sep + newMasterVersion
            masterFiles = os.listdir(masterPath)
            for file in os.listdir(versionPath):
                if file in masterFiles and file != "versioninfo.json":
                    os.remove(os.path.join(versionPath, file))

        self.accept()

    
    def get_texture_tree_format_bit(self):
        export_info = {}

        for i in range(self.texture_tree.topLevelItemCount()):
            material_item = self.texture_tree.topLevelItem(i)
            material_name = material_item.text(0)
            maps_data = {}

            for j in range(material_item.childCount()):
                map_item = material_item.child(j)
                map_name = map_item.text(0)

                format_combo = self.texture_tree.itemWidget(map_item, 1)
                bit_combo = self.texture_tree.itemWidget(map_item, 2)

                maps_data[map_name] = {
                    "fileFormat": format_combo.currentText() if format_combo else "png",
                    "bitDepth": bit_combo.currentText().split(" ")[0] if bit_combo else "8",
                    "dithering": "dithering" in (bit_combo.currentText().lower() if bit_combo else ""),
                }

            export_info[material_name] = maps_data

        return export_info

    def build_export_config(self, export_path, product, asset):

        export_lists = []
        export_parameters = []

        for i in range(self.texture_tree.topLevelItemCount()):
            material_item = self.texture_tree.topLevelItem(i)
            material_name = material_item.text(0)
            export_list = {}
            export_list["rootPath"] = f"{material_name}"
            export_list["exportPreset"] = "preset1"
            outputMaps = []

            for j in range(material_item.childCount()):
                map_item = material_item.child(j)

                # ✅ Skip if the checkbox is not checked
                if map_item.checkState(0) != Qt.Checked:
                    continue

                map_name = map_item.text(0)

                format_combo = self.texture_tree.itemWidget(map_item, 1)
                bit_combo = self.texture_tree.itemWidget(map_item, 2)

                file_format = format_combo.currentText() if format_combo else "png"
                bit_depth = bit_combo.currentText().split(" ")[0] if bit_combo else "8"
                dithering = "dithering" in (bit_combo.currentText().lower() if bit_combo else "")
                res = self.res_combo.currentText()
                res = res.replace("128", "7")
                res = res.replace("256", "8")
                res = res.replace("512", "9")
                res = res.replace("1024", "10")
                res = res.replace("2048", "11")
                res = res.replace("4096", "12")
                res = res.replace("8192", "13")
                res = res.split("x")
                res = list(map(int,res))

                srcMapType = "documentMap"

                # Each map has its own rootPath and parameters
                export_parameters.append(
                    {
                        "fileName" : f"{asset}_{product}_{material_name}_{map_name}(_$colorSpace)(.$udim)",
                        "channels": [
                            {
                            "destChannel": "R",
                            "srcChannel": "R",
                            "srcMapType": srcMapType,
                            "srcMapName": map_name
                        },
                        {
                            "destChannel": "G",
                            "srcChannel": "G",
                            "srcMapType": srcMapType,
                            "srcMapName": map_name
                        },
                        {
                            "destChannel": "B",
                            "srcChannel": "B",
                            "srcMapType": srcMapType,
                            "srcMapName": map_name
                        }
                        ],
                        "parameters": {
                            "fileFormat": file_format,
                            "bitDepth": bit_depth,
                            "dithering": dithering,
                            "sizeLog2" : res,
                            "paddingAlgorithm" : "infinite" 
                        }
                    }
                )
                outputMaps.append(f"{asset}_{product}_{material_name}_{map_name}(_$colorSpace)(.$udim)")

            export_list["filter"] = {"outputMaps": outputMaps}
            export_lists.append(export_list)

        export_config = {
            "exportShaderParams": False,
            "exportPath": export_path,
            "defaultExportPreset": "preset1",
            "exportPresets":[{
                "name": "preset1",
                "maps": export_parameters
                
            }],
            "exportList":export_lists,
        }

        return export_config

    def updateMasterVersion(self, data, path):
        #delete current files in master version except versioninfo.json if next version is unchecked
        if not self.use_next_version.isChecked():
            folderPath = self.core.products.getVersionInfoPathFromProductFilepath(path)
            infoPath = self.core.getVersioninfoPath(folderPath)
            infoData = self.core.getConfig(configPath=infoPath)
            if infoData:
                origVersion = infoData.get("version")
                masterFolderPath = os.path.dirname(path).replace(origVersion, "master")
                if os.path.exists(masterFolderPath):
                    shutil.rmtree(masterFolderPath)
                    print("Removed existing master version files...")

        ext = path[-4:]
        forcedLoc = os.getenv("PRISM_PRODUCT_MASTER_LOC")
        if forcedLoc:
            location = forcedLoc
        else:
            location = self.core.products.getLocationFromFilepath(path)
        origVersion = data.get("version")

        #data["type"] = self.core.paths.getEntityTypeFromPath(path)
        masterPath = self.core.products.generateProductPath(
            entity=data,
            task=data.get("product"),
            extension=ext,
            version="master",
            location=location,
        )

        if masterPath:
            print("updating master version: %s from %s" % (masterPath, path))
        else:
            print("failed to generate masterpath: %s %s" % (data, location))
            msg = "Failed to generate masterpath. Please contact the support."
            self.core.popup(msg)
            return None
        result = self.core.products.deleteMasterVersion(masterPath, "Failed to update master version...")

        if not os.path.exists(masterPath):
            os.makedirs(os.path.dirname(masterPath), exist_ok=True)
        masterDrive = os.path.splitdrive(masterPath)[0]
        drive = os.path.splitdrive(path)[0]
        seqFiles = self.core.detectFileSequence(path)

        useHL = os.getenv("PRISM_USE_HARDLINK_MASTER", None)

        masterPathPadded = masterPath

        for seqFile in seqFiles:
            if len(seqFiles) > 1:
                extData = self.core.paths.splitext(seqFile)
                base = extData[0]
                frameStr = "." + base[-self.core.framePadding:]
                base, ext = self.core.paths.splitext(masterPath)
                masterPathPadded = base + frameStr + ext
            else:
                masterPathPadded = masterPath
            if (
                platform.system() == "Windows"
                and drive == masterDrive
                and useHL
                and not masterDrive.startswith("\\")
            ):
                self.core.createSymlink(masterPathPadded, seqFile)
            else:
                shutil.copy2(seqFile, masterPathPadded)

        folderPath = self.core.products.getVersionInfoPathFromProductFilepath(path)
        infoPath = self.core.getVersioninfoPath(folderPath)
        folderPath = self.core.products.getVersionInfoPathFromProductFilepath(masterPath)
        masterInfoPath = self.core.getVersioninfoPath(folderPath)

        if (
            platform.system() == "Windows"
            and drive == masterDrive
            and useHL
            and not masterDrive.startswith("\\")
        ):
            self.core.createSymlink(masterInfoPath, infoPath)
        else:
            if os.path.exists(infoPath):
                shutil.copy2(infoPath, masterInfoPath)
        infoData = self.core.getConfig(configPath=infoPath)

        if infoData and "preferredFile" in infoData:
            if infoData["preferredFile"] == os.path.basename(path):
                newPreferredFile = os.path.basename(masterPathPadded)
                if newPreferredFile != infoData["preferredFile"]:
                    self.core.setConfig("preferredFile", val=newPreferredFile, configPath=masterInfoPath)
        processedFiles = [os.path.basename(infoPath)] + [os.path.basename(b) for b in seqFiles]
        files = os.listdir(os.path.dirname(path))

        for file in files:
            filepath = os.path.join(os.path.dirname(path), file)
            fileTargetName = os.path.basename(filepath)
            if data["product"] == "_ShotCam" and not os.path.isdir(filepath) and origVersion in fileTargetName:
                fileTargetName = fileTargetName.replace(origVersion, "master")
            fileTargetPath = os.path.join(os.path.dirname(masterPathPadded), fileTargetName)
            os.makedirs(os.path.dirname(fileTargetPath), exist_ok=True)
            fileTargetPath = fileTargetPath.replace("\\", "/")
            if os.path.isdir(filepath):
                self.core.copyfolder(filepath, fileTargetPath)
            else:
                self.core.copyfile(filepath, fileTargetPath)

        self.core.configs.clearCache(path=masterInfoPath)
        self.core.callback(name="masterVersionUpdated", args=[masterPath])

        return masterPath


    def cleanup(self):
        # disconnect UI signals
        try:
            self.edit_preset_btn.clicked.disconnect()
        except Exception:
            pass
        try:
            self.preset_check.stateChanged.disconnect()
        except Exception:
            pass
        try:
            self.export_btn.clicked.disconnect()
        except Exception:
            pass

        # Clear attributes that may hold references to host resources
        self.core = None

        # Break references to child widgets (if any)
        try:
            self.texture_tree = None
            self.comment_edit = None
            self.identifier_edit = None
            self.res_combo = None
            self.use_next_version = None
        except Exception:
            pass
