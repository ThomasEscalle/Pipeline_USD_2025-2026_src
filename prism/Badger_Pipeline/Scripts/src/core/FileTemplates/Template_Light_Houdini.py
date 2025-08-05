# Mod/Houdini

from src.core.FileTemplateBase import FileTemplateBase
from src.core.StandaloneScriptHoudini import StandaloneScriptHoudini
import os


class FileTemplateLightHoudini(FileTemplateBase):

    def __init__(self):
        super().__init__()
        self.template_name = "LightHoudini"
        self.template_software = "Houdini"

    def construct(self, parent, path, origin):

        # {'paths': [{'location': 'global', 'path': 'E:\\3D\\PIPELINE\\USD_Uptight_2025_v001\\00_Template\\Uptight\\03_Production\\02_Shots\\sq_010\\master'}], 'sequence': 'sq_010', 'shot': 'master', 'type': 'shot'}

        filepath = os.path.dirname(__file__)
        outputHoudiniFilePath = os.path.join(filepath, "output.hip")
        outputHoudiniFilePath = outputHoudiniFilePath.replace("\\", "/")

        ##### GET THE MASTER LIGHT REFERENCE FILE #####

        masterLight = ""

        parent.console.log(origin.getCurrentEntity())
        assetType = origin.getCurrentEntity()["type"]
        assetName = origin.getCurrentEntity()["sequence"] + "_" + origin.getCurrentEntity()["shot"]

        masterLight = origin.getCurrentEntity()["paths"][0]["path"]
        masterLight.replace("\\", "/")
        masterLight = os.path.dirname(masterLight)
        masterLight = os.path.join(masterLight, "Master" , "Export" , "MasterLight_Publish", "master")

        # Check if the reference file directory exists
        if not os.path.exists(masterLight):
            parent.console.log(f"Reference file directory does not exist: {masterLight}")
            return
        # Check if there is a .usda file in the reference directory
        usdaFiles = [f for f in os.listdir(masterLight) if f.endswith('.usda')]
        if not usdaFiles:
            parent.console.log(f"No .usda files found in the reference directory: {masterLight}")
            return
        # Use the first .usda file found
        masterLight = os.path.join(masterLight, usdaFiles[0])
        masterLight = masterLight.replace("\\", "/")
        
        parent.console.log(f"Reference file: {masterLight}")


        ### GET THE ASSEMBLY REFERENCE FILE ###
        assembly = origin.getCurrentEntity()["paths"][0]["path"]
        assembly.replace("\\", "/")
        assembly = os.path.join(assembly , "Export" , "Assembly_Publish", "master")
        # Check if the assembly file directory exists
        if not os.path.exists(assembly):
            parent.console.log(f"Assembly file directory does not exist: {assembly}")
            return
        # Check if there is a .usda file in the assembly directory
        usdaFiles = [f for f in os.listdir(assembly) if f.endswith('.usda')]
        if not usdaFiles:
            parent.console.log(f"No .usda files found in the assembly directory: {assembly}")
            return
        # Use the first .usda file found
        assembly = os.path.join(assembly, usdaFiles[0])
        assembly = assembly.replace("\\", "/")


        script = StandaloneScriptHoudini("Stdl_Light_Houdini.py", parent)
        script.replaceVariable("$$ASSET_NAME$$", assetName)
        script.replaceVariable("$$OUTPUT_PATH$$", outputHoudiniFilePath)
        script.replaceVariable("$$TYPE_ASSET$$", assetType)
        script.replaceVariable("$$MASTER_LIGHT_PATH$$", masterLight)
        script.replaceVariable("$$ASSEMBLY_PATH$$", assembly)
        script.run()

        # Add the scene to the current project
        scene = { "path": outputHoudiniFilePath }
        origin.createSceneFromPreset(scene)

        # Delete the scene
        os.remove(outputHoudiniFilePath)