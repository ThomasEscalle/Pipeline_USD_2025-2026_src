from src.core.FileTemplateBase import FileTemplateBase
from src.core.StandaloneScriptMaya import StandaloneScriptMaya
from src.ui.AskForProductToImport import ProductImportDialog, QDialog
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

        # Crées le chemin ou maya vas enregistrer son fichier.
        # A la fin, on copiras le fichier crée dans Prism sous une nouvelle version.
        filepath = os.path.dirname(__file__)
        outputMayaFilePath = os.path.join(filepath, "output.ma")
        outputMayaFilePath = outputMayaFilePath.replace("\\", "/")


        # Ici on recuperer tous products qui sont des ".abc" , et dont le nom contiens "ModL" et Publish, 
        # Depuis l'entitée "Current".
        ImportReference = True
        ReferenceFiles = self.getMatchingProductsFromEntity(origin.getCurrentEntity(), ".usd", origin, ["ModL", "Publish"])

        
        # Demande a l'utilisateur quel produits a importer
        dialog = ProductImportDialog( origin.core, parent, None)
        default_selected = [
            {
                "type" : "folder",
                "name" : "Models Low",
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
            {
                "setting_name": "Import with namespace",
                "type": "checkbox",
                "default_value": True
            },
            {
                "setting_name": "Import Namespace",
                "type": "lineedit",
                "default_value": "MOD_LOW"
            },
            {
                "setting_name": "Import Method",
                "type": "combobox",
                "default_value": "Reference",
                "options": ["Reference", "Import"]
            },
        ]

        # Set the default selected product
        dialog.setDefaultSelectedProduct(default_selected)
        
        # Set the settings configuration
        dialog.setSettings(settings)

        dialog.setWindowTitle("Import Products")
        result = dialog.exec_()


        # On annule si jamais l'utilisateur a demandé annulé sur le dialogue.
        if result != QDialog.Accepted:
            return
        
        # On recupere les items a importer.
        items = dialog.getResult()
        itemModelLow = items["Models Low"]

        # On recuper les fichiers correspondant a la liste de products
        referencePaths = self.getPreferedFilePathsFromProductList(itemModelLow, origin)
        print("REFERENCE PATHS : ")
        print(referencePaths)
        
        referencePathsStr = str(referencePaths)

        # Si il n'y a pas de references attachés, on met le ImportReference a false pour
        # Eviter que maya n'essaye d'importer des references.
        if ReferenceFiles is None or len(ReferenceFiles) == 0:
            ImportReference = False
            ReferenceFiles = []
        else:
            ImportReference = True

        # Get the result settings
        resultSettings = dialog.getSettings()

        numberOfGroups = resultSettings["Number of output groups"]
        importMethod = resultSettings["Import Method"]
        doImportNamespace = resultSettings["Import with namespace"]
        importNamespace = resultSettings["Import Namespace"]

        if ImportReference:
            if resultSettings["Create References"] is False:
                ImportReference = False

        # Get the asset type
        assetType = origin.getCurrentEntity()["asset_path"].split("\\")[0]
        assetName = origin.getCurrentEntity()["asset_path"].split("\\")[-1]
        




        # Create the standalone script and replace the variables
        script = StandaloneScriptMaya("Stdl_ModHigh_Maya.py")
        script.replaceVariable("ASSET_NAME", assetName)
        script.replaceVariable("TYPE_ASSET", assetType)
        script.replaceVariable("OUTPUT_PATH", outputMayaFilePath)
        
        # Only set the import reference if it exists
        script.replaceVariable("IMPORT_REFERENCE", "True" if ImportReference == True else "False" )
        script.replaceVariable("REFERENCE_PATH", referencePathsStr if ImportReference else "")

        script.replaceVariable("IMPORT_METHOD", importMethod)
        script.replaceVariable("DO_IMPORT_NAMESPACE", "True" if doImportNamespace else "False")
        script.replaceVariable("IMPORT_NAMESPACE", importNamespace)

        script.replaceVariable("NUMBER_OF_GROUPS", numberOfGroups)






        # Lance le script
        script.run()

        # Add the scene to the current project
        scene = { "path": outputMayaFilePath }
        origin.createSceneFromPreset(scene)

        # Delete the scene
        os.remove(outputMayaFilePath)


