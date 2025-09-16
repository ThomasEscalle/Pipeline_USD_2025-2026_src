import PrismInit

from PySide2 import QtWidgets, QtGui, QtCore
import hou
import os
import json

# Define some colors for bookmarks
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


# The navigator is a list widget displayed on the left side of the asset browser
# It contains shortcuts to different asset categories and bookmarks
class NavigatorListWidget(QtWidgets.QListWidget):
    def __init__(self,core, parent=None):
        super().__init__(parent)
        self.core = core
        self.setObjectName("Navigator")
        
        # Title tree widget
        title = QtWidgets.QListWidgetItem("Quick Navigator")
        title.setFlags(QtCore.Qt.NoItemFlags)
        title.setTextAlignment(QtCore.Qt.AlignCenter)
        title.setSizeHint(QtCore.QSize(0, 40))
        self.addItem(title)

        # self.addItems(["Chars", "Items" , "Props" , "Modules"])

        bold_font = QtGui.QFont()
        bold_font.setBold(True)


        self.item_chars = QtWidgets.QListWidgetItem("Chars")
        self.item_chars.setIcon( self.core.getPlugin("Badger_Pipeline").getIcon("char.png"))
        self.item_chars.setFont(bold_font)
        self.addItem(self.item_chars)
        # Set the current_path to "Chars"

        self.item_items = QtWidgets.QListWidgetItem("Items")
        self.item_items.setIcon( self.core.getPlugin("Badger_Pipeline").getIcon("item.png"))
        self.item_items.setFont(bold_font)
        self.addItem(self.item_items)
        # Set the current_path to "Items"

        self.item_props = QtWidgets.QListWidgetItem("Props")
        self.item_props.setIcon( self.core.getPlugin("Badger_Pipeline").getIcon("prop.png"))
        self.item_props.setFont(bold_font)
        self.addItem(self.item_props)
        # Set the current_path to "Props"

        self.item_modules = QtWidgets.QListWidgetItem("Modules")
        self.item_modules.setIcon( self.core.getPlugin("Badger_Pipeline").getIcon("module_2.png"))
        self.item_modules.setFont(bold_font)
        self.addItem(self.item_modules)
        # Set the current_path to "Modules"

        self.setMinimumWidth(150)
    
    
        # Add a separator
        separator = QtWidgets.QListWidgetItem(self)
        separator.setFlags(QtCore.Qt.NoItemFlags)
        separator.setSizeHint(QtCore.QSize(0, 15))

        # Add a title for "Bookmarks"
        title = QtWidgets.QListWidgetItem("Bookmarks")
        title.setFlags(QtCore.Qt.NoItemFlags)
        title.setTextAlignment(QtCore.Qt.AlignCenter)
        title.setSizeHint(QtCore.QSize(0, 40))
        self.addItem(title)

        for color_name, color_value in colors.items():
            item = QtWidgets.QListWidgetItem(color_name)
            item.setIcon( self.core.getPlugin("Badger_Pipeline").getIcon("collection_" + color_name + ".png"))
            item.setBackground(QtGui.QColor(color_value))
            self.addItem(item)



        # Connect itemClicked to slot
        self.itemClicked.connect(self.on_nav_item_clicked)


    def set_items_list_widget(self, items_list_widget):
        self.items_list_widget = items_list_widget

    def on_nav_item_clicked(self, item):
        nav_names = ["Chars", "Items", "Props", "Modules"]
        if item.text() in nav_names and hasattr(self, "items_list_widget"):
            self.items_list_widget.set_current_path(item.text())

# The items list is a QListWidget that displays the assets in the main area of the asset browser
class ItemsListWidget(QtWidgets.QListWidget):

    def __init__(self, core, parent=None):
        super().__init__(parent)
        self.core = core
        self.setObjectName("Items")
        self.addItems(["01_Assets", "02_Shots"])
        self.setMinimumWidth(300)

        self.itemDoubleClicked.connect(self.onItemDoubleClicked)

        # Modes: 'list' or 'grid'
        self._view_mode = 'list'
        self.set_list_mode()

        # Ajout des attributs current_path et filter
        self._current_path = ""
        self._filter = ""

        # Fill the database with assets from the core
        self.fill_assets()

    # Getter/setter pour current_path
    def get_current_path(self):
        return self._current_path

    def set_current_path(self, path):
        self._current_path = path
        self.fill_assets()

    # Getter/setter pour filter
    def get_filter(self):
        return self._filter

    def set_filter(self, filter_str):
        self._filter = filter_str
        self.fill_assets()

    # Fonction pour remonter d'un dossier
    def go_up(self):
        if self._current_path:
            parts = self._current_path.rstrip("/\\").split("/" if "/" in self._current_path else "\\")
            if len(parts) > 1:
                self._current_path = "/".join(parts[:-1])
            else:
                self._current_path = ""
            self.fill_assets()
        else:
            # Déjà à la racine
            pass

    # Fill the database with assets from the core
    def fill_assets(self):
        """
        Remplit la liste d'assets en fonction du current_path et du filtre.
        Structure attendue de getAssets():
        [
            {
                "type": "asset",
                "asset_path": "Chars\\AAA"
            },
            ...
        ]
        """

        self.clear()
        assets = self.core.entities.getAssets()
        filtered_assets = []
        folders = []

        # Filtrage par current_path et filter
        for asset in assets:
            path = asset.get('asset_path', '')

            # Asset name is the last part of the path,
            # Asset path is the rest, if any
            asset_splited = path.replace("\\", "/").split("/")
            asset_path = ""
            asset_name = ""

            if len(asset_splited) > 1:
                asset_name = asset_splited[-1]
                asset_path = "/".join(asset_splited[:-1])
            else:
                asset_name = asset_splited[0]
                asset_path = ""

            # Collecte des dossiers
            if asset_path and asset_path not in folders and self._current_path in asset_path and asset_path != self._current_path:
                folders.append(asset_path)


            # Filtrage par current_path
            if asset_path != self._current_path:
                continue

            # Filtrage par filter
            if self._filter:
                if self._filter.lower() not in asset_name.lower():
                    continue

            filtered_assets.append(asset)

        # Creation des dossiers
        for folder in folders:
            item = QtWidgets.QListWidgetItem(folder)
            name = folder.split("/")[-1].split("\\")[-1]
            item.setText(name)
            item.setIcon(self.core.getPlugin("Badger_Pipeline").getIcon("folder.png"))
            item.setWhatsThis("folder")
            self.addItem(item)

        # Création des assets
        for asset in filtered_assets:
            item = QtWidgets.QListWidgetItem(asset['asset_path'])
            name = asset['asset_path'].split("/")[-1].split("\\")[-1]
            item.setText(name)
            item.setWhatsThis("asset")
            item.setToolTip(json.dumps(asset, indent=4))
            icon_path = self.core.entities.getEntityPreviewPath(asset)
            # if the file exists
            if icon_path and os.path.exists(icon_path):
                item.setIcon(QtGui.QIcon(icon_path))
            else:
                item.setIcon(self.core.getPlugin("Badger_Pipeline").getIcon("noFileSmall.png"))

            
            self.addItem(item)




    # Switch to list mode
    def set_list_mode(self):
        self.setViewMode(QtWidgets.QListView.ListMode)
        self.setIconSize(QtCore.QSize(32, 32))
        self.setGridSize(QtCore.QSize(36, 36))
        self._view_mode = 'list'

    # Switch to grid mode
    def set_grid_mode(self):
        self.setViewMode(QtWidgets.QListView.IconMode)
        self.setIconSize(QtCore.QSize(96, 96))
        self.setGridSize(QtCore.QSize(110, 110))
        self._view_mode = 'grid'

    # Toggle between list and grid mode
    def toggle_mode(self, mode):
        if mode == 'list':
            self.set_list_mode()
        elif mode == 'grid':
            self.set_grid_mode()

    # When an item is double clicked
    # @todo : Create the corresponding houdini node
    def onItemDoubleClicked(self, item):
        # Vérifie si l'item est un dossier via whatsThis
        if item.whatsThis() == "folder":
            folder_name = item.text()
            self.set_current_path(folder_name)
            return
        

        # The item is an asset. Create a corresponding houdini node
        asset = json.loads(item.toolTip())
        products = self.core.products.getProductsFromEntity(asset)
        for product in products:
            if "USD_Asset" in product["product"]:
                product_path = product["path"]
                product_path = product_path.replace("\\", "/")
                product_path = os.path.join(product_path, "asset.usda")

                # Check if the file exists
                if not os.path.exists(product_path):
                    QtWidgets.QMessageBox.warning(self, "File Not Found", f"The USD file does not exist:\n{product_path}")
                    return
                
                pane = hou.ui.paneTabOfType(hou.paneTabType.SceneViewer)
                current_context = pane.pwd()


                # Create a "assetreference" node named after the asset's name
                node = current_context.createNode("assetreference", item.text())
                node.parm("filepath").set(product_path)


                displayed_node = current_context.displayNode()
                if displayed_node :
                    
                    # If the displayed node has already input, store it and disconnect it, then reconnect it to the new node
                    if displayed_node.inputs():
                        input_node = displayed_node.inputs()[0]
                        displayed_node.setInput(0, None)
                        node.setInput(0, input_node)

                    # Connect the new node output to the displayed node input
                    displayed_node.setInput(0, node)

                    # Layout the nodes
                    current_context.layoutChildren()
                    

# The main widget that contains the navigator and the items list
class ProjectBrowserWidget(QtWidgets.QWidget):
    def __init__(self, core , parent=None):
        super().__init__(parent)
        self.core = core
        # Layout principal vertical
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # --- Search bar + mode button ---
        search_layout = QtWidgets.QHBoxLayout()

        # Mode button
        self.mode_button = QtWidgets.QPushButton("", self)
        self.mode_button.setIcon(self.core.getPlugin("Badger_Pipeline").getIcon("menu.png"))
        search_layout.addWidget(self.mode_button)

        # QMenu for mode selection
        self.mode_menu = QtWidgets.QMenu(self)
        self.action_list = self.mode_menu.addAction("Liste")
        self.action_grid = self.mode_menu.addAction("Grille")
        # Les items sont créés plus bas, donc on connecte après

        # Up button
        self.up_button = QtWidgets.QPushButton("", self)
        self.up_button.setIcon(self.core.getPlugin("Badger_Pipeline").getIcon("up.png"))
        search_layout.addWidget(self.up_button)

        # Search bar
        self.search_bar = QtWidgets.QLineEdit(self)
        self.search_bar.setPlaceholderText("Rechercher...")
        search_layout.addWidget(self.search_bar)

        # Clear button
        self.clear_button = QtWidgets.QPushButton("", self)
        self.clear_button.setIcon(self.core.getPlugin("Badger_Pipeline").getIcon("backspace.png"))
        search_layout.addWidget(self.clear_button)
        main_layout.addLayout(search_layout)

        # --- Splitter ---
        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.items = ItemsListWidget(core)
        self.navigator = NavigatorListWidget(core)
        self.navigator.set_items_list_widget(self.items)
        splitter.addWidget(self.navigator)
        splitter.addWidget(self.items)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        main_layout.addWidget(splitter)

        # Connect mode actions après création de self.items
        self.action_list.triggered.connect(lambda: self.items.toggle_mode('list'))
        self.action_grid.triggered.connect(lambda: self.items.toggle_mode('grid'))
        self.mode_button.setMenu(self.mode_menu)

        # Connect bouton up à go_up
        self.up_button.clicked.connect(lambda: self.items.go_up())
        # Connect clear button
        self.clear_button.clicked.connect(self.search_bar.clear)
        # Connecte la barre de recherche au filtre
        self.search_bar.textChanged.connect(lambda text: self.items.set_filter(text))

    def on_up_clicked(self):
        # Navigue vers le dossier parent dans ItemsListWidget
        self.items.go_up()

# Create and return the main interface widget
# Entry point used by Houdini
def createInterface():
    try:
        core = PrismInit.pcore
        return ProjectBrowserWidget(core)

    except Exception as e:
        print(f"Error initializing PrismInit: {e}")
        return QtWidgets.QLabel("Error initializing PrismInit")