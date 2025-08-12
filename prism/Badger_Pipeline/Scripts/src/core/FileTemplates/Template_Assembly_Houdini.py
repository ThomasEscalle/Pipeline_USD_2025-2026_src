# Mod/Houdini

from src.core.FileTemplateBase import FileTemplateBase
from src.core.StandaloneScriptHoudini import StandaloneScriptHoudini
import os




 
class FileTemplateAssemblyHoudini(FileTemplateBase):

    def __init__(self):
        super().__init__()
        self.template_name = "AssemblyHoudini"
        self.template_software = "Houdini"

    def construct(self, parent, path, origin):

        # {'paths': [{'location': 'global', 'path': 'E:\\3D\\PIPELINE\\USD_Uptight_2025_v001\\00_Template\\Uptight\\03_Production\\02_Shots\\sq_010\\master'}], 'sequence': 'sq_010', 'shot': 'master', 'type': 'shot'}

        filepath = os.path.dirname(__file__)
        outputHoudiniFilePath = os.path.join(filepath, "output.hip")
        outputHoudiniFilePath = outputHoudiniFilePath.replace("\\", "/")

        
        ImportReference = True
        ReferenceFile = ""


        parent.console.log(origin.getCurrentEntity())
        assetType = origin.getCurrentEntity()["type"]
        assetName = origin.getCurrentEntity()["sequence"] + "_" + origin.getCurrentEntity()["shot"]

        referenceFile = origin.getCurrentEntity()["paths"][0]["path"]
        referenceFile.replace("\\", "/")
        referenceFile = os.path.dirname(referenceFile)
        referenceFile = os.path.join(referenceFile, "Master" , "Export" , "SedD_Publish", "master")

        # Check if the reference file directory exists
        if not os.path.exists(referenceFile):
            parent.console.log(f"Reference file directory does not exist: {referenceFile}")
            return
        
        # Check if there is a .usda file in the reference directory
        usdaFiles = [f for f in os.listdir(referenceFile) if f.endswith('.usda')]
        if not usdaFiles:
            parent.console.log(f"No .usda files found in the reference directory: {referenceFile}")
            return
        # Use the first .usda file found
        referenceFile = os.path.join(referenceFile, usdaFiles[0])
        referenceFile = referenceFile.replace("\\", "/")
        
        parent.console.log(f"Reference file: {referenceFile}")



        script = StandaloneScriptHoudini("Stdl_Assembly_Houdini.py", parent)
        script.replaceVariable("$$ASSET_NAME$$", assetName)
        script.replaceVariable("$$OUTPUT_PATH$$", outputHoudiniFilePath)
        script.replaceVariable("$$TYPE_ASSET$$", assetType)
        script.replaceVariable("$$SET_DRESSING_PATH$$", referenceFile)
        script.run()

        # Add the scene to the current project
        scene = { "path": outputHoudiniFilePath }
        origin.createSceneFromPreset(scene)

        # Delete the scene
        os.remove(outputHoudiniFilePath)