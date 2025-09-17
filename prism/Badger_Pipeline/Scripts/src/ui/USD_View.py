from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

import subprocess

def custom_cleanAndClose(self):
    # Ici, mets le code pour fermer seulement la fenêtre, pas toute l'application
    # Par exemple : self._window.close() ou autre selon l'implémentation
    print("AppController se ferme sans quitter toute l'application.")
    # ... ton code ...
    # This function is called by the main window's closeEvent handler.
    # Close stage and release renderer resources (if applicable).
    self._closeStage()

    self._configManager.close()
    # If the current path widget is focused when closing usdview, it can
    # trigger an "editingFinished()" signal, which will look for a prim in
    # the scene (which is already deleted). This prevents that.
    # XXX:
    # This method is reentrant and calling disconnect twice on a signal
    # causes an exception to be thrown.
    try:
        self._ui.currentPathWidget.editingFinished.disconnect(
            self._currentPathChanged)
    except RuntimeError:
        pass
    # Shut down some timers and our eventFilter
    self._primViewUpdateTimer.stop()
    self._guiResetTimer.stop()
    QApplication.instance().removeEventFilter(self._filterObj)
    
    # If the timer is currently active, stop it from being invoked while
    # the USD stage is being torn down.
    if self._qtimer.isActive():
        self._qtimer.stop()


def custom_setStyleSheetUsingState(self):
    # Ici, mets le code pour appliquer le style sans affecter l'application entière
    print("Application du style personnalisé sans affecter l'application entière.")
    # ... ton code ...

class USD_View():


    def __init__(self, file_path):
        
        from pxr import Usdviewq, Usd, UsdGeom, Ar, UsdAppUtils,UsdUtils ,Sdf
        from pxr.Usdviewq.appController import AppController
        from pxr.Usdviewq.settings import ConfigManager
        import argparse


        def my_context_creator(usdFile):
            r = Ar.GetResolver()
            # Optionnel, pour compatibilité avec Ar 1.0
            if hasattr(r, "ConfigureResolverForAsset"):
                r.ConfigureResolverForAsset(usdFile)
            return r.CreateDefaultContextForAsset(usdFile)

        # Crée un objet arg_parse_result minimal
        arg_parse_result = argparse.Namespace(
            usdFile=file_path,
            primPath="/",
            complexity = UsdAppUtils.complexityArgs.RefinementComplexities.LOW,
            camera=Sdf.Path(UsdUtils.GetPrimaryCameraName()),
            populationMask=None,
            clearSettings=False,
            config=ConfigManager.defaultConfig,
            defaultSettings=False,
            noRender=False,
            noPlugins=False,
            unloaded=False,
            timing=False,
            allowAsync=False,
            traceToFile=None,
            traceFormat="chrome",
            tracePython=False,
            mallocTagStats="none",
            numThreads=0,
            firstframe=None,
            lastframe=None,
            currentframe=None,
            quitAfterStartup=False,
            sessionLayer=None,
            muteLayersRe=None,
            detachLayers=False,
            detachLayersInclude=None,
            detachLayersExclude=None,
            rendererPlugin=None,
        )

        resolverContextFn = lambda usdFile: my_context_creator(usdFile)

        # Run the app
        AppController._cleanAndClose = custom_cleanAndClose
        AppController._setStyleSheetUsingState = custom_setStyleSheetUsingState
        appController = AppController(arg_parse_result, resolverContextFn)