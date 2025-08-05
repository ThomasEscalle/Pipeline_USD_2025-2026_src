from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *
import os


class ProductImportDialog(QDialog):
    """
    Dialog for selecting products to import into a scene.
    Allows drag & drop from available products (left tree) to selected products (right tree).
    """
    
    def __init__(self, available_data=None, selected_data=None, parent=None):
        super(ProductImportDialog, self).__init__(parent)
        
        self.setWindowTitle("Select Products to Import")
        self.setModal(True)
        self.resize(800, 600)
        
        # Initialize data
        self.available_data = available_data or {}
        self.selected_data = selected_data or {}
        
        # Setup UI
        self.setup_ui()
        self.populate_trees()
        
        # Result data
        self.result_data = None
        
    def setup_ui(self):
        """Setup the main UI layout and widgets."""
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Trees container with splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Left side - Available products
        left_widget = QWidget()
        left_container = QVBoxLayout(left_widget)
        left_label = QLabel("Available Products:")
        left_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        left_container.addWidget(left_label)
        
        self.available_tree = QTreeWidget()
        self.available_tree.setHeaderLabel("Available")
        self.available_tree.setDragEnabled(True)
        self.available_tree.setDragDropMode(QAbstractItemView.DragOnly)
        self.available_tree.setDefaultDropAction(Qt.CopyAction)
        left_container.addWidget(self.available_tree)
        
        # Right side - Selected products
        right_widget = QWidget()
        right_container = QVBoxLayout(right_widget)
        right_label = QLabel("Selected Products:")
        right_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        right_container.addWidget(right_label)
        
        self.selected_tree = QTreeWidget()
        self.selected_tree.setHeaderLabel("Selected")
        self.selected_tree.setAcceptDrops(True)
        self.selected_tree.setDragDropMode(QAbstractItemView.DropOnly)
        self.selected_tree.setDefaultDropAction(Qt.CopyAction)
        
        # Set custom item height for groups to be taller
        self.selected_tree.setStyleSheet("""
            QTreeWidget::item {
                height: 24px;
            }
            QTreeWidget::item:has-children {
                height: 30px;
                font-weight: bold;
            }
        """)
        
        right_container.addWidget(self.selected_tree)
        
        # Buttons for selected tree management
        selected_buttons_layout = QHBoxLayout()
        selected_buttons_layout.addStretch()
        
        self.remove_button = QPushButton("-")
        self.remove_button.setMaximumWidth(30)
        self.remove_button.setToolTip("Remove selected item")
        self.remove_button.clicked.connect(self.remove_selected_item)
        selected_buttons_layout.addWidget(self.remove_button)
        
        self.clear_button = QPushButton("Clear")
        self.clear_button.setToolTip("Clear all items (keep groups)")
        self.clear_button.clicked.connect(self.clear_selected_items)
        selected_buttons_layout.addWidget(self.clear_button)
        
        right_container.addLayout(selected_buttons_layout)
        
        # Add widgets to splitter
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        
        # Set equal sizes for both sides initially
        splitter.setSizes([400, 400])
        
        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_button)
        
        self.create_button = QPushButton("Create")
        self.create_button.clicked.connect(self.accept_selection)
        self.create_button.setDefault(True)
        buttons_layout.addWidget(self.create_button)
        
        # Add all to main layout
        main_layout.addWidget(splitter)
        main_layout.addLayout(buttons_layout)
        
        # Setup drag & drop
        self.selected_tree.dragEnterEvent = self.drag_enter_event
        self.selected_tree.dragMoveEvent = self.drag_move_event
        self.selected_tree.dropEvent = self.drop_event
        
    def populate_trees(self):
        """Populate both trees with data."""
        self.populate_available_tree()
        self.populate_selected_tree()
        
    def populate_available_tree(self):
        """Populate the available products tree."""
        self.available_tree.clear()
        
        if "items" in self.available_data:
            for item_data in self.available_data["items"]:
                self._create_tree_item(self.available_tree, item_data)
                
        self.available_tree.expandAll()
        
    def populate_selected_tree(self):
        """Populate the selected products tree."""
        self.selected_tree.clear()
        
        for group_name, group_data in self.selected_data.items():
            group_item = QTreeWidgetItem(self.selected_tree, [group_name])
            
            # Store group configuration in UserRole
            group_config = {"type": "group", "name": group_name}
            
            # Handle both old format (list) and new format (dict with icon)
            if isinstance(group_data, dict):
                # New format with optional icon and constraints
                icon_path = group_data.get("icon")
                if icon_path and os.path.exists(icon_path):
                    group_item.setIcon(0, QIcon(icon_path))
                
                # Store group constraints
                group_config["max_items"] = group_data.get("max_items", None)  # None = unlimited
                group_config["allowed_extensions"] = group_data.get("allowed_extensions", None)  # None = all extensions
                
                items = group_data.get("items", [])
            else:
                # Old format (direct list)
                items = group_data
            
            group_item.setData(0, Qt.UserRole, group_config)
            
            # Add tooltip with group constraints
            tooltip_parts = [f"Group: {group_name}"]
            if group_config.get("max_items"):
                tooltip_parts.append(f"Max items: {group_config['max_items']}")
            else:
                tooltip_parts.append("Max items: Unlimited")
            
            if group_config.get("allowed_extensions"):
                tooltip_parts.append(f"Allowed extensions: {', '.join(group_config['allowed_extensions'])}")
            else:
                tooltip_parts.append("Allowed extensions: All")
            
            group_item.setToolTip(0, "\n".join(tooltip_parts))
            
            for item_data in items:
                if item_data.get("type") == "item":
                    file_path = item_data.get("path", "")
                    file_name = os.path.basename(file_path)
                    child_item = QTreeWidgetItem(group_item, [file_name])
                    child_item.setData(0, Qt.UserRole, file_path)
                    
                    # Add tooltip with full path
                    child_item.setToolTip(0, file_path)
                    
                    # Add icon if provided
                    icon_path = item_data.get("icon")
                    if icon_path and os.path.exists(icon_path):
                        child_item.setIcon(0, QIcon(icon_path))
                    
        self.selected_tree.expandAll()
        
    def _create_tree_item(self, parent, item_data):
        """Recursively create tree items from data structure."""
        if item_data.get("type") == "group":
            group_name = item_data.get("name", "Unknown Group")
            
            # Determine if parent is a tree widget or tree widget item
            if isinstance(parent, QTreeWidget):
                group_item = QTreeWidgetItem(parent, [group_name])
            else:
                group_item = QTreeWidgetItem(parent, [group_name])
                
            group_item.setData(0, Qt.UserRole, {"type": "group", "name": group_name})
            
            # Add icon if provided
            icon_path = item_data.get("icon")
            if icon_path and os.path.exists(icon_path):
                group_item.setIcon(0, QIcon(icon_path))
            
            # Add children
            children = item_data.get("childrens", [])  # Note: using "childrens" as in your example
            for child_data in children:
                self._create_tree_item(group_item, child_data)
                
        elif item_data.get("type") == "item":
            file_path = item_data.get("path", "")
            file_name = os.path.basename(file_path)
            
            if isinstance(parent, QTreeWidget):
                item = QTreeWidgetItem(parent, [file_name])
            else:
                item = QTreeWidgetItem(parent, [file_name])
                
            item.setData(0, Qt.UserRole, file_path)
            
            # Add tooltip with full path
            item.setToolTip(0, file_path)
            
            # Add icon if provided
            icon_path = item_data.get("icon")
            if icon_path and os.path.exists(icon_path):
                item.setIcon(0, QIcon(icon_path))
            
    def drag_enter_event(self, event):
        """Handle drag enter event."""
        if event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
            event.acceptProposedAction()
        else:
            event.ignore()
            
    def drag_move_event(self, event):
        """Handle drag move event."""
        if event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
            event.acceptProposedAction()
        else:
            event.ignore()
            
    def drop_event(self, event):
        """Handle drop event."""
        if not event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
            event.ignore()
            return
            
        # Get the drop target
        drop_item = self.selected_tree.itemAt(event.pos())
        target_group = None
        
        if drop_item is None:
            # Dropped on empty space - create a new group or ignore
            event.ignore()
            return
        elif drop_item.parent() is None:
            # Dropped on a top-level group
            target_group = drop_item
        else:
            # Dropped on a child item - use its parent group
            target_group = drop_item.parent()
            
        # Get group constraints
        group_data = target_group.data(0, Qt.UserRole)
        max_items = group_data.get("max_items") if isinstance(group_data, dict) else None
        allowed_extensions = group_data.get("allowed_extensions") if isinstance(group_data, dict) else None
        
        # Get selected items from available tree
        selected_items = self.available_tree.selectedItems()
        
        # Check constraints and add items
        items_added = 0
        current_item_count = target_group.childCount()
        
        for item in selected_items:
            item_data = item.data(0, Qt.UserRole)
            
            if isinstance(item_data, str):  # It's a file path
                file_path = item_data
                file_name = os.path.basename(file_path)
                file_extension = os.path.splitext(file_path)[1].lower()
                
                # Check extension filter
                if allowed_extensions and file_extension not in allowed_extensions:
                    self._show_warning(f"File '{file_name}' has extension '{file_extension}' which is not allowed in group '{target_group.text(0)}'.\nAllowed extensions: {', '.join(allowed_extensions)}")
                    continue
                
                # Check max items constraint
                if max_items and (current_item_count + items_added) >= max_items:
                    if max_items == 1:
                        # Replace the existing item
                        if target_group.childCount() > 0:
                            target_group.removeChild(target_group.child(0))
                            current_item_count = 0
                    else:
                        self._show_warning(f"Group '{target_group.text(0)}' can only contain {max_items} item(s). Current: {current_item_count}")
                        break
                
                # Check if item already exists in target group
                if not self._item_exists_in_group(target_group, file_path):
                    new_item = QTreeWidgetItem(target_group, [file_name])
                    new_item.setData(0, Qt.UserRole, file_path)
                    
                    # Add tooltip with full path
                    new_item.setToolTip(0, file_path)
                    
                    # Copy the icon from the source item
                    source_icon = item.icon(0)
                    if not source_icon.isNull():
                        new_item.setIcon(0, source_icon)
                    
                    items_added += 1
                    
        self.selected_tree.expandAll()
        event.acceptProposedAction()
        
    def _show_warning(self, message):
        """Show a warning message to the user."""
        from qtpy.QtWidgets import QMessageBox
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Constraint Violation")
        msg_box.setText(message)
        msg_box.exec_()
        
    def _item_exists_in_group(self, group_item, file_path):
        """Check if an item with the given file path already exists in the group."""
        for i in range(group_item.childCount()):
            child = group_item.child(i)
            child_data = child.data(0, Qt.UserRole)
            if child_data == file_path:
                return True
        return False
        
    def accept_selection(self):
        """Accept the selection and prepare result data."""
        self.result_data = {}
        
        # Iterate through top-level items (groups) in selected tree
        for i in range(self.selected_tree.topLevelItemCount()):
            group_item = self.selected_tree.topLevelItem(i)
            group_name = group_item.text(0)
            
            # Collect all file paths in this group
            file_paths = []
            for j in range(group_item.childCount()):
                child_item = group_item.child(j)
                file_path = child_item.data(0, Qt.UserRole)
                if isinstance(file_path, str):
                    file_paths.append(file_path)
                    
            if file_paths:  # Only add groups that have items
                self.result_data[group_name] = file_paths
                
        self.accept()
        
    def get_selected_products(self):
        """Get the selected products as a dictionary."""
        return self.result_data
    
    def remove_selected_item(self):
        """Remove the currently selected item from the selected tree."""
        current_item = self.selected_tree.currentItem()
        
        if current_item is None:
            return
            
        # Only remove if it's a child item (not a group)
        if current_item.parent() is not None:
            parent = current_item.parent()
            parent.removeChild(current_item)
            
    def clear_selected_items(self):
        """Clear all items from groups but keep the groups."""
        for i in range(self.selected_tree.topLevelItemCount()):
            group_item = self.selected_tree.topLevelItem(i)
            
            # Remove all children (items) but keep the group
            while group_item.childCount() > 0:
                group_item.removeChild(group_item.child(0))
        

# Example usage and test function
def test_product_import_dialog():
    """Test function to demonstrate the dialog usage."""
    import sys

    # Sample available data
    available_data = {
        "items": [
            {
                "type": "group",
                "name": "Rigs",
                "icon": "C:/Users/Thomas/OneDrive/Bureau/Pipeline 2025/Pipeline_USD_2025-2026_src/prism/Badger_Pipeline/Scripts/rc/Icons/folder.png",  # Optional icon for group
                "childrens": [
                    {
                        "type": "item",
                        "path": "C:/projects/rigs/rig_low_voiture.ma",
                        "icon": "C:/Users/Thomas/OneDrive/Bureau/Pipeline 2025/Pipeline_USD_2025-2026_src/prism/Badger_Pipeline/Scripts/rc/Icons/file.png"  # Optional icon for item
                    },
                    {
                        "type": "item",
                        "path": "C:/projects/rigs/rig_low_maya.ma",
                        "icon": "C:/Users/Thomas/OneDrive/Bureau/Pipeline 2025/Pipeline_USD_2025-2026_src/prism/Badger_Pipeline/Scripts/rc/Icons/file.png"
                    },
                    {
                        "type": "group",
                        "name": "Props",
                        "icon": "C:/Users/Thomas/OneDrive/Bureau/Pipeline 2025/Pipeline_USD_2025-2026_src/prism/Badger_Pipeline/Scripts/rc/Icons/folder.png",
                        "childrens": [
                            {
                                "type": "item",
                                "path": "C:/projects/props/prop_low_voiture.ma",
                                "icon": "C:/Users/Thomas/OneDrive/Bureau/Pipeline 2025/Pipeline_USD_2025-2026_src/prism/Badger_Pipeline/Scripts/rc/Icons/file.png"
                            },
                            {
                                "type": "item",
                                "path": "C:/projects/props/prop_low_maya.ma",
                                "icon": "C:/Users/Thomas/OneDrive/Bureau/Pipeline 2025/Pipeline_USD_2025-2026_src/prism/Badger_Pipeline/Scripts/rc/Icons/file.png"
                            }
                        ]
                    }
                ]
            },
            {
                "type": "group",
                "name": "Assets",
                "icon": "C:/Users/Thomas/OneDrive/Bureau/Pipeline 2025/Pipeline_USD_2025-2026_src/prism/Badger_Pipeline/Scripts/rc/Icons/folder.png",
                "childrens": [
                    {
                        "type": "item",
                        "path": "C:/projects/assets/asset_building.usd",
                        "icon": "C:/Users/Thomas/OneDrive/Bureau/Pipeline 2025/Pipeline_USD_2025-2026_src/prism/Badger_Pipeline/Scripts/rc/Icons/file.png"
                    }
                ]
            }
        ]
    }
    
    # Sample selected data
    selected_data = {
        "Cameras": {
            "icon": "C:/Users/Thomas/OneDrive/Bureau/Pipeline 2025/Pipeline_USD_2025-2026_src/prism/Badger_Pipeline/Scripts/rc/Icons/collection_light_blue.png",
            "max_items": 1,  # Only one camera allowed
            "allowed_extensions": [".abc", ".usd"],  # Only Alembic and USD files
            "items": [
                {
                    "type": "item",
                    "path": "C:/projects/cams/cam_main.abc",
                    "icon": "C:/Users/Thomas/OneDrive/Bureau/Pipeline 2025/Pipeline_USD_2025-2026_src/prism/Badger_Pipeline/Scripts/rc/Icons/file.png"
                }
            ]
        },
        "Rigs": {
            "icon": "C:/Users/Thomas/OneDrive/Bureau/Pipeline 2025/Pipeline_USD_2025-2026_src/prism/Badger_Pipeline/Scripts/rc/Icons/collection_amber.png",
            "max_items": None,  # Unlimited rigs allowed
            "allowed_extensions": [".ma", ".mb"],  # Only Maya files
            "items": []
        },
        "Props": {
            "icon": "C:/Users/Thomas/OneDrive/Bureau/Pipeline 2025/Pipeline_USD_2025-2026_src/prism/Badger_Pipeline/Scripts/rc/Icons/collection_light_blue.png",
            "max_items": 5,  # Maximum 5 props
            "allowed_extensions": [".ma", ".mb", ".abc", ".usd"],  # Multiple extensions
            "items": []
        }
    }
    
    dialog = ProductImportDialog(available_data, selected_data)
    
    if dialog.exec_() == QDialog.Accepted:
        result = dialog.get_selected_products()
        print("Selected products:", result)
    else:
        print("Dialog cancelled")


if __name__ == "__main__":
    test_product_import_dialog()
