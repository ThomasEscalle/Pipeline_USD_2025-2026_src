# Mod/Houdini

from src.core.FileTemplateBase import FileTemplateBase
from src.core.StandaloneScriptHoudini import StandaloneScriptHoudini
from src.ui.AskForProductToImport import ProductImportDialog, QDialog
import os

try:
    from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QDialogButtonBox, QMessageBox
except:
    from PySide2.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QDialogButtonBox, QMessageBox



class FileTemplateLightHoudini(FileTemplateBase):

    def __init__(self):
        super().__init__()
        self.template_name = "LightHoudini"
        self.template_software = "Houdini"

    def construct(self, parent, path, origin):

        # {'paths': [{'location': 'global', 'path': 'E:\\3D\\PIPELINE\\USD_Uptight_2025_v001\\00_Template\\Uptight\\03_Production\\02_Shots\\sq_010\\master'}], 'sequence': 'sq_010', 'shot': 'master', 'type': 'shot'}

        # Define the output Houdini temp file path
        filepath = os.path.dirname(__file__)
        outputHoudiniFilePath = os.path.join(filepath, "output.hipnc")
        outputHoudiniFilePath = outputHoudiniFilePath.replace("\\", "/")

        
        # Current entity
        current_entity = origin.getCurrentEntity()
        master_entity = self.getCurrentShotMaster(current_entity, origin)

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

        # Ici, on vas recuperer l'assembly du shot courant.
        importReference_Assembly = True
        assembly_Files = self.getMatchingProductsFromEntity(current_entity, [".usd", ".usda" , ".usdc"], origin, ["Assembly", "Publish"])

        # Ici on vas recuperer le master light du shot courant.
        importReference_MasterLight = True
        masterLight_Files = self.getMatchingProductsFromEntity(master_entity, [".usd", ".usda" , ".usdc"], origin, ["MLgt", "Publish"])


        # Demande a l'utilisateur quel produits a eventuelement importer, ainsi que les settings
        dialog = ProductImportDialog( origin.core, parent, None)
        default_selected = [
            {
                "type" : "folder",
                "name" : "Assembly",
                "settings" : {
                    "accepted_files" : [
                        "usd", "usda", "usdc",
                    ]
                },
                "items" : assembly_Files,
                "select_only_one_file": True
            },
            {
                "type" : "folder",
                "name" : "Master Light",
                "settings" : {
                    "accepted_files" : [
                        "usd", "usda", "usdc",
                    ]
                },
                "items" : masterLight_Files,
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
        dialog.setHelpLink("https://thomasescalle.github.io/Pipeline_USD_2025/departements/Lighting/#comment-creer-une-scene-dans-houdini")
        dialog.setWindowTitle("Import Settings")
        result = dialog.exec_()


        # On annule si jamais l'utilisateur a demandé annulé sur le dialogue.
        if result != QDialog.Accepted:
            return
        

        # Get the items results
        items = dialog.getResult()
        items_assembly = items.get("Assembly", [])
        items_masterLight = items.get("Master Light", [])


        # On recupere les products associés aux items
        products_assembly = self.getPreferedFilePathsFromProductList(items_assembly, origin)
        # Si il y'a plus d'un assembly, on prend que le premier.
        if len(products_assembly) > 1 :
            products_assembly = [products_assembly[0]]

        products_masterLight = self.getPreferedFilePathsFromProductList(items_masterLight, origin)
        # Si il y'a plus d'un master light, on prend que le premier.
        if len(products_masterLight) > 1 :
            products_masterLight = [products_masterLight[0]]



        products_assembly_str = str(products_assembly[0]) if len(products_assembly) > 0 else ""
        products_masterLight_str = str(products_masterLight[0]) if len(products_masterLight) > 0 else ""


        if products_assembly_str == "" :
            importReference_Assembly = False
        if products_masterLight_str == "" :
            importReference_MasterLight = False


        # Get the settings results from the dialog
        settings = dialog.getSettings()

        assetType = current_entity["type"]
        assetName = current_entity["sequence"] + "_" + current_entity["shot"]
        task = origin.getCurrentTask()
        department = origin.getCurrentDepartment()



        ###################################################################
        ################### CREATE THE SCENE ##############################
        ###################################################################

        script = StandaloneScriptHoudini("Stdl_Light_Houdini.py", parent)

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

        script.replaceVariable("$$MASTER_LIGHT_PATH$$", products_masterLight_str.replace("\\", "/") if importReference_MasterLight else "")
        script.replaceVariable("$$ASSEMBLY_PATH$$", products_assembly_str.replace("\\", "/") if importReference_Assembly else "")
        
        try:
            script.run()
        except Exception as e:
            print(e)





        # Add the scene to the current project
        scene = { "path": outputHoudiniFilePath }
        origin.createSceneFromPreset(scene)

        # Delete the scene
        os.remove(outputHoudiniFilePath)