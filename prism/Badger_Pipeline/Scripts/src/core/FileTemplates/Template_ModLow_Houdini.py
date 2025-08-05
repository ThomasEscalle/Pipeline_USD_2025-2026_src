# Mod/Houdini

from src.core.FileTemplateBase import FileTemplateBase
from src.core.StandaloneScriptHoudini import StandaloneScriptHoudini
import os


class FileTemplateModelingLowHoudini(FileTemplateBase):

    def __init__(self):
        super().__init__()
        self.template_name = "ModLHoudini"
        self.template_software = "Houdini"

    def construct(self, parent, path, origin):

        # {'paths': [{'location': 'global', 'path': 'E:\\3D\\PIPELINE\\USD_Uptight_2025_v001\\00_Template\\Uptight\\03_Production\\02_Shots\\sq_010\\master'}], 'sequence': 'sq_010', 'shot': 'master', 'type': 'shot'}

        filepath = os.path.dirname(__file__)
        outputHoudiniFilePath = os.path.join(filepath, "output.hip")
        outputHoudiniFilePath = outputHoudiniFilePath.replace("\\", "/")

        parent.console.log(origin.getCurrentEntity())
        assetType = origin.getCurrentEntity()["asset_path"].split("\\")[0]
        assetName = origin.getCurrentEntity()["asset_path"].split("\\")[-1]

        script = StandaloneScriptHoudini("Stdl_ModLow_Houdini.py", parent)
        script.replaceVariable("$$ASSET_NAME$$", assetName)
        script.replaceVariable("$$TYPE_ASSET$$", assetType)
        script.replaceVariable("$$OUTPUT_PATH$$", outputHoudiniFilePath)
        script.run()

        # Add the scene to the current project
        scene = { "path": outputHoudiniFilePath }
        origin.createSceneFromPreset(scene)

        # Delete the scene
        os.remove(outputHoudiniFilePath)