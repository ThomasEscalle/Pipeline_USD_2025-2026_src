# Mod/Houdini

from src.core.FileTemplateBase import FileTemplateBase
from src.core.StandaloneScriptHoudini import StandaloneScriptHoudini
from src.ui.AskForProductToImport import ProductImportDialog, QDialog
import os

try:
    from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QDialogButtonBox, QMessageBox
except:
    from PySide2.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QDialogButtonBox, QMessageBox



 
class FileTemplateAssemblyHoudini(FileTemplateBase):

    def __init__(self):
        super().__init__()
        self.template_name = "AssemblyHoudini"
        self.template_software = "Houdini"

    def construct(self, parent, path, origin):

        # {'paths': [{'location': 'global', 'path': 'E:\\3D\\PIPELINE\\USD_Uptight_2025_v001\\00_Template\\Uptight\\03_Production\\02_Shots\\sq_010\\master'}], 'sequence': 'sq_010', 'shot': 'master', 'type': 'shot'}


        # Define the output Houdini temp file path
        filepath = os.path.dirname(__file__)
        outputHoudiniFilePath = os.path.join(filepath, "output.hip")
        outputHoudiniFilePath = outputHoudiniFilePath.replace("\\", "/")

        # Current entity
        current_entity = origin.getCurrentEntity()


        shot_details = self.getShotDetails(current_entity, origin)  # {'range': [1001, 1005], 'length': 5, 'metadata': {'preroll': {'value': '5', 'show': True}, 'postroll': {'value': '5', 'show': True}}}
        shot_range = shot_details.get("range", [1001, 1100])
        shot_length = shot_details.get("length", 100)

        # Get the preroll and postroll from the shot metadata if it exists
        shot_metadata = shot_details.get("metadata", {})
        shot_preroll = 0
        shot_postroll = 0
        if "preroll" in shot_metadata and "value" in shot_metadata["preroll"]:
            try:
                shot_preroll = int(shot_metadata["preroll"]["value"])
            except ValueError:
                shot_preroll = 0
        if "postroll" in shot_metadata and "value" in shot_metadata["postroll"]:
            try:
                shot_postroll = int(shot_metadata["postroll"]["value"])
            except ValueError:
                shot_postroll = 0

        # Ici, on vas recuperer le setdress de l'entitée master du shot courant.
        importReference_SetDress = True
        master_entity = self.getCurrentShotMaster(current_entity, origin)
        setDress_Files = self.getMatchingProductsFromEntity(master_entity, [".usd", ".usda" , ".usdc"], origin, ["SetD", "Publish"])

        


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
                "items" : setDress_Files,
                "select_only_one_file": True
            }
        ]
        settings = [
        ]


        # Set the default selected product
        dialog.setDefaultSelectedProduct(default_selected)

        # Set the settings configuration
        dialog.setSettings(settings)

        dialog.navigate(current_entity)
        dialog.setHelpLink("https://thomasescalle.github.io/Pipeline_USD_2025/departements/Assembly/#comment-creer-une-scene-dans-houdini")
        dialog.setWindowTitle("Import Settings")
        result = dialog.exec_()


        # On annule si jamais l'utilisateur a demandé annulé sur le dialogue.
        if result != QDialog.Accepted:
            return

        # Get the items results
        items = dialog.getResult()
        items_setDress = items.get("Set Dress", [])

        # On recupere les products associés aux items
        products_setDress = self.getPreferedFilePathsFromProductList(items_setDress, origin)
        # Si il y'a plus d'un set dress, on prend que le premier.
        if len(products_setDress) > 1 :
            products_setDress = [products_setDress[0]]

        products_setDress_str = str(products_setDress[0]) if len(products_setDress) > 0 else ""



        # Get the settings results from the dialog
        settings = dialog.getSettings()

        assetType = current_entity["type"]
        assetName = current_entity["sequence"] + "_" + current_entity["shot"]
        task = origin.getCurrentTask()
        department = origin.getCurrentDepartment()

        
        ###################################################################
        ################### CREATE THE SCENE ##############################
        ###################################################################

        script = StandaloneScriptHoudini("Stdl_Assembly_Houdini.py", parent)

        script.replaceVariable("$$OUTPUT_PATH$$", outputHoudiniFilePath)

        script.replaceVariable("$$ASSET_NAME$$", assetName)
        script.replaceVariable("$$TYPE_ASSET$$", assetType)
        script.replaceVariable("$$TASK_NAME$$", task)
        script.replaceVariable("$$DEPARTMENT_NAME$$", department)

        script.replaceVariable("$$SHOT_START$$", str(shot_range[0]))
        script.replaceVariable("$$SHOT_END$$", str(shot_range[1]))
        script.replaceVariable("$$SHOT_LENGTH$$", str(shot_length))
        script.replaceVariable("$$SHOT_PREROLL$$", str(shot_preroll))
        script.replaceVariable("$$SHOT_POSTROLL$$", str(shot_postroll))

        script.replaceVariable("$$SETDRESS_FILEPATH$$", products_setDress_str.replace("\\", "/"))

        try:
            script.run()
        except Exception as e:
            print(e)
        # Add the scene to the current project
        scene = { "path": outputHoudiniFilePath }
        origin.createSceneFromPreset(scene)

        # Delete the scene
        os.remove(outputHoudiniFilePath)