# Mod/Houdini

from src.core.FileTemplateBase import FileTemplateBase
from src.core.StandaloneScriptHoudini import StandaloneScriptHoudini
import os
from src.ui.AskForProductToImport import ProductImportDialog, QDialog
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

        # Crées le chemin ou maya vas enregistrer son fichier.
        # A la fin, on copiras le fichier crée dans Prism sous une nouvelle version.
        filepath = os.path.dirname(__file__)
        outputHoudiniFilePath = os.path.join(filepath, "output.hip")
        outputHoudiniFilePath = outputHoudiniFilePath.replace("\\", "/")

        # Ici on recuperer tous products qui sont des ".usd" , et dont le nom contiens "SetD" et Publish, 
        # Depuis l'entitée "Current".
        ImportReference = True
        ReferenceFiles = self.getMatchingProductsFromEntity(origin.getCurrentEntity(), [".usd", ".usda" , ".usdc"], origin, ["SetD", "Publish"])


        # Demande a l'utilisateur quel produits a eventuelement importer, ainsi que les settings
        dialog = ProductImportDialog( origin.core, parent, None)
        default_selected = [
            {
                "type" : "folder",
                "name" : "Set Dress",
                "settings" : {
                    "accepted_files" : [
                        "usd", "usda", "usdc",
                    ]
                },
                "items" : ReferenceFiles,
                "select_only_one_file": True
            }
        ]
        settings = [
            {
                "setting_name": "import_title",
                "type": "title",
                "default_value": "Globals"
            },
            {
                "setting_name": "Create References",
                "type": "checkbox",
                "default_value": True
            },
        ]

        # Set the default selected product
        dialog.setDefaultSelectedProduct(default_selected)
        
        # Set the settings configuration
        dialog.setSettings(settings)

        dialog.navigate(origin.getCurrentEntity())
        dialog.setHelpLink("https://thomasescalle.github.io/Pipeline_USD_2025/departements/MasterLighting/#comment-creer-une-scene-dans-houdini")
        dialog.setWindowTitle("Import Settings")
        result = dialog.exec_()

        # On annule si jamais l'utilisateur a demandé annulé sur le dialogue.
        if result != QDialog.Accepted:
            return


        # On recupere les items a importer.
        items = dialog.getResult()
        itemsSetDress = items["Set Dress"]

        # On recuper les fichiers correspondant a la liste de products
        referencePaths = self.getPreferedFilePathsFromProductList(itemsSetDress, origin)
        # Si il y a plus d'un fichier, on ne prend que le premier.
        if len(referencePaths) > 1:
            referencePaths = referencePaths[0:1]
        referencePathsStr = str(referencePaths)

                # Si il n'y a pas de references attachés, on met le ImportReference a false pour
        # Eviter que maya n'essaye d'importer des references.
        if referencePaths is None or len(referencePaths) == 0 or referencePathsStr == "[]" or referencePathsStr == "":
            ImportReference = False
            referencePaths = []
        else:
            ImportReference = True

        # Get the result settings
        resultSettings = dialog.getSettings()
        # Process the settings here. No settings for now.

        if ImportReference:
            if resultSettings["Create References"] is False:
                ImportReference = False

        # Get the asset type
        assetType = origin.getCurrentEntity()["type"]
        assetName = origin.getCurrentEntity()["sequence"] + "_" + origin.getCurrentEntity()["shot"]
        task = origin.getCurrentTask()
        department = origin.getCurrentDepartment()


        # Create the standalone script and replace the variables
        script = StandaloneScriptHoudini("Stdl_MasterLight_Houdini.py", parent)

        script.replaceVariable("$$OUTPUT_PATH$$", outputHoudiniFilePath)

        script.replaceVariable("$$ASSET_NAME$$", assetName)
        script.replaceVariable("$$TYPE_ASSET$$", assetType)
        script.replaceVariable("$$TASK_NAME$$", task)
        script.replaceVariable("$$DEPARTMENT_NAME$$", department)

        # Only set the import reference if it exists
        script.replaceVariable("$$REFERENCE_PATH$$", referencePathsStr if ImportReference == True else "")
        script.replaceVariable("$$IMPORT_REFERENCE$$", "True" if ImportReference == True else "False")

        try:
            script.run()
        except Exception as e:
            print(e)



        # Add the scene to the current project
        scene = { "path": outputHoudiniFilePath }
        origin.createSceneFromPreset(scene)

        # Delete the scene
        os.remove(outputHoudiniFilePath)