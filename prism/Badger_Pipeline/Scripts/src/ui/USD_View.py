from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

import requests
import json
import os

from src.ui.ChatMoche import getUnChatMoche


from PrismUtils.Decorators import err_catcher_plugin as err_catcher


colors = {
    "red": "#FF0000",
    "pink": "#FF00FF",
    "purple": "#800080",
    "deep_purple": "#673AB7",
    "indigo": "#3F51B5",
    "blue": "#2196F3",
    "light_blue": "#03A9F4",
    "cyan": "#00BCD4",
    "teal": "#009688",
    "green": "#4CAF50",
    "light_green": "#8BC34A",
    "lime": "#CDDC39",
    "yellow": "#FFEB3B",
    "amber": "#FFC107",
    "orange": "#FF9800",
    "deep_orange": "#FF5722",
    "brown": "#795548",
}



class USD_ViewListWidget(QListWidget):
    def __init__(self, parent=None, root=None):
        super(USD_ViewListWidget, self).__init__(parent)
        self.parent = parent
        self.root = root
        self.setDragEnabled(True)
        #self.setViewMode(QListWidget.IconMode)
        self.setDragDropMode(QAbstractItemView.DragOnly)
        self.setAcceptDrops(False)
        self.setIconSize(QSize(80, 80))  # Set icon size for items

        # Connect the custom context menu to the right-click event
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openContextMenu)
        
    
    def startDrag(self, supported_actions):

        
        # Create a custom drag object
        drag = QDrag(self)
        # Get the selected items
        selected_items = self.selectedItems()
        if not selected_items:
            return
        
        if selected_items[0].whatsThis() == "Asset":
        
            # Create a QMimeData object to hold the data
            mime_data = QMimeData()

            path = selected_items[0].data(Qt.UserRole)
            # Try to read the asset info from the usd_info.txt file
            asset_info_path = os.path.join(path, "usd_info.txt")
            asset_info_path = asset_info_path.replace("\\", "/")
            fileName = ""
            if not os.path.isfile(asset_info_path):
                return
            try:
                with open(asset_info_path, "r") as info_file:
                    asset_data = json.load(info_file)
                    fileName = asset_data["entry_file"]

            except json.JSONDecodeError as e:
                self.root.console.log(f"Error decoding JSON from {asset_info_path}: {e}")
                return
            except Exception as e:
                self.root.console.log(f"Error reading asset info from {asset_info_path}: {e}")
                return
            
            name = selected_items[0].text()
            
            

            biteData = {
                "ids": ["q"],
                "types": ["sidefx_usd_database_source"],
                "assettypes": ["asset"],
                "labels": [name],
                "filepaths": [os.path.join(path, fileName)],
                "sources": [["DB", ""]],
                "asset_data": [json.dumps(asset_data)]
            }
            # Join the file paths with a newline character
            biteArray = QByteArray( json.dumps(biteData).encode('utf-8'))
            mime_data.setData("application/sidefx-houdini-asset.gallery.entry", biteArray)

            # Set the pixmap for the drag
            pixmap = QPixmap(getUnChatMoche())
            drag.setPixmap(pixmap)


            # Set the QMimeData object for the drag
            drag.setMimeData(mime_data)
            
            # Start the drag operation
            drag.exec_(supported_actions, Qt.CopyAction | Qt.MoveAction)


    def openContextMenu(self, pos):
        print("Right click on item at position:", pos)


class USD_View(QWidget):
    def __init__(self, parent=None, root=None):
        super(USD_View, self).__init__(parent)

        self.parent = parent
        self.root = root

        # Créer un QSplitter horizontal pour séparer les widgets
        splitter = QSplitter(Qt.Horizontal, self)

        # Créer le QListWidget pour le menu
        self.menuWidget = QListWidget(self)
        self.listWidget = USD_ViewListWidget(self, root=self.root)

        self.listWidget.setIconSize(QSize(80, 80))  # Set icon size for items
        # Enable the drags and drops
        self.listWidget.setDragEnabled(True)
        self.listWidget.setDragDropMode(QAbstractItemView.DragOnly)

        # Ajouter les widgets au splitter
        splitter.addWidget(self.menuWidget)
        splitter.addWidget(self.listWidget)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 4)

        # Créer un layout vertical et y ajouter le splitter
        layout = QVBoxLayout(self)
        layout.addWidget(splitter)

        # Set the layout for this widget
        self.setLayout(layout)

        # Load the file hierarchy into the list widget
        self.usd_path = self.root.core.projects.getResolvedProjectStructurePath("usd_path")
        self.usd_path = self.usd_path.replace("\\", "/")  # Normalize path for consistency
        self.loadFileHierarchy(self.root.core.projects.getResolvedProjectStructurePath("usd_path"))

        # Connect the itemClicked signal to the onDirectoryClicked method
        self.listWidget.itemClicked.connect(self.onItemClicked)

        self.fillMenuWidget()


    def fillMenuWidget(self):
        self.menuWidget.clear()
        # Add the "Asset"
        item1 = QListWidgetItem("Assets", self.menuWidget)
        item1.setWhatsThis("Assets")
        item1.setIcon(self.root.getIcon("asset.png"))
        font_item1 = item1.font()
        font_item1.setBold(True)
        font_item1.setPointSize(10)
        item1.setFont(font_item1)

        # Add the "Shot" item   
        item2 = QListWidgetItem("Shots", self.menuWidget)
        item2.setWhatsThis("Shots")
        item2.setIcon(self.root.getIcon("shot.png"))
        item2.setFont(font_item1)

        # Add a separator
        separator = QListWidgetItem(self.menuWidget)
        separator.setFlags(Qt.NoItemFlags)
        separator.setSizeHint(QSize(0, 10))
        
        # Add a "Collection" item title
        item3 = QListWidgetItem("Collections : ", self.menuWidget)
        item3.setWhatsThis("Collections")
        item3.setFont(font_item1)

        # Add the collection item (one for each color)
        for color_name, color_hex in colors.items():
            goodColorName = color_name.replace("_", " ")
            goodColorName = goodColorName.capitalize()
            item = QListWidgetItem(goodColorName, self.menuWidget)
            item.setWhatsThis("Collection")
            item.setIcon(self.root.getIcon(f"collection_{color_name}.png"))




    def loadFileHierarchy(self, path):
        self.listWidget.clear()
        self.addItems(path)

    def addItems(self, dirPath):
        dirPath = dirPath.replace("\\", "/")  # Normalize path for consistency

        # if the path is not the usd_path, add the .. 
        if dirPath != self.usd_path:
            itemDotDot = QListWidgetItem("", self.listWidget)
            itemDotDot.setWhatsThis("Up")
            itemDotDot.setIcon(self.root.getIcon("return.png"))  # Assuming you have a method to get icons
            itemDotDot.setData(Qt.UserRole, dirPath)  # Store the directory path in the item data
            itemDotDot.setSizeHint(QSize(0, 90))  # Set the height of the item to 50
            self.listWidget.addItem(itemDotDot)

        if not os.path.isdir(dirPath):
            self.root.console.log(f"Directory does not exist: {dirPath}")
            return
        try:
            entries = os.listdir(dirPath)
            self.root.console.log(f"Entries in {dirPath}: {entries}")
            dirs = []
            files = []
            for entry in entries:
                full_path = os.path.join(dirPath, entry)
                if os.path.isdir(full_path):
                    dirs.append(entry)
                else:
                    self.root.console.log(f"Adding file: {full_path}")
                    files.append(entry)
            # Sort alphabetically
            dirs.sort()
            files.sort()

            for entry in dirs:
                self.addDirectory(os.path.join(dirPath, entry))
            for entry in files:
                self.addFile(os.path.join(dirPath, entry))


        except Exception as e:
            self.root.console.log(f"Error reading directory {dirPath}: {e}")

    def addFile(self, filePath):
        self.root.console.log(f"Adding file: {filePath}")
        if not os.path.isfile(filePath):
            self.root.console.log(f"File does not exist: {filePath}")
            return
        fileName = os.path.basename(filePath)
        item = QListWidgetItem(fileName)
        item.setWhatsThis("File")
        item.setIcon(self.root.getIcon("file.png"))
        # Set the height of the item to 50
        item.setSizeHint(QSize(0, 90))
        # Set the text to be bold
        font = item.font()
        font.setBold(True)
        font.setPointSize(15)
        item.setFont(font)

        item.setData(Qt.UserRole, filePath)  # Store the file path in the item data

        self.listWidget.addItem(item)



    def addDirectory(self, dirPath):
        if not os.path.isdir(dirPath):
            self.root.console.log(f"Directory does not exist: {dirPath}")
            return
        dirName = os.path.basename(dirPath)
        self.root.console.log(f"Adding directory: {dirPath}")
        item = QListWidgetItem(f"{dirName}")
        item.setData(Qt.UserRole, dirPath)  # Store the directory path in the item data
        item.setWhatsThis("Dir")

        # If the directory is an asset directory, set the icon to asset
        asset_type = self.getAssetType(dirPath)
        if asset_type == "asset":
            item.setWhatsThis("Asset")
            
            # Check if the asset contains a "thumbnail.png" file
            thumbnail_path = os.path.join(dirPath, "thumbnail.png")
            thumbnail_path = thumbnail_path.replace("\\", "/")  # Normalize path for consistency
            if os.path.isfile(thumbnail_path):
                item.setIcon(QIcon(thumbnail_path))
            else:
                item.setIcon(self.root.getIcon("asset.png"))



        elif asset_type == "module":
            item.setWhatsThis("Module")
            item.setIcon(self.root.getIcon("module.png"))
        else:
            item.setWhatsThis("Dir")
            item.setIcon(self.root.getIcon("folder.png"))  # Assuming you have a method to get icons



        # Set the heigh of the item to 50
        item.setSizeHint(QSize(0, 90))
        # Set the text to be bold
        font = item.font()
        font.setPointSize(15)
        item.setFont(font)

        self.listWidget.addItem(item)


    # Check if the given directory path is an asset or just a directory
    def getAssetType(self, dirPath):
        dirPath = dirPath.replace("\\", "/")  # Normalize path for consistency
        if not os.path.isdir(dirPath):
            return "Dir"
            
        
        # Check for the presence of a "usd_info.txt" file
        info_file_path = os.path.join(dirPath, "usd_info.txt")
        info_file_path = info_file_path.replace("\\", "/")  # Normalize path for consistency
        if os.path.isfile(info_file_path):
            try:
                with open(info_file_path, "r") as info_file:
                    data = json.load(info_file)
                    self.root.console.log(f"Asset type data found: {data}")
                    if "type" in data:
                        return data["type"]
            except json.JSONDecodeError as e:
                self.root.console.log(f"Error decoding JSON from {info_file_path}: {e}")
        self.root.console.log(f"No valid asset type found in {dirPath}")
        return "dir"




    def onItemClicked(self, item):
        item = self.listWidget.currentItem()
        print(f"Item clicked: {item.whatsThis()} - {item.text()}")

        if item is None:
            return
        
        elif item.whatsThis() == "File":
            return
        
        if item.whatsThis() == "Dir":
            dirPath = item.data(Qt.UserRole)
            if dirPath and os.path.isdir(dirPath):
                self.root.console.log(f"Directory clicked: {dirPath}")
                self.loadFileHierarchy(dirPath)
            else:
                self.root.console.log(f"Clicked item is not a directory: {item.text()}")
            return

        if item.whatsThis() == "Up":
            parentDir = os.path.dirname(item.data(Qt.UserRole))
            self.loadFileHierarchy(parentDir)
            return



  

    @err_catcher(name=__name__)
    def entered(self, prevTab=None, navData=None):
        print("Entered the calendar tab")

    @err_catcher(name=__name__)
    def refreshUI(self):
        self.loadFileHierarchy(self.root.core.projects.getResolvedProjectStructurePath("usd_path"))

    @err_catcher(name=__name__)
    def getSelectedContext(self):
        return 0
