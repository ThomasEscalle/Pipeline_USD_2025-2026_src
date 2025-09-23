# RigL/Maya

from src.core.FileTemplateBase import FileTemplateBase
from src.core.StandaloneScriptMaya import StandaloneScriptMaya
from src.ui.AskForProductToImport import ProductImportDialog, QDialog
import os

try:
    from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QDialogButtonBox, QMessageBox
except:
    from PySide2.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QDialogButtonBox, QMessageBox



class FileTemplateFLOMaya(FileTemplateBase):

    def __init__(self):
        super().__init__()
        self.template_name = "FLOMaya"
        self.template_software = "Maya"

    def construct(self, parent, path, origin):

        # Les elements a importer pour ce template sont :
        # - Le set dress (.USD)
        # - Les rigs des assets connectés (char et prop) (.ma ou .mb en high)
        # - Soit la caméra du RLO, soit créer une caméra rig
        # - Le temps que prend la séquence (pour créer la timeline), plus son pré-roll et post-roll 
        # - Eventuellement le ghost du RLO (si il y'en a un)


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
        importReference_SetDress = True
        master_entity = self.getCurrentShotMaster(current_entity, origin)
        setDress_Files = self.getMatchingProductsFromEntity(master_entity, [".usd", ".usda" , ".usdc"], origin, ["SetD", "Publish"])


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
        dialog.setHelpLink("https://thomasescalle.github.io/Pipeline_USD_2025/departements/FLO/#comment-creer-une-scene-dans-maya")
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


        # Get the asset type
        assetType = current_entity["type"]
        assetName = current_entity["sequence"] + "_" + current_entity["shot"]
        task = origin.getCurrentTask()
        department = origin.getCurrentDepartment()

        ###################################################################
        ################### CREATE THE SCENE ##############################
        ###################################################################
        script = StandaloneScriptMaya("Stdl_FLO_Maya.py")
        script.replaceVariable("$$OUTPUT_PATH$$", outputMayaFilePath)

        script.replaceVariable("$$SEQUENCE_TYPE$$", assetType)
        script.replaceVariable("$$ASSET_NAME$$", assetName)
        script.replaceVariable("$$TASK$$", task)
        script.replaceVariable("$$DEPARTMENT$$", department)

        script.replaceVariable("$$SHOT_RANGE$$", str(shot_range))
        script.replaceVariable("$$SHOT_LENGTH$$", str(shot_length))
        script.replaceVariable("$$SHOT_PREROLL$$", str(shot_preroll))
        script.replaceVariable("$$SHOT_POSTROLL$$", str(shot_postroll))

        script.replaceVariable("$$CAMERA_RIG_PATH$$", camera_file_path)

        script.replaceVariable("$$SET_DRESS_PATH$$", products_setDress_str)
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


        """
        filepath = os.path.dirname(__file__)
        outputMayaFilePath = os.path.join(filepath, "output.ma")
        outputMayaFilePath = outputMayaFilePath.replace("\\", "/")


        assetType = origin.getCurrentEntity()["type"]
        assetName = origin.getCurrentEntity()["sequence"] + "_" + origin.getCurrentEntity()["shot"]
        sequenceName = origin.getCurrentEntity()["sequence"]

        #################################################
        ### GET THE SET DRESS REFERENCE FILE ############
        #################################################
        setDress_ref_path = self.getMasterPathFromEntity(origin.getCurrentEntity(), ".usda", origin, ["SetD", "Publish"])
        setDress_found = True
        if setDress_ref_path == "":
            setDress_found = False
            QMessageBox.warning(parent, "Reference File Not Found", "No Set Dress reference file found for this shot. Proceeding without reference.")
        

        ##############################################
        # GET THE SHOTS IN THE SAME SEQUENCE  ########
        ##############################################
        ### @Todo Utiliser getShotsFromSequence de projectEntities  

        path = origin.getCurrentEntity()["paths"][0]["path"]
        # Go one level up to get the sequence folder
        sequence_path = os.path.dirname(path)
        # Loop through all the shots and make sure they are not the current shot
        shots = []
        current_shot = origin.getCurrentEntity()["shot"]
        for shot in os.listdir(sequence_path):
            if os.path.isdir(os.path.join(sequence_path, shot)) and shot != current_shot:
                shots.append(shot)
        number_of_shots = len(shots)

        print("Number of shots in the same sequence:", number_of_shots)
        print("Shots in the same sequence:", shots)  # List of shots in the same sequence




        ##################################################
        ## GET THE ASSETS CONNECTED TO THE SHOT ##########
        ###################################################
        connected_entities = origin.core.entities.getConnectedEntities(origin.getCurrentEntity())
        print("Connected entities:", connected_entities)

        # Get the asset path  @todo 
        assets_path = origin.getCurrentEntity()["paths"][0]["path"]
        assets_path = os.path.dirname(assets_path)
        assets_path = os.path.dirname(assets_path)
        assets_path = os.path.dirname(assets_path)
        asset_path = os.path.join(assets_path, "01_Assets")

        # Loop through the connected entities and get their paths
        rig_paths_props = []
        rig_paths_chars = []

        for entity in connected_entities:

            if "char" in entity["asset_path"].lower() or "prop" in entity["asset_path"].lower():
                
                asset_path = os.path.join(asset_path, entity["asset_path"])
                asset_path = asset_path.replace("\\", "/")

                rig_path = os.path.join(asset_path, "Export", "RigL_Publish" , "master" )
                rig_path = rig_path.replace("\\", "/")

                # Check if the rig file exists
                if not os.path.exists(rig_path):
                    parent.console.log(f"Rig file does not exist: {rig_path}")
                    return
                
                # Get the first .ma file in the rig directory
                maFiles = [f for f in os.listdir(rig_path) if f.endswith('.ma')]
                if not maFiles:
                    parent.console.log(f"No .ma files found in the rig directory: {rig_path}")
                    return
                
                rig_path = os.path.join(rig_path, maFiles[0])
                rig_path = rig_path.replace("\\", "/")

                # Check if the rig_path exists
                if not os.path.exists(rig_path):
                    parent.console.log(f"Rig file does not exist: {rig_path}")
                    return
                
                # Check if the rig is a prop or a character
                if "char" in entity["asset_path"].lower():  
                    rig_paths_chars.append(rig_path)
                elif "prop" in entity["asset_path"].lower():
                    rig_paths_props.append(rig_path)

        print("Rig paths for characters:", rig_paths_chars)
        print("Rig paths for props:", rig_paths_props)
        


        ###################################################
        ### CREATE THE SCENE ##############################
        ###################################################
        script = StandaloneScriptMaya("Stdl_FLO_Maya.py")
        script.replaceVariable("$$OUTPUT_PATH$$", outputMayaFilePath)
        script.replaceVariable("$$ASSET_NAME$$", assetName)
        script.replaceVariable("$$RIG_PATHS_PROPS$$", str(rig_paths_props))
        script.replaceVariable("$$RIG_PATHS_CHARS$$", str(rig_paths_chars))
        script.replaceVariable("$$SHOTS$$", str(shots))
        script.replaceVariable("$$SEQUENCE_NAME$$", sequenceName)

        script.replaceVariable("$$SET_DRESS_PATH$$", setDress_ref_path)    # <- If there was some set dress that was found
        script.replaceVariable("$$SET_DRESS_FOUND$$", "True" if setDress_found else "False")

        script.run()


        # Add the scene to the current project
        scene = { "path": outputMayaFilePath }
        origin.createSceneFromPreset(scene)

        """