# RigL/Houdini

from src.core.FileTemplateBase import FileTemplateBase
from src.core.StandaloneScriptHoudini import StandaloneScriptHoudini
import os

try:
    from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QDialogButtonBox, QMessageBox
except:
    from PySide2.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QDialogButtonBox, QMessageBox


class FileTemplateSurfHoudini(FileTemplateBase):

    def __init__(self):
        super().__init__()
        self.template_name = "SurfHoudini"
        self.template_software = "Houdini"

    def construct(self, parent, path, origin):
        filepath = os.path.dirname(__file__)
        outputHoudiniFilePath = os.path.join(filepath, "output.hip")
        outputHoudiniFilePath = outputHoudiniFilePath.replace("\\", "/")

        ImportReference = True
        ReferenceFile = self.getMasterPathFromEntity(origin.getCurrentEntity(), ".abc", origin, ["ModH", "Publish"])
        if ReferenceFile == "":
            ImportReference = False
            ReferenceFile = ""
            QMessageBox.warning(parent, "Reference Not Found", "No reference file found for Modeling High. Proceeding without reference.")

        assetType = origin.getCurrentEntity()["asset_path"].split("\\")[0]
        assetName = origin.getCurrentEntity()["asset_path"].split("\\")[-1]

        script = StandaloneScriptHoudini("Stdl_Surf_Houdini.py", parent)
        script.replaceVariable("$$ASSET_NAME$$", assetName)
        script.replaceVariable("$$TYPE_ASSET$$", assetType)
        script.replaceVariable("$$OUTPUT_PATH$$", outputHoudiniFilePath)
        if ImportReference == True:
            script.replaceVariable("$$IMPORT_REFERENCE$$", "True")
        else:
            script.replaceVariable("$$IMPORT_REFERENCE$$", "False")
        script.replaceVariable("$$REFERENCE_PATH$$", ReferenceFile)
        script.run()

        # Add the scene to the current project
        scene = { "path": outputHoudiniFilePath }
        origin.createSceneFromPreset(scene)

        # Delete the scene
        os.remove(outputHoudiniFilePath)


