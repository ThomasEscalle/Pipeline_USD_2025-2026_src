import PrismInit

from PySide2 import QtWidgets, QtGui, QtCore
import hou

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

        self.item_chars = QtWidgets.QListWidgetItem("Chars")
        self.item_chars.setIcon( self.core.getPlugin("Badger_Pipeline").getIcon("char.png"))
        # Set the font of the item to bold
        font = self.item_chars.font()
        font.setBold(True)
        self.item_chars.setFont(font)
        self.addItem(self.item_chars)

        self.item_items = QtWidgets.QListWidgetItem("Items")
        self.item_items.setIcon( self.core.getPlugin("Badger_Pipeline").getIcon("item.png"))
        font = self.item_items.font()
        font.setBold(True)
        self.item_items.setFont(font)
        self.addItem(self.item_items)

        self.item_props = QtWidgets.QListWidgetItem("Props")
        self.item_props.setIcon( self.core.getPlugin("Badger_Pipeline").getIcon("prop.png"))
        font = self.item_props.font()
        font.setBold(True)
        self.item_props.setFont(font)
        self.addItem(self.item_props)

        self.item_modules = QtWidgets.QListWidgetItem("Modules")
        self.item_modules.setIcon( self.core.getPlugin("Badger_Pipeline").getIcon("module_2.png"))
        font = self.item_modules.font()
        font.setBold(True)
        self.item_modules.setFont(font)
        self.addItem(self.item_modules)

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

        assets = self.core.entities.getAssets( )

        for asset in assets:
            item = QtWidgets.QListWidgetItem(asset['asset_path'])
            name = asset['asset_path'].split("/")[-1]
            item.setText(name)
            item.setIcon( QtGui.QIcon(self.core.entities.getEntityPreviewPath(asset)) )
            self.addItem(item)
        print(assets)

    def set_list_mode(self):
        self.setViewMode(QtWidgets.QListView.ListMode)
        self.setIconSize(QtCore.QSize(32, 32))
        self.setGridSize(QtCore.QSize(36, 36))
        self._view_mode = 'list'

    def set_grid_mode(self):
        self.setViewMode(QtWidgets.QListView.IconMode)
        self.setIconSize(QtCore.QSize(96, 96))
        self.setGridSize(QtCore.QSize(110, 110))
        self._view_mode = 'grid'

    def toggle_mode(self, mode):
        if mode == 'list':
            self.set_list_mode()
        elif mode == 'grid':
            self.set_grid_mode()

    def onItemDoubleClicked(self, item):
        print(f"Double clicked on item: {item.text()}")
        # Create a houdini node
        node = hou.node("/stage").createNode("subnet", item.text())

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
        self.action_list.triggered.connect(lambda: self.items.toggle_mode('list'))
        self.action_grid.triggered.connect(lambda: self.items.toggle_mode('grid'))
        self.mode_button.setMenu(self.mode_menu)

        # Up button
        self.up_button = QtWidgets.QPushButton("", self)
        self.up_button.setIcon(self.core.getPlugin("Badger_Pipeline").getIcon("up.png"))
        self.up_button.clicked.connect(self.up_button_clicked)
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
        self.navigator = NavigatorListWidget(core)
        splitter.addWidget(self.navigator)
        self.items = ItemsListWidget(core)
        splitter.addWidget(self.items)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        main_layout.addWidget(splitter)

        # Connect clear button
        self.clear_button.clicked.connect(self.search_bar.clear)

    def up_button_clicked(self):
        print("Up button clicked")

def createInterface():

    try:
        core = PrismInit.pcore
        return ProjectBrowserWidget(core)

    except Exception as e:
        print(f"Error initializing PrismInit: {e}")
        return QtWidgets.QLabel("Error initializing PrismInit")