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



        # Crées le chemin ou maya vas enregistrer son fichier temporaire.
        # A la fin, on copiras le fichier crée dans Prism sous une nouvelle version.
        filepath = os.path.dirname(__file__)
        outputMayaFilePath = os.path.join(filepath, "output.ma")
        outputMayaFilePath = outputMayaFilePath.replace("\\", "/")

        # Current entity
        current_entity = origin.getCurrentEntity()



        # Ici, on vas recuperer tous les shots de la sequence, 
        # Sauf le master, ni l'entitée courante.
        sequence_data = self.getAllShotsFromCurrentSequence(current_entity, origin, includeMaster=False, excludeCurrent=True)
        shots_in_sequence = sequence_data["shots"]
        total_frames = sequence_data["total_frames"]
        # Display a warning if there is no other shots in the sequence
        if len(shots_in_sequence) == 0:
            QMessageBox.warning(parent, "No Other Shots Found", "There are no other shots in the sequence. The scene cannot be created.")
            return


        # Ici, on vas recuperer le setdress de l'entitée "Current".
        importReference_SetDress = True
        setDress_Files = self.getMatchingProductsFromEntity(origin.getCurrentEntity(), [".usd", ".usda" , ".usdc"], origin, ["SetD", "Publish"])


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
                products = self.getMatchingProductsFromEntity(entity, [".ma" , ".mb"], origin, ["RigL", "Publish"])
                rigs_chars.extend(products)
            # Si c'est un prop
            elif "prop" in entity["asset_path"].lower() :
                products = self.getMatchingProductsFromEntity(entity, [".ma" , ".mb"], origin, ["RigL", "Publish"])
                rigs_props.extend(products)

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
            {
                "setting_name": "import_title",
                "type": "title",
                "default_value": "Globals"
            },
            {
                "setting_name": "Import Camera Rig",
                "type": "checkbox",
                "default_value": True
            },
            {
                "setting_name": "Auto Hide Cameras (Only one visible at a time)",
                "type": "checkbox",
                "default_value": True
            },
            {
                "setting_name": "Create Bookmarks for Shots",
                "type": "checkbox",
                "default_value": True
            }
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



        # Get the settings results
        resultSettings = dialog.getSettings()
        import_camera_rig = resultSettings["Import Camera Rig"]
        create_bookmarks = resultSettings["Create Bookmarks for Shots"]
        auto_hide_cameras = resultSettings["Auto Hide Cameras (Only one visible at a time)"]



        # Get the camera rig path
        project_pipeline_path = origin.core.projects.getResolvedProjectStructurePath("pipeline" , context = {})
        camera_file_path = os.path.join(project_pipeline_path, "Templates" , "camera_template.ma")
        camera_file_path = camera_file_path.replace("\\", "/")
        # Check if the camera file exists
        if not os.path.exists(camera_file_path):
            camera_file_path = ""



        # Create a new product on the current entity named "RLO_Edit_SetD_Publish"
        product = origin.core.products.createProduct(current_entity , "RLO_Edit_SetD_Publish",location="global" )
        version = origin.core.products.ingestProductVersion(files=[], entity=current_entity,product="RLO_Edit_SetD_Publish", location="global")
        print("Created product : " + str(product))
        print("Created version : " + str(version))

        save_path_edit_setD = version["versionPath"]
        save_path_edit_setD = save_path_edit_setD.replace("\\", "/")

        versionInfo = origin.core.getConfig(configPath=version) or {}
        versionInfo["extension"] = ".usda"
        origin.core.setConfig(data=versionInfo, configPath=version)


        save_path_edit_setD = os.path.join(save_path_edit_setD, "RLO_Edit_SetD_Publish.usda")
        save_path_edit_setD = save_path_edit_setD.replace("\\", "/")



        # Prepare the shots list as a string for the script
        shots_in_sequence_str = str(shots_in_sequence)
        shots_in_sequence_str = shots_in_sequence_str.replace("\\", "/")


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
        script.replaceVariable("$$AUTO_HIDE_CAMERAS$$", "True" if auto_hide_cameras else "False")

        script.replaceVariable("$$SET_DRESS_PATH$$", products_setDress_str)
        script.replaceVariable("$$SAVE_PATH_EDIT_SETD$$", save_path_edit_setD)
        script.replaceVariable("$$RIGS_CHARS_PATHS$$", products_rigs_chars_str)
        script.replaceVariable("$$RIGS_PROPS_PATHS$$", products_rigs_props_str)

        script.replaceVariable("$$CREATE_BOOKMARKS$$", "True" if create_bookmarks else "False")

        script.replaceVariable("$$NUMBER_OF_FRAMES$$", str(total_frames))
        script.replaceVariable("$$FIRST_FRAME$$", "1001")

        script.replaceVariable("$$SHOTS$$", shots_in_sequence_str)

        try:
            script.run()
        except Exception as e:
            print(e)


        # Add the scene to the current project
        scene = { "path": outputMayaFilePath }
        origin.createSceneFromPreset(scene)

        # Delete the scene
        os.remove(outputMayaFilePath)
