from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *
import os

from src.ui.SelectProductsWidget import SelectProductWidget


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
        self.selected_tree = QTreeWidget()
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

    # Get the result of the selection
    def getResult(self):
        return {}


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

    # Initialise the widgets with the given settings
    def init(self, settings):
        pass


    # Add the selected product to the right tree widget
    def onBtnAddItemClicked(self):
        """ When the add button is pressed """

        ## Get the selected items from both trees
        left_selected_items = self.select_product_widget.getSelectedItems()
        right_selected_items = self.selected_tree.selectedItems()

        if not left_selected_items or not right_selected_items:
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



    # Add a product from the left to the right (selectProducts to right_selected_item
    def addProductToSelectedTree(self, left_products, right_parent):

        # Check if the right_selected_item has settings
        settings = right_parent.toolTip(0)
        if settings:
            # Check if the settings allow to pass (filters)
            pass

        
        # Add the item inside of the right selected item
        for item in left_products:
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


    # Clear all products from the right tree widget (not the folders)
    def onBtnClearItemsClicked(self):
        print("CLEAR")
        # todo


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
                    treeWidgetItem_child = self.select_product_widget.createItemFromProduct(item, treeWidgetItem)
                    treeWidgetItem.addChild(treeWidgetItem_child)

            self.selected_tree.addTopLevelItem(treeWidgetItem)

