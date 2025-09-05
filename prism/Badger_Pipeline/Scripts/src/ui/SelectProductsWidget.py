from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *
import os
import json

import EntityWidget


from qtpy.QtCore import Signal



class SelectProductWidget(QWidget):

    # Signaux personnalisés
    OnItemClicked = Signal(QTreeWidgetItem, int)
    OnItemDoubleClicked = Signal(QTreeWidgetItem, int)

    
    """
    Widget that allow the user to select a product in the pipeline
    """

    def __init__(self, core, pluggin_parent, parent=None):
        super(SelectProductWidget, self).__init__(parent)
        
        self.core = core
        self.pluggin_parent = pluggin_parent
        
        self.setupUi()
        

    # Setup the UI
    def setupUi(self) :
        # Main Splitter
        self.splitter = QSplitter(Qt.Vertical, self)

        # w_entities is the prism widget that allow the user to select an entity.
        self.w_entities = EntityWidget.EntityWidget(core=self.core, refresh=True)

        self.w_entities.getPage("Assets").itemChanged.connect(self.onSelectedEntityChanged)
        self.w_entities.getPage("Shots").itemChanged.connect(self.onSelectedEntityChanged)

        # Make sure that we can only select one item
        self.w_entities.getPage("Assets").tw_tree.setSelectionMode(QAbstractItemView.SingleSelection)
        self.w_entities.getPage("Shots").tw_tree.setSelectionMode(QAbstractItemView.SingleSelection)

        # Left Tree widget
        self.available_tree = QTreeWidget(self.splitter)
        self.available_tree.setHeaderLabels(["Product name" , "Format" , "Asset"])

        # Enable drag for available_tree
        self.available_tree.setDragEnabled(True)
        self.available_tree.setSelectionMode(QAbstractItemView.SingleSelection)
        self.available_tree.setDragDropMode(QAbstractItemView.DragOnly)

        # Connect item click/double click signals
        self.available_tree.itemClicked.connect(self.OnItemClicked.emit)
        self.available_tree.itemDoubleClicked.connect(self.OnItemDoubleClicked.emit)

        # Add the widgets to the splitter
        self.splitter.addWidget(self.w_entities)
        self.splitter.addWidget(self.available_tree)

        # Set the layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.splitter)
        self.setLayout(layout)

    def navigate(self, entity):
        self.w_entities.navigate(entity)

    # When the selected entity changes
    # Pupulate the Tree 
    def onSelectedEntityChanged(self, item=None):
        if item:
            entities = [self.w_entities.getCurrentPage().getDataFromItem(item)]
            self.refreshAvailableTree(entities)

        else:
            self.refreshAvailableTree()


    # Refresh the tree by clearing and repopulating it 
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

    # Populate the tree from an entity.
    # Search for the products inside the tree and create the item that corresponds to its
    def populateAvailableTreeFromEntity(self, entity):

        # Get all the available products from the entity
        products = self.core.products.getProductsFromEntity(entity)

        for product in products:
            treeWidgetItem = self.createItemFromProduct(product, self.available_tree)
            self.available_tree.addTopLevelItem(treeWidgetItem)
    


    # Create an item that corresponds to the given product. 
    # Add it to the given tree
    def createItemFromProduct(self, product , tree = None) :
        
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
        

        treeWidgetItem = None
        if tree:
            treeWidgetItem = QTreeWidgetItem(tree)
        else:
            treeWidgetItem = QTreeWidgetItem()
        treeWidgetItem.setText(0, product["product"])
        treeWidgetItem.setText(1, pformat)
        if "asset" in product:
            treeWidgetItem.setText(2, product["asset"])
        elif "shot" in product:
            treeWidgetItem.setText(2, product["shot"])
        else:
            treeWidgetItem.setText(2, "")
        treeWidgetItem.setWhatsThis(0, "product")

        # Convert the product to json str
        product_str = json.dumps(product)
        treeWidgetItem.setData(0, Qt.UserRole, product_str)
        treeWidgetItem.setToolTip(0, product_str)

        # Set the icon according to if the product is a export or a publish
        if("_Publish" in product["product"]):
            treeWidgetItem.setIcon(0, self.pluggin_parent.getIcon("publish.png"))
        else:
            treeWidgetItem.setIcon(0, self.pluggin_parent.getIcon("other.png")) 
        
        return treeWidgetItem


    # Get the list of select TreeWidgetItem
    def getSelectedItems(self):
        return self.available_tree.selectedItems()