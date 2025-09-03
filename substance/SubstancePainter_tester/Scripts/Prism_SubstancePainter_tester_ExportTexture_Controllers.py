from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from qtpy.QtCore import Qt

from Prism_SubstancePainter_tester_ExportTextureUI import TextureExportUI
import substance_painter.export
import substance_painter.resource

import json
import os
import logging
import platform
import shutil

logger = logging.getLogger(__name__)

class TextureExportController(TextureExportUI):
    def __init__(self, core, parent=None):
        super().__init__(parent)
        self.core = core

        self.edit_preset_btn.clicked.connect(self.on_edit_preset)
        self.preset_check.stateChanged.connect(self.on_preset_toggled)

        self.export_btn.clicked.connect(self.on_export_btn_clicked)

        #create the state
        self.sm = self.core.getStateManager()

        self.state = self.sm.createState("ExportTexture")
        self.currentState = getattr(self.state, "state", None)


    def on_edit_preset(self):
        print("current state : ", self.currentState)

        return self.state

    def on_preset_toggled(self, state):
        self.preset_combo.setEnabled(state == Qt.Checked)
    
    def on_export_btn_clicked(self):
        print("Export button clicked")
        #get the context
        contextPath = self.core.getCurrentFileName()[:-4] + "versioninfo.json"
        #context = self.core.getScenefileData(fileName=self.core.getCurrentFileName(path=False))
        with open(contextPath, 'r') as file:
            context = json.load(file)

        #get the task and comment
        task = "texturing"
        comment=""
        try :
            task = context["task"]
        except:
            print("There is no task in the current file data")
        try :
            comment = self.comment_edit.text()
        except:
            print("No comment commited")

        #get the extensions
        extensions = self.get_texture_tree_format_bit()

        #get the export path 
        version = self.core.products.getNextAvailableVersion(context, task)
        if not self.use_next_version.isChecked():
            if version == "v0001":
                pass
            else:
                intVersion = int(version[1:])
                intVersion += -1
                version = "v"+str(intVersion).zfill(4)
        exportPath = self.core.products.generateProductPath(
            task=task,
            entity=context,
            extension=".exr",
            comment=comment,
            version=version
        )
        exportPath = exportPath.replace("\\", "/")
        exportPath = exportPath.split("/")
        exportPath.pop(-1)
        exportPath = '/'.join(exportPath)

        # Save states to scene so PB finds them
        self.sm.saveStatesToScene()

        #export the texture

        #prepare the export config 
        exportConfig = self.build_export_config(export_path=exportPath)

        print("export config : ", exportConfig)

        if not os.path.exists(exportPath) :
            os.makedirs(exportPath)

        exportResultState = substance_painter.export.export_project_textures(exportConfig)
        exportResult = substance_painter.export.list_project_textures(exportConfig)

        print(exportResult)

        #customise the data to have match product's data
        productContext = context
        productContext["product"] = context["task"]
        productContext["version"] = version
        productContext["comment"] = comment
        productContext["Identifier"] = self.identifier_edit.text()
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
        self.updateMasterVersion(productContext, allTextures)  

    
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

    def build_export_config(self, export_path="C:/export"):

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
                res = res.split("x")
                res = list(map(int,res))

                srcMapType = "documentMap"

                # Each map has its own rootPath and parameters
                export_parameters.append(
                    {
                        "fileName" : f"{self.core.getCurrentFileName(path=False)[:-6]}_{material_name}_{map_name}(_$colorSpace)(.$udim)",
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
                outputMaps.append(f"{self.core.getCurrentFileName(path=False)[:-6]}_{material_name}_{map_name}(_$colorSpace)(.$udim)")

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

    def updateMasterVersion(self, data, paths):
        if not isinstance(paths, (list, tuple)):
            paths = [paths]  # ensure it's iterable

        results = []

        for path in paths:
            forcedLoc = os.getenv("PRISM_PRODUCT_MASTER_LOC")
            if forcedLoc:
                location = forcedLoc
            else:
                location = self.core.products.getLocationFromFilepath(path)

            origVersion = data.get("version")
            if not origVersion:
                msg = "Invalid product version. Make sure the version contains valid files."
                self.core.popup(msg)
                continue

            data["type"] = self.core.paths.getEntityTypeFromPath(path)
            masterPath = self.core.products.generateProductPath(
                entity=data,
                task=data.get("product"),
                extension=data.get("extension", ""),
                version="master",
                location=location,
            )
            if masterPath:
                logger.debug("updating master version: %s from %s" % (masterPath, path))
            else:
                logger.warning("failed to generate masterpath: %s %s" % (data, location))
                msg = "Failed to generate masterpath. Please contact the support."
                self.core.popup(msg)
                continue

            result = self.core.products.deleteMasterVersion(masterPath, "Failed to update master version...")
            if not result:
                continue

            os.makedirs(os.path.dirname(masterPath), exist_ok=True)

            masterDrive = os.path.splitdrive(masterPath)[0]
            drive = os.path.splitdrive(path)[0]

            seqFiles = self.core.detectFileSequence(path)
            if not seqFiles:
                continue

            useHL = os.getenv("PRISM_USE_HARDLINK_MASTER", None)
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
                if file in processedFiles:
                    continue

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

            results.append(masterPath)

        return results
