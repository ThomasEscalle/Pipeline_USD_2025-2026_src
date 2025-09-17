from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from pxr import Usdviewq, Usd, UsdGeom

# Product Viewer is a 3D Viewer for the USD Files
class Product3DViewer(QDialog):
    def __init__(self, parent=None):
        super(Product3DViewer, self).__init__(parent)
        self.setObjectName("Product3DViewer")

        self.setWindowTitle("Product 3D Viewer")

        # Create the main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Create the QMenuBar
        self.menuBar = QMenuBar(self)
        self.menuBar.setObjectName("menuBar")
        self.layout.addWidget(self.menuBar)

        # Create the 3D view
        self._dataModel = None
        self.stageview = None
        
        try:
            from pxr import Usd, UsdGeom, Usdviewq

            # 1. Créer un Timer simple (fonction makeTimer)
            def make_timer(label, printTiming=False):
                return Usdviewq.common.Timer(label=label, printTiming=printTiming)
            
            # 2. Créer des Settings minimales (éphémères, sans fichier)
            settings = Usdviewq.settings.Settings(version = "1")

            # 3. Créer un DataModel avec les settings et le timer
            self._dataModel = Usdviewq.appController.UsdviewDataModel(settings=settings, makeTimer=make_timer)

            self.stageview = Usdviewq.stageView.StageView( parent = self ,dataModel = self._dataModel)
            # Make the stageview fill the entire ProductViewer
            self.stageview.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.layout.addWidget(self.stageview)
        except Exception as e:
            # Si l'initialisation USD échoue, afficher un message d'erreur
            error_label = QLabel(f"Erreur lors de l'initialisation USD: {str(e)}")
            error_label.setAlignment(Qt.AlignCenter)
            error_label.setStyleSheet("color: red; font-size: 14px;")
            self.layout.addWidget(error_label)


        self.initMenu()


    def setStage(self, stage):
        # Vérifier si le _dataModel est correctement initialisé
        if not hasattr(self, '_dataModel') or self._dataModel is None:
            QMessageBox.warning(self, "Erreur", "Le viewer USD n'est pas correctement initialisé.")
            return
        
        # Set the stage in the data model
        try:
            self._dataModel.stage = stage
            self.stageview.updateView(resetCam=True, forceComputeBBox=False)
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Impossible de définir la scène: {str(e)}")

    def setFileStage(self, filePath):
        # Vérifier si le _dataModel est correctement initialisé
        if not hasattr(self, '_dataModel') or self._dataModel is None:
            QMessageBox.warning(self, "Erreur", "Le viewer USD n'est pas correctement initialisé.")
            return
        
        # Set the stage from a file path
        try:
            self._dataModel.stage = Usd.Stage.Open(filePath)
            self.stageview.updateView(resetCam=True, forceComputeBBox=False)
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Impossible de charger la scène depuis le fichier: {str(e)}")


    def initMenu(self):
        # Create the "File" menu
        fileMenu = self.menuBar.addMenu("File")

        # Create the "Edit" menu
        editMenu = self.menuBar.addMenu("Edit")

        # Create the "View" menu
        viewMenu = self.menuBar.addMenu("View")

        # Add a "Render Mode menu to the View menu
        renderModeMenu = viewMenu.addMenu("Render Mode")
        # WIREFRAME = "Wireframe"
        # WIREFRAME_ON_SURFACE = "WireframeOnSurface"
        # SMOOTH_SHADED = "Smooth Shaded"
        # FLAT_SHADED = "Flat Shaded"
        # POINTS = "Points"
        # GEOM_ONLY = "Geom Only"
        # GEOM_FLAT = "Geom Flat"
        # GEOM_SMOOTH = "Geom Smooth"
        # HIDDEN_SURFACE_WIREFRAME = "Hidden Surface Wireframe"
        
        # Create one action for each render mode
        WireFrameAction = QAction("Wireframe", self)
        WireFrameAction.triggered.connect(lambda: self.setRenderMode("Wireframe"))
        renderModeMenu.addAction(WireFrameAction)

        WireFrameOnSurfaceAction = QAction("Wireframe On Surface", self)
        WireFrameOnSurfaceAction.triggered.connect(lambda: self.setRenderMode("WireframeOnSurface"))
        renderModeMenu.addAction(WireFrameOnSurfaceAction)

        SmoothShadedAction = QAction("Smooth Shaded", self)
        SmoothShadedAction.triggered.connect(lambda: self.setRenderMode("SmoothShaded"))
        renderModeMenu.addAction(SmoothShadedAction)

        FlatShadedAction = QAction("Flat Shaded", self)
        FlatShadedAction.triggered.connect(lambda: self.setRenderMode("FlatShaded"))
        renderModeMenu.addAction(FlatShadedAction)

        PointsAction = QAction("Points", self)
        PointsAction.triggered.connect(lambda: self.setRenderMode("Points"))
        renderModeMenu.addAction(PointsAction)

        GeomOnlyAction = QAction("Geom Only", self)
        GeomOnlyAction.triggered.connect(lambda: self.setRenderMode("GeomOnly"))
        renderModeMenu.addAction(GeomOnlyAction)

        GeomFlatAction = QAction("Geom Flat", self)
        GeomFlatAction.triggered.connect(lambda: self.setRenderMode("GeomFlat"))
        renderModeMenu.addAction(GeomFlatAction)

        GeomSmoothAction = QAction("Geom Smooth", self)
        GeomSmoothAction.triggered.connect(lambda: self.setRenderMode("GeomSmooth"))
        renderModeMenu.addAction(GeomSmoothAction)

        # Add a toggle Wireframe action
        wireframeAction = QAction("Toggle Wireframe", self)
        wireframeAction.setShortcut(QKeySequence("W"))
        wireframeAction.triggered.connect(self.wireframeActionTriggered)
        viewMenu.addAction(wireframeAction)

        # Add a separator
        viewMenu.addSeparator()

        # Add a Center View action
        centerViewAction = QAction("Frame View", self)
        centerViewAction.setShortcut(QKeySequence("F"))
        centerViewAction.triggered.connect(self.frameViewActionTriggered)
        viewMenu.addAction(centerViewAction)

        # Add a separator
        viewMenu.addSeparator()

        # Add a Display Proxy geometry action
        displayProxyAction = QAction("Display Proxy", self)
        displayProxyAction.setCheckable(True)
        displayProxyAction.setChecked(True)
        displayProxyAction.triggered.connect(self.toggleDisplayProxy)
        viewMenu.addAction(displayProxyAction)

        # Add a display Render geometry action
        displayRenderAction = QAction("Display Render", self)
        displayRenderAction.setCheckable(True)
        displayRenderAction.setChecked(False)
        viewMenu.addAction(displayRenderAction)

    def toggleDisplayProxy(self, checked):
        self._dataModel.viewSettings.displayProxy = not checked

    def toggleDisplayRender(self, checked):
        self._dataModel.viewSettings.displayRender = checked

    def setRenderMode(self, mode):
        # Vérifier si le _dataModel est correctement initialisé
        if not hasattr(self, '_dataModel') or self._dataModel is None:
            QMessageBox.warning(self, "Erreur", "Le viewer USD n'est pas correctement initialisé.")
            return
        
        # Set the render mode
        try:
            from pxr.Usdviewq.common import RenderModes
            
            if mode == "Wireframe":
                self._dataModel.viewSettings.renderMode = RenderModes.WIREFRAME
            elif mode == "WireframeOnSurface":
                self._dataModel.viewSettings.renderMode = RenderModes.WIREFRAME_ON_SURFACE
            elif mode == "SmoothShaded":
                self._dataModel.viewSettings.renderMode = RenderModes.SMOOTH_SHADED
            elif mode == "FlatShaded":
                self._dataModel.viewSettings.renderMode = RenderModes.FLAT_SHADED
            elif mode == "Points":
                self._dataModel.viewSettings.renderMode = RenderModes.POINTS
            elif mode == "GeomOnly":
                self._dataModel.viewSettings.renderMode = RenderModes.GEOM_ONLY
            elif mode == "GeomFlat":
                self._dataModel.viewSettings.renderMode = RenderModes.GEOM_FLAT
            elif mode == "GeomSmooth":
                self._dataModel.viewSettings.renderMode = RenderModes.GEOM_SMOOTH
            elif mode == "HiddenSurfaceWireframe":
                self._dataModel.viewSettings.renderMode = RenderModes.HIDDEN_SURFACE_WIREFRAME

        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Impossible de changer le mode de rendu: {str(e)}")

    # Wireframe action triggered
    def wireframeActionTriggered(self):
        # Vérifier si le _dataModel est correctement initialisé
        if not hasattr(self, '_dataModel') or self._dataModel is None:
            QMessageBox.warning(self, "Erreur", "Le viewer USD n'est pas correctement initialisé.")
            return
        
        # Toggle wireframe mode
        try:
            from pxr.Usdviewq.common import RenderModes
            
            current_mode = self._dataModel.viewSettings.renderMode
            
            if current_mode == RenderModes.WIREFRAME:
                self._dataModel.viewSettings.renderMode = RenderModes.SMOOTH_SHADED
            else:
                self._dataModel.viewSettings.renderMode = RenderModes.WIREFRAME

        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Impossible de changer le mode wireframe: {str(e)}")



    def frameViewActionTriggered(self):
        # Vérifier si le _dataModel est correctement initialisé
        if not hasattr(self, '_dataModel') or self._dataModel is None:
            QMessageBox.warning(self, "Erreur", "Le viewer USD n'est pas correctement initialisé.")
            return
        
        # Frame the view
        try:
            self.stageview.updateView(resetCam=True, forceComputeBBox=False)
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Impossible de centrer la vue: {str(e)}")