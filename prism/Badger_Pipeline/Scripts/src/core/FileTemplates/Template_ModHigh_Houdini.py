from src.core.FileTemplateBase import FileTemplateBase
from src.core.StandaloneScriptHoudini import StandaloneScriptHoudini
from src.ui.AskForProductToImport import ProductImportDialog, QDialog
import os

try:
    from PySide6.QtWidgets import QMessageBox
except:
    from PySide2.QtWidgets import QMessageBox



class FileTemplateModelingHighHoudini(FileTemplateBase):

    def __init__(self):
        super().__init__()
        self.template_name = "ModelingHighHoudini"
        self.template_software = "Houdini"

    def construct(self, parent, path, origin):

        # Crées le chemin ou maya vas enregistrer son fichier.
        # A la fin, on copiras le fichier crée dans Prism sous une nouvelle version.
        filepath = os.path.dirname(__file__)
        outputHoudiniFilePath = os.path.join(filepath, "output.hip")
        outputHoudiniFilePath = outputHoudiniFilePath.replace("\\", "/")

        # Ici on recuperer tous products qui sont des ".usd" , et dont le nom contiens "ModL" et Publish, 
        # Depuis l'entitée "Current".
        ImportReference = True
        ReferenceFiles = self.getMatchingProductsFromEntity(origin.getCurrentEntity(), [".usd", ".usda" , ".usdc", ".abc" , ".obj"], origin, ["ModL", "Publish"])



        # Demande a l'utilisateur quel produits a eventuelement importer, ainsi que les settings
        dialog = ProductImportDialog( origin.core, parent, None)
        default_selected = [
            {
                "type" : "folder",
                "name" : "Models Low",
                "settings" : {
                    "accepted_files" : [
                        "abc",
                        "usd", "usda", "usdc",
                        "obj" , "abc" ,
                    ]
                },
                "items" : ReferenceFiles
            }
        ]
        settings = [
            {
                "setting_name": "import_title",
                "type": "title",
                "default_value": "Globals"
            },         
            {
                "setting_name": "Creation method",
                "type": "combobox",
                "default_value": "Modeling Low first",
                "options": ["Modeling Low first" , "Number of variant first"]
            },
            {
                "setting_name": "Number of output groups",
                "type": "combobox",
                "default_value": "01",
                "options": ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16"]
            },
            {
                "setting_name": "import_title",
                "type": "title",
                "default_value": "ModLow Import Settings"
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
        dialog.setHelpLink("https://thomasescalle.github.io/Pipeline_USD_2025/departements/ModelingHigh/#comment-creer-une-scene-dans-houdini")
        dialog.setWindowTitle("Import Settings")
        result = dialog.exec_()

        # On annule si jamais l'utilisateur a demandé annulé sur le dialogue.
        if result != QDialog.Accepted:
            return
        
        # On recupere les items a importer.
        items = dialog.getResult()
        itemModelLow = items["Models Low"]
        
        # On recuper les fichiers correspondant a la liste de products
        referencePaths = self.getPreferedFilePathsFromProductList(itemModelLow, origin)
        referencePathsStr = str(referencePaths)

        # Si il n'y a pas de references attachés, on met le ImportReference a false pour
        # Eviter que houdini n'essaye d'importer des references.
        if referencePaths is None or len(referencePaths) == 0:
            ImportReference = False
            referencePaths = []
        else:
            ImportReference = True

        # Get the result settings
        resultSettings = dialog.getSettings()

        creationMethod = resultSettings["Creation method"]
        numberOfGroups = resultSettings["Number of output groups"]

        if ImportReference:
            if resultSettings["Create References"] is False:
                ImportReference = False

        # Get the asset type
        assetType = origin.getCurrentEntity()["asset_path"].split("\\")[0]
        assetName = origin.getCurrentEntity()["asset_path"].split("\\")[-1]
        task = origin.getCurrentTask()
        department = origin.getCurrentDepartment()


        # Create the standalone script and replace the variables
        script = StandaloneScriptHoudini("Stdl_ModHigh_Houdini.py", parent)

        script.replaceVariable("$$ASSET_NAME$$", assetName)
        script.replaceVariable("$$TYPE_ASSET$$", assetType)
        script.replaceVariable("$$OUTPUT_PATH$$", outputHoudiniFilePath)

        # Only set the import reference if it exists
        script.replaceVariable("$$IMPORT_REFERENCE$$", "True" if ImportReference == True else "False" )
        script.replaceVariable("$$REFERENCE_PATH$$", referencePathsStr if ImportReference else "")

        script.replaceVariable("$$CREATION_METHOD$$", creationMethod)
        script.replaceVariable("$$NUMBER_OF_GROUPS$$", numberOfGroups)

        script.replaceVariable("$$TASK_NAME$$", task)
        script.replaceVariable("$$DEPARTMENT_NAME$$", department)

        script.run()

        # Add the scene to the current project
        scene = { "path": outputHoudiniFilePath }
        origin.createSceneFromPreset(scene)

        # Delete the scene
        os.remove(outputHoudiniFilePath)