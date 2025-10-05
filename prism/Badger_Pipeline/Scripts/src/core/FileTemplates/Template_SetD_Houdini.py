# Mod/Houdini

from src.core.FileTemplateBase import FileTemplateBase
from src.core.StandaloneScriptHoudini import StandaloneScriptHoudini
import os


class FileTemplateSetDressHoudini(FileTemplateBase):

    def __init__(self):
        super().__init__()
        self.template_name = "SetDressHoudini"
        self.template_software = "Houdini"

    def construct(self, parent, path, origin):

        # Crées le chemin ou maya vas enregistrer son fichier.
        # A la fin, on copiras le fichier crée dans Prism sous une nouvelle version.
        filepath = os.path.dirname(__file__)
        outputHoudiniFilePath = os.path.join(filepath, "output.hipnc")
        outputHoudiniFilePath = outputHoudiniFilePath.replace("\\", "/")

        # Todo : Crées un dialogue si besoin ici
        # Pour l'instant, pas besoin de dialogue

        assetType = origin.getCurrentEntity()["type"]
        assetName = origin.getCurrentEntity()["sequence"] + "_" + origin.getCurrentEntity()["shot"]
        task = origin.getCurrentTask()
        department = origin.getCurrentDepartment()

        script = StandaloneScriptHoudini("Stdl_SetD_Houdini.py", parent)
        script.replaceVariable("$$ASSET_NAME$$", assetName)
        script.replaceVariable("$$OUTPUT_PATH$$", outputHoudiniFilePath)
        script.replaceVariable("$$TYPE_ASSET$$", assetType)
        script.replaceVariable("$$TASK_NAME$$", task)
        script.replaceVariable("$$DEPARTMENT_NAME$$", department)
        try:
            script.run()
        except Exception as e:
            print(e)

        # Add the scene to the current project
        scene = { "path": outputHoudiniFilePath }
        origin.createSceneFromPreset(scene)

        # Delete the scene
        os.remove(outputHoudiniFilePath)