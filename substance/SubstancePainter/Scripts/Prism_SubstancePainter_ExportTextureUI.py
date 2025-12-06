import os
import json 

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from PySide6.QtCore import Qt
import sys

import substance_painter.textureset
import substance_painter.ui

# Get the type used by flags in this Qt binding
FLAG_TYPE = type(QTreeWidgetItem().flags())

# --- Cross-version compatibility for Qt item flags ---
def _get_flag(name, default_value):
    """Try to get a flag from Qt, else fallback to int and cast to FLAG_TYPE."""
    for path in [name, f"ItemFlag.{name}"]:
        try:
            parts = path.split('.')
            obj = Qt
            for p in parts:
                obj = getattr(obj, p)
            return FLAG_TYPE(obj)
        except AttributeError:
            pass
    return FLAG_TYPE(default_value)

ITEM_IS_TRISTATE = _get_flag("ItemIsTristate", 0x00000020)
ITEM_IS_USER_CHECKABLE = _get_flag("ItemIsUserCheckable", 0x00000010)
ITEM_IS_SELECTABLE = _get_flag("ItemIsSelectable", 0x00000001)


class TextureExportUI(QDialog):
    def __init__(self, parent, core):
        super().__init__(parent)
        self.setWindowTitle("Texture Export")
        self.resize(600, 500)

        self.core = core

        main_layout = QVBoxLayout(self)

        # --- Top form layout ---
        form_layout = QFormLayout()
        self.identifier_edit = QComboBox()
        self.identifier_edit.setEditable(True)
        self.identifier_edit.setCurrentText("texturing")

        currentFileName = self.core.appPlugin.getCurrentFileName(self.core)
        dataPath = currentFileName[:-4] + "versioninfo.json"
        if os.path.exists(dataPath):
            with open(dataPath, 'r') as f:
                data = json.load(f)
        else:
            data = {}
        products = self.core.products.getProductNamesFromEntity(data)

        for product in products:
            #check if the product is texturing related
            productPath = self.core.products.getProductPathFromEntity(data, product)
            productPath = productPath.split(os.sep)
            productPath[-1] = product
            productPath.append(os.sep + "master" + os.sep + "versioninfo.json")
            productPath = os.sep.join(productPath)
            with open(productPath, 'r') as f:
                productData = json.load(f)
            try:
                if productData["sourceScene"].endswith(".spp"):    
                    self.identifier_edit.addItem(product)
                else:
                    print("Skipping product ", product, " as it is not a texturing product")
            except:
                pass

        self.comment_edit = QLineEdit()
        self.use_next_version = QCheckBox("Version Up")
        self.version_comboBox = QComboBox()
        self.createVersion()
        self.location_combo = QComboBox()
        self.location_combo.addItems(["Global", "Local"])

        form_layout.addRow("Product Name:", self.identifier_edit)
        form_layout.addRow("Comment:", self.comment_edit)
        form_layout.addRow(self.use_next_version, self.version_comboBox)
        form_layout.addRow("Location:", self.location_combo)

        main_layout.addLayout(form_layout)

        # Spacer between Location and Texture Options
        main_layout.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # --- Texture Options group ---
        pen_icon = self.style().standardIcon(QStyle.SP_FileDialogDetailedView)  # or any icon close to a pen

        self.preset_check = QCheckBox("Preset")

        self.preset_combo = QComboBox()
        self.populatePreset()
        self.edit_preset_btn = QPushButton("")
        self.edit_preset_btn.setIcon(pen_icon)

        child_layout = QHBoxLayout()
        child_layout.addWidget(self.preset_combo)
        child_layout.addWidget(self.edit_preset_btn)

        self.res_combo = QComboBox()
        self.res_combo.addItems(["256x256", "512x512", "1024x1024", "2048x2048", "4096x4096", "8192x8192"])

        tex_opts_layout = QFormLayout()
        tex_opts_layout.addRow(self.preset_check, child_layout)
        tex_opts_layout.addRow("Resolution:", self.res_combo)

        main_layout.addLayout(tex_opts_layout)

        # --- Tree widget ---
        self.texture_tree = QTreeWidget()
        self.texture_tree.setHeaderLabels(["Texture", "Format", "Bits"])
        main_layout.addWidget(self.texture_tree)

        # Spacer between tree and Export button
        main_layout.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # --- Export button ---
        self.export_btn = QPushButton("Export")
        main_layout.addWidget(self.export_btn)

        # Populate tree (stub function)
        self.populate_texture_tree()

        #connection
        self.use_next_version.toggled.connect(self.toggle_version_option)
        self.preset_check.toggled.connect(self.toggle_preset_option)

        #init state
        self.toggle_version_option(self.use_next_version.isChecked())
        self.toggle_preset_option(self.preset_check.isChecked())
    
    def populatePreset(self):
        # Retrieve all predefined export presets
        predefined_presets = substance_painter.export.list_predefined_export_presets()
        # Retrieve all resource export presets
        resource_presets = substance_painter.export.list_resource_export_presets()
        for preset in predefined_presets:
            self.preset_combo.addItem(preset.name)
        for preset in resource_presets:
            self.preset_combo.addItem(preset.resource_id.name)

    def toggle_version_option(self, checked):
        self.version_comboBox.setEnabled(not checked)

    def toggle_preset_option(self, checked):
        self.preset_combo.setEnabled(checked)
        self.edit_preset_btn.setEnabled(checked)

    def createVersion(self):
        #clear the combo
        self.version_comboBox.clear()
        #read the json file of the current scene to get the next available version
        currentFileName = self.core.appPlugin.getCurrentFileName(self.core)
        jsonPath = os.path.splitext(currentFileName)[0] + "versioninfo.json"
        with open(jsonPath, "r") as f:
            entity = json.load(f)

        products = self.core.products.getProductNamesFromEntity(entity)
        product = self.identifier_edit.currentText()
        exists = False
        for prod in products:
            if prod == product:
                exists = True
                break
        if exists:
            nextVersion = self.core.products.getNextAvailableVersion(entity, product)
            version = int(nextVersion[1:]) -1 # remove the "v" prefix and convert to int
        else:
            version = 1

        items = []
        for i in range(version):
            items.append("v" + str(i+1).zfill(4))
        self.version_comboBox.addItems(items)

    def populate_texture_tree(self, preset=None):
        texture_data = self.get_texture_maps(preset)

        for material_name, maps in texture_data.items():
            material_item = QTreeWidgetItem([material_name, "", ""])
            material_item.setFlags(material_item.flags() | ITEM_IS_USER_CHECKABLE | ITEM_IS_TRISTATE | ITEM_IS_SELECTABLE)
            material_item.setCheckState(0, Qt.Checked)
            self.texture_tree.addTopLevelItem(material_item)

            for map_name in maps:
                if preset:
                    map_name = eval("{\"baseColor\":"+map_name)  # Convert string representation back to dictionary
                    if "(" in map_name["fileName"]:
                        name = map_name["fileName"].split("_")[2][:-1]
                    else:
                        name = map_name["fileName"].replace("$textureSet", material_name).split("/")[-1][len(material_name)+1:]  # Extract the map name from the preset structure
                else:
                    name = map_name
                map_item = QTreeWidgetItem([name, "", ""])
                map_item.setFlags(map_item.flags() | ITEM_IS_USER_CHECKABLE | ITEM_IS_SELECTABLE)
                map_item.setCheckState(0, Qt.Checked)

                format_combo = QComboBox()
                format_combo.addItems(["png", "jpg", "tiff", "exr"])
                if preset:
                    #set the format according to the preset
                    format_combo.setCurrentText(map_name["parameters"]["fileFormat"])

                bit_combo = QComboBox()
                bit_combo.addItems(["8 bit", "8 bit + dithering", "16 bit", "16f bit", "32f bit"])
                if preset:
                    #set the bit depth according to the preset
                    dithering = map_name["parameters"]["dithering"]
                    if dithering:
                        bit_combo.setCurrentText("8 bit + dithering")
                    else:
                        bit_combo.setCurrentText(map_name["parameters"]["bitDepth"] + " bit")

                material_item.addChild(map_item)
                self.texture_tree.setItemWidget(map_item, 1, format_combo)
                self.texture_tree.setItemWidget(map_item, 2, bit_combo)


    def on_item_changed(self, item: QTreeWidgetItem, column: int):
        if item.childCount() > 0:
            parent_state = item.checkState(0)
            for i in range(item.childCount()):
                child = item.child(i)
                child.setCheckState(0, parent_state)
                self._set_item_widgets_enabled(child, parent_state == Qt.Checked)
        else:
            self._set_item_widgets_enabled(item, item.checkState(0) == Qt.Checked)

    def _set_item_widgets_enabled(self, item: QTreeWidgetItem, enabled: bool):
        fmt_widget = self.texture_tree.itemWidget(item, 1)
        res_widget = self.texture_tree.itemWidget(item, 2)
        if fmt_widget:
            fmt_widget.setEnabled(enabled)
        if res_widget:
            res_widget.setEnabled(enabled)

    def get_texture_maps(self, preset=None):
        #let's build a list that assemble all the texture set and their stack 
        textureData = {}

        # List all the Texture Sets: 
        allTextureSet = substance_painter.textureset.all_texture_sets()

        for texture_set in allTextureSet: 

            stacks = texture_set.all_stacks()
            allStacks = []
            for stack in stacks :
                if not preset:
                    dictChannels = stack.all_channels()
                else:
                    try:
                        dictChannels = preset.list_output_maps(stack)
                    except :
                        dictChannels = preset.list_output_maps()              
                for channelType in dictChannels:
                    allStacks.append(str(channelType)[12:])

            textureSetName = texture_set.name()

            textureData[textureSetName] = allStacks

        return textureData

    def __del__(self):
        print("Texture Export UI has been deleted !")