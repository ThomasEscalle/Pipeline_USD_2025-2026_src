#   ______           _                  ______ _            _ _            
#   | ___ \         | |                 | ___ (_)          | (_)           
#   | |_/ / __ _  __| | __ _  ___ _ __  | |_/ /_ _ __   ___| |_ _ __   ___ 
#   | ___ \/ _` |/ _` |/ _` |/ _ \ '__| |  __/| | '_ \ / _ \ | | '_ \ / _ \
#   | |_/ / (_| | (_| | (_| |  __/ |    | |   | | |_) |  __/ | | | | |  __/
#   \____/ \__,_|\__,_|\__, |\___|_|    \_|   |_| .__/ \___|_|_|_| |_|\___|
#                       __/ |                   | |                        
#                      |___/                    |_|                        
#
# @file Badger Pipeline Functions
# @brief This file contains the entry functions for the Badger Pipeline plugin for Prism.


from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

import requests
import json
import os
import sys
import tempfile

from PrismUtils.Decorators import err_catcher_plugin as err_catcher

from src.ui.USD_View import USD_View
from src.ui.ConsoleDialog import ConsoleDialog
from src.ui.CreateProduct import CreateProductDialog

from src.core.USD_utils import USDUtils
from src.core.FileTemplateManager import FileTemplateManager

from src.ui.WidgetLinker import LinksWidget




class Prism_Badger_Pipeline_Functions(object):


    def __init__(self, core, plugin):
        self.core = core
        self.version = "v1.0.0"

        self.usdView = None

        # Register the callbacks

        # This function is called when prism UI is started
        self.core.registerCallback("onProjectBrowserStartup", self.onProjectBrowserStartup, plugin=self)

        # This function is called when an asset was just created
        self.core.registerCallback("onAssetCreated", self.onAssetCreated, plugin=self)

        # This function is called when a shot was just created
        self.core.registerCallback("onShotCreated", self.onShotCreated, plugin=self)

        # This function is called when the user wants to create a new template
        self.core.registerCallback("openPBFileContextMenu", self.onOpenPBFileContextMenu, plugin=self)

        # This function is called when a master gets updated
        self.core.registerCallback("masterVersionUpdated", self.onMasterUpdated, plugin=self)

        # This function is called when the user wants to create a new product
        self.core.registerCallback("openPBAssetContextMenu", self.onOpenPBAssetContextMenu, plugin=self)





        # Register the project structure items

        # Create a new entry in the project structure for the USD path
        usdPath_data = {"label": "USD Path", "key": "@usd_path@", "value": "@project_path@/05_USD", "requires": []}
        self.core.projects.addProjectStructureItem("usd_path", usdPath_data)

        # Create a new entry in the project structure for the USD Assets path
        usdAssets_data = {"label": "USD Assets", "key": "@usd_assets@", "value": "@usd_path@/01_Assets", "requires": []}
        self.core.projects.addProjectStructureItem("usd_assets", usdAssets_data)

        # Create a new entry in the project structure for the USD Shots path
        usdShots_data = {"label": "USD Shots", "key": "@usd_shots@", "value": "@usd_path@/02_Shots", "requires": []}
        self.core.projects.addProjectStructureItem("usd_shots", usdShots_data)




        sys.path.append("D:/Houdini 20.5.370/python311/lib/site-packages")


        # Monkey patch the setEntityPreview function to paste the asset preview in the USD folder when it is updated
        self.core.plugins.monkeyPatch(self.core.entities.setEntityPreview, self.setEntityPreview, self, force=True)


        os.environ["PATH"] += os.pathsep + "C:/Users/Thomas/OneDrive/Documents/Prism_Pluggins/USD_modules_v2.0.10/USD/ExternalModules/USD/bin"
        os.environ["PATH"] += os.pathsep + "C:/Users/Thomas/OneDrive/Documents/Prism_Pluggins/USD_modules_v2.0.10/USD/ExternalModules/USD/lib"
        os.environ["PYTHONPATH"] = "C:/Users/Thomas/OneDrive/Documents/Prism_Pluggins/USD_modules_v2.0.10/USD/ExternalModules/USD/lib/python"

        sys.path.append("C:/Users/Thomas/OneDrive/Documents/Prism_Pluggins/USD_modules_v2.0.10/USD/ExternalModules")
        sys.path.insert(0, "C:/Users/Thomas/OneDrive/Documents/Prism_Pluggins/USD_modules_v2.0.10/USD/ExternalModules/USD/lib/python")
        

    # region Callbacks



    # This function is called when the entity preview is set
    def setEntityPreview(self, *args, **kwargs):
        # Call the original function
        returnValue = self.core.plugins.callUnpatchedFunction(self.core.entities.setEntityPreview, *args, **kwargs)
        
        # Get the entity from the args
        entity = args[0] if len(args) > 0 else None

        if entity is None:
            self.console.log("No entity provided to setEntityPreview")
            return returnValue

        if entity["type"] == "asset":
            # If the entity is an asset, we want to set the preview to the USD filea
            usd_assetPath = self.core.projects.getResolvedProjectStructurePath("usd_assets")
            assetPath = entity["asset_path"].replace("\\", "/")  # Ensure the path is in the correct format
            path = os.path.join(usd_assetPath, assetPath)
            path = path.replace("\\", "/")  # Ensure the path is in the correct format
            print ("ENTITY " + str(entity))

            image_path = entity["preview"]

            # Check if the folder exists
            if not os.path.exists(path):
                self.console.log("Asset path does not exist: %s" % path)
                return returnValue
            
            # Copy the preview image to the asset folder
            finalImagePath = os.path.join(path, "thumbnail.png")
            finalImagePath = finalImagePath.replace("\\", "/")  # Ensure the path is in the correct format
            with open(finalImagePath, "wb") as f:
                with open(image_path, "rb") as img_f:
                    f.write(img_f.read())

            self.console.log("The entity preview for asset %s has been set to %s" % (entity["asset"], finalImagePath))

            pass

        elif entity["type"] == "shot":
            # The entity is a shot
            # @todo
            pass

        return returnValue


    def onOpenPBAssetContextMenu(self, origin, rcMenu, asset):
        # Asset is a PySide6.QtCore.QModelIndex
        # Get the item
        item = asset.data(Qt.UserRole)
        if item is None:
            return
        print("Item: %s" % item)

        # {'asset': 'Round_Lichen', 'asset_path': 'Items\\Round_Lichen', 'paths': ['E:\\3D\\Projects\\06_Ouyang\\03_Production\\01_Assets\\Items\\Round_Lichen'], 'type': 'asset'}
        # Check if the item is an asset
        if item["type"] != "asset":
            return
        
        # Create an action named "Open in USD View" and add it to the context menu
        openInUSDViewAction = QAction(self.getIcon("usd.png"), "Open in USD View", origin)
        openInUSDViewAction.setToolTip("Open the asset in the USD View")
        openInUSDViewAction.triggered.connect(lambda: print("Open in USD View clicked for asset: %s" % item["asset"]))
        rcMenu.addAction(openInUSDViewAction)
        
        # Create an action named "Variants connection"
        variantsConnectionAction = QAction(self.getIcon("variant.png"), "Variants connection", origin)
        variantsConnectionAction.setToolTip("Connect the asset to the variants")
        variantsConnectionAction.triggered.connect(lambda: self.openVariantsConnection(item))
        rcMenu.addAction(variantsConnectionAction)


    def openVariantsConnection(self, item):
        print("Open variants connection for asset: %s" % item["asset"])

        widget = LinksWidget(self.projectBrowser)
        widget.setWindowTitle("Variants Connection for %s" % item["asset"])
        widget.resize(600, 400)

        #Set the stylesheet of the widget to the current stylesheet of the project browser
        widget.setStyleSheet(self.projectBrowser.styleSheet())

        # @TODO : Build the widget with the already existing connections
        widget.add_column('left', 'Variations', [
            ("g1", "Variation 01"),
            ("g2", "Variation 02"),
            ("g3", "Variation 03"),
            ("g4", "Variation 04"),
        ])
        widget.add_column('right', 'Materiaux', [
            ("t1", "Mat 01"),
            ("t2", "Mat 02"),
            ("t3", "Mat 03"),
            ("t4", "Mat 04"),
        ])
        widget.add_column('right', 'Geometries', [
            ("g1", "Geo 01"),
            ("g2", "Geo 02"),
            ("g3", "Geo 03"),
            ("g4", "Geo 04"),
        ])
        # Exemple de pré-remplissage de connexions
        widget.add_connections([
            {
                "from": {"column": "Variations", "slot_id": "g1"},
                "to":   {"column": "Materiaux", "slot_id": "t1"}
            },
            {
                "from": {"column": "Variations", "slot_id": "g1"},
                "to":   {"column": "Geometries", "slot_id": "g1"}
            }
        ])
        result = widget.exec_()
        if result == QDialog.Accepted:
            # Get the connections
            connections = widget.get_result_json()

            print("Connections: %s" % connections)

            # @TODO : Save the connections to a file or do something with them
        else :
            print("Dialog cancelled, no connections made.")



    # This function is called when an asset was just created
    def onAssetCreated(self, origin, entity, dlg):
        ## Asset created: {'type': 'asset', 'asset_path': 'Chars/zqdqz', 'asset': 'zqdqz', 'project_path': 'E:\\3D\\PIPELINE\\USD_Uptight_2025_v001\\00_Template\\Uptight', 'project_name': 'Uptight'}
        self.console.log("Asset created: %s" % entity)

        ## Create an asset in the USD folder.
        path = self.core.projects.getResolvedProjectStructurePath("usd_assets")
        self.console.log("Resolved path: %s" % path)

        assetPath = os.path.join(path, entity["asset_path"])
        self.console.log("Asset path: %s" % assetPath)

        # Create the asset folder
        if not os.path.exists(assetPath):
            os.makedirs(assetPath)
            self.console.log("Created asset folder: %s" % assetPath)
        else:
            self.console.log("Asset folder already exists: %s" % assetPath)

        # Check if the asset path contains the "Modules" folder
        utils = USDUtils()
        asset_path = entity["asset_path"]
        asset_path = asset_path.replace("\\", "/")  # Ensure the path is in the correct format

        # If the asset is a module
        if "Modules/" in asset_path:
            # Create the module USD file
            utils.createUsdModule(entity, assetPath, self)
        else:
            # Create the asset USD file
            utils.createUsdAsset(entity, assetPath, self)




        
    def onShotCreated(self, origin, entity):
        ## {'type': 'shot', 'sequence': 'sq_010', 'shot': 'sh_040', 'project_path': 'E:\\3D\\PIPELINE\\USD_Uptight_2025_v001\\00_Template\\Uptight', 'project_name': 'Uptight'}
        self.console.log("Shot created: %s" % entity)

        ## Create a shot in the USD folder.
        path = self.core.projects.getResolvedProjectStructurePath("usd_shots")
        self.console.log("Resolved path: %s" % path)

        shotPath = os.path.join(path, entity["sequence"], entity["shot"])
        self.console.log("Shot path: %s" % shotPath)

        # Create the shot folder
        if not os.path.exists(shotPath):
            os.makedirs(shotPath)
            self.console.log("Created shot folder: %s" % shotPath)

        # Create the placeholder USD file (for now just an empty file)
        usdFile = os.path.join(shotPath, "%s.usda" % entity["shot"])
        self.createPlaceholderUSD(usdFile)


    # This function is called when prism UI is started
    def onProjectBrowserStartup(self, origin):

        self.console = ConsoleDialog(origin)
        self.createProductDialog = CreateProductDialog(origin, self.core)
        # self.console.show()
        self.projectBrowser = origin

        origin.mainMenu = QMenu("Uptight")

        # Add the Create Product action
        createProductAction = QAction(self.getIcon("download.png"), "Create Product", origin)
        createProductAction.triggered.connect(self.createProductDialog.show)
        createProductAction.setShortcut(QKeySequence("P"))
        origin.mainMenu.addAction(createProductAction)


        # Add the Show console action
        showConsoleAction = QAction(self.getIcon("console.png"), "Show Console", origin)
        showConsoleAction.triggered.connect(self.console.show)
        showConsoleAction.setShortcut(QKeySequence("Shift+C"))
        origin.mainMenu.addAction(showConsoleAction)

        # Create a help action
        helpAction = QAction(self.getIcon("help.png"), "Help", origin)
        helpAction.triggered.connect(self.onActionHelp)
        helpAction.setShortcut(QKeySequence("Ctrl+,"))
        origin.mainMenu.addAction(helpAction)

        origin.menubar.addMenu(origin.mainMenu)


        self.productBrowser = origin.productBrowser

        self.usdView = USD_View(origin, self)
        origin.addTab("USD", self.usdView)

        # Monkeypath the updateIdentifiers function of the product browser
        self.productBrowserUpdateIdentifiers()

        self.productBrowser.tw_versions.itemDoubleClicked.connect(self.productOnVersionDoubleClicked)


        from src.ui.ProductViewer import ProductViewer
        self.productViewer = ProductViewer(self.productBrowser)
        splitter = self.productBrowser.findChild(QSplitter, "splitter1")
        splitter.addWidget(self.productViewer)

        self.productViewer.setFileStage("C:/Users/Thomas/OneDrive/Documents/Prism_Pluggins/HelloWorld.usda")



    def productOnVersionDoubleClicked(self):
        print("Current product version changed")
        
        # Get the current item
        currentItem = self.productBrowser.tw_versions.currentItem()
        if currentItem is None:
            self.console.log("No current item selected in the product browser")
            return

        currentVersion = self.productBrowser.getCurrentVersion()

        if currentVersion is None:
            self.console.log("No current version found in the product browser")
            return
        

        # Set the USD file in the product viewer
        path = currentVersion.get("path")

        if path is None or not os.path.exists(path):
            self.console.log("No path found for the current version")
            return
        

        # Get all the .usd, .usda, .usdc files or .abc files in the path
        usdFiles = [f for f in os.listdir(path) if f.endswith(('.usd', '.usda', '.usdc', '.abc'))]

        if usdFiles:
            # Set the first USD file found in the product viewer
            usdFilePath = os.path.join(path, usdFiles[0])

            usdFilePath = usdFilePath.replace("\\", "/")  # Ensure the path is in the correct format

            # self.productViewer.setFileStage(usdFilePath)
            self.console.log("Set USD file in product viewer: %s" % usdFilePath)


        else:
            self.console.log("No USD files found in path: %s" % path)

        # self.productViewer.setFileStage(usdFilePath)


    def productBrowserUpdateIdentifiers(self, *args, **kwargs):

        returnValue = self.core.plugins.callUnpatchedFunction(self.productBrowser.updateIdentifiers, *args, **kwargs)

        print("Product Browser Update Identifiers called")

        # Check if there is a product browser
        if self.productBrowser is None:
            self.console.log("No product browser found, skipping updateIdentifiers")
            return returnValue


        ### Update the icons of the "tw_identifier" tree Widget from the productBrowser class
        # Get the tree widget from the product browser
        tw_identifier = self.productBrowser.tw_identifier

        if tw_identifier is None:
            self.console.log("No tw_identifier found in the product browser, skipping updateIdentifiers")
            return returnValue

        # Get all the items in the tree widget
        items = tw_identifier.findItems("", Qt.MatchContains | Qt.MatchRecursive)
        if items is None:
            self.console.log("No items found in the tw_identifier tree widget, skipping updateIdentifiers")
            return returnValue

        for item in items:
            # Get the text of the item
            text = item.text(0)
            # If the item to lower contains "Publish"
            if "publish" in text.lower():
                # Set the icon of the item to the publish icon
                item.setIcon(0, self.getIcon("publish.png"))
            else:
                item.setIcon(0, self.getIcon("other.png"))

        return returnValue
        

        

    def onOpenPBFileContextMenu(self, origin, rcMenu, filePath):

        # Add a menu to the rcMenu 'Create Template'
        createTemplateMenu = QMenu("Create Template")
        createTemplateMenu.setIcon(self.getIcon("add.png"))
        createTemplateMenu.setToolTip("Create a template from this file")
        # Make the createTemplateButton the first action in the menu
        rcMenu.insertMenu(rcMenu.actions()[0], createTemplateMenu)

        # Add an action to the menu for creating a Maya template
        mayaAction = QAction(self.getIcon("maya.png"), "Auto Maya", createTemplateMenu)
        mayaAction.triggered.connect(lambda: self.onCreateMayaTemplate(filePath, origin))
        createTemplateMenu.addAction(mayaAction)

        # Add an action to the menu for creating a Houdini template
        houdiniAction = QAction(self.getIcon("houdini.png"), "Auto Houdini", createTemplateMenu)
        houdiniAction.triggered.connect(lambda: self.onCreateHoudiniTemplate(filePath, origin))
        createTemplateMenu.addAction(houdiniAction)

        # Add an action to the menu for creating a Substance template
        substanceAction = QAction(self.getIcon("substance.png"), "Auto Substance", createTemplateMenu)
        substanceAction.triggered.connect(lambda: self.onCreateSubstanceTemplate(filePath, origin))
        createTemplateMenu.addAction(substanceAction)


        # Add a separator
        createTemplateMenu.addSeparator()


        # Modeling Low
        modelingLowMenu = createTemplateMenu.addMenu("Modeling")

        modelingLow_MayaAction = QAction(self.getIcon("maya.png"), "Maya - Low", modelingLowMenu)
        modelingLow_MayaAction.triggered.connect(lambda: self.createTemplate("ModL/Maya", origin))
        modelingLowMenu.addAction(modelingLow_MayaAction)
        modelingLow_HoudiniAction = QAction(self.getIcon("houdini.png"), "Houdini - Low", modelingLowMenu)
        modelingLow_HoudiniAction.triggered.connect(lambda: self.createTemplate("ModL/Houdini", origin))
        modelingLowMenu.addAction(modelingLow_HoudiniAction)
        
        modelingLowMenu.addSeparator()

        modelingHigh_MayaAction = QAction(self.getIcon("maya.png"), "Maya - High", modelingLowMenu)
        modelingHigh_MayaAction.triggered.connect(lambda: self.createTemplate("ModH/Maya", origin))
        modelingLowMenu.addAction(modelingHigh_MayaAction)
        modelingHigh_HoudiniAction = QAction(self.getIcon("houdini.png"), "Houdini - High", modelingLowMenu)
        modelingHigh_HoudiniAction.triggered.connect(lambda: self.createTemplate("ModH/Houdini", origin))
        modelingLowMenu.addAction(modelingHigh_HoudiniAction)

        # Rigging Low   
        riggingLowMenu = createTemplateMenu.addMenu("Rigging")
        riggingLow_MayaAction = QAction(self.getIcon("maya.png"), "Maya - Low", riggingLowMenu)
        riggingLow_MayaAction.triggered.connect(lambda: self.createTemplate("RigL/Maya", origin))
        riggingLowMenu.addAction(riggingLow_MayaAction)
        riggingLowMenu.addSeparator()
        riggingHigh_MayaAction = QAction(self.getIcon("maya.png"), "Maya - High", riggingLowMenu)
        riggingHigh_MayaAction.triggered.connect(lambda: self.createTemplate("RigH/Maya", origin))
        riggingLowMenu.addAction(riggingHigh_MayaAction)

        # Lookdev
        lookdevMenu = createTemplateMenu.addMenu("Lookdev")
        lookdev_SubstanceAction = QAction(self.getIcon("substance.png"), "Substance", lookdevMenu)
        lookdev_SubstanceAction.triggered.connect(lambda: self.createTemplate("Surf/Substance", origin))
        lookdevMenu.addAction(lookdev_SubstanceAction)
        lookdev_houdiniAction = QAction(self.getIcon("houdini.png"), "Houdini", lookdevMenu)
        lookdev_houdiniAction.triggered.connect(lambda: self.createTemplate("Surf/Houdini", origin))
        lookdevMenu.addAction(lookdev_houdiniAction)

        # Modules
        modulesMenu = createTemplateMenu.addMenu("Modules")
        modules_MayaAction = QAction(self.getIcon("houdini.png"), "Houdini", modulesMenu)
        modules_MayaAction.triggered.connect(lambda: self.createTemplate("Mod/Houdini", origin))
        modulesMenu.addAction(modules_MayaAction)

        # SetDressing
        setDressingMenu = createTemplateMenu.addMenu("Set Dress")
        setDressing_HoudiniAction = QAction(self.getIcon("houdini.png"), "Houdini", setDressingMenu)
        setDressing_HoudiniAction.triggered.connect(lambda: self.createTemplate("SetD/Houdini", origin))
        setDressingMenu.addAction(setDressing_HoudiniAction)

        # RLO
        animationMenu = createTemplateMenu.addMenu("Animation")

        rlo_MayaAction = QAction(self.getIcon("maya.png"), "Maya - RLO", animationMenu)
        rlo_MayaAction.triggered.connect(lambda: self.createTemplate("rlo/Maya", origin))
        animationMenu.addAction(rlo_MayaAction)
        animationMenu.addSeparator()
        # FLO
        flo_MayaAction = QAction(self.getIcon("maya.png"), "Maya - FLO", animationMenu)
        flo_MayaAction.triggered.connect(lambda: self.createTemplate("flo/Maya", origin))
        animationMenu.addAction(flo_MayaAction)
        animationMenu.addSeparator()

        # Animation
        animation_MayaAction = QAction(self.getIcon("maya.png"), "Maya - Anim", animationMenu)
        animation_MayaAction.triggered.connect(lambda: self.createTemplate("Anim/Maya", origin))
        animationMenu.addAction(animation_MayaAction)



        # Assembly  
        assemblyMenu = createTemplateMenu.addMenu("Assembly")
        assembly_MayaAction = QAction(self.getIcon("houdini.png"), "Houdini", assemblyMenu)
        assembly_MayaAction.triggered.connect(lambda: self.createTemplate("abl/Houdini", origin))
        assemblyMenu.addAction(assembly_MayaAction)

        # Lighting
        lightingMenu = createTemplateMenu.addMenu("Lighting")
        masterLighting_HoudiniAction = QAction(self.getIcon("houdini.png"), "Houdini - Master", lightingMenu)
        masterLighting_HoudiniAction.triggered.connect(lambda: self.createTemplate("MLgt/Houdini", origin))
        lightingMenu.addAction(masterLighting_HoudiniAction)
        lighting_MayaAction = QAction(self.getIcon("houdini.png"), "Houdini - Lighting", lightingMenu)
        lighting_MayaAction.triggered.connect(lambda: self.createTemplate("lgt/Houdini", origin))
        lightingMenu.addAction(lighting_MayaAction)

        # TLO
        tloMenu = createTemplateMenu.addMenu("TLO")
        tlo_HoudiniAction = QAction(self.getIcon("houdini.png"), "Houdini", tloMenu)
        tlo_HoudiniAction.triggered.connect(lambda: self.createTemplate("tlo/Houdini", origin))
        tloMenu.addAction(tlo_HoudiniAction)


        self.console.log("Right click on file: %s" % filePath)



    def copyFile(self, source, target):
        content = None
        # Copy the file
        with open(source, "rb") as f:
            content = f.read()
        with open(target, "wb") as f:
            f.write(content)

        self.console.log("Copied file: %s to %s" % (source, target))



    def onMasterUpdated(self, path):
        self.console.log("Master updated: %s" % path)
        path = path.replace("\\", "/")
        splitedPath = path.split("/")

        # We want to update the abc in the USD folder
        usdPath = self.core.projects.getResolvedProjectStructurePath("usd_assets")

        # Master updated: E:\3D\PIPELINE\USD_Uptight_2025_v001\00_Template\Uptight\03_Production\01_Assets\Items\Trombone\Export\Modeling_Low\master\Trombone_Modeling_Low_master.abc
        # Check if the master is in "Modeling_Low" folder

        # Name of the export
        name = splitedPath[-3]

        if "Publish" not in name:
            self.console.log("The Master you are trying to publish is not a Publish")
            return
        
        # Check if the updated master is an asset or a shot
        if "01_Assets" in path:

            # Remove everything before "01_Assets" and everything after "Export" 
            assetPath = path.split("01_Assets/")[1]
            assetPath = assetPath.split("/Export")[0]

            variation = name.split("_")[-1]

            return

        if "02_Shots" in path:
            return

        
        """
        # If the updated file is a ModL, we want to copy it to the USD folder
        if "ModL" in name:
            # Create the new path
            targetPath = os.path.join(usdPath, assetPath,"geo" )
            if not os.path.exists(targetPath):
                os.makedirs(targetPath)
            targetPath = os.path.join(targetPath ,"geo_low_" + variation + ".abc")

            # Copy the file to the usd folder
            self.copyFile(path, targetPath)

        # If the updated file is a ModH, we want to copy it to the USD folder
        elif "ModH" in name:
            # Create the new path
            targetPath = os.path.join(usdPath, assetPath,"geo" )
            if not os.path.exists(targetPath):
                os.makedirs(targetPath)
            targetPath = os.path.join(targetPath ,"geo_high_" + variation + ".abc")

            # Copy the file to the usd folder
            self.copyFile(path, targetPath)
        """


    #endregion Callbacks





    def getIcon(self, iconName):
        folder = os.path.dirname(__file__)
        return QIcon(os.path.join(folder, "rc", "Icons", iconName))


    #region Helper functions

    # Create a placeholder USD file (for now just an empty file)
    def createPlaceholderUSD(self, path):
        # Create the placeholder USD file (for now just an empty file)
        if not os.path.exists(path):
            with open(path, "w") as f:
                f.write("#usda 1.0\n")
                f.write("def Xform \"\" {\n")
                f.write("}\n")
            self.console.log("Created USD file: %s" % path)
        else:
            self.console.log("USD file already exists: %s" % path)


    # Open the given URL in the default web browser
    def openUrl(self, urle):
        url = QUrl(urle)
        # Open the URL in the default web browser
        if not url.isValid():
            self.core.popup("Invalid URL")
            return
        QDesktopServices.openUrl(url)

    #endregion Helper functions

    #region Actions

    # Open the help page in the default web browser
    def onActionHelp(self):

        # Dans un script Python USD
        from pxr import Plug

        # Lister tous les plugins
        registry = Plug.Registry()
        plugins = registry.GetAllPlugins()

        # Chercher le plugin Alembic
        for plugin in plugins:
            if 'alembic' in plugin.name.lower() or 'abc' in plugin.name.lower():
                print(f"Plugin Alembic trouvé: {plugin.name}")
                print(f"Chemin: {plugin.path}")
                print(f"Chargé: {plugin.isLoaded}")
                plugin.Load()  # Charger le plugin si ce n'est pas déjà fait
        """


        

        

        import argparse

        stage = Usd.Stage.CreateNew('C:/Users/Thomas/OneDrive/Documents/Prism_Pluggins/HelloWorld.usda')
        xformPrim = UsdGeom.Xform.Define(stage, '/hello')
        spherePrim = UsdGeom.Sphere.Define(stage, '/hello/world')

        # Delete the file if it already exists
        if os.path.exists('C:/Users/Thomas/OneDrive/Documents/Prism_Pluggins/HelloWorld.usda'):
            os.remove('C:/Users/Thomas/OneDrive/Documents/Prism_Pluggins/HelloWorld.usda')

        stage.GetRootLayer().Save()



        # Open the help page in the default web browser
        #self.openUrl("https://thomasescalle.github.io/Pipeline_USD_2025/")
        """
        pass

    def createTemplate(self, path, origin):
        # Get the template from the FileTemplateManager
        manager = FileTemplateManager()
        template = manager.getTemplate(path)
        if template == None:
            # Use QMessageBox to show the error
            QMessageBox.warning(self.console, "Error", "Cette template n'existe pas : %s" % path)
            return
        
        self.console.log("Template found: %s" % template.template_name)
        template.construct(self, path, origin)


    # Create a Maya template
    def onCreateMayaTemplate(self, filePath, origin):
        self.console.log("Creating Maya template: %s" % filePath)
        path = filePath

        # Get the good path for the template
        # Split the file path into parts and join the two last parts with "/"
        pathParts = filePath.split("/")
        filePath = ""
        if len(pathParts) > 2:
            filePath = pathParts[-2]
        else:
            filePath = pathParts[0]

        filePath += "/Maya"

        self.console.log("File path: %s" % filePath)

        # Get the template from the FileTemplateManager
        self.createTemplate(filePath, origin)



    # Create a Houdini template
    def onCreateHoudiniTemplate(self, filePath, origin):
        self.console.log("Creating Houdini template: %s" % filePath)
        path = filePath


        # Get the good path for the template
        # Split the file path into parts and join the two last parts with "/"
        pathParts = filePath.split("/")
        filePath = ""
        if len(pathParts) > 2:
            filePath = pathParts[-2]
        else:
            filePath = pathParts[0]

        filePath += "/Houdini"

        # Create the template
        self.createTemplate(filePath, origin)


    # Create a Substance template
    def onCreateSubstanceTemplate(self, filePath, origin):
        self.console.log("Creating Substance template: %s" % filePath)
        path = filePath
        # Get the good path for the template
        # Split the file path into parts and join the two last parts with "/"
        pathParts = filePath.split("/")
        filePath = ""
        if len(pathParts) > 2:
            filePath = pathParts[-2]
        else:
            filePath = pathParts[0]

        filePath += "/Substance"


        # Create the template
        self.createTemplate(filePath, origin)





    #endregion Actions


    # if returns true, the plugin will be loaded by Prism
    @err_catcher(name=__name__)
    def isActive(self):
        return True
