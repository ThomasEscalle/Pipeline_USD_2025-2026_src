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
        outputHoudiniFilePath = os.path.join(filepath, "output.hipnc")
        outputHoudiniFilePath = outputHoudiniFilePath.replace("\\", "/")

        # Current entity
        current_entity = origin.getCurrentEntity()
        connected_entities = origin.core.entities.getConnectedEntities(origin.getCurrentEntity())

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
        
        # On cherche d'abord un éventuel setdress éditable sur le shot courant.
        # Si on en trouve pas, on prend celui du master.
        edit_setDress_Files = self.getMatchingProductsFromEntity(current_entity, [".usd", ".usda" , ".usdc"], origin, ["FLO_Edit_SetD_Publish"], onlyOne=True)
        if len(edit_setDress_Files) > 0 :
            setDress_Files = edit_setDress_Files
        else :
            setDress_Files = self.getMatchingProductsFromEntity(master_entity, [".usd", ".usda" , ".usdc"], origin, ["SetD_Publish"], onlyOne=True)


        # On vas chercher la camera qui a été publish dans le shot au moment de l'animation
        camera_file = self.getMatchingProductsFromEntity(current_entity, [".usd", ".usda" , ".usdc", ".abc"], origin, ["Anim_Cam_Publish"], onlyOne=True)


        # Recuperer les animations des personnages "anims"
        character_animations = self.getMatchingProductsFromEntity(current_entity, [".usd", ".usda" , ".usdc"], origin, ["Anim_Char", "_Publish"])


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
            },
            {
                "type" : "folder",
                "name" : "Camera",
                "settings" : {
                    "accepted_files" : [
                        "usd", "usda", "usdc", "abc"
                    ]
                },
                "items" : camera_file,
                "select_only_one_file": True
            },
            {
                "type" : "folder",
                "name" : "Character Animations",
                "settings" : {
                    "accepted_files" : [
                        "usd", "usda", "usdc"
                    ]
                },
                "items" : character_animations,
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

        # On recupere les products associés aux items
        items_setDress = items.get("Set Dress", [])
        products_setDress = self.getPreferedFilePathsFromProductList(items_setDress, origin)
        # Si il y'a plus d'un set dress, on prend que le premier.
        if len(products_setDress) > 1 :
            products_setDress = [products_setDress[0]]

        products_setDress_str = str(products_setDress[0]) if len(products_setDress) > 0 else ""


        # On recupere les products associés aux items
        products_camera = dialog.getResult().get("Camera", [])
        products_camera = self.getPreferedFilePathsFromProductList(products_camera, origin)
        # Si il y'a plus d'un camera, on prend que le premier.
        if len(products_camera) > 1 :
            products_camera = [products_camera[0]]

        products_camera_str = str(products_camera[0]) if len(products_camera) > 0 else ""



        ############################################################################
        # On recupere les products des character animations associés aux items #####
        ############################################################################
        products_character_animations = dialog.getResult().get("Character Animations", [])
        products_character_animations_files = self.getPreferedFilePathsFromProductList(products_character_animations, origin)
        for i in range(len(products_character_animations_files)):
            print("Character Animation File Selected : ", products_character_animations_files[i])
            products_character_animations[i]["product_file_path"] = products_character_animations_files[i]

            for entity in connected_entities:
                # print(" - Connected Entity : ", entity)
                # {'type': 'asset', 'asset_path': 'Chars\\Albert'}
                product = products_character_animations[i]["product"]
                product = product.replace("\\", "/")
                product = product.replace("Anim_Char_", "")
                product = product.replace("_Publish", "")

                if product in entity["asset_path"]:
                    products_character_animations[i]["connected_entity"] = entity
                    
                    # 1. Recuperer la liste de products dans l'entitée connectée.
                    products_in_entity = origin.core.products.getProductsFromEntity(entity)
                    
                    # 2. Trouver le product qui s'appelle "USD_Asset"
                    for p in products_in_entity:
                        if "USD_Asset" in p["product"]:
                            products_character_animations[i]["asset_product"] = p
                            print("   - Found USD_Asset Product : ", p)
                            
                            # 3. Recuperer le "asset.usda" du product
                            path = p.get("path", "")
                            path = path.replace("\\", "/")
                            path = os.path.join(path, "asset.usda")
                            path = path.replace("\\", "/")  

                            if os.path.exists(path):
                                products_character_animations[i]["asset_file_path"] = path
                            break


        # To str
        products_character_animations_str = str(products_character_animations) if len(products_character_animations) > 0 else ""

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


        script.replaceVariable("$$CAMERA_FILEPATH$$", products_camera_str.replace("\\", "/"))

        script.replaceVariable("$$SETDRESS_FILEPATH$$", products_setDress_str.replace("\\", "/"))

        script.replaceVariable("$$CHARACTER_ANIMATIONS_FILEPATH$$", products_character_animations_str.replace("\\", "/"))

        try:
            script.run()
        except Exception as e:
            print(e)
            
        # Add the scene to the current project
        scene = { "path": outputHoudiniFilePath }
        origin.createSceneFromPreset(scene)

        # Delete the scene
        os.remove(outputHoudiniFilePath)