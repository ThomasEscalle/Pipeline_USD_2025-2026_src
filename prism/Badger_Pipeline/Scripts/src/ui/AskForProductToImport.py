from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *
import os
from .SettingsWidget import SettingsWidget



class ProductImportDialog(QDialog):
    """
    Dialog for selecting products to import into a scene.
    Allows drag & drop from available products (left tree) to selected products (right tree).
    """

    def __init__(self, core, pluggin_parent, parent=None):
        super(ProductImportDialog, self).__init__(parent)
        
        self.setWindowTitle("Select Products to Import")
        self.setModal(True)
        self.resize(800, 600)
        
        self.core = core
        self.pluggin_parent = pluggin_parent
        self.setupUi()
        
    def setupUi(self) :
        self.main_layout = QVBoxLayout(self)

        # Create the tab widget
        self.tab_widget = QTabWidget(self)
        
        # First tab - Settings
        self.settings_tab = QWidget()
        self.settings_layout = QVBoxLayout(self.settings_tab)
        
        # Create the settings widget
        self.settings_widget = SettingsWidget(parent=self.settings_tab)
        self.settings_layout.addWidget(self.settings_widget)
        
        # Second tab - Product Import
        self.import_tab = QWidget()
        self.import_layout = QVBoxLayout(self.import_tab)
        
        self.splitter = QSplitter(Qt.Horizontal, self.import_tab)

        # LEFT
        self.left_splitter = QSplitter(Qt.Vertical, self.splitter)

        import EntityWidget
        self.w_entities = EntityWidget.EntityWidget(core=self.core, refresh=True)
        self.left_splitter.addWidget(self.w_entities)

        self.w_entities.getPage("Assets").itemChanged.connect(self.onSelectedEntityChanged)
        self.w_entities.getPage("Shots").itemChanged.connect(self.onSelectedEntityChanged)
        
        # Make sure that we can only select one item
        self.w_entities.getPage("Assets").tw_tree.setSelectionMode(QAbstractItemView.SingleSelection)
        self.w_entities.getPage("Shots").tw_tree.setSelectionMode(QAbstractItemView.SingleSelection)

        # Left Tree widget
        self.available_tree = QTreeWidget(self.left_splitter)
        self.available_tree.setHeaderLabels(["Product name" , "Format" , "File path"])


        # RIGHT
        self.right_container_widget = QWidget(self.splitter)
        self.right_layout = QVBoxLayout(self.right_container_widget)


        # Right Tree widget
        self.selected_tree = QTreeWidget()
        self.selected_tree.setHeaderLabels(["Product name" , "Format" , "File path"])
        self.right_layout.addWidget(self.selected_tree)

        # Right Button layout (left to right)
        self.right_buttons_layout = QHBoxLayout()
        
        self.btn_add = QPushButton("")
        self.right_buttons_layout.addWidget(self.btn_add)
        self.btn_add.setIcon(self.pluggin_parent.getIcon("add_cross.png"))
        self.btn_add.setToolTip("Add selected products to the right tree")
        self.btn_add.clicked.connect(self.addItem)

        self.btn_remove = QPushButton("")
        self.right_buttons_layout.addWidget(self.btn_remove)
        self.btn_remove.setIcon(self.pluggin_parent.getIcon("remove.png"))
        self.btn_remove.setToolTip("Remove selected products from the right tree")
        self.btn_remove.clicked.connect(self.removeItem)

        self.btn_clear = QPushButton("")
        self.right_buttons_layout.addWidget(self.btn_clear)
        self.btn_clear.setIcon(self.pluggin_parent.getIcon("clear.png"))
        self.btn_clear.setToolTip("Clear all products from the right tree")
        self.btn_clear.clicked.connect(self.clearItems)

        self.right_layout.addLayout(self.right_buttons_layout)

        # Add the splitter to the import tab layout
        self.import_layout.addWidget(self.splitter)
        
        # Add tabs to the tab widget
        self.tab_widget.addTab(self.settings_tab, "Settings")
        self.tab_widget.addTab(self.import_tab, "Import Products")

        # BOTTOM
        # Button layout 
        self.buttons_layout = QHBoxLayout()

        self.btn_import = QPushButton("Create")
        self.btn_import.setIcon(self.pluggin_parent.getIcon("check.png"))
        self.btn_import.clicked.connect(self.onCreate)

        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setIcon(self.pluggin_parent.getIcon("cancel.png"))
        self.btn_cancel.clicked.connect(self.reject)

        self.buttons_layout.addStretch()
        self.buttons_layout.addWidget(self.btn_import)
        self.buttons_layout.addWidget(self.btn_cancel)

        # Add tab widget and buttons to main layout
        self.main_layout.addWidget(self.tab_widget)
        self.main_layout.addLayout(self.buttons_layout)
        self.setLayout(self.main_layout)

    # Hide the import tab
    def hideImportTab(self):
        self.tab_widget.removeTab(self.tab_widget.indexOf(self.import_tab))

    def onCreate(self):
        print("CREATE")
        self.accept()

    def setSettings(self, settings_config):
        """Set the settings configuration for the settings widget"""
        self.settings_widget.setSettingsConfig(settings_config)

    def getSettings(self):
        """Get the current settings values as a dictionary"""
        return self.settings_widget.getSettings()

    def getSettingsAsJson(self):
        """Get the current settings values as a JSON string"""
        return self.settings_widget.getSettingsAsJson()

    def setSettingsValues(self, settings_dict):
        """Set specific settings values"""
        self.settings_widget.setSettingsFromDict(settings_dict)

    def onSelectedEntityChanged(self, item=None):
        if item:
            entities = [self.w_entities.getCurrentPage().getDataFromItem(item)]
            self.refreshAvailableTree(entities)

        else:
            self.refreshAvailableTree()

    def refreshAvailableTree(self, entities=None):
        # If there are no entities, clear the available tree
        if not entities:
            self.available_tree.clear()
            return
        
        self.available_tree.clear()

        for entity in entities:
            if entity["type"] == "assetFolder":
                continue  # Skip folders

            # Get all the products from the entity
            self.populateAvailableTreeFromEntity(entity)

    def populateAvailableTreeFromEntity(self, entity):

        # Get all the available products from the entity
        products = self.core.products.getProductsFromEntity(entity)

        for product in products:
            treeWidgetItem = self.createItemFromProduct(product, self.available_tree)
            self.available_tree.addTopLevelItem(treeWidgetItem)
        
    def createItemFromProduct(self, product , tree) :

        pformat = ""
        filepath = ""

        if "path" in product:
            data = self.core.products.getVersionsFromContext(product)

            if not data:
                print("No versions found for product:", product["product"])
                return None
            
            latestVersion = self.core.products.getLatestVersionFromVersions(data)

            if not latestVersion:
                print("No latest version found for product:", product["product"])
                return None
            
            filepath = latestVersion.get("path", "")
            prefered_file = self.core.products.getPreferredFileFromVersion(latestVersion)
            if prefered_file:
                pformat = prefered_file.split(".")[-1]
        
        treeWidgetItem = QTreeWidgetItem(tree)
        treeWidgetItem.setText(0, product["product"])
        treeWidgetItem.setText(1, pformat)
        treeWidgetItem.setText(2, filepath)

        product_str = str(product)
        treeWidgetItem.setData(0, Qt.UserRole, product_str)
        treeWidgetItem.setToolTip(0, product_str)

        # Set the icon according to if the product is a export or a publish
        if("_Publish" in product["product"]):
            treeWidgetItem.setIcon(0, self.pluggin_parent.getIcon("publish.png"))
        else:
            treeWidgetItem.setIcon(0, self.pluggin_parent.getIcon("other.png")) 


    def setDefaultSelectedProduct(self, products):
        """ Fill the right container with the default selected products """
        self.selected_tree.clear()
        for product in products:
            treeWidgetItem = QTreeWidgetItem(self.selected_tree)
            treeWidgetItem.setText(0, product["name"])
            treeWidgetItem.setWhatsThis(0, "folder")
            if "folder" in product["type"]:
                treeWidgetItem.setIcon(0, self.pluggin_parent.getIcon("folder.png"))
            else:
                treeWidgetItem.setIcon(0, self.pluggin_parent.getIcon("other.png"))

            if "settings" in product:
                settings = product["settings"]
                settings_str =  str(settings)
                treeWidgetItem.setToolTip(0, settings_str)

            # If there are child items
            if "items" in product:
                items = product["items"]
                for item in items:
                    treeWidgetItem_child = self.createItemFromProduct(item, treeWidgetItem)
                    treeWidgetItem.addChild(treeWidgetItem_child)

            self.selected_tree.addTopLevelItem(treeWidgetItem)



    def addItem(self):
        """ When the add button is pressed """
        print("Add item pressed")
        ## Get the selected items from both trees
        left_selected_items = self.available_tree.selectedItems()
        right_selected_items = self.selected_tree.selectedItems()

        if not left_selected_items:
            return
        
        if not right_selected_items:
            return

        # Take the first right selected item, and make sure it is a top-level item
        right_selected_item = right_selected_items[0]
        if right_selected_item.parent() is not None:
            # Get the parent item
            right_selected_item = right_selected_item.parent()

        # Check if the right_selected_item is a folder
        if right_selected_item.whatsThis(0) != "folder":
            QMessageBox.warning(self, "Invalid Selection", "Please select a folder to add items to.")
            return

        # Check if the right_selected_item has settings
        settings = right_selected_item.toolTip(0)
        if settings:
            # Check if the settings allow to pass
            pass

        # Add the item inside of the right selected item
        for item in left_selected_items:
            right_selected_item.addChild(item.clone())


    def removeItem(self):
        """ When the remove button is pressed, remove the selected item from the right tree, if it is not a folder """
        print("Remove item pressed")
        right_selected_items = self.selected_tree.selectedItems()
        if not right_selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a product to remove.")
            return

        for item in right_selected_items:
            if item.parent() is None:
                QMessageBox.warning(self, "Invalid Selection", "Please select a child item to remove.")
                return
            item.parent().removeChild(item)

    def getResult(self):
        """ Get the result of the dialog """
        result = {}

        # Iterate through the folders in the right tree
        for i in range(self.selected_tree.topLevelItemCount()):
            folder_item = self.selected_tree.topLevelItem(i)
            folder_name = folder_item.text(0)
            folder_settings = folder_item.toolTip(0)
            folder_items = []

            # Iterate through the child items
            for j in range(folder_item.childCount()):
                child_item = folder_item.child(j)
                child_name = child_item.text(0)
                child_data = child_item.toolTip(0)
                child_data = eval(child_data)

                folder_items.append(child_data)

            result[folder_name] = folder_items

        return result

    def clearItems(self):
        """ When the clear button is pressed """
        print("Clear items pressed")


def test_product_import_dialog(core , pluggin_parent):

    default_selected = [
        {
            "type" : "folder",
            "name" : "Cameras",
            "settings" : {
                "accepted_files" : [
                    "abc",
                    "fbx"
                ],
                "select_only_one_file": True
            },
            "items" : [
                {
                    "product" : "Camera_00.abc",
                    "type" : "asset"
                }
            ]
        },
        {
            "type" : "folder",
            "name" : "Rigs",
            "items" : [
                {
                    "type" : "asset",
                    "product" : "Rig_01.fbx"
                },
                {
                    "type" : "asset",
                    "product" : "Rig_02.fbx"
                }
            ]
        }
    ]

    # Example settings configuration
    settings_config = [
        {
            "setting_name": "import_title",
            "type": "title",
            "default_value": "Import Settings"
        },
        {
            "setting_name": "Create References",
            "type": "checkbox",
            "default_value": True
        },
        {
            "setting_name": "Import Namespace",
            "type": "lineedit",
            "default_value": "imported"
        },
        {
            "setting_name": "Import Mode",
            "type": "combobox",
            "default_value": "Reference",
            "options": ["Reference", "Import", "Proxy"]
        },
        {
            "setting_name": "transform_title",
            "type": "title",
            "default_value": "Transform Settings"
        },
        {
            "setting_name": "Maintain Hierarchy",
            "type": "checkbox",
            "default_value": True
        },
        {
            "setting_name": "Scale Factor",
            "type": "lineedit",
            "default_value": "1.0"
        },
        {
            "setting_name": "Up Axis",
            "type": "combobox",
            "default_value": "Y",
            "options": ["X", "Y", "Z"]
        }
    ]

    dialog = ProductImportDialog(core=core, pluggin_parent=pluggin_parent)
    
    # Set the settings configuration
    dialog.setSettings(settings_config)
    
    # Set the default selected products
    dialog.setDefaultSelectedProduct(default_selected)
    
    # Show the dialog
    if dialog.exec_() == QDialog.Accepted:
        print("Dialog accepted!")
        print("Settings values:")
        settings = dialog.getSettings()
        for key, value in settings.items():
            print(f"  {key}: {value}")
        
        print("\nSettings as JSON:")
        print(dialog.getSettingsAsJson())
    else:
        print("Dialog cancelled")
