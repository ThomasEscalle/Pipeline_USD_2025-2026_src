from src.core.FileTemplateBase import FileTemplateBase
from src.core.StandaloneScriptMaya import StandaloneScriptMaya
from src.ui.AskForProductToImport import ProductImportDialog, QDialog
import os


class FileTemplateModelingLowMaya(FileTemplateBase):

    def __init__(self):
        super().__init__()
        self.template_name = "ModelingLowMaya"
        self.template_software = "Maya"

    def construct(self, parent, path, origin):

        # Crées le chemin ou maya vas enregistrer son fichier.
        # A la fin, on copiras le fichier crée dans Prism sous une nouvelle version.
        filepath = os.path.dirname(__file__)
        outputMayaFilePath = os.path.join(filepath, "output.ma")
        outputMayaFilePath = outputMayaFilePath.replace("\\", "/")


                
        # Demande a l'utilisateur quel produits a eventuelement importer, ainsi que les settings
        dialog = ProductImportDialog( origin.core, parent, None)
        default_selected = [
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
            }
        ]

        # Set the default selected product
        dialog.setDefaultSelectedProduct(default_selected)
        
        # Set the settings configuration
        dialog.setSettings(settings)
        dialog.hideImportTab()

        dialog.navigate(origin.getCurrentEntity())
        dialog.setHelpLink("https://thomasescalle.github.io/Pipeline_USD_2025/departements/ModelingLow/#comment-creer-une-scene-dans-maya")
        dialog.setWindowTitle("Import Settings")
        result = dialog.exec_()

        # On annule si jamais l'utilisateur a demandé annulé sur le dialogue.
        if result != QDialog.Accepted:
            return

        # Get the result settings
        resultSettings = dialog.getSettings()

        numberOfGroups = resultSettings["Number of output groups"]


        assetType = origin.getCurrentEntity()["asset_path"].split("\\")[0]
        assetName = origin.getCurrentEntity()["asset_path"].split("\\")[-1]

        # Create the standalone script and replace the variables
        script = StandaloneScriptMaya("Stdl_ModLow_Maya.py")
        script.replaceVariable("ASSET_NAME", assetName)
        script.replaceVariable("OUTPUT_PATH", outputMayaFilePath)
        script.replaceVariable("TYPE_ASSET", assetType)
        script.replaceVariable("NUMBER_OF_GROUPS", numberOfGroups)


        script.run()

        # Add the scene to the current project
        scene = { "path": outputMayaFilePath }
        origin.createSceneFromPreset(scene)

        # Delete the scene
        os.remove(outputMayaFilePath)