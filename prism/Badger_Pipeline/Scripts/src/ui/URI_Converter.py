"""
URI Converter Dialog

Ce module contient la classe URI_Converter_Dialog qui permet de convertir 
entre les chemins de fichiers et les URIs logiques du pipeline.
"""

import os
from qtpy.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, 
    QPushButton, QFileDialog, QGroupBox, QSizePolicy, QCheckBox
)
from qtpy.QtCore import Qt, Signal
from qtpy.QtGui import QIcon

from src.core.URI_Helper import URI_Helper


class URI_Converter_Dialog(QDialog):
    """
    Dialog pour convertir entre les chemins de fichiers et les URIs logiques.
    
    La classe contient deux LineEdit :
    - Une éditable pour saisir le chemin de fichier
    - Une en lecture seule qui affiche l'URI converti automatiquement
    """
    
    # Signal émis quand la conversion est mise à jour
    uriConverted = Signal(str, str)  # (file_path, uri)
    
    def __init__(self, core=None, pluggin_parent=None, parent=None):
        """
        Initialise le dialog URI Converter.
        
        Args:
            core: Instance du core Prism
            pluggin_parent: Parent plugin instance
            parent: Widget parent Qt
        """
        super(URI_Converter_Dialog, self).__init__(parent)
        
        self.core = core
        self.pluggin_parent = pluggin_parent
        
        self.setupUI()
        self.connectSignals()
        
    def setupUI(self):
        """Configure l'interface utilisateur."""
        self.setWindowTitle("URI Converter")
        self.setMinimumSize(600, 200)
        self.setModal(True)
        
        # Layout principal
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # Groupe pour la conversion Path -> URI
        path_to_uri_group = QGroupBox("Path to URI Conversion")
        path_to_uri_layout = QVBoxLayout()
        path_to_uri_group.setLayout(path_to_uri_layout)
        
        # Label et LineEdit pour le chemin de fichier
        file_path_label = QLabel("File Path:")
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setPlaceholderText("Enter or paste a file path...")
        
        # Bouton pour parcourir les fichiers
        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(self.browseForFile)
        
        # Layout horizontal pour le chemin et le bouton browse
        file_path_layout = QHBoxLayout()
        file_path_layout.addWidget(self.file_path_edit)
        file_path_layout.addWidget(browse_button)
        
        # Checkbox pour la version latest
        self.latest_checkbox = QCheckBox("Latest Version")
        self.latest_checkbox.setChecked(True)  # Cochée par défaut
        self.latest_checkbox.setToolTip("Check to use 'latest' version, uncheck to use specific version number")
        
        # Label et LineEdit pour l'URI (lecture seule)
        uri_label = QLabel("Generated URI:")
        self.uri_edit = QLineEdit()
        self.uri_edit.setReadOnly(True)
        self.uri_edit.setPlaceholderText("URI will appear here automatically...")
        
        # Bouton pour copier l'URI
        copy_uri_button = QPushButton("Copy URI")
        copy_uri_button.clicked.connect(self.copyUriToClipboard)
        
        # Layout horizontal pour l'URI et le bouton copy
        uri_layout = QHBoxLayout()
        uri_layout.addWidget(self.uri_edit)
        uri_layout.addWidget(copy_uri_button)
        
        # Ajout des éléments au groupe
        path_to_uri_layout.addWidget(file_path_label)
        path_to_uri_layout.addLayout(file_path_layout)
        path_to_uri_layout.addWidget(self.latest_checkbox)
        path_to_uri_layout.addWidget(uri_label)
        path_to_uri_layout.addLayout(uri_layout)
        
        # Boutons de contrôle
        button_layout = QHBoxLayout()
        
        clear_button = QPushButton("Clear")
        close_button = QPushButton("Close")
        
        clear_button.clicked.connect(self.clearFields)
        close_button.clicked.connect(self.close)
        
        button_layout.addStretch()
        button_layout.addWidget(clear_button)
        button_layout.addWidget(close_button)
        
        # Ajout au layout principal
        main_layout.addWidget(path_to_uri_group)
        main_layout.addLayout(button_layout)
        
    def connectSignals(self):
        """Connecte les signaux."""
        # Connecter le signal textChanged pour la conversion automatique
        self.file_path_edit.textChanged.connect(self.onFilePathChanged)
        # Connecter le signal stateChanged de la checkbox pour rafraîchir la conversion
        self.latest_checkbox.stateChanged.connect(self.onLatestCheckboxChanged)
        
    def onFilePathChanged(self, text):
        """
        Slot appelé quand le texte du chemin de fichier change.
        Convertit automatiquement le chemin en URI.
        
        Args:
            text (str): Le nouveau texte dans le LineEdit
        """
        if not text.strip():
            self.uri_edit.clear()
            return
            
        try:
            # Utiliser URI_Helper pour convertir le chemin en URI
            latest_version = self.latest_checkbox.isChecked()
            uri = URI_Helper.createFromPath(text, latest_version)
            self.uri_edit.setText(uri)
            
            # Émettre le signal de conversion
            self.uriConverted.emit(text, uri)
            
        except Exception as e:
            # En cas d'erreur, afficher un message d'erreur dans l'URI
            self.uri_edit.setText(f"Error: {str(e)}")
            
    def onLatestCheckboxChanged(self, state):
        """
        Slot appelé quand l'état de la checkbox "Latest" change.
        Rafraîchit automatiquement la conversion URI.
        
        Args:
            state (int): L'état de la checkbox (Qt.Checked ou Qt.Unchecked)
        """
        # Relancer la conversion avec le nouveau paramètre latest_version
        current_text = self.file_path_edit.text()
        if current_text.strip():
            self.onFilePathChanged(current_text)
            
    def browseForFile(self):
        """Ouvre un dialog pour sélectionner un fichier."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            "",
            "All Files (*.*)"
        )
        
        if file_path:
            self.file_path_edit.setText(file_path)
            
    def copyUriToClipboard(self):
        """Copie l'URI généré dans le presse-papier."""
        from qtpy.QtWidgets import QApplication
        
        uri_text = self.uri_edit.text()
        if uri_text and not uri_text.startswith("Error:"):
            clipboard = QApplication.clipboard()
            clipboard.setText(uri_text)
            
            # Optionnel : afficher un message de confirmation
            if self.core:
                self.core.popup("URI copied to clipboard!")
                
    def clearFields(self):
        """Efface tous les champs."""
        self.file_path_edit.clear()
        self.uri_edit.clear()
        
    def setFilePath(self, path):
        """
        Définit le chemin de fichier programmatiquement.
        
        Args:
            path (str): Le chemin de fichier à définir
        """
        self.file_path_edit.setText(path)
        
    def getFilePath(self):
        """
        Retourne le chemin de fichier actuel.
        
        Returns:
            str: Le chemin de fichier
        """
        return self.file_path_edit.text()
        
    def getUri(self):
        """
        Retourne l'URI généré actuel.
        
        Returns:
            str: L'URI généré
        """
        return self.uri_edit.text()


# Fonction utilitaire pour créer et afficher le dialog
def show_uri_converter(core=None, pluggin_parent=None, parent=None):
    """
    Fonction utilitaire pour créer et afficher le URI Converter Dialog.
    
    Args:
        core: Instance du core Prism
        pluggin_parent: Parent plugin instance  
        parent: Widget parent Qt
        
    Returns:
        URI_Converter_Dialog: L'instance du dialog créé
    """
    dialog = URI_Converter_Dialog(core, pluggin_parent, parent)
    dialog.show()
    return dialog