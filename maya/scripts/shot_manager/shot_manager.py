# -*- coding: utf-8 -*-
"""
Maya 2024 Shot Manager Tool
Description: Outil de gestion des shots pour le Rough Layout (RLO) dans Maya 2024
Compatible avec PySide2/Qt
"""

from PySide6.QtWidgets import (QDialog, QTreeWidget, QTreeWidgetItem, QVBoxLayout, 
                               QHBoxLayout, QPushButton, QColorDialog, QSpinBox,
                               QLineEdit, QHeaderView, QAbstractItemView)
from PySide6.QtCore import Qt, Signal, QObject
from PySide6.QtGui import QColor, QPalette


class ShotData(QObject):
    """
    Classe représentant un objet Shot dans le pipeline.
    Sert uniquement à stocker les données, indépendamment de l'UI.
    """
    
    def __init__(self, name="", start_frame=1, end_frame=24, color=None):
        """
        Initialise un objet ShotData.
        
        Args:
            name (str): Nom du shot
            start_frame (int): Frame de début
            end_frame (int): Frame de fin
            color (QColor): Couleur associée au shot
        """
        super(ShotData, self).__init__()
        self.name = name
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.color = color if color is not None else QColor(100, 150, 200)
    
    def __str__(self):
        """Représentation textuelle du shot."""
        return f"Shot(name='{self.name}', start={self.start_frame}, end={self.end_frame})"
    
    def __repr__(self):
        return self.__str__()


class ColorButton(QPushButton):
    """
    Bouton personnalisé pour afficher et sélectionner une couleur.
    """
    colorChanged = Signal(QColor)
    
    def __init__(self, color=None):
        super(ColorButton, self).__init__()
        self.color = color if color is not None else QColor(100, 150, 200)
        self.setText("")
        self.setFixedSize(30, 20)
        self.updateStyle()
        self.clicked.connect(self.selectColor)
    
    def updateStyle(self):
        """Met à jour le style du bouton avec la couleur actuelle."""
        style = f"background-color: rgb({self.color.red()}, {self.color.green()}, {self.color.blue()}); border: 1px solid black;"
        self.setStyleSheet(style)
    
    def selectColor(self):
        """Ouvre un sélecteur de couleur."""
        color = QColorDialog.getColor(self.color, None, "Sélectionner une couleur")
        if color.isValid():
            self.color = color
            self.updateStyle()
            self.colorChanged.emit(color)
    
    def setColor(self, color):
        """Définit la couleur du bouton."""
        self.color = color
        self.updateStyle()


class ShotTreeWidget(QTreeWidget):
    """
    Widget d'arbre personnalisé pour afficher et gérer les shots.
    Hérite de QTreeWidget et gère l'affichage sous forme de tableau.
    """
    
    # Signaux émis pour notifier les changements
    shotAdded = Signal(object, int)      # (shot, index)
    shotRemoved = Signal(object, int)    # (shot, index)
    shotModified = Signal(object, int)   # (shot, index)
    colorChanged = Signal(object, QColor) # (shot, color)
    
    def __init__(self):
        super(ShotTreeWidget, self).__init__()
        self.setupUI()
        self.shots_data = []  # Liste des objets ShotData
    
    def setupUI(self):
        """Configure l'interface utilisateur du tree widget."""
        # Configuration des colonnes
        headers = ["Nom", "Start Frame", "End Frame", "Couleur"]
        self.setHeaderLabels(headers)
        self.setColumnCount(len(headers))
        
        # Configuration du tree widget
        self.setRootIsDecorated(False)
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        
        # Redimensionnement automatique des colonnes
        header = self.header()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Nom
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Start Frame
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # End Frame
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Couleur
        
        # Connexions des signaux
        self.itemDoubleClicked.connect(self.onItemDoubleClicked)
    
    def addShot(self, shot_data, index=None):
        """
        Ajoute un shot dans le tree widget.
        
        Args:
            shot_data (ShotData): Données du shot à ajouter
            index (int): Index où insérer le shot (None = à la fin)
        """
        if index is None:
            index = len(self.shots_data)
        
        # Ajouter aux données
        self.shots_data.insert(index, shot_data)
        
        # Créer l'item dans le tree widget
        item = QTreeWidgetItem()
        item.setText(0, shot_data.name)
        item.setText(1, str(shot_data.start_frame))
        item.setText(2, str(shot_data.end_frame))
        
        # Rendre les colonnes éditables
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        
        # Insérer l'item
        self.insertTopLevelItem(index, item)
        
        # Créer et ajouter le bouton de couleur
        color_button = ColorButton(shot_data.color)
        color_button.colorChanged.connect(lambda color, s=shot_data: self.onColorChanged(s, color))
        self.setItemWidget(item, 3, color_button)
        
        # Émettre le signal
        self.shotAdded.emit(shot_data, index)
    
    def removeSelectedShot(self):
        """Supprime le shot sélectionné."""
        current_item = self.currentItem()
        if current_item is None:
            return
        
        index = self.indexOfTopLevelItem(current_item)
        if index >= 0:
            shot_data = self.shots_data[index]
            
            # Supprimer des données et de l'interface
            self.shots_data.pop(index)
            self.takeTopLevelItem(index)
            
            # Émettre le signal
            self.shotRemoved.emit(shot_data, index)
    
    def getSelectedIndex(self):
        """Retourne l'index du shot sélectionné."""
        current_item = self.currentItem()
        if current_item is None:
            return -1
        return self.indexOfTopLevelItem(current_item)
    
    def onItemDoubleClicked(self, item, column):
        """Gère le double-clic sur un item pour l'édition."""
        if column in [0, 1, 2]:  # Nom, Start Frame ou End Frame
            self.editItem(item, column)
    
    def onColorChanged(self, shot_data, color):
        """Gère le changement de couleur d'un shot."""
        shot_data.color = color
        index = self.shots_data.index(shot_data)
        self.colorChanged.emit(shot_data, color)
        self.shotModified.emit(shot_data, index)
    
    def updateShotData(self, item, column):
        """Met à jour les données du shot après édition."""
        index = self.indexOfTopLevelItem(item)
        if index < 0 or index >= len(self.shots_data):
            return
        
        shot_data = self.shots_data[index]
        
        try:
            if column == 0:  # Nom
                shot_data.name = item.text(0)
            elif column == 1:  # Start Frame
                shot_data.start_frame = int(item.text(1))
            elif column == 2:  # End Frame
                shot_data.end_frame = int(item.text(2))
            
            self.shotModified.emit(shot_data, index)
        except ValueError:
            # Restaurer la valeur précédente en cas d'erreur
            item.setText(0, shot_data.name)
            item.setText(1, str(shot_data.start_frame))
            item.setText(2, str(shot_data.end_frame))
    
    def clearShots(self):
        """Efface tous les shots."""
        self.clear()
        self.shots_data.clear()
    
    def getShotsData(self):
        """Retourne la liste des shots."""
        return self.shots_data.copy()


class ShotManagerDialog(QDialog):
    """
    Fenêtre principale de gestion des shots.
    Hérite de QDialog et regroupe toute l'interface utilisateur.
    """
    
    def __init__(self, parent=None):
        super(ShotManagerDialog, self).__init__(parent)
        self.setupUI()
        self.connectSignals()
        self.original_shots = []  # Sauvegarde pour le bouton Annuler
    
    def setupUI(self):
        """Configure l'interface utilisateur de la fenêtre."""
        self.setWindowTitle("Shot Manager - RLO")
        self.setModal(True)
        self.resize(600, 400)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        
        # Tree widget pour les shots
        self.shot_tree = ShotTreeWidget()
        main_layout.addWidget(self.shot_tree)
        
        # Layout des boutons d'action sur les shots
        action_layout = QHBoxLayout()
        
        self.btn_add_above = QPushButton("Ajouter au-dessus")
        self.btn_add_below = QPushButton("Ajouter en-dessous")
        self.btn_remove = QPushButton("Supprimer")
        
        action_layout.addWidget(self.btn_add_above)
        action_layout.addWidget(self.btn_add_below)
        action_layout.addWidget(self.btn_remove)
        action_layout.addStretch()  # Espace flexible
        
        main_layout.addLayout(action_layout)
        
        # Layout des boutons de validation
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # Espace flexible à gauche
        
        self.btn_apply = QPushButton("Appliquer")
        self.btn_cancel = QPushButton("Annuler")
        
        button_layout.addWidget(self.btn_apply)
        button_layout.addWidget(self.btn_cancel)
        
        main_layout.addLayout(button_layout)
    
    def connectSignals(self):
        """Connecte tous les signaux aux callbacks."""
        # Boutons d'action
        self.btn_add_above.clicked.connect(self.onAddShotAbove)
        self.btn_add_below.clicked.connect(self.onAddShotBelow)
        self.btn_remove.clicked.connect(self.onRemoveShot)
        
        # Boutons de validation
        self.btn_apply.clicked.connect(self.onApply)
        self.btn_cancel.clicked.connect(self.onCancel)
        
        # Signaux du tree widget
        self.shot_tree.shotAdded.connect(self.onShotAdded)
        self.shot_tree.shotRemoved.connect(self.onShotRemoved)
        self.shot_tree.shotModified.connect(self.onShotModified)
        self.shot_tree.colorChanged.connect(self.onColorChanged)
        
        # Signal pour mise à jour après édition
        self.shot_tree.itemChanged.connect(self.shot_tree.updateShotData)
    
    def initializeShots(self, shots_list):
        """
        Initialise la fenêtre avec une liste de shots existants.
        
        Args:
            shots_list (list): Liste d'objets ShotData ou de dictionnaires
        """
        # Sauvegarder l'état original pour le bouton Annuler
        self.original_shots = []
        
        # Vider le tree widget
        self.shot_tree.clearShots()
        
        # Ajouter chaque shot
        for shot_info in shots_list:
            if isinstance(shot_info, ShotData):
                shot_data = shot_info
            elif isinstance(shot_info, dict):
                # Créer un ShotData à partir d'un dictionnaire
                shot_data = ShotData(
                    name=shot_info.get('name', ''),
                    start_frame=shot_info.get('start_frame', 1001),
                    end_frame=shot_info.get('end_frame', 1050),
                    color=shot_info.get('color', QColor(100, 150, 200))
                )
            else:
                continue
            
            # Sauvegarder l'original
            original = ShotData(shot_data.name, shot_data.start_frame, 
                              shot_data.end_frame, QColor(shot_data.color))
            self.original_shots.append(original)
            
            # Ajouter au tree widget
            self.shot_tree.addShot(shot_data)
    
    def getCurrentShots(self):
        """Retourne la liste actuelle des shots."""
        return self.shot_tree.getShotsData()
    
    def _extractShotNumber(self, shot_name):
        """Extrait le numéro d'un nom de shot (ex: 'sh_020' -> 20)."""
        import re
        # Recherche le pattern sh_### ou ###
        match = re.search(r'(sh_)?(\d{3})', shot_name.lower())
        if match:
            return int(match.group(2))
        return None
    
    def _generateShotName(self, insert_index):
        """Génère un nom de shot intelligent basé sur la position d'insertion."""
        shots_data = self.shot_tree.getShotsData()
        
        # Si pas de shots, commencer à 010
        if not shots_data:
            return "sh_010"
        
        # Extraire tous les numéros existants
        existing_numbers = []
        for shot in shots_data:
            num = self._extractShotNumber(shot.name)
            if num is not None:
                existing_numbers.append(num)
        
        # Si aucun numéro trouvé, commencer à 010
        if not existing_numbers:
            return "sh_010"
        
        existing_numbers.sort()
        
        # Insertion au début
        if insert_index == 0:
            first_num = existing_numbers[0]
            if first_num > 10:
                # Prendre un numéro avant le premier
                new_num = max(10, first_num - 10)
            else:
                # Prendre 5 si le premier est 10
                new_num = 5
            return f"sh_{new_num:03d}"
        
        # Insertion à la fin
        if insert_index >= len(shots_data):
            last_num = existing_numbers[-1]
            new_num = last_num + 10
            return f"sh_{new_num:03d}"
        
        # Insertion au milieu
        # Regarder les shots avant et après la position d'insertion
        prev_shot_index = insert_index - 1
        next_shot_index = insert_index
        
        prev_num = None
        next_num = None
        
        if prev_shot_index >= 0:
            prev_num = self._extractShotNumber(shots_data[prev_shot_index].name)
        
        if next_shot_index < len(shots_data):
            next_num = self._extractShotNumber(shots_data[next_shot_index].name)
        
        # Calculer le numéro à insérer
        if prev_num is not None and next_num is not None:
            # Insérer entre deux shots
            if next_num - prev_num > 1:
                # Il y a de la place, prendre le milieu
                new_num = prev_num + ((next_num - prev_num) // 2)
                # Si c'est exactement au milieu et qu'on peut faire +5, le faire
                if (next_num - prev_num) == 10:
                    new_num = prev_num + 5
            else:
                # Pas de place, décaler tout vers la droite
                new_num = next_num
                # Décaler tous les shots suivants
                self._shiftShotNumbers(next_shot_index, 10)
        elif prev_num is not None:
            # Insérer après le dernier shot avec numéro
            new_num = prev_num + 10
        elif next_num is not None:
            # Insérer avant le premier shot avec numéro
            new_num = max(10, next_num - 10)
        else:
            # Fallback
            new_num = 10
        
        return f"sh_{new_num:03d}"
    
    def _shiftShotNumbers(self, start_index, increment):
        """Décale les numéros de shots à partir d'un index donné."""
        shots_data = self.shot_tree.getShotsData()
        
        for i in range(start_index, len(shots_data)):
            shot = shots_data[i]
            current_num = self._extractShotNumber(shot.name)
            if current_num is not None:
                new_num = current_num + increment
                # Mettre à jour le nom dans les données
                shot.name = f"sh_{new_num:03d}"
                # Mettre à jour l'affichage
                item = self.shot_tree.topLevelItem(i)
                if item:
                    item.setText(0, shot.name)
    
    # === CALLBACKS (vides comme demandé) ===
    
    def onAddShotAbove(self):
        """Callback : Ajouter un shot au-dessus du shot sélectionné."""
        selected_index = self.shot_tree.getSelectedIndex()
        insert_index = max(0, selected_index) if selected_index >= 0 else 0
        
        # Générer un nom intelligent pour le nouveau shot
        shot_name = self._generateShotName(insert_index)
        
        # Créer un nouveau shot avec le nom généré
        new_shot = ShotData(
            name=shot_name,
            start_frame=1001,
            end_frame=1050,
            color=QColor(100, 150, 200)
        )
        
        self.shot_tree.addShot(new_shot, insert_index)
        # TODO: Implémenter la logique spécifique Maya
        pass
    
    def onAddShotBelow(self):
        """Callback : Ajouter un shot en-dessous du shot sélectionné."""
        selected_index = self.shot_tree.getSelectedIndex()
        insert_index = selected_index + 1 if selected_index >= 0 else len(self.shot_tree.shots_data)
        
        # Générer un nom intelligent pour le nouveau shot
        shot_name = self._generateShotName(insert_index)
        
        # Créer un nouveau shot avec le nom généré
        new_shot = ShotData(
            name=shot_name,
            start_frame=1001,
            end_frame=1050,
            color=QColor(100, 150, 200)
        )
        
        self.shot_tree.addShot(new_shot, insert_index)
        # TODO: Implémenter la logique spécifique Maya
        pass
    
    def onRemoveShot(self):
        """Callback : Supprimer le shot sélectionné."""
        self.shot_tree.removeSelectedShot()
        # TODO: Implémenter la logique spécifique Maya
        pass
    
    def onShotAdded(self, shot, index):
        """Callback : Un shot a été ajouté."""
        # TODO: Implémenter la logique spécifique Maya
        pass
    
    def onShotRemoved(self, shot, index):
        """Callback : Un shot a été supprimé."""
        # TODO: Implémenter la logique spécifique Maya
        pass
    
    def onShotModified(self, shot, index):
        """Callback : Un shot a été modifié."""
        # TODO: Implémenter la logique spécifique Maya
        pass
    
    def onColorChanged(self, shot, color):
        """Callback : La couleur d'un shot a changé."""
        # TODO: Implémenter la logique spécifique Maya
        pass
    
    def onApply(self):
        """Callback : Appliquer les modifications."""
        # TODO: Implémenter la logique d'application dans Maya
        self.accept()  # Ferme la fenêtre avec un code de succès
        pass
    
    def onCancel(self):
        """Callback : Annuler les modifications."""
        # Restaurer l'état original
        if self.original_shots:
            self.initializeShots(self.original_shots)
        # TODO: Implémenter la logique d'annulation dans Maya
        self.reject()  # Ferme la fenêtre avec un code d'annulation
        pass


# === FONCTIONS D'UTILITÉ ===

def showShotManager(shots_list=None):
    """
    Fonction d'aide pour afficher le gestionnaire de shots.
    
    Args:
        shots_list (list): Liste optionnelle de shots existants
    
    Returns:
        ShotManagerDialog: Instance de la fenêtre (None si annulée)
    """
    dialog = ShotManagerDialog()
    
    # Initialiser avec des shots si fournis
    if shots_list:
        dialog.initializeShots(shots_list)
    else:
        # Créer quelques shots d'exemple
        example_shots = [
            ShotData("SH_010", 1, 48, QColor(255, 100, 100)),
            ShotData("SH_020", 49, 96, QColor(100, 255, 100)),
            ShotData("SH_030", 97, 144, QColor(100, 100, 255)),
        ]
        dialog.initializeShots(example_shots)
    
    # Afficher la fenêtre
    result = dialog.exec_()
    
    if result == QDialog.Accepted:
        return dialog
    return None


# === EXEMPLE D'UTILISATION ===

if __name__ == "__main__":
    """
    Code d'exemple pour tester l'outil en dehors de Maya.
    Dans Maya, utilisez directement showShotManager().
    """
    import sys
    from PySide6.QtWidgets import QApplication
    
    # Créer l'application Qt si elle n'existe pas
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # Exemple de shots
    example_shots = [
        ShotData("sh_010", 1001, 1005, QColor(255, 120, 120)),
        ShotData("sh_020", 1001, 1025, QColor(120, 255, 120)),
        ShotData("sh_030", 1001, 1030, QColor(120, 120, 255)),
        ShotData("sh_040", 1031, 1006, QColor(255, 255, 120)),
    ]
    
    # Afficher le gestionnaire de shots
    dialog = showShotManager(example_shots)
    
    if dialog:
        print("Shots finaux:")
        for i, shot in enumerate(dialog.getCurrentShots()):
            print(f"  {i+1}. {shot}")
    else:
        print("Opération annulée.")
    
    # Quitter l'application si on l'a créée
    if 'app' in locals():
        sys.exit(app.exec_())


# === UTILISATION DANS MAYA ===
