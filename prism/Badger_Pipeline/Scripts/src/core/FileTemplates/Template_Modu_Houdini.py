# Mod/Houdini

from src.core.FileTemplateBase import FileTemplateBase
from src.core.StandaloneScriptHoudini import StandaloneScriptHoudini
import os


class FileTemplateModulesHoudini(FileTemplateBase):

    def __init__(self):
        super().__init__()
        self.template_name = "ModulesHoudini"
        self.template_software = "Houdini"

    def construct(self, parent, path, origin):

        filepath = os.path.dirname(__file__)
        outputHoudiniFilePath = os.path.join(filepath, "output.hip")
        outputHoudiniFilePath = outputHoudiniFilePath.replace("\\", "/")

        parent.console.log(origin.getCurrentEntity())
        assetType = origin.getCurrentEntity()["asset_path"].split("\\")[0]
        assetName = origin.getCurrentEntity()["asset_path"].split("\\")[-1]

        script = StandaloneScriptHoudini("Stdl_Modu_Houdini.py", parent)
        script.replaceVariable("$$ASSET_NAME$$", assetName)
        script.replaceVariable("$$OUTPUT_PATH$$", outputHoudiniFilePath)
        script.replaceVariable("$$TYPE_ASSET$$", assetType)
        script.run()

        # Add the scene to the current project
        scene = { "path": outputHoudiniFilePath }
        origin.createSceneFromPreset(scene)

        # Delete the scene
        os.remove(outputHoudiniFilePath)