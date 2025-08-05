
from qtpy.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QHBoxLayout, QPushButton, QWidget,QMessageBox,QLineEdit, QLabel


class DropWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    # When a drag enters the widget
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    # When files are dropped onto the widget
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            file_paths = [url.toLocalFile() for url in event.mimeData().urls()]
            self.handleDroppedFiles(file_paths)

    def handleDroppedFiles(self, file_paths):
        # Here you can handle the dropped files, e.g., display them in a text area
        # For now, we will just print them to the console
        self.parent().handleDroppedFiles(file_paths)


# Qt dialog where you can drag and drop files and create a product from those files
class CreateProductDialog(QDialog):
    def __init__(self, parent=None, core=None):
        super().__init__(parent)
        self.core = core
        self.setWindowTitle("Create Product")
        self.setMinimumSize(400, 300)

        # Main layout
        main_layout = QVBoxLayout(self)

        # Text area for drag and drop
        self.drop_widget = DropWidget(self)
        main_layout.addWidget(self.drop_widget)

        # H box layout for buttons
        bottom_layout = QHBoxLayout()


        # Label for the product name
        self.product_name_label = QLabel("Product Name:", self)
        bottom_layout.addWidget(self.product_name_label)

        # Line edit for the product name
        self.product_name_edit = QLineEdit(self)
        self.product_name_edit.setPlaceholderText("Enter product name here...")
        self.product_name_edit.setText("Textures_Export")
        bottom_layout.addWidget(self.product_name_edit)

        main_layout.addLayout(bottom_layout)

    def handleDroppedFiles(self, file_paths):

        if(self.product_name_edit.text() == ""):
            # Message box to alert the user to enter a product name
            QMessageBox.warning(self, "Warning", "Please enter a product name before dropping files.")
            return
        
        # Get the product name from the line edit
        product_name = self.product_name_edit.text()

        # Handle the dropped files here
        # For now, we will just print the file paths to the console
        print(self.core.pb.sceneBrowser.tbw_project.currentWidget().property("tabType"))
        print(f"Creating product '{product_name}' with files:")


