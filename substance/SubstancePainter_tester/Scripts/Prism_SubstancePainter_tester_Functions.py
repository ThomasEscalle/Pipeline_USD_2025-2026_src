import os
import traceback
import json
import pathlib
import time
import tempfile

os.environ["QT_API"] = "pyside6"   # force qtpy to use PySide6
import qtpy

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6 import QtCore

from PrismUtils.Decorators import err_catcher as err_catcher

import substance_painter.project
import substance_painter.ui
import substance_painter.export
import substance_painter.resource
import substance_painter.event

from PrismUtils import PrismWidgets

from Prism_SubstancePainter_tester_ExportTexture_Controllers import TextureExportController



class Prism_SubstancePainter_tester_Functions(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin
        self.currentState = {
                "states": [
                    {
                        "statename": "publish",
                        "comment": "",
                        "description": ""
                    }
                ]
            }
        self.currentState = json.dumps(self.currentState)  # convert dict to JSON string

        # Add tracking lists for cleanup
        self._actions = []
        self._qt_objects = []
        self._dock_widgets = []
        self._timers = []
        self._threads = []
        self._event_tokens = []

        #app = QApplication.instance()
        #if app:
        #    app.aboutToQuit.connect(self.on_app_quit)


    @err_catcher(name=__name__)
    def startup(self, origin):
        #origin.startAutosaveTimer()
        origin.timer.stop()
        origin.messageParent = substance_painter.ui.get_main_window()          
        self.createMenu(origin)
        pass

    @err_catcher(name=__name__)
    def createMenu(self, origin):
    # Try to find an existing Prism menu in the menu bar
        existing_menu = None
        for menu in substance_painter.ui.get_main_window().menuBar().findChildren(QMenu):
            if menu.title() == "Prism":
                existing_menu = menu
                break

        if existing_menu:
            # Menu exists, track it
            self.prism_menu = existing_menu
            return  # Already present, no need to add again
        
        # Create the Prism menu
        self.prism_menu = QMenu("Prism", substance_painter.ui.get_main_window())
        substance_painter.ui.add_menu(self.prism_menu)

        iconPath = self.core.getConfig("globals", "current project").replace("\\", "/")[:-13]  + "Icons/TOPHIT.png"
        print(iconPath)

        icon = QIcon(iconPath)
        self.prism_menu.setIcon(icon)

        # Add actions
        self.add_menu_action("Save", self.save)
        self.add_menu_action("Save Version", self.save_version)
        self.add_menu_action("Save Comment", self.save_comment)
        self.add_menu_action("Project Browser", self.open_project_browser)
        self.add_menu_action("Import Geometry", self.import_geometry)
        self.add_menu_action("Export Textures", self.export_textures)
        self.add_menu_action("Settings", self.open_settings)
    
    @err_catcher(name=__name__)
    def add_menu_action(self, name, callback):
        action = QAction(name, substance_painter.ui.get_main_window())
        action.triggered.connect(callback)
        self.prism_menu.addAction(action)
        self._actions.append(action)  # Track action for cleanup


    # Example function
    @err_catcher(name=__name__)
    def save(self):
        curFileName = self.core.getCurrentFileName()

        substance_painter.project.save()

        #getting data
        data = self.core.getScenefileData(curFileName)
        self.core.saveVersionInfo(curFileName, data)

        #getting thumbnail
        self.captureViewportThumbnail()

    @err_catcher(name=__name__)
    def save_version(self):
        print("saving version...")
        # call your existing logic here to save version
        curFileName = self.core.getCurrentFileName()
        filePath = curFileName.split(".")[0]

        ext = curFileName.split(".")[1]
        version = int(filePath[-4:])
        newVersion = version + 1
        versName = filePath[:-4] + str(newVersion).zfill(4) + "." + ext
        substance_painter.project.save_as(versName)

        #getting data
        data = self.core.getScenefileData(versName)        
        self.core.saveVersionInfo(versName, data)
        #getting thumbnail
        self.captureViewportThumbnail()
    
    @err_catcher(name=__name__)
    def save_comment(self):
        print("Saving comment...")
        if not self.core.projects.ensureProject():
            return False

        if not self.core.users.ensureUser():
            return False

        if not self.core.fileInPipeline():
            self.core.showFileNotInProjectWarning()
            return False

        self.core.savec = PrismWidgets.SaveComment(core=self.core)
        self.core.savec.accepted.connect(lambda: self.core.saveWithCommentAccepted(self.core.savec))
        self.core.savec.show()
        self.core.savec.activateWindow()
        return True


    @err_catcher(name=__name__)
    def open_project_browser(self):
        print("Opening Project Browser...")
        # call your existing logic here to show the browser
        try:
            if not hasattr(self, "_project_browser") or self._project_browser is None:
                print("Creating Prism Project Browser...")
                self._project_browser = self.core.projectBrowser()

            self._project_browser.show()
            self._project_browser.raise_()
            self._project_browser.activateWindow()

        except Exception as e:
            import traceback
            print("Error opening Project Browser:", e)
            traceback.print_exc()

    @err_catcher(name=__name__)
    def import_geometry(self):
        print("Importing geometry...")
        # call your existing logic here to import geometry

        #create the state
        sm = self.core.getStateManager()

        state = sm.createState(
            "ImportFile",
            setActive=True,
            openProductsBrowser=False,
        )
        self.currentState = getattr(state, "state", None)

        # state is a QTreeWidgetItem — the UI object is on state.ui
        import_state = getattr(state, "ui", None)
        if import_state is None:
            print("State UI not found on the returned item. inspect state:", dir(state))
            return state

        # Save states to scene so PB finds them
        sm.saveStatesToScene()

        import_state.browse()

        return state

    @err_catcher(name=__name__)
    def export_textures(self):
        print("Exporting textures...")
        # call your existing logic here to export texture
        if substance_painter.project.is_open():
            _textureUI = TextureExportController(core=self.core, parent=substance_painter.ui.get_main_window())
            _textureUI.exec_()
        else:
            print("No project is open.")

    @err_catcher(name=__name__)
    def open_settings(self):
        print("Opening Settings...")
        # call your existing logic here to show the browser


    @err_catcher(name=__name__)
    def autosaveEnabled(self, origin):
        # get autosave enabled
        return False

    @err_catcher(name=__name__)
    def sceneOpen(self, origin):
        if self.core.shouldAutosaveTimerRun():
            origin.startAutosaveTimer()

    @err_catcher(name=__name__)
    def getCurrentFileName(self, origin, path=True):
        if substance_painter.project.is_open():
            if path:
                try :
                    name = substance_painter.project.file_path()
                except Exception as e:
                    print("failed to get current file name : ", e)
                    traceback.print_exc()
            else:
                try:
                    name = substance_painter.project.name()
                except Exception as e:
                    print("failed to get current file name : ", e)
                    traceback.print_exc()
        else:
            name = "no file path yet"
        return name

    @err_catcher(name=__name__)
    def getSceneExtension(self, origin):
        return self.sceneFormats[0]

    @err_catcher(name=__name__)
    def saveScene(self, origin, filepath, details={}):
        """Save the current scene to the given path from Prism's versioning system."""
        #make sure it ends with .spp
        filepath = filepath.split(".")[0]
        filepath += ".spp"

        try:
            # Ensure we have a project open
            if not substance_painter.project.is_open():
                print("No project open in Substance Painter.")
                return

            substance_painter.project.save_as(filepath)
            print(f"Scene saved to new version: {filepath}")

        except Exception as e:
            print("Failed to save new version:", e)
            traceback.print_exc()        
        return True

    @err_catcher(name=__name__)
    def getImportPaths(self, origin):
        return []


    @err_catcher(name=__name__)
    def getAppVersion(self, origin):
        return "1.0"

    @err_catcher(name=__name__)
    def openScene(self, origin, filepath, force=False):
        if not substance_painter.project.is_open():
            substance_painter.project.open(filepath)
            return True
        else :
            return True

    @err_catcher(name=__name__)
    def sm_export_addObjects(self, origin, objects=None):
        if not objects:
            objects = []  # get selected objects from scene

        for i in objects:
            if not i in origin.nodes:
                origin.nodes.append(i)

        origin.updateUi()
        origin.stateManager.saveStatesToScene()

    @err_catcher(name=__name__)
    def getNodeName(self, origin, node):
        if self.isNodeValid(origin, node):
            try:
                return node.name
            except:
                QMessageBox.warning(
                    self.core.messageParent, "Warning", "Cannot get name from %s" % node
                )
                return node
        else:
            return "invalid"

    @err_catcher(name=__name__)
    def selectNodes(self, origin):
        if origin.lw_objects.selectedItems() != []:
            nodes = []
            for i in origin.lw_objects.selectedItems():
                node = origin.nodes[origin.lw_objects.row(i)]
                if self.isNodeValid(origin, node):
                    nodes.append(node)
            # select(nodes)

    @err_catcher(name=__name__)
    def isNodeValid(self, origin, handle):
        return True

    @err_catcher(name=__name__)
    def sm_export_startup(self, origin):
        pass

    @err_catcher(name=__name__)
    def sm_export_removeSetItem(self, origin, node):
        pass

    @err_catcher(name=__name__)
    def sm_export_clearSet(self, origin):
        pass

    @err_catcher(name=__name__)
    def sm_export_updateObjects(self, origin):
        pass

    @err_catcher(name=__name__)
    def sm_export_exportShotcam(self, origin, startFrame, endFrame, outputName):
        result = self.sm_export_exportAppObjects(
            origin,
            startFrame,
            endFrame,
            (outputName + ".abc"),
            nodes=[origin.curCam],
            expType=".abc",
        )
        result = self.sm_export_exportAppObjects(
            origin,
            startFrame,
            endFrame,
            (outputName + ".fbx"),
            nodes=[origin.curCam],
            expType=".fbx",
        )
        return result

    @err_catcher(name=__name__)
    def sm_export_exportAppObjects(
        self,
        origin,
        startFrame,
        endFrame,
        outputName,
        scaledExport=False,
        nodes=None,
        expType=None,
    ):
        self._textureUI = TextureExportController(substance_painter.ui.get_main_window())
        self._textureUI.exec_()

    @err_catcher(name=__name__)
    def sm_export_preDelete(self, origin):
        pass

    @err_catcher(name=__name__)
    def sm_export_unColorObjList(self, origin):
        origin.lw_objects.setStyleSheet(
            "QListWidget { border: 3px solid rgb(50,50,50); }"
        )

    @err_catcher(name=__name__)
    def sm_export_typeChanged(self, origin, idx):
        pass

    @err_catcher(name=__name__)
    def sm_export_preExecute(self, origin, startFrame, endFrame):
        warnings = []

        return warnings

    @err_catcher(name=__name__)
    def sm_export_loadData(self, origin, data):
        pass

    @err_catcher(name=__name__)
    def sm_export_getStateProps(self, origin, stateProps):
        stateProps.update()

        return stateProps

    @err_catcher(name=__name__)
    def sm_render_openPasses(self, origin, item=None):
        pass

    @err_catcher(name=__name__)
    def removeAOV(self, aovName):
        pass

    @err_catcher(name=__name__)
    def sm_render_getDeadlineParams(self, origin, dlParams, homeDir):
        pass

    @err_catcher(name=__name__)
    def getCurrentSceneFiles(self, origin):
        curFileName = self.core.getCurrentFileName()
        scenefiles = [curFileName]
        return scenefiles

    @err_catcher(name=__name__)
    def sm_render_preExecute(self, origin):
        warnings = []

        return warnings

    @err_catcher(name=__name__)
    def getProgramVersion(self, origin):
        return "1.0"

    @err_catcher(name=__name__)
    def sm_render_getDeadlineSubmissionParams(self, origin, dlParams, jobOutputFile):
        dlParams["Build"] = dlParams["build"]
        dlParams["OutputFilePath"] = os.path.split(jobOutputFile)[0]
        dlParams["OutputFilePrefix"] = os.path.splitext(
            os.path.basename(jobOutputFile)
        )[0]
        dlParams["Renderer"] = self.getCurrentRenderer(origin)

        if origin.chb_resOverride.isChecked() and "resolution" in dlParams:
            resString = "Image"
            dlParams[resString + "Width"] = str(origin.sp_resWidth.value())
            dlParams[resString + "Height"] = str(origin.sp_resHeight.value())

        return dlParams

    @err_catcher(name=__name__)
    def deleteNodes(self, origin, handles, num=0):
        pass

    @err_catcher(name=__name__)
    def sm_import_disableObjectTracking(self, origin):
        self.deleteNodes(origin, [origin.setName])

    @err_catcher(name=__name__)
    def sm_import_importToApp(self, origin, doImport, update, impFileName):
        result = substance_painter.project.create(mesh_file_path=impFileName)
        result = True
        return {"result": result, "doImport": doImport}

    @err_catcher(name=__name__)
    def sm_import_updateObjects(self, origin):
        pass

    @err_catcher(name=__name__)
    def sm_import_removeNameSpaces(self, origin):
        pass

    @err_catcher(name=__name__)
    def sm_playblast_startup(self, origin):
        frange = self.getFrameRange(origin)
        origin.sp_rangeStart.setValue(frange[0])
        origin.sp_rangeEnd.setValue(frange[1])

    @err_catcher(name=__name__)
    def sm_saveStates(self, origin, buf):
        pass

    @err_catcher(name=__name__)
    def sm_saveImports(self, origin, importPaths):
        pass

    @err_catcher(name=__name__)
    def sm_readStates(self, origin):
        if substance_painter.project.is_open():
            state = self.currentState
            if isinstance(state, dict):
                state = json.dumps(state)  # convert dict to JSON string
        else:
            fallback_state = {
                "states": [
                    {
                        "statename": "publish",
                        "comment": "",
                        "description": ""
                    }
                ]
            }
            state = json.dumps(fallback_state)  # produces a JSON str
        return state

    
    @err_catcher(name=__name__)
    def sm_deleteStates(self, origin):
        pass

    @err_catcher(name=__name__)
    def sm_getExternalFiles(self, origin):
        extFiles = []
        return [extFiles, []]

    @err_catcher(name=__name__)
    def sm_createRenderPressed(self, origin):
        origin.createPressed("Render")

    @err_catcher(name=__name__)
    def captureViewportThumbnail(self):
        """Capture the current viewport as a thumbnail image."""
        try:
            if not substance_painter.project.is_open():
                print("No project is open to capture a thumbnail.")
                return None

            rect = substance_painter.ui.get_main_window().findChild(QWidget, "Viewer3D").rect()

            pixmap = QPixmap(rect.size())
            substance_painter.ui.get_main_window().findChild(QWidget, "Viewer3D").render(pixmap, QPoint(), QRegion(rect))

            if pixmap:
                thumbnail_path = self.core.getCurrentFileName().replace(".spp", "preview.jpg")
                pixmap.save(thumbnail_path, "JPG")
                print(f"Thumbnail saved to: {thumbnail_path}")
                return pixmap
            else:
                print("Failed to capture viewport snapshot.")
                return None
        except Exception as e:
            print("Error capturing viewport thumbnail:", e)
            traceback.print_exc()
            return None

    @err_catcher(name=__name__)
    def unregister(self):
        """Clean up plugin resources when Substance Painter closes."""
        # Remove actions and menus from UI, but do NOT delete them
        for action in self.prism_menu.menuAction():
            substance_painter.ui.delete_ui_element(action)
        self._actions.clear()

        if hasattr(self, "prism_menu") and self.prism_menu:
            substance_painter.ui.delete_ui_element(self.prism_menu)
            self.prism_menu = None

        # Clear Python references to widgets and dialogs
        self._qt_objects.clear()
        self._dock_widgets.clear()
        self._textureUI = None
        self._project_browser = None
        self.plugin = None
        self.currentState = None
        
    def on_app_quit(self):
        self.plugin = None
        self.currentState = None
        self._qt_objects.clear()
        self._dock_widgets.clear()
        self._actions.clear()


