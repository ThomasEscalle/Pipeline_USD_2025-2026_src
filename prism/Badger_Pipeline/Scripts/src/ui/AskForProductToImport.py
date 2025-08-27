from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *
import os
from src.ui.SettingsWidget import SettingsWidget
from src.ui.SelectProductsToImportWidget import SelectProductsToImportWidget


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
        
        # Create the SelectProductsToImportWidget
        self.select_products_widget = SelectProductsToImportWidget(core=self.core, pluggin_parent=self.pluggin_parent)

        # Add the widget to the import tab layout
        self.import_layout.addWidget(self.select_products_widget)



        # Add tabs to the tab widget
        self.tab_widget.addTab(self.settings_tab, "Settings")
        self.tab_widget.addTab(self.import_tab, "Import Products")





        # Bottom buttons layout
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

    def setDefaultSelectedProduct(self, products):
        self.select_products_widget.setDefaultSelectedProduct(products)


    def getResult(self):
        """ Get the result of the dialog """
        result = self.select_products_widget.getResult()
        return result



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
            "settings" : {
                "accepted_files" : [
                    "ma",
                    "mb"
                ]
            },
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

        print("RESULTS" )
        print(dialog.getResult())
    else:
        print("Dialog cancelled")
