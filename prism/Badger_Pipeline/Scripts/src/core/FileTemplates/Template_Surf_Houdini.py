# RigL/Houdini

from src.core.FileTemplateBase import FileTemplateBase
from src.core.StandaloneScriptHoudini import StandaloneScriptHoudini
import os
from src.ui.AskForProductToImport import ProductImportDialog, QDialog
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

        # Crées le chemin ou maya vas enregistrer son fichier.
        # A la fin, on copiras le fichier crée dans Prism sous une nouvelle version.
        filepath = os.path.dirname(__file__)
        outputHoudiniFilePath = os.path.join(filepath, "output.hip")
        outputHoudiniFilePath = outputHoudiniFilePath.replace("\\", "/")

        # Ici on recuperer tous products qui sont des géometries ".usd" , et dont le nom contiens "ModH" et Publish, 
        # Depuis l'entitée "Current".
        ImportReference = True
        ReferenceFiles = self.getMatchingProductsFromEntity(origin.getCurrentEntity(), [".usd", ".usda" , ".usdc", ".abc" , ".obj"], origin, ["ModH", "Publish"])

        # Demande a l'utilisateur quel produits a importer
        dialog = ProductImportDialog( origin.core, parent, None)
        default_selected = [
            {
                "type" : "folder",
                "name" : "Models High",
                "settings" : {
                    "accepted_files" : [
                        "abc",
                        "usd", "usda", "usdc",
                        "obj"
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
                "default_value": "Modeling high first",
                "options": ["Modeling high first" , "Number of variant first"]
            },
            {
                "setting_name": "Number of output groups",
                "type": "combobox",
                "default_value": "01",
                "options": ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16"]
            },
            {
                "setting_name" : "Variants share same materials",
                "type" : "checkbox",
                "default_value" : False
            },
            {
                "setting_name": "import_title",
                "type": "title",
                "default_value": "ModHigh Import Settings"
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
        dialog.setHelpLink("https://thomasescalle.github.io/Pipeline_USD_2025/departements/Surfacing/#comment-creer-une-scene-dans-houdini")
        dialog.setWindowTitle("Import Settings")
        result = dialog.exec_()

        # On annule si jamais l'utilisateur a demandé annulé sur le dialogue.
        if result != QDialog.Accepted:
            return

        # On recupere les items a importer.
        items = dialog.getResult()
        itemModelsHigh = items["Models High"]

        # On recupere les fichiers correspondant a la liste de products
        # ReferencePaths is the adjusted list of paths to import based on user selection in the dialog
        referencePaths = self.getPreferedFilePathsFromProductList(itemModelsHigh, origin) 
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

        variantsShareSameMaterials = resultSettings["Variants share same materials"]
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
        script = StandaloneScriptHoudini("Stdl_Surf_Houdini.py", parent)
        script.replaceVariable("$$OUTPUT_PATH$$", outputHoudiniFilePath)
        script.replaceVariable("$$ASSET_NAME$$", assetName)
        script.replaceVariable("$$TYPE_ASSET$$", assetType)
        script.replaceVariable("$$TASK_NAME$$", task)
        script.replaceVariable("$$DEPARTMENT_NAME$$", department)

        script.replaceVariable("$$VARIANTS_SHARE_SAME_MATERIALS$$", "True" if variantsShareSameMaterials else "False" )
        script.replaceVariable("$$CREATION_METHOD$$", creationMethod)
        script.replaceVariable("$$NUMBER_OF_GROUPS$$", numberOfGroups)

        script.replaceVariable("$$IMPORT_REFERENCE$$", "True" if ImportReference == True else "False" )
        script.replaceVariable("$$REFERENCE_PATH$$", referencePathsStr if ImportReference else "")

        try:
            script.run()
        except Exception as e:
            print(e)
        
        

        # Add the scene to the current project
        scene = { "path": outputHoudiniFilePath }
        origin.createSceneFromPreset(scene)

        # Delete the scene
        os.remove(outputHoudiniFilePath)


