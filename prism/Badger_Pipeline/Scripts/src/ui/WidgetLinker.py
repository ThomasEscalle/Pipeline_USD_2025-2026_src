from qtpy.QtWidgets import QDialog, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from qtpy.QtCore import QRectF, Qt
from qtpy.QtGui import QColor, QBrush, QPen
import random


# --- Refactorisation en sous-classes et ajout de commentaires ---

class SlotItem:
    """
    Représente un slot graphique (carré coloré + label) dans une colonne.
    """
    def __init__(self, slot_id, label, color, scene, x=0, y=0):
        self.slot_id = slot_id
        # S'assure que la couleur est un QColor
        if isinstance(color, str):
            self.color = QColor(color)
        else:
            self.color = color
        self.circle = QGraphicsRectItem(x, y, 14, 14)
        self.circle.setBrush(QBrush(self.color))
        self.circle.setPen(QPen(QColor(80, 80, 80), 1))
        scene.addItem(self.circle)
        self.label = QGraphicsTextItem(label)
        self.label.setDefaultTextColor(Qt.white)
        scene.addItem(self.label)

    def set_position(self, x, y, label_x, label_y):
        """Positionne le carré et le label dans la scène."""
        self.circle.setRect(x, y, 14, 14)
        self.label.setPos(label_x, label_y)

    def contains(self, pos):
        """Teste si la position (QPointF) est dans le carré du slot."""
        return self.circle.sceneBoundingRect().contains(pos)

    def center(self):
        """Retourne le centre du carré du slot (QPointF)."""
        return self.circle.sceneBoundingRect().center()


class ColumnItem:
    """
    Représente une colonne (gauche ou droite) avec un titre et une liste de slots.
    """
    def __init__(self, side, title, slots, scene, color_func):
        self.side = side
        self.title = title
        self.scene = scene
        self.col_width = 220
        self.title_height = 30
        self.slot_height = 24
        self.slot_margin = 6
        self.margin = 10
        # Fond clair, outline gris foncé
        self.rect = QGraphicsRectItem(0, 0, self.col_width, self.title_height)
        self.rect.setBrush(QBrush(QColor("#232323")))  # fond foncé
        #self.rect.setRadius(5)  # coins arrondis
        self.rect.setPen(QPen(QColor("#232323"), 0))      # outline gris foncé
        scene.addItem(self.rect)
        self.title_item = QGraphicsTextItem(title)
        self.title_item.setDefaultTextColor(Qt.white)
        # Make the title bold
        font = self.title_item.font()
        font.setBold(True)
        self.title_item.setFont(font)

        scene.addItem(self.title_item)
        self.slot_items = []
        for i, (slot_id, slot_label) in enumerate(slots):
            y = self.title_height + i * (self.slot_height + self.slot_margin)
            if side == 'left':
                slot_color = color_func()
            else:
                slot_color = QColor("#616161")
            slot = SlotItem(slot_id, slot_label, slot_color, scene)
            self.slot_items.append(slot)

    def set_position(self, x, y):
        """Positionne la colonne et ses slots dans la scène."""
        n_slots = len(self.slot_items)
        col_height = self.title_height + n_slots * (self.slot_height + self.slot_margin) + self.margin
        self.rect.setRect(x, y, self.col_width, col_height)
        self.title_item.setTextWidth(self.col_width - 40)
        self.title_item.setPos(x + 20, y + 5)
        self.title_item.setTextInteractionFlags(Qt.NoTextInteraction)
        for i, slot in enumerate(self.slot_items):
            slot_y = y + self.title_height + i * (self.slot_height + self.slot_margin)
            if self.side == 'left':
                circle_x = x + self.col_width - 8 - 14
                label_x = circle_x - 8 - slot.label.boundingRect().width()
                slot.set_position(circle_x, slot_y + 5, label_x, slot_y + 2)
            else:
                slot.set_position(x + 8, slot_y + 5, x + 30, slot_y + 2)
        return col_height

    def find_slot_at_pos(self, pos):
        """Retourne l'index du slot sous la position pos, ou None."""
        for idx, slot in enumerate(self.slot_items):
            if slot.contains(pos):
                return idx
        return None


class ConnectionManager:
    """
    Gère les connexions graphiques entre slots (lignes).
    """
    def __init__(self, scene, columns):
        self.scene = scene
        self.columns = columns
        self.connections = []
        self._preview_line = None
        self._linking = None

    def add_connection(self, left_col_idx, left_slot_idx, right_col_idx, right_slot_idx):
        """Ajoute une connexion graphique entre deux slots."""
        color = self.columns[left_col_idx].slot_items[left_slot_idx].color
        line = self.scene.addLine(0, 0, 0, 0, QPen(color, 3))
        self.connections.append({
            'left': (left_col_idx, left_slot_idx),
            'right': (right_col_idx, right_slot_idx),
            'line': line,
            'color': color
        })
        self.update_connections()

    def update_connections(self):
        """Met à jour la position des lignes de connexion."""
        for conn in self.connections:
            p1 = self.columns[conn['left'][0]].slot_items[conn['left'][1]].center()
            p2 = self.columns[conn['right'][0]].slot_items[conn['right'][1]].center()
            conn['line'].setLine(p1.x(), p1.y(), p2.x(), p2.y())

    def remove_connection(self, idx):
        """Supprime une connexion graphique."""
        conn = self.connections.pop(idx)
        self.scene.removeItem(conn['line'])
        self.update_connections()

    def find_connection_at_pos(self, pos):
        """Retourne l'index de la connexion dont la ligne est proche de pos (en px)."""
        threshold = 8.0
        for idx, conn in enumerate(self.connections):
            line = conn['line'].line()
            x0, y0 = pos.x(), pos.y()
            x1, y1, x2, y2 = line.x1(), line.y1(), line.x2(), line.y2()
            dx, dy = x2 - x1, y2 - y1
            if dx == dy == 0:
                dist = ((x0 - x1)**2 + (y0 - y1)**2)**0.5
            else:
                t = max(0, min(1, ((x0 - x1) * dx + (y0 - y1) * dy) / (dx*dx + dy*dy)))
                proj_x = x1 + t * dx
                proj_y = y1 + t * dy
                dist = ((x0 - proj_x)**2 + (y0 - proj_y)**2)**0.5
            if dist < threshold:
                return idx
        return None

    def start_linking(self, col_idx, slot_idx):
        """Commence la création d'une connexion (ligne preview)."""
        self._linking = {'from': (col_idx, slot_idx)}
        self._preview_line = self.scene.addLine(0, 0, 0, 0, QPen(QColor(80, 200, 255), 2, Qt.DashLine))

    def update_preview_line(self, scene_pos):
        """Met à jour la ligne de preview lors du drag."""
        if self._linking and self._preview_line:
            p1 = self.columns[self._linking['from'][0]].slot_items[self._linking['from'][1]].center()
            p2 = scene_pos
            self._preview_line.setLine(p1.x(), p1.y(), p2.x(), p2.y())

    def remove_preview_line(self):
        """Supprime la ligne de preview si elle existe."""
        if self._preview_line is not None:
            self.scene.removeItem(self._preview_line)
            self._preview_line = None

    def finish_linking(self, scene_pos, find_slot_at_pos, columns):
        """Termine la création d'une connexion si possible."""
        if not self._linking:
            return
        from_col, from_slot = self._linking['from']
        if columns[from_col].side != 'left':
            self.remove_preview_line()
            self._linking = None
            return
        to = find_slot_at_pos(scene_pos, side='right')
        if to:
            to_col, to_slot = to
            self.add_connection(from_col, from_slot, to_col, to_slot)
        self.remove_preview_line()
        self._linking = None


import json

class LinksWidget(QDialog):
    def add_connections(self, connections):
        """
        Ajoute plusieurs connexions à partir d'une liste de dictionnaires :
        [
            {
                "from": {"column": <titre_colonne_gauche>, "slot_id": <id_slot_gauche>},
                "to":   {"column": <titre_colonne_droite>, "slot_id": <id_slot_droite>}
            }, ...
        ]
        """
        for conn in connections:
            from_col_title = conn["from"]["column"]
            from_slot_id = conn["from"]["slot_id"]
            to_col_title = conn["to"]["column"]
            to_slot_id = conn["to"]["slot_id"]

            # Trouver les indices de colonne et de slot
            left_col_idx = next((i for i, c in enumerate(self.columns)
                                 if c.title == from_col_title and c.side == 'left'), None)
            right_col_idx = next((i for i, c in enumerate(self.columns)
                                  if c.title == to_col_title and c.side == 'right'), None)
            if left_col_idx is None or right_col_idx is None:
                continue
            left_slot_idx = next((i for i, s in enumerate(self.columns[left_col_idx].slot_items)
                                  if s.slot_id == from_slot_id), None)
            right_slot_idx = next((i for i, s in enumerate(self.columns[right_col_idx].slot_items)
                                   if s.slot_id == to_slot_id), None)
            if left_slot_idx is None or right_slot_idx is None:
                continue

            self.connection_manager.add_connection(left_col_idx, left_slot_idx, right_col_idx, right_slot_idx)
    def get_result_json(self):
        """
        Retourne la liste des connexions sous forme de JSON.
        Format :
        [
            {
                "from": {"column": <titre_colonne_gauche>, "slot_id": <id_slot_gauche>},
                "to":   {"column": <titre_colonne_droite>, "slot_id": <id_slot_droite>}
            }, ...
        ]
        """
        result = []
        for conn in self.connection_manager.connections:
            left_col_idx, left_slot_idx = conn['left']
            right_col_idx, right_slot_idx = conn['right']
            left_col = self.columns[left_col_idx]
            right_col = self.columns[right_col_idx]
            left_slot = left_col.slot_items[left_slot_idx]
            right_slot = right_col.slot_items[right_slot_idx]
            result.append({
                "from": {
                    "column": left_col.title,
                    "slot_id": left_slot.slot_id
                },
                "to": {
                    "column": right_col.title,
                    "slot_id": right_slot.slot_id
                }
            })
        return json.dumps(result, indent=2, ensure_ascii=False)
    """
    Widget principal pour la gestion des colonnes, slots et connexions.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)
        
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Ajouter la vue graphique
        layout.addWidget(self.view)
        
        # Créer la zone des boutons
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(10, 10, 10, 10)
        
        # Espaceur pour pousser le bouton Save à droite
        button_layout.addStretch()

        # Bouton Save (à droite)
        self.save_button = QPushButton("Save")
        #self.save_button.setFixedSize(80, 30)
        self.save_button.clicked.connect(lambda: self.accept())  # Ferme le dialog et sauvegarde les connexions
        button_layout.addWidget(self.save_button)


        # Bouton Cancel (à gauche)
        self.cancel_button = QPushButton("Cancel")
        #self.cancel_button.setFixedSize(80, 30)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        

        
        # Ajouter la zone des boutons au layout principal
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.columns = []  # Liste de ColumnItem
        self.connection_manager = ConnectionManager(self.scene, self.columns)
        self._draw_columns()
        self._lock_columns_to_sides()
        self._setup_linking_events()

    def _random_color(self):
        """Génère une couleur vive aléatoire."""
        material_colors = [
            "#F44336",
            "#E91E63",
            "#9C27B0",
            "#673AB7",
            "#8E44AD" ,
            "#3F51B5",
            "#2196F3",
            "#03A9F4",
            "#00BCD4",
            "#009688",
            "#4CAF50",
            "#8BC34A",
            "#CDDC39",
            "#FFEB3B",
            "#FFC107",
            "#FF9800",
            "#FF5722",
            
        ]
        return random.choice(material_colors)

    def _draw_columns(self):
        """Initialise le fond de la vue graphique (inversé : foncé -> clair)."""
        self.view.setRenderHint(self.view.renderHints())
        self.view.setBackgroundBrush(QBrush(QColor(50, 53, 55)))  # fond général foncé

    def add_column(self, side, title, slots):
        """
        Ajoute une colonne à gauche ('left') ou à droite ('right') avec le titre donné.
        slots: liste de tuple (id, label) à afficher en colonne sous le titre.
        """
        col = ColumnItem(side, title, slots, self.scene, self._random_color)
        self.columns.append(col)
        self._update_column_positions()

    def _update_column_positions(self):
        """Place toutes les colonnes sur leur côté respectif, empilées verticalement."""
        view_width = self.view.viewport().width()
        margin = 10
        col_width = 220
        left_y = margin
        right_y = margin
        for col in self.columns:
            if col.side == 'left':
                x = margin
                y = left_y
                col_height = col.set_position(x, y)
                left_y += col_height + 8
            elif col.side == 'right':
                x = view_width - col_width - margin
                y = right_y
                col_height = col.set_position(x, y)
                right_y += col_height + 8
        total_height = max(left_y, right_y) + margin
        self.scene.setSceneRect(0, 0, view_width, total_height)
        self.connection_manager.update_connections()

    def _lock_columns_to_sides(self):
        """Met à jour la position des colonnes lors du resize de la vue."""
        def update_positions():
            self._update_column_positions()
        self.view.resizeEvent = lambda event: (update_positions(), QGraphicsView.resizeEvent(self.view, event))
        update_positions()

    def _find_slot_at_pos(self, pos, side=None):
        """Retourne (col_idx, slot_idx) du slot sous la position scene pos, ou None."""
        for col_idx, col in enumerate(self.columns):
            if side is not None and col.side != side:
                continue
            slot_idx = col.find_slot_at_pos(pos)
            if slot_idx is not None:
                return (col_idx, slot_idx)
        return None

    def _setup_linking_events(self):
        """Configure les événements souris pour la création/suppression de liens."""
        self.view.setMouseTracking(True)
        cm = self.connection_manager
        orig_mousePress = self.view.mousePressEvent
        orig_mouseMove = self.view.mouseMoveEvent
        orig_mouseRelease = self.view.mouseReleaseEvent

        def mousePressEvent(event):
            scene_pos = self.view.mapToScene(event.pos())
            if event.button() == Qt.RightButton:
                conn_idx = cm.find_connection_at_pos(scene_pos)
                if conn_idx is not None:
                    cm.remove_connection(conn_idx)
                    return
            slot = self._find_slot_at_pos(scene_pos, side='left')
            if slot and event.button() == Qt.LeftButton:
                cm.start_linking(*slot)
            else:
                orig_mousePress(event)

        def mouseMoveEvent(event):
            scene_pos = self.view.mapToScene(event.pos())
            if cm._linking:
                cm.update_preview_line(scene_pos)
            else:
                orig_mouseMove(event)

        def mouseReleaseEvent(event):
            scene_pos = self.view.mapToScene(event.pos())
            if cm._linking:
                cm.finish_linking(scene_pos, self._find_slot_at_pos, self.columns)
            else:
                orig_mouseRelease(event)

        self.view.mousePressEvent = mousePressEvent
        self.view.mouseMoveEvent = mouseMoveEvent
        self.view.mouseReleaseEvent = mouseReleaseEvent





if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    widget = LinksWidget()
    widget.resize(600, 400)

    widget.add_column('left', 'Variations', [
        ("g1", "Variation 01"),
        ("g2", "Variation 02"),
        ("g3", "Variation 03"),
        ("g4", "Variation 04"),
    ])
    widget.add_column('right', 'Materiaux', [
        ("t1", "Mat 01"),
        ("t2", "Mat 02"),
        ("t3", "Mat 03"),
        ("t4", "Mat 04"),
    ])
    widget.add_column('right', 'Geometries', [
        ("g1", "Geo 01"),
        ("g2", "Geo 02"),
        ("g3", "Geo 03"),
        ("g4", "Geo 04"),
    ])
    # Exemple de pré-remplissage de connexions
    widget.add_connections([
        {
            "from": {"column": "Variations", "slot_id": "g1"},
            "to":   {"column": "Materiaux", "slot_id": "t1"}
        },
        {
            "from": {"column": "Variations", "slot_id": "g1"},
            "to":   {"column": "Geometries", "slot_id": "g1"}
        }
    ])
    widget.show()
    # Affiche le résultat JSON à la fermeture de l'application
    def print_result():
        print("\nRésultat des connexions (JSON):\n" + widget.get_result_json())

    app.aboutToQuit.connect(print_result)
    sys.exit(app.exec())