from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *
import os
import json
from src.ui.SelectProductsWidget import SelectProductWidget


class VariantTreeWidget(QTreeWidget):
    """
    Custom QTreeWidget that accepts drops.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.pparent = parent

    def dropEvent(self, event):
        if self.is_drop_accepted(event):
            super().dropEvent(event)
        else:
            event.ignore()

    def is_drop_accepted(self, event):
        # Get the item
        item = self.itemAt(event.pos())

        if item:
            
            self.pparent.addProductToVariantTree([event.source().currentItem()], item)
                
        return False



class AssignVariantsDialog(QDialog):
    
    """
    This dialog is used to asign products to variants.
    One variant is composed of :
        - One Geometry Low 
        - One Geometry High
        - One Surfacing
    
    """

    def __init__(self, core, pluggin_parent, parent=None):
        super(AssignVariantsDialog, self).__init__(parent)
        self.core = core
        self.pluggin_parent = pluggin_parent
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Assign Variants")
        self.setMinimumWidth(400)
        self.setModal(True)

        self.main_layout = QVBoxLayout(self)

        self.splitter = QSplitter(Qt.Horizontal, self)

        # Left : Create the product to import widget at the left of the splitter
        self.product_import_widget = SelectProductWidget(self.core, self.pluggin_parent)
        self.product_import_widget.OnItemDoubleClicked.connect(self.onLeftItemDoubleClicked)
        self.splitter.addWidget(self.product_import_widget)


        # Right : Create a layout that contains a treeWidget, and a bunch of buttons
        self.right_container_widget = QWidget(self)
        self.vertical_layout = QVBoxLayout(self.right_container_widget)

        # Tree widget
        self.variant_tree = VariantTreeWidget(parent = self)
        self.variant_tree.setHeaderLabels(["Variant name", "Format"])
        self.vertical_layout.addWidget(self.variant_tree)


        # Buttons layout (horizontal)
        self.right_buttons_layout = QHBoxLayout()

        #Add  button (from left to right)
        self.btn_add = QPushButton("")
        self.btn_add.setIcon(self.pluggin_parent.getIcon("arrow_right.png"))
        self.btn_add.setToolTip("Add selected products to the right tree")
        self.btn_add.clicked.connect(self.onAddItemClicked)
        self.right_buttons_layout.addWidget(self.btn_add)

        # Remove an item button
        self.btn_remove = QPushButton("")
        self.btn_remove.setIcon(self.pluggin_parent.getIcon("remove.png"))
        self.btn_remove.setToolTip("Remove selected products from the right tree")
        self.btn_remove.clicked.connect(self.onRemoveButtonClicked)
        self.right_buttons_layout.addWidget(self.btn_remove)


        # Create variant button
        self.btn_create_variant = QPushButton("")
        self.btn_create_variant.setIcon(self.pluggin_parent.getIcon("add_cross.png"))
        self.btn_create_variant.setToolTip("Create a new variant")
        self.btn_create_variant.clicked.connect(self.createVariant)
        self.right_buttons_layout.addWidget(self.btn_create_variant)



        self.vertical_layout.addLayout(self.right_buttons_layout)
        self.splitter.addWidget(self.right_container_widget)
        self.main_layout.addWidget(self.splitter)

        # Dialog buttons (Accept/Cancel) at the bottom, using custom QPushButton
        self.dialog_buttons_layout = QHBoxLayout()




        # Dialog's accept button
        self.accept_button = QPushButton("OK")
        self.accept_button.setIcon(self.pluggin_parent.getIcon("check.png"))
        self.accept_button.clicked.connect(self.onAcceptBtnPressed)


        # Dialog's cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setIcon(self.pluggin_parent.getIcon("cancel.png"))
        self.cancel_button.clicked.connect(self.reject)



        self.dialog_buttons_layout.addStretch()
        self.dialog_buttons_layout.addWidget(self.accept_button)
        self.dialog_buttons_layout.addWidget(self.cancel_button)
        self.main_layout.addLayout(self.dialog_buttons_layout)

        self.setLayout(self.main_layout)


        # ACTIONS :

        # Add action : add a variant when click "+"
        self.create_variant_action = QAction(self)
        self.create_variant_action.setIcon(self.pluggin_parent.getIcon("add_cross.png"))
        self.create_variant_action.setToolTip("Create a new variant")
        self.create_variant_action.setShortcut(QKeySequence("+"))
        self.create_variant_action.triggered.connect(self.createVariant)
        self.addAction(self.create_variant_action)

        # Remove action : remove the selected item when click suppr
        self.remove_variant_action = QAction(self)
        self.remove_variant_action.setIcon(self.pluggin_parent.getIcon("remove.png"))
        self.remove_variant_action.setToolTip("Remove the selected variant")
        self.remove_variant_action.setShortcut(QKeySequence("Delete"))
        self.remove_variant_action.triggered.connect(self.onRemoveButtonClicked)
        self.addAction(self.remove_variant_action)

    # Setup from a given entity
    def setupFromEntity(self, entity):
        self.navigate(entity)
        self.current_entity = entity

    # Create a new variant and append it to the end of the list
    def createVariant(self):
        # Add a variant to the variant tree.
        # It consist of a treeWidgetItem that is named by it's index in the list
        item = QTreeWidgetItem(self.variant_tree)
        item.setWhatsThis(0,"folder")
        item.setIcon(0, self.pluggin_parent.getIcon("folder.png"))
        self.variant_tree.addTopLevelItem(item)

        # Add three 'subfolder' : Modeling Low, Modeling High and Surfacing
        mod_low_item = QTreeWidgetItem(item)
        mod_low_item.setText(0, "Modeling Low")
        mod_low_item.setWhatsThis(0,"Modeling_Low_grp")
        mod_low_item.setIcon(0, self.pluggin_parent.getIcon("Modeling Low.png"))
        item.addChild(mod_low_item)

        mod_high_item = QTreeWidgetItem(item)
        mod_high_item.setText(0, "Modeling High")
        mod_high_item.setWhatsThis(0,"Modeling_High_grp")
        mod_high_item.setIcon(0, self.pluggin_parent.getIcon("Modeling High.png"))
        item.addChild(mod_high_item)

        surfacing_item = QTreeWidgetItem(item)
        surfacing_item.setText(0, "Surfacing")
        surfacing_item.setWhatsThis(0,"Surfacing_grp")
        surfacing_item.setIcon(0, self.pluggin_parent.getIcon("Surfacing.png"))
        item.addChild(surfacing_item)

        self.updateVariantNames()

    
    # When you double-click an item in the left tree, add it to the right tree
    def onLeftItemDoubleClicked(self, item):

        right_item = self.variant_tree.currentItem()

        if not right_item:
            return
        
        # ignore if the item is a group
        if "_grp" in right_item.whatsThis(0):
            return

        """ When an item in the left tree is double clicked, add it to the right tree """
        self.addProductToVariantTree([item], right_item)


    # Update the variant names in the tree.
    def updateVariantNames(self):
        # Update the variant names in the tree.
        # This rename the variants (top level item) of the tree widget to their index.
        # If there is only one item, sets the name to "default"
        for i in range(self.variant_tree.topLevelItemCount()):
            item = self.variant_tree.topLevelItem(i)
            item.setText(0, f"variant_{i}" if self.variant_tree.topLevelItemCount() > 1 else "default")

            # If there is only one item, sets the name to "default"
            if self.variant_tree.topLevelItemCount() == 1:
                item.setText(0, "default")

    def remove_all_children(self,item):
        for child in item.takeChildren():
            del child  # Explicitly delete the child to free memory

    def navigate(self, entity):
        self.product_import_widget.navigate(entity)

    # Add a product from the left to the right (selectProducts to right_selected_item)
    def addProductToVariantTree(self, left_products, right_parent):
        
        
        # Add the item inside of the right selected item
        for item in left_products:


            # If the right parent is type "product"
            if right_parent.whatsThis(0) == "product":
                right_parent = right_parent.parent()

            # If the right_parent is a top_level_item, we need to find the correct parent
            if right_parent.parent() is None:
                left_item_settings = item.toolTip(0)
                left_item_settings = json.loads(left_item_settings)

                path = left_item_settings.get("path", "")
                path = path.lower()
                if(path == ""):
                    QMessageBox.warning(self, "Invalid Product", f"The product '{item.text(0)}' does not have a path.")
                    continue # Continue if path is empty

                if("modl" in path):
                    # Add the item to the modeling low group
                    right_parent = right_parent.child(0) # Modeling Low
                    self.remove_all_children(right_parent)
                    right_parent.addChild(item.clone())
                    continue
                elif("modh" in path):
                    # Add the item to the modeling high group
                    right_parent = right_parent.child(1) # Modeling High
                    self.remove_all_children(right_parent)
                    right_parent.addChild(item.clone())
                    continue
                elif("surf" in path):
                    # Add the item to the surfacing group
                    right_parent = right_parent.child(2) # Surfacing
                    self.remove_all_children(right_parent)
                    right_parent.addChild(item.clone())
                    continue
                else:
                    QMessageBox.warning(self, "Invalid Product", f"The product '{item.text(0)}' does not have a recognized path. It should contain 'modl', 'modh' or 'surf' in its path.")
                    continue # Continue if path is not recognized

            else :
                self.remove_all_children(right_parent)
                right_parent.addChild(item.clone())


    # Add the selected product to the right tree widget
    def onAddItemClicked(self):
        """ When the add button is pressed """

        ## Get the selected items from both trees
        left_selected_items = self.product_import_widget.getSelectedItems()
        right_selected_items = self.variant_tree.selectedItems()

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
        self.addProductToVariantTree(left_selected_items, right_selected_item)
        

    # Remove the selected item in the right tree
    def onRemoveButtonClicked(self):
        right_item = self.variant_tree.currentItem()

        if not right_item:
            return

        if right_item.parent() is None:
            # Top level item
            index = self.variant_tree.indexOfTopLevelItem(right_item)
            self.variant_tree.takeTopLevelItem(index)
            self.updateVariantNames()
        else:
            # Remove the item
            right_item.parent().removeChild(right_item)

    def getItemProductPath(self, product):
        if product and product.whatsThis(0) == "product":
            product_settings = product.toolTip(0)
            product_settings = json.loads(product_settings)
            path = product_settings.get("path", "")
            path = path.replace("\\", "/")
            return path
        return ""

    def getResult(self):
        variants = []

        for i in range(self.variant_tree.topLevelItemCount()):
            item = self.variant_tree.topLevelItem(i)
            variant = {
                "geometry_low":  self.getItemProductPath(item.child(0).child(0))  if item.child(0).childCount() > 0 else "",
                "geometry_high": self.getItemProductPath(item.child(1).child(0))  if item.child(1).childCount() > 0 else "",
                "surfacing":     self.getItemProductPath(item.child(2).child(0))  if item.child(2).childCount() > 0 else ""
            }
            variants.append(variant)

        result = {"variants": variants}
        return result

    def onAcceptBtnPressed(self) :
        print(json.dumps(self.getResult(), indent=4))
        self.accept()