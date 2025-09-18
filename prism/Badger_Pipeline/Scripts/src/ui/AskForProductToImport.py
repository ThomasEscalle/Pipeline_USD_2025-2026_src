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
        
    def setupUi(self):
        self.main_layout = QVBoxLayout(self)

        # Create stacked widget for pages
        self.stacked_widget = QStackedWidget(self)
        
        # Page 0 - Settings
        self.settings_page = QWidget()
        self.settings_layout = QVBoxLayout(self.settings_page)
        
        # Create the settings widget
        self.settings_widget = SettingsWidget(parent=self.settings_page)
        self.settings_layout.addWidget(self.settings_widget)
        
        # Page 1 - Import Products
        self.import_page = QWidget()
        self.import_layout = QVBoxLayout(self.import_page)
        
        # Create the SelectProductsToImportWidget
        self.select_products_widget = SelectProductsToImportWidget(core=self.core, pluggin_parent=self.pluggin_parent)

        # Add the widget to the import page layout
        self.import_layout.addWidget(self.select_products_widget)

        # Add pages to the stacked widget
        self.stacked_widget.addWidget(self.settings_page)
        self.stacked_widget.addWidget(self.import_page)





        # Bottom buttons layout
        self.buttons_layout = QHBoxLayout()

        self.btn_help = QPushButton("Help")
        self.btn_help.setIcon(self.pluggin_parent.getIcon("help.png"))
        self.btn_help.clicked.connect(self.openHelp)
        self.btn_help.setVisible(False)

        self.btn_previous = QPushButton("Previous")
        self.btn_previous.setIcon(self.pluggin_parent.getIcon("previous.png"))
        self.btn_previous.clicked.connect(self.goToSettingsPage)
        self.btn_previous.setVisible(False)

        self.btn_next = QPushButton("Next")
        self.btn_next.setIcon(self.pluggin_parent.getIcon("next.png"))
        self.btn_next.clicked.connect(self.goToImportPage)

        self.btn_import = QPushButton("Create")
        self.btn_import.setIcon(self.pluggin_parent.getIcon("check.png"))
        self.btn_import.clicked.connect(self.onCreate)
        self.btn_import.setVisible(False)

        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setIcon(self.pluggin_parent.getIcon("cancel.png"))
        self.btn_cancel.clicked.connect(self.reject)

        self.buttons_layout.addWidget(self.btn_help)
        self.buttons_layout.addStretch()
        self.buttons_layout.addWidget(self.btn_previous)
        self.buttons_layout.addWidget(self.btn_next)
        self.buttons_layout.addWidget(self.btn_import)
        self.buttons_layout.addWidget(self.btn_cancel)

        # Add stacked widget and buttons to main layout
        self.main_layout.addWidget(self.stacked_widget)
        self.main_layout.addLayout(self.buttons_layout)
        self.setLayout(self.main_layout)

        # Initialize state
        self.import_page_hidden = False
        self.help_link = ""
        self.updateButtons()

    def navigate(self, entity):
        self.select_products_widget.navigate(entity)

    def updateButtons(self):
        """Update button visibility based on current page and import_page_hidden state"""
        page = self.stacked_widget.currentIndex()
        
        # Update help button visibility
        self.btn_help.setVisible(bool(self.help_link))
        
        if self.import_page_hidden:
            # Only settings page, show Create and Cancel
            self.btn_previous.setVisible(False)
            self.btn_next.setVisible(False)
            self.btn_import.setVisible(True)
        else:
            if page == 0:  # Settings page
                self.btn_previous.setVisible(False)
                self.btn_next.setVisible(True)
                self.btn_import.setVisible(False)
            elif page == 1:  # Import page
                self.btn_previous.setVisible(True)
                self.btn_next.setVisible(False)
                self.btn_import.setVisible(True)

    def goToSettingsPage(self):
        """Navigate to the settings page"""
        self.stacked_widget.setCurrentIndex(0)
        self.updateButtons()

    def goToImportPage(self):
        """Navigate to the import page"""
        self.stacked_widget.setCurrentIndex(1)
        self.updateButtons()

    def openHelp(self):
        """Open the help link in the default browser"""
        if self.help_link:
            QDesktopServices.openUrl(QUrl(self.help_link))

    def setHelpLink(self, help_link):
        """Set the help link URL"""
        self.help_link = help_link
        self.updateButtons()

    # Hide the import page (show only settings and Create)
    def hideImportTab(self):
        self.import_page_hidden = True
        self.stacked_widget.setCurrentIndex(0)
        self.updateButtons()

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
                "required" : True,
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
