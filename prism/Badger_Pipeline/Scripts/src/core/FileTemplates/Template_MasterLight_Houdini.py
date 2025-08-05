# Mod/Houdini

from src.core.FileTemplateBase import FileTemplateBase
from src.core.StandaloneScriptHoudini import StandaloneScriptHoudini
import os

try:
    from PySide6.QtWidgets import QMessageBox
except:
    from PySide2.QtWidgets import QMessageBox

class FileTemplateMasterLightHoudini(FileTemplateBase):

    def __init__(self):
        super().__init__()
        self.template_name = "MasterLightHoudini"
        self.template_software = "Houdini"

    def construct(self, parent, path, origin):

        # {'paths': [{'location': 'global', 'path': 'E:\\3D\\PIPELINE\\USD_Uptight_2025_v001\\00_Template\\Uptight\\03_Production\\02_Shots\\sq_010\\master'}], 'sequence': 'sq_010', 'shot': 'master', 'type': 'shot'}

        filepath = os.path.dirname(__file__)
        outputHoudiniFilePath = os.path.join(filepath, "output.hip")
        outputHoudiniFilePath = outputHoudiniFilePath.replace("\\", "/")

        # Try to get the reference of the setDress if the current shot
        ImportReference = True
        ReferenceFile = ""

        
        parent.console.log(origin.getCurrentEntity())

        ReferenceFile = self.getMasterPathFromEntity(origin.getCurrentEntity(), ".usda", origin, ["SetD", "Publish"])
        if ReferenceFile == "":
            ImportReference = False
            QMessageBox.warning(parent, "Reference File Not Found", "No Set Dress reference file found for this shot. Proceeding without reference.")
        
        parent.console.log(f"Reference file: {ReferenceFile}")
        
        assetType = origin.getCurrentEntity()["type"]
        assetName = origin.getCurrentEntity()["sequence"] + "_" + origin.getCurrentEntity()["shot"]

        script = StandaloneScriptHoudini("Stdl_MasterLight_Houdini.py", parent)
        script.replaceVariable("$$ASSET_NAME$$", assetName)
        script.replaceVariable("$$OUTPUT_PATH$$", outputHoudiniFilePath)
        script.replaceVariable("$$TYPE_ASSET$$", assetType)
        script.replaceVariable("$$REFERENCE_PATH$$", ReferenceFile)
        script.replaceVariable("$$IMPORT_REFERENCE$$", "True" if ImportReference == True else "False" )
        script.run()

        # Add the scene to the current project
        scene = { "path": outputHoudiniFilePath }
        origin.createSceneFromPreset(scene)

        # Delete the scene
        os.remove(outputHoudiniFilePath)