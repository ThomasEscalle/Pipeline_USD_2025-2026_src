# AutorigRigL01/Maya

from src.core.FileTemplateBase import FileTemplateBase
from src.core.StandaloneScriptMaya import StandaloneScriptMaya
import os
from src.ui.AskForProductToImport import ProductImportDialog, QDialog
try:
    from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QDialogButtonBox, QMessageBox
except:
    from PySide2.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QDialogButtonBox, QMessageBox



class FileTemplateAutorigRigHigh01Maya(FileTemplateBase):

    def __init__(self):
        super().__init__()
        self.template_name = "AutorigRigH01"
        self.template_software = "Maya"

    def construct(self, parent, path, origin):

        # Crées le chemin ou maya vas enregistrer son fichier.
        # A la fin, on copiras le fichier crée dans Prism sous une nouvelle version.
        filepath = os.path.dirname(__file__)
        outputMayaFilePath = os.path.join(filepath, "output.ma")
        outputMayaFilePath = outputMayaFilePath.replace("\\", "/")



        # Ici on recuperer tous products qui sont des ".usd" , et dont le nom contiens "ModH" et Publish, 
        # Depuis l'entitée "Current".
        ImportReference = True
        ReferenceFiles = self.getMatchingProductsFromEntity(origin.getCurrentEntity(), [".usd", ".usda" , ".usdc", ".abc" , ".obj"], origin, ["ModH", "Publish"], onlyOne=True)


        # Demande a l'utilisateur quel produits a importer
        dialog = ProductImportDialog( origin.core, parent, None)
        default_selected = [
            {
                "type" : "folder",
                "name" : "Model High",
                "settings" : {
                    "accepted_files" : [
                        "abc",
                        "usd", "usda", "usdc",
                        "obj"
                    ],
                    "select_only_one_file": True
                },
                "items" : ReferenceFiles
            }
        ]
        settings = [
            {
                "setting_name": "Controllers placement",
                "type": "combobox",
                "default_value": "bottom",
                "options": ["top", "centered", "bottom"],
            }
        ]

        # Set the default selected product
        dialog.setDefaultSelectedProduct(default_selected)
        
        # Set the settings configuration
        dialog.setSettings(settings)

        dialog.navigate(origin.getCurrentEntity())
        dialog.setHelpLink("https://thomasescalle.github.io/Pipeline_USD_2025/departements/RiggingHigh/#comment-creer-une-scene-dans-maya")
        dialog.setWindowTitle("Import Settings")
        result = dialog.exec_()


        # On annule si jamais l'utilisateur a demandé annulé sur le dialogue.
        if result != QDialog.Accepted:
            return
        
        # On recupere les items a importer.
        items = dialog.getResult()
        itemModelHigh = items["Model High"]


        # On recuper les fichiers correspondant a la liste de products
        referencePaths = self.getPreferedFilePathsFromProductList(itemModelHigh, origin)
        # Si il y a plus d'un fichier, on ne prend que le premier.
        if len(referencePaths) > 1:
            referencePaths = referencePaths[0:1]
        referencePathsStr = str(referencePaths)
        
        # Si il n'y a pas de references attachés, on met le ImportReference a false pour
        # Eviter que maya n'essaye d'importer des references.
        if referencePaths is None or len(referencePaths) == 0:
            ImportReference = False
            referencePaths = []
        else:
            ImportReference = True

        # Get the result settings
        resultSettings = dialog.getSettings()
        ctrl_placements = resultSettings["Controllers placement"]

        if ImportReference:
            if "Create References" in resultSettings and resultSettings["Create References"] is False:
                ImportReference = False

        # Get the asset type
        assetType = origin.getCurrentEntity()["asset_path"].split("\\")[0]
        assetName = origin.getCurrentEntity()["asset_path"].split("\\")[-1]

        
        script = StandaloneScriptMaya("Stdl_Autorig_Rig_01_Maya.py")

        script.replaceVariable("$$ASSET_NAME$$", assetName)
        script.replaceVariable("$$TYPE_ASSET$$", assetType)
        script.replaceVariable("$$OUTPUT_PATH$$", outputMayaFilePath)

        script.replaceVariable("$$REFERENCE_PATH$$", referencePaths[0] if len(referencePaths) >= 1 else "")

        script.replaceVariable("$$CTRL_PLACEMENTS$$", ctrl_placements)
        script.replaceVariable("$$SUBDIV_LEVEL$$", "righ")
        
        script.run()

        # Add the scene to the current project
        scene = { "path": outputMayaFilePath }
        origin.createSceneFromPreset(scene)

        # Delete the scene
        os.remove(outputMayaFilePath)

