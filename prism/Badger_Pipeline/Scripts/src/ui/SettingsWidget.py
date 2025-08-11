from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *
import json


class SettingsWidget(QWidget):
    """
    A configurable settings widget that can be parameterized from a JSON configuration.
    Supports various widget types: title, checkbox, lineedit, combobox.
    """
    
    def __init__(self, settings_config=None, parent=None):
        super(SettingsWidget, self).__init__(parent)
        
        self.settings_config = settings_config or []
        self.settings_widgets = {}  # Store references to the created widgets
        
        self.setupUi()
        self.loadSettings()
    
    def setupUi(self):
        """Initialize the main layout as a form layout"""
        self.main_layout = QVBoxLayout(self)
        
        # Create scroll area to handle many settings
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Create the settings container widget
        self.settings_container = QWidget()
        self.form_layout = QFormLayout(self.settings_container)
        
        # Set the container as the scroll area widget
        self.scroll_area.setWidget(self.settings_container)
        
        # Add scroll area to main layout
        self.main_layout.addWidget(self.scroll_area)
    
    def setSettingsConfig(self, settings_config):
        """Set the settings configuration and rebuild the UI"""
        self.settings_config = settings_config
        self.clearSettings()
        self.loadSettings()
    
    def loadSettings(self):
        """Load settings from the configuration and create appropriate widgets"""
        if not self.settings_config:
            return
        
        for setting in self.settings_config:
            self.createSettingWidget(setting)
    
    def createSettingWidget(self, setting):
        """Create a widget based on the setting configuration"""
        setting_name = setting.get("setting_name", "")
        setting_type = setting.get("type", "")
        default_value = setting.get("default_value", "")
        
        if setting_type == "title":
            self.createTitleWidget(setting_name, default_value)
        elif setting_type == "checkbox":
            self.createCheckboxWidget(setting_name, default_value)
        elif setting_type == "lineedit":
            self.createLineEditWidget(setting_name, default_value)
        elif setting_type == "combobox":
            options = setting.get("options", [])
            self.createComboboxWidget(setting_name, default_value, options)
        else:
            print(f"Unknown setting type: {setting_type}")
    
    def createTitleWidget(self, setting_name, default_value):
        """Create a title/label widget"""
        title_label = QLabel(str(default_value))
        
        # Set the font to bold
        title_label.setFont(QFont("Arial", 14, QFont.Bold))

        # Add the title to the form layout spanning both columns
        self.form_layout.addRow("", title_label)  # Empty widget as second parameter
        
        # Store reference (titles don't have editable values, but we store them for consistency)
        self.settings_widgets[setting_name] = {
            "widget": title_label,
            "type": "title",
            "get_value": lambda: str(default_value)
        }
    
    def createCheckboxWidget(self, setting_name, default_value):
        """Create a checkbox widget"""
        checkbox = QCheckBox()
        checkbox.setChecked(bool(default_value))
        
        self.form_layout.addRow(setting_name, checkbox)
        
        # Store reference
        self.settings_widgets[setting_name] = {
            "widget": checkbox,
            "type": "checkbox",
            "get_value": lambda: checkbox.isChecked()
        }
    
    def createLineEditWidget(self, setting_name, default_value):
        """Create a line edit widget"""
        line_edit = QLineEdit()
        line_edit.setText(str(default_value))
        
        self.form_layout.addRow(setting_name, line_edit)
        
        # Store reference
        self.settings_widgets[setting_name] = {
            "widget": line_edit,
            "type": "lineedit",
            "get_value": lambda: line_edit.text()
        }
    
    def createComboboxWidget(self, setting_name, default_value, options):
        """Create a combobox widget"""
        combobox = QComboBox()
        
        # Add options to combobox
        for option in options:
            combobox.addItem(str(option))
        
        # Set default selection
        if default_value in options:
            index = options.index(default_value)
            combobox.setCurrentIndex(index)
        
        self.form_layout.addRow(setting_name, combobox)
        
        # Store reference
        self.settings_widgets[setting_name] = {
            "widget": combobox,
            "type": "combobox",
            "get_value": lambda: combobox.currentText()
        }
    
    def getSettings(self):
        """Get all settings values as a dictionary"""
        settings_values = {}
        
        for setting_name, widget_info in self.settings_widgets.items():
            try:
                value = widget_info["get_value"]()
                settings_values[setting_name] = value
            except Exception as e:
                print(f"Error getting value for {setting_name}: {e}")
                settings_values[setting_name] = None
        
        return settings_values
    
    def getSettingsAsJson(self):
        """Get all settings values as a JSON string"""
        settings_values = self.getSettings()
        return json.dumps(settings_values, indent=2)
    
    def setSettingsFromDict(self, settings_dict):
        """Set settings values from a dictionary"""
        for setting_name, value in settings_dict.items():
            if setting_name in self.settings_widgets:
                widget_info = self.settings_widgets[setting_name]
                widget = widget_info["widget"]
                widget_type = widget_info["type"]
                
                try:
                    if widget_type == "checkbox":
                        widget.setChecked(bool(value))
                    elif widget_type == "lineedit":
                        widget.setText(str(value))
                    elif widget_type == "combobox":
                        index = widget.findText(str(value))
                        if index >= 0:
                            widget.setCurrentIndex(index)
                    # Title widgets are not editable
                except Exception as e:
                    print(f"Error setting value for {setting_name}: {e}")
    
    def setSettingsFromJson(self, json_string):
        """Set settings values from a JSON string"""
        try:
            settings_dict = json.loads(json_string)
            self.setSettingsFromDict(settings_dict)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
    
    def clearSettings(self):
        """Clear all settings widgets"""
        # Clear the form layout
        while self.form_layout.count():
            child = self.form_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Clear the settings widgets dictionary
        self.settings_widgets.clear()
    
    def addSetting(self, setting_config):
        """Add a single setting to the existing configuration"""
        self.settings_config.append(setting_config)
        self.createSettingWidget(setting_config)
    
    def removeSetting(self, setting_name):
        """Remove a setting by name"""
        # Remove from configuration
        self.settings_config = [s for s in self.settings_config if s.get("setting_name") != setting_name]
        
        # Rebuild the UI
        self.clearSettings()
        self.loadSettings()


class SettingsDialog(QDialog):
    """
    A dialog wrapper for the SettingsWidget.
    Provides OK/Cancel buttons and easy integration.
    """
    
    def __init__(self, settings_config=None, title="Settings", parent=None):
        super(SettingsDialog, self).__init__(parent)
        
        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(500, 600)
        
        self.setupUi()
        
        # Create and add the settings widget
        self.settings_widget = SettingsWidget(settings_config, self)
        self.main_layout.insertWidget(0, self.settings_widget)
    
    def setupUi(self):
        """Setup the dialog UI"""
        self.main_layout = QVBoxLayout(self)
        
        # Button layout
        self.button_layout = QHBoxLayout()
        
        self.btn_ok = QPushButton("OK")
        self.btn_ok.clicked.connect(self.accept)
        
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.clicked.connect(self.reject)
        
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.btn_ok)
        self.button_layout.addWidget(self.btn_cancel)
        
        self.main_layout.addLayout(self.button_layout)
    
    def getSettings(self):
        """Get settings from the widget"""
        return self.settings_widget.getSettings()
    
    def getSettingsAsJson(self):
        """Get settings as JSON string"""
        return self.settings_widget.getSettingsAsJson()
    
    def setSettings(self, settings_dict):
        """Set settings in the widget"""
        self.settings_widget.setSettingsFromDict(settings_dict)


# Example usage and test function
def test_settings_widget():
    """Test function to demonstrate the SettingsWidget"""
    app = QApplication([])
    
    # Example configuration
    settings_config = [
        {
            "setting_name": "title_0",
            "type": "title",
            "default_value": "General Settings"
        },
        {
            "setting_name": "Setting 1",
            "type": "checkbox",
            "default_value": True
        },
        {
            "setting_name": "Setting 2",
            "type": "lineedit",
            "default_value": "Default text"
        },
        {
            "setting_name": "Setting 3",
            "type": "combobox",
            "default_value": "Option 1",
            "options": ["Option 1", "Option 2", "Option 3"]
        },
        {
            "setting_name": "title_1",
            "type": "title",
            "default_value": "Advanced Settings"
        },
        {
            "setting_name": "Enable Debug Mode",
            "type": "checkbox",
            "default_value": False
        },
        {
            "setting_name": "Output Directory",
            "type": "lineedit",
            "default_value": "C:/Output"
        },
        {
            "setting_name": "Render Quality",
            "type": "combobox",
            "default_value": "High",
            "options": ["Low", "Medium", "High", "Ultra"]
        }
    ]
    
    # Test with dialog
    dialog = SettingsDialog(settings_config, "Test Settings")
    
    if dialog.exec_() == QDialog.Accepted:
        # Print the settings values
        settings = dialog.getSettings()
        print("Settings values:")
        for key, value in settings.items():
            print(f"  {key}: {value}")
        
        print("\nSettings as JSON:")
        print(dialog.getSettingsAsJson())
    
    app.quit()


if __name__ == "__main__":
    test_settings_widget()
