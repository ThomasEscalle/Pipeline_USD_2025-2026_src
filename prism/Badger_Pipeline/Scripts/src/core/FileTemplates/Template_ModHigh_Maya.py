from src.core.FileTemplateBase import FileTemplateBase
from src.core.StandaloneScriptMaya import StandaloneScriptMaya
import os

try:
    from PySide6.QtWidgets import QMessageBox
except:
    from PySide2.QtWidgets import QMessageBox



class FileTemplateModelingHighMaya(FileTemplateBase):

    def __init__(self):
        super().__init__()
        self.template_name = "ModelingHighMaya"
        self.template_software = "Maya"

    def construct(self, parent, path, origin):

        filepath = os.path.dirname(__file__)

        # Save path
        outputMayaFilePath = os.path.join(filepath, "output.ma")
        outputMayaFilePath = outputMayaFilePath.replace("\\", "/")

        # Search for the reference
        ImportReference = True
        ReferenceFile = self.getMasterPathFromEntity(origin.getCurrentEntity(), ".abc", origin, ["ModL", "Publish"])

        if ReferenceFile == "":
            ImportReference = False
            ReferenceFile = ""
            QMessageBox.warning(parent, "Reference Not Found", "No reference file found for Modeling Low. Proceeding without reference.")

        assetType = origin.getCurrentEntity()["asset_path"].split("\\")[0]
        assetName = origin.getCurrentEntity()["asset_path"].split("\\")[-1]
        
        script = StandaloneScriptMaya("Stdl_ModHigh_Maya.py")
        script.replaceVariable("ASSET_NAME", assetName)
        script.replaceVariable("TYPE_ASSET", assetType)
        script.replaceVariable("OUTPUT_PATH", outputMayaFilePath)
        
        # Only set the import reference if it exists
        script.replaceVariable("IMPORT_REFERENCE", "True" if ImportReference == True else "False" )
        script.replaceVariable("REFERENCE_PATH", ReferenceFile if ImportReference else "")

        script.run()

        # Add the scene to the current project
        scene = { "path": outputMayaFilePath }
        origin.createSceneFromPreset(scene)

        # Delete the scene
        os.remove(outputMayaFilePath)


