from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *
import os


class AreYouSureDialog(QDialog):
    """
    Dialog to confirm user actions with Yes/No options.
    """

    def __init__(self, parent=None , pparent =None):
        super(AreYouSureDialog, self).__init__(parent)
        self.parent = parent
        self.pparent = pparent

        self.setWindowTitle("Confirmation")
        self.setModal(True)
        self.resize(400, 150)

        self.setupUi()

    def setupUi(self):
        self.main_layout = QVBoxLayout(self)

        # Image label
        self.image_label = QLabel(self)
        movie = QMovie(__file__ + "../../../../rc/minion.gif")
        self.image_label.setMovie(movie)
        movie.start()
        self.main_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)

        # Path label
        self.path_label = QLabel("", self)
        self.path_label.setWordWrap(True)
        self.main_layout.addWidget(self.path_label)

        # Message label
        self.message_label = QLabel("Are you sure?", self)
        self.message_label.setWordWrap(True)
        self.main_layout.addWidget(self.message_label)

        # Buttons layout
        self.buttons_layout = QHBoxLayout()
        self.main_layout.addLayout(self.buttons_layout)

        # Spacer to push buttons to the right
        self.buttons_layout.addStretch()

        # Yes button
        self.yes_button = QPushButton("Yes", self)
        self.yes_button.setIcon(self.pparent.getIcon("check"))
        self.yes_button.clicked.connect(self.accept)
        self.buttons_layout.addWidget(self.yes_button)

        # No button
        self.no_button = QPushButton("No", self)
        self.no_button.setIcon(self.pparent.getIcon("cancel"))
        self.no_button.clicked.connect(self.reject)
        self.buttons_layout.addWidget(self.no_button)

    def setPath(self, path):
        self.path_label.setText(f"Path: {path}")



