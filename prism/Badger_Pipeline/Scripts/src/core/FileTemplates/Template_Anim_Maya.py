# RigL/Maya

from src.core.FileTemplateBase import FileTemplateBase
from src.core.StandaloneScriptMaya import StandaloneScriptMaya
from src.ui.AskForProductToImport import ProductImportDialog, QDialog
import os

try:
    from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QDialogButtonBox, QMessageBox
except:
    from PySide2.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QDialogButtonBox, QMessageBox



class FileTemplateAnimMaya(FileTemplateBase):

    def __init__(self):
        super().__init__()
        self.template_name = "AnimMaya"
        self.template_software = "Maya"

    def construct(self, parent, path, origin):

        # Les elements a importer pour ce template sont :
        # - Le set dress (.USD)
        # - Les rigs des assets connectés (char et prop) (.ma ou .mb en high)
        # - Soit la caméra du RLO, soit créer une caméra rig
        # - Le temps que prend la séquence (pour créer la timeline), plus son pré-roll et post-roll 
        # - Eventuellement le ghost du FLO (si il y'en a un)



        # Crées le chemin ou maya vas enregistrer son fichier temporaire.
        # A la fin, on copiras le fichier crée dans Prism sous une nouvelle version.
        filepath = os.path.dirname(__file__)
        outputMayaFilePath = os.path.join(filepath, "output.ma")
        outputMayaFilePath = outputMayaFilePath.replace("\\", "/")

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
        ## 
        # Todo : recuperer le EditSetDress du FLO si il existe, sinon le SetDress.
        ##
        importReference_SetDress = True
        master_entity = self.getCurrentShotMaster(current_entity, origin)

        edit_setDress_Files = self.getMatchingProductsFromEntity(current_entity, [".usd", ".usda" , ".usdc"], origin, ["FLO_Edit_SetD_Publish"], onlyOne=True)
        if len(edit_setDress_Files) > 0 :
            setDress_Files = edit_setDress_Files
        else :
            setDress_Files = self.getMatchingProductsFromEntity(master_entity, [".usd", ".usda" , ".usdc"], origin, ["SetD_Publish"], onlyOne=True)
        

        # On vas récupérer tous les assets connectés a l'entitée courante.
        # [
        #     { "type": "asset", "asset_path": "Chars\\Nathan"   },
        #     { "type": "asset", "asset_path": "Chars\\Mathilde" },
        # ...
        connected_entities = origin.core.entities.getConnectedEntities(origin.getCurrentEntity())
        rigs_chars = []
        rigs_props = []

        # Loop through the connected entities and get their rigs
        for entity in connected_entities:
            # Si c'est un character
            if "char" in entity["asset_path"].lower() :
                products = self.getMatchingProductsFromEntity(entity, [".ma" , ".mb"], origin, ["RigH", "Publish"])
                rigs_chars.extend(products)
            # Si c'est un prop
            elif "prop" in entity["asset_path"].lower() :
                products = self.getMatchingProductsFromEntity(entity, [".ma" , ".mb"], origin, ["RigH", "Publish"])
                rigs_props.extend(products)
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
                "name" : "Rigs (Characters)",
                "settings" : {
                    "accepted_files" : [
                        "ma", "mb"
                    ]
                },
                "items" : rigs_chars
            },
            {
                "type" : "folder",
                "name" : "Rigs (Props)",
                "settings" : {
                    "accepted_files" : [
                        "ma",
                    ]
                },
                "items" : rigs_props
            },
        ]
        settings = [
        ]

        # Set the default selected product
        dialog.setDefaultSelectedProduct(default_selected)
        
        # Set the settings configuration
        dialog.setSettings(settings)

        dialog.navigate(origin.getCurrentEntity())
        dialog.setHelpLink("https://thomasescalle.github.io/Pipeline_USD_2025/departements/Anim/#comment-creer-une-scene-dans-maya")
        dialog.setWindowTitle("Import Settings")
        result = dialog.exec_()

        # On annule si jamais l'utilisateur a demandé annulé sur le dialogue.
        if result != QDialog.Accepted:
            return
        

        # Get the items results
        items = dialog.getResult()
        items_setDress = items.get("Set Dress", [])
        items_rigs_chars = items.get("Rigs (Characters)", [])
        items_rigs_props = items.get("Rigs (Props)", [])

        # On recupere les products associés aux items
        products_setDress = self.getPreferedFilePathsFromProductList(items_setDress, origin)
        products_rigs_chars = self.getPreferedFilePathsFromProductList(items_rigs_chars, origin)
        products_rigs_props = self.getPreferedFilePathsFromProductList(items_rigs_props, origin)

        # Si il y'a plus d'un set dress, on prend que le premier.
        if len(products_setDress) > 1 :
            products_setDress = [products_setDress[0]]

        products_setDress_str = str(products_setDress)
        products_rigs_chars_str = str(products_rigs_chars)
        products_rigs_props_str = str(products_rigs_props)


        # Get the camera rig path
        project_pipeline_path = origin.core.projects.getResolvedProjectStructurePath("pipeline" , context = {})
        camera_file_path = os.path.join(project_pipeline_path, "Templates" , "camera_template.ma")
        camera_file_path = camera_file_path.replace("\\", "/")
        # Check if the camera file exists
        if not os.path.exists(camera_file_path):
            camera_file_path = ""


        # Get the settings results from the dialog
        settings = dialog.getSettings()
        create_bookmarks = True



        # Prepare the path for the EditSetDress.usda
        ###############################################################   
        ###############################################################

        # Create a new product on the current entity named "Anim_Edit_SetD_Publish"
        product = origin.core.products.createProduct(current_entity , "Anim_Edit_SetD_Publish",location="global" )
        version = origin.core.products.ingestProductVersion(files=[], entity=current_entity,product="Anim_Edit_SetD_Publish", location="global")
        print("Created product : " + str(product))
        print("Created version : " + str(version))

        save_path_edit_setD = version["versionPath"]
        save_path_edit_setD = save_path_edit_setD.replace("\\", "/")

        versionInfo = origin.core.getConfig(configPath=save_path_edit_setD+ "/versioninfo.json") or {}
        versionInfo["extension"] = ".usda"
        origin.core.setConfig(data=versionInfo, configPath=save_path_edit_setD+ "/versioninfo.json")

        save_path_edit_setD = os.path.join(save_path_edit_setD, "Anim_Edit_SetD_Publish.usda")
        save_path_edit_setD = save_path_edit_setD.replace("\\", "/")

        ###############################################################
        ###############################################################



        # Get the asset type
        assetType = origin.getCurrentEntity()["type"]
        assetName = origin.getCurrentEntity()["sequence"] + "_" + origin.getCurrentEntity()["shot"]
        task = origin.getCurrentTask()
        department = origin.getCurrentDepartment()
        shot_str = str(current_entity)
        shot_str = shot_str.replace("\\", "/")
        shot_str = shot_str.replace("\\\\", "/")

        ###################################################################
        ################### CREATE THE SCENE ##############################
        ###################################################################
        script = StandaloneScriptMaya("Stdl_Anim_Maya.py")
        script.replaceVariable("$$OUTPUT_PATH$$", outputMayaFilePath)

        script.replaceVariable("$$SEQUENCE_TYPE$$", assetType)
        script.replaceVariable("$$ASSET_NAME$$", assetName)
        script.replaceVariable("$$TASK$$", task)
        script.replaceVariable("$$DEPARTMENT$$", department)

        script.replaceVariable("$$SHOT$$", shot_str)   # Infos about the current shot, as string dictionary

        script.replaceVariable("$$SHOT_RANGE$$", str(shot_range))
        script.replaceVariable("$$SHOT_LENGTH$$", str(shot_length))
        script.replaceVariable("$$SHOT_PREROLL$$", str(shot_preroll))
        script.replaceVariable("$$SHOT_POSTROLL$$", str(shot_postroll))

        script.replaceVariable("$$CAMERA_RIG_PATH$$", camera_file_path)
        script.replaceVariable("$$IMPORT_CAMERA_FROM_FLO$$", "False")

        script.replaceVariable("$$SET_DRESS_PATH$$", products_setDress_str)
        script.replaceVariable("$$SAVE_PATH_EDIT_SETD$$", save_path_edit_setD)
        script.replaceVariable("$$RIGS_CHARS_PATHS$$", products_rigs_chars_str)
        script.replaceVariable("$$RIGS_PROPS_PATHS$$", products_rigs_props_str)

        script.replaceVariable("$$CREATE_BOOKMARKS$$", "True" if create_bookmarks else "False")

    
        try:
            script.run()
        except Exception as e:
            print(e)


        # Add the scene to the current project
        scene = { "path": outputMayaFilePath }
        origin.createSceneFromPreset(scene)

        # Delete the scene
        os.remove(outputMayaFilePath)