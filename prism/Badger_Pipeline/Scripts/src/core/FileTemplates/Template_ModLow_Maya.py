from src.core.FileTemplateBase import FileTemplateBase
from src.core.StandaloneScriptMaya import StandaloneScriptMaya
import os


class FileTemplateModelingLowMaya(FileTemplateBase):

    def __init__(self):
        super().__init__()
        self.template_name = "ModelingLowMaya"
        self.template_software = "Maya"

    def construct(self, parent, path, origin):
        
        filepath = os.path.dirname(__file__)
        outputMayaFilePath = os.path.join(filepath, "output.ma")
        outputMayaFilePath = outputMayaFilePath.replace("\\", "/")

        print("Creating a new Maya scene for low poly modeling... at : " + outputMayaFilePath)

        parent.console.log(origin.getCurrentEntity())
        assetType = origin.getCurrentEntity()["asset_path"].split("\\")[0]
        assetName = origin.getCurrentEntity()["asset_path"].split("\\")[-1]

        script = StandaloneScriptMaya("Stdl_ModLow_Maya.py")
        script.replaceVariable("ASSET_NAME", assetName)
        script.replaceVariable("OUTPUT_PATH", outputMayaFilePath)
        script.replaceVariable("TYPE_ASSET", assetType)
        script.run()

        # Add the scene to the current project
        scene = { "path": outputMayaFilePath }
        origin.createSceneFromPreset(scene)

        # Delete the scene
        os.remove(outputMayaFilePath)