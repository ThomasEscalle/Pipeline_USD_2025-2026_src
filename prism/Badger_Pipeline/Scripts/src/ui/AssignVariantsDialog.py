from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *
import os
from src.ui.SelectProductsWidget import SelectProductWidget



class AssignVariantsDialog(QDialog):
    

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
        self.splitter.addWidget(self.product_import_widget)


        # Right : Create a layout that contains a treeWidget, and a bunch of buttons
        self.right_container_widget = QWidget(self)
        self.vertical_layout = QVBoxLayout(self.right_container_widget)

        # Tree widget
        self.variant_tree = QTreeWidget()
        self.variant_tree.setHeaderLabels(["Variant name", "Format"])
        self.vertical_layout.addWidget(self.variant_tree)



        # Buttons layout (horizontal)
        self.right_buttons_layout = QHBoxLayout()

        #Add  button (from left to right)
        self.btn_add = QPushButton("")
        self.btn_add.setIcon(self.pluggin_parent.getIcon("arrow_right.png"))
        self.btn_add.setToolTip("Add selected products to the right tree")
        self.right_buttons_layout.addWidget(self.btn_add)

        # Remove an item button
        self.btn_remove = QPushButton("")
        self.btn_remove.setIcon(self.pluggin_parent.getIcon("remove.png"))
        self.btn_remove.setToolTip("Remove selected products from the right tree")
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

        self.accept_button = QPushButton("OK")
        self.accept_button.clicked.connect(self.accept)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)

        self.dialog_buttons_layout.addStretch()
        self.dialog_buttons_layout.addWidget(self.accept_button)
        self.dialog_buttons_layout.addWidget(self.cancel_button)
        self.main_layout.addLayout(self.dialog_buttons_layout)

        self.setLayout(self.main_layout)

    def createVariant(self):
        # Add a variant to the variant tree.
        # It consist of a treeWidgetItem that is named by it's index in the list
        item = QTreeWidgetItem(self.variant_tree)
        item.setIcon(0, self.pluggin_parent.getIcon("folder.png"))
        self.variant_tree.addTopLevelItem(item)

        self.updateVariantNames()

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