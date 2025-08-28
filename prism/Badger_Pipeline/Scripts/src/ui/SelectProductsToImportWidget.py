from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *


from src.ui.SelectProductsWidget import SelectProductWidget
import os
import json




class SelectedTreeWidget(QTreeWidget):
    """
    Custom QTreeWidget that accepts drops.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.pparent = parent

    # Handle the drop event
    def dropEvent(self, event):
        if self.is_drop_accepted(event):
            super().dropEvent(event)
        else:
            event.ignore()

    # When an item is dropped
    def is_drop_accepted(self, event):
        # Get the item
        item = self.itemAt(event.pos())
        if item:

            # If the item is a group
            if item.whatsThis(0) == "folder":
                self.pparent.addProductToSelectedTree([event.source().currentItem().clone()], item)

                return False  # Return false because we manualy copied the item
            else:
                # Try to get the parent of the item
                item = item.parent()
                if item and item.whatsThis(0) == "folder":
                    # Manualy Copy the pasted item in the folder
                    # Otherwise the item will be placed into the child and not the folder
                    self.pparent.addProductToSelectedTree([event.source().currentItem().clone()], item)

                    return False  # Return false because we manualy copied the item
                
        return False
    


class SelectProductsToImportWidget(QWidget):

    """
    Widget that allows the user to select products to import before the scenes are created.
    It consist of a SelectProductWidget, and a tree widget to display the selected products.
    Both widgets are placed in a splitter.

    Under the treewidget, are three buttons : One to add the selected product at the left , 
        to the selected item in the right tree widget.
        - One to remove the selected item at the right
        - One to clear the items
    """

    def __init__(self, core, pluggin_parent, parent=None):
        super(SelectProductsToImportWidget, self).__init__(parent)

        self.core = core
        self.pluggin_parent = pluggin_parent

        self.setupUi()

    # Setup the UI
    def setupUi(self):
        # Main splitter
        self.splitter = QSplitter(Qt.Horizontal, self)

        # Left: SelectProductWidget
        self.select_product_widget = SelectProductWidget(core=self.core, pluggin_parent=self.pluggin_parent)
        self.select_product_widget.OnItemDoubleClicked.connect(self.onLeftItemDoubleClicked)
        self.splitter.addWidget(self.select_product_widget)

        # Right: Container widget with vertical layout (tree + buttons)
        self.right_container_widget = QWidget(self)
        self.vertical_layout = QVBoxLayout(self.right_container_widget)

        # Tree widget
        self.selected_tree = SelectedTreeWidget(parent =self)
        self.selected_tree.setHeaderLabels(["Product name", "Format"])
        self.vertical_layout.addWidget(self.selected_tree)

        # Buttons layout (horizontal)
        self.right_buttons_layout = QHBoxLayout()

        self.btn_add = QPushButton("")
        self.btn_add.setIcon(self.pluggin_parent.getIcon("arrow_right.png"))
        self.btn_add.setToolTip("Add selected products to the right tree")
        self.btn_add.clicked.connect(self.onBtnAddItemClicked)
        self.right_buttons_layout.addWidget(self.btn_add)

        self.btn_remove = QPushButton("")
        self.btn_remove.setIcon(self.pluggin_parent.getIcon("remove.png"))
        self.btn_remove.setToolTip("Remove selected products from the right tree")
        self.btn_remove.clicked.connect(self.onBtnRemoveItemClicked)
        self.right_buttons_layout.addWidget(self.btn_remove)

        self.vertical_layout.addLayout(self.right_buttons_layout)

        # Add the right container to the splitter
        self.splitter.addWidget(self.right_container_widget)

        # Main layout
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.splitter)
        self.setLayout(self.main_layout)

    def navigate(self, entity):
        self.select_product_widget.navigate(entity)

    # Get the result of the selection
    def getResult(self):
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

    # When you double-click an item in the left tree, add it to the right tree
    def onLeftItemDoubleClicked(self, item):

        right_item = self.selected_tree.currentItem()

        if not right_item:
            return
        
        if right_item.parent() is not None:
            # Get the parent item
            right_item = right_item.parent()

        # Check if the right_item is a folder
        if right_item.whatsThis(0) != "folder":
            QMessageBox.warning(self, "Invalid Selection", "Please select a folder to add items to.")
            return

        """ When an item in the left tree is double clicked, add it to the right tree """
        self.addProductToSelectedTree([item], right_item)


    # Add the selected product to the right tree widget
    def onBtnAddItemClicked(self):
        """ When the add button is pressed """

        ## Get the selected items from both trees
        left_selected_items = self.select_product_widget.getSelectedItems()
        right_selected_items = self.selected_tree.selectedItems()

        if not left_selected_items:
            QMessageBox.warning(self, "Invalid Selection", "Please select items to add.")
            return

        if not right_selected_items:
            QMessageBox.warning(self, "Invalid Selection", "Please select a folder to add items to.")
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

        # Add the product to the selected tree
        self.addProductToSelectedTree(left_selected_items, right_selected_item)

    def remove_all_children(self,item):
        for child in item.takeChildren():
            del child  # Explicitly delete the child to free memory

    # Add a product from the left to the right (selectProducts to right_selected_item
    def addProductToSelectedTree(self, left_products, right_parent):
        # Check if the right_selected_item has settings
        settings = right_parent.toolTip(0)

        # Add the item inside of the right selected item
        for item in left_products:
            if settings:
                # Parse the settings from json
                settings = json.loads(settings)

                # if the settings where successfully parsed
                if settings:

                    # If there is the settings "select_only_one_file" and if it is set to True,
                    # We clear the right_parent childrens
                    if settings.get("select_only_one_file", False):
                        self.remove_all_children(right_parent)


                    # If there is the setting "accepted_files", we check if the left_product 's extension
                    # match one of the accepted extensions
                    if "accepted_files" in settings:
                        accepted_files = settings["accepted_files"]
                        left_extension = item.text(1)
                        if left_extension not in accepted_files:
                            QMessageBox.warning(self, "Invalid File Type", f"The file type '{left_extension}' is not accepted.")
                            return

            right_parent.addChild(item.clone())

    # Remove the selected product from the right tree widget
    def onBtnRemoveItemClicked(self):
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




    # Fill the right container with the default selected products (initialisation)
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
                settings_str =  json.dumps(settings)
                treeWidgetItem.setToolTip(0, settings_str)

                if "select_only_one_file" in settings and settings["select_only_one_file"]:
                    treeWidgetItem.setText(1,"(Single file)")
                if "accepted_files" in settings:
                    exts = settings["accepted_files"]
                    treeWidgetItem.setText(1, treeWidgetItem.text(1) + " (." + ", .".join(exts) + ")")

                if "required" in settings and settings["required"]:
                    treeWidgetItem.setText(0, treeWidgetItem.text(0) + " *")

            # If there are child items
            if "items" in product:
                items = product["items"]
                for item in items:
                    treeWidgetItem_child = self.select_product_widget.createItemFromProduct(item, treeWidgetItem)
                    treeWidgetItem.addChild(treeWidgetItem_child)

            self.selected_tree.addTopLevelItem(treeWidgetItem)

