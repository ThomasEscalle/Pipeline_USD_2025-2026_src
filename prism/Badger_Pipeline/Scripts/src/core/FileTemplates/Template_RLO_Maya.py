# RigL/Maya

from src.core.FileTemplateBase import FileTemplateBase
from src.core.StandaloneScriptMaya import StandaloneScriptMaya
from src.ui.AskForProductToImport import ProductImportDialog, QDialog
import os

try:
    from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QDialogButtonBox, QMessageBox
except:
    from PySide2.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QDialogButtonBox, QMessageBox



class FileTemplateRLOMaya(FileTemplateBase):

    def __init__(self):
        super().__init__()
        self.template_name = "RLOMaya"
        self.template_software = "Maya"

    def construct(self, parent, path, origin):

        # Les elements a importer pour ce template sont :
        # - Le set dress (.USD)
        # - Les rigs des assets connectés (char et prop) (.ma)
        # - Le nombre d'autres shots dans la séquence (pour créer les cameras)
        # - Le temps que prend la séquence (pour créer la timeline)


        # Current entity
        current_entity = origin.getCurrentEntity()

        # Ici, on vas recuperer tous les shots de la sequence.
        all_shots_in_sequence = origin.core.entities.getShotsFromSequence(current_entity["sequence"])
        shots_in_sequence = []
        for shot in all_shots_in_sequence:
            # If the shot is not "Master", we add it to the list
            if shot["shot"].lower() != "master" and shot != current_entity:
                shots_in_sequence.append(shot)

        # Warn the user if no other shots were found in the sequence
        if len(shots_in_sequence) == 0:
            QMessageBox.warning(parent, "No Shots Found", "No other shots found in the same sequence. Please make sure there are other shots in the sequence.")
            return
        
        # Store the total frames of the sequence
        total_frames = 0

        # Get the range and length of each shot and add it to the shot dict
        for shot in shots_in_sequence:
            range = origin.core.entities.getShotRange(shot)
            shot["range"] = range

            length = range[1] - range[0] + 1
            shot["length"] = length
            total_frames += length

            metadata = origin.core.entities.getMetaData(shot)
            shot["metadata"] = metadata


        print("Shots in the same sequence:", shots_in_sequence)  # List of shots in the same sequence


        # Crées le chemin ou maya vas enregistrer son fichier.
        # A la fin, on copiras le fichier crée dans Prism sous une nouvelle version.
        filepath = os.path.dirname(__file__)
        outputMayaFilePath = os.path.join(filepath, "output.ma")
        outputMayaFilePath = outputMayaFilePath.replace("\\", "/")


        # Ici, on vas recuperer le setdress de l'entitée "Current".
        importReference_SetDress = True
        setDress_Files = self.getMatchingProductsFromEntity(origin.getCurrentEntity(), [".usd", ".usda" , ".usdc"], origin, ["SetD", "Publish"])




        # Demande a l'utilisateur quel produits a eventuelement importer, ainsi que les settings
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
                "name" : "Rigs",
                "settings" : {
                    "accepted_files" : [
                        "ma",
                    ]
                },
                # "items" : rig_paths_chars + rig_paths_props,
            }
        ]
        settings = [

        ]

        # Set the default selected product
        dialog.setDefaultSelectedProduct(default_selected)
        
        # Set the settings configuration
        dialog.setSettings(settings)

        dialog.navigate(origin.getCurrentEntity())
        dialog.setHelpLink("https://thomasescalle.github.io/Pipeline_USD_2025/departements/RLO/#comment-creer-une-scene-dans-maya")
        dialog.setWindowTitle("Import Settings")
        result = dialog.exec_()

        # On annule si jamais l'utilisateur a demandé annulé sur le dialogue.
        if result != QDialog.Accepted:
            return


        # Get the camera rig path
        project_pipeline_path = origin.core.projects.getResolvedProjectStructurePath("pipeline" , context = {})
        camera_file_path = os.path.join(project_pipeline_path, "Templates" , "camera_template.ma")
        camera_file_path = camera_file_path.replace("\\", "/")
        # Check if the camera file exists
        if not os.path.exists(camera_file_path):
            camera_file_path = ""

        # Get the asset type
        assetType = origin.getCurrentEntity()["type"]
        assetName = origin.getCurrentEntity()["sequence"] + "_" + origin.getCurrentEntity()["shot"]
        task = origin.getCurrentTask()
        department = origin.getCurrentDepartment()

        ###################################################################
        ################### CREATE THE SCENE ##############################
        ###################################################################
        script = StandaloneScriptMaya("Stdl_RLO_Maya.py")
        script.replaceVariable("$$OUTPUT_PATH$$", outputMayaFilePath)

        script.replaceVariable("$$SEQUENCE_TYPE$$", assetType)
        script.replaceVariable("$$ASSET_NAME$$", assetName)
        script.replaceVariable("$$TASK$$", task)
        script.replaceVariable("$$DEPARTMENT$$", department)

        script.replaceVariable("$$CAMERA_RIG_PATH$$", camera_file_path)
        script.replaceVariable("$$IMPORT_CAMERA_RIG$$", "True" if camera_file_path != "" else "False")

        script.replaceVariable("$$NUMBER_OF_FRAMES$$", str(total_frames))
        script.replaceVariable("$$FIRST_FRAME$$", "1001")

        script.replaceVariable("$$SHOTS$$", str(shots_in_sequence))

        script.run()


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
        script = StandaloneScriptMaya("Stdl_RLO_Maya.py")
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