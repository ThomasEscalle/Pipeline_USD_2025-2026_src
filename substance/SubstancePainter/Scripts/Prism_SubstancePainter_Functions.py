import os
import traceback
import json
import shutil
import time

import shiboken6
import weakref

os.environ["QT_API"] = "PySide6"   # force qtpy to use PySide6

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from PrismUtils.Decorators import err_catcher as err_catcher

import substance_painter.project
import substance_painter.ui
import substance_painter.export
import substance_painter.resource

from PrismUtils import PrismWidgets

from Prism_SubstancePainter_ExportTexture_Controllers import TextureExportController


class Prism_SubstancePainter_Functions(object):
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

        self.susMainWin = substance_painter.ui.get_main_window()

        self.core.registerCallback("masterVersionUpdated", self.fix_master_filename)
        self._event_tokens.append("masterVersionUpdated")

    @err_catcher(name=__name__)
    def startup(self, origin):
        origin.messageParent = None       
        self.createMenu(origin)

    @err_catcher(name=__name__)
    def createMenu(self, origin):
        # Create or get the top menu bar
        for menu in substance_painter.ui.get_main_window().menuBar().findChildren(QMenu):
            if menu.title() == "Prism":
                self.prism_menu = menu
                break
        else:
            # Create the Prism menu
            self.prism_menu = QMenu("Prism", substance_painter.ui.get_main_window())
            #menu_bar.addMenu(self.prism_menu)
            substance_painter.ui.add_menu(self.prism_menu)

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
        self._actions.append(action)

    # Example function
    @err_catcher(name=__name__)
    def save(self):
        print("saving version...")
        if not self.core.fileInPipeline():
            print("No file in pipeline, please save a scene first with the project browser.")
            return False
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
        if not self.core.fileInPipeline():
            print("No file in pipeline, please save a scene first with the project browser.")
            return False
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
            print("No project open")
            return False

        if not self.core.users.ensureUser():
            return False

        if not self.core.fileInPipeline():
            print("No file in pipeline, please save a scene first with the project browser.")
            return False
        
        self.core.messageParent = substance_painter.ui.get_main_window()

        self.savec = PrismWidgets.SaveComment(core=self.core)
        self.savec.accepted.connect(lambda: self.core.saveWithCommentAccepted(self.savec))
        self.savec.exec_()
        self.savec.activateWindow()

        self.core.messageParent = None

        return True


    @err_catcher(name=__name__)
    def open_project_browser(self):
        print("Opening Project Browser...")
        # call your existing logic here to show the browser
        try:
            if not hasattr(self, "_project_browser") or self._project_browser is None:
                print("Creating Prism Project Browser...")
                self.core.messageParent = substance_painter.ui.get_main_window()
                self._project_browser = self.core.projectBrowser()

            self._project_browser.show()

            self._project_browser.raise_()
            self._project_browser.activateWindow()
            self._project_browser.destroyed.connect(lambda: setattr(self.core, "messageParent", None))
            self.core.messageParent = None

        except Exception as e:
            import traceback
            print("Error opening Project Browser:", e)
            traceback.print_exc()

    @err_catcher(name=__name__)
    def import_geometry(self):
        if substance_painter.project.is_open():
            print("You can't import anything if a project is already open. Please open an empty Subtance Painter scene to import geometry.")
            return False
        print("Importing geometry...")
        # call your existing logic here to import geometry

        #create the state
        self.sm = self.core.getStateManager()

        state = self.sm.createState(
            "ImportFile",
            setActive=True,
            openProductsBrowser=False,
        )
        self.currentState = getattr(state, "state", None)

        # state is a QTreeWidgetItem — the UI object is on state.ui
        self.import_state = getattr(state, "ui", None)
        if self.import_state is None:
            print("State UI not found on the returned item. inspect state:", dir(state))
            return state

        # Save states to scene so PB finds them
        self.sm.saveStatesToScene()

        self.core.messageParent = substance_painter.ui.get_main_window()
        self.import_state.browse()
        self.core.messageParent = None

        return state

    @err_catcher(name=__name__)
    def export_textures(self):
        print("Exporting textures...")
        # call your existing logic here to export texture
        if substance_painter.project.is_open():
            self._textureUI = TextureExportController(core=self.core, parent=substance_painter.ui.get_main_window())
            self._textureUI.show()
        else:
            print("No project is open.")

    @err_catcher(name=__name__)
    def open_settings(self):
        print("Opening Settings...")
        self.core.messageParent = substance_painter.ui.get_main_window()
        self.settings = self.core.prismSettings()
        self.core.messageParent = None

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
        if name == None:
            name = ""
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
    def getCamNodes(self, origin):
        return []

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
        #mimic export texture logic but as a function with args
        pass

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
        #copy the given file into a temp folder before importing
        tempFolder = os.path.join(os.path.dirname(__file__), "importTemp")
        if not os.path.exists(tempFolder):
            os.makedirs(tempFolder)
        tempFile = os.path.join(tempFolder, os.path.basename(impFileName))
        shutil.copy2(impFileName, tempFile)
        print("importing file :", tempFile)
        result = substance_painter.project.create(mesh_file_path=tempFile)

        #clean the temp folder
        shutil.rmtree(tempFolder)
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
    
    def fix_master_filename(self, master_path):
        folder = os.path.dirname(master_path)
        files = os.listdir(folder)

        json_file = os.path.join(folder, "versioninfo.json")
        if not os.path.exists(json_file):
            print("[FixMasterName] No versioninfo.json found in:", folder)
            return

        with open(json_file, 'r') as file:
            context = json.load(file)

        version = context.get("version")
        if not version:
            print("[FixMasterName] No version found in versioninfo.json")
            return

        version_base = folder.replace("\\", "/").split("/")
        version_base.pop(-1)
        version_folder = "/".join(version_base) + "/" + version

        if not os.path.exists(version_folder):
            print("[FixMasterName] Version folder not found:", version_folder)
            return

        correct_files = os.listdir(version_folder)
        if not correct_files:
            print("[FixMasterName] No files in version folder:", version_folder)
            return
        if len(correct_files)<5:
            return

        correct_name = list(set(correct_files) - set(files))

        for f in files:
            if "master." in f:
                old_path = os.path.join(folder, f)
                new_path = os.path.join(folder, correct_name[0])
                print(f"[FixMasterName] Renaming {old_path} → {new_path}")
                os.rename(old_path, new_path)

    @err_catcher(name=__name__)
    def captureViewportThumbnail(self):
        """Capture the current viewport as a thumbnail image."""
        try:
            if not substance_painter.project.is_open():
                print("No project is open to capture a thumbnail.")
                return None

            viewer3D = self.susMainWin.findChild(QWidget, "Viewer3D")
            rect = viewer3D.rect()

            pixmap = QPixmap(rect.size())
            viewer3D.render(pixmap, QPoint(), QRegion(rect))

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
        print("Unregistering Prism SubstancePainter plugin...")
        self.susMainWin = None
        # --- 1. Remove menu actions ---
        try:
            for action in getattr(self, "_actions", []):
                self.prism_menu.removeAction(action)
                substance_painter.ui.delete_ui_element(action)
            self._actions.clear()
            substance_painter.ui.delete_ui_element(self.prism_menu)
            self.prism_menu = None
        except Exception as e:
            print("Error removing menu action:", e)
            traceback.print_exc()
        
        # --- 2. Remove QWidget ---
        if hasattr(self, "savec"):
            self.cleanup_widget(self.savec)
            self.savec = None

        if hasattr(self, "_project_browser"):
            self.cleanup_widget(self._project_browser)
            self._project_browser = None

        if hasattr(self, "import_state"):
            self.cleanup_widget(self.import_state)
            self.import_state = None

        if hasattr(self, "_textureUI"):
            if hasattr(self._textureUI, "state") and not hasattr(self, "sm"):
                self.cleanup_widget(self._textureUI.state)
                self._textureUI.state = None
            if hasattr(self._textureUI, "sm") and not hasattr(self, "sm"):
                self.cleanup_widget(self._textureUI.sm)
                try: 
                    self._textureUI.sm.tw_export.clear()
                except:
                    pass
                self._textureUI.sm = None
            self._textureUI.cleanup()
            self.cleanup_widget(self._textureUI)
            self._textureUI = None

        #Clean up the product browser if it exists
        for w in QApplication.allWidgets():
            try:
                if isinstance(w, QWidget) and "productbrowser" in w.__class__.__name__.lower():
                    self.cleanup_widget(w)
            except Exception:
                pass

        if hasattr(self, "sm"):
            self.cleanup_widget(self.sm)
            self.sm = None

        if hasattr(self, "settings"):
            self.cleanup_widget(self.settings)
            self.settings = None

        for info in getattr(self, "_event_tokens", []) or []:
            try:
                # Try different host APIs safely
                if hasattr(self.core, "unregisterCallback"):
                    try:
                        self.core.unregisterCallback(info)
                    except Exception:
                        # fallback to removeCallback or remove_callback variants
                        pass

            except Exception:
                pass
        self._event_tokens.clear()
        # --- 6. Clear remaining references ---
        self.currentState = None
        self.susMainWin = None
        self.plugin = None


    def cleanup_widget(self, widget: QWidget):
        """
        Safely remove and delete a QWidget and all its children.
        """
        if widget is None:
            return

        try:
            #---STop thread and timer---
            for t in widget.findChildren(QTimer):
                t.stop()
                t.deleteLater()
            for th in widget.findChildren(QThread):
                th.quit()
                th.wait(2000)
                th.deleteLater()

            print(widget)
            widget.setParent(None)
            # Hide before deleting (optional, prevents UI glitches)
            widget.hide()
            #disconnect signals
            for signal in widget.findChildren(QObject):
                try:
                    signal.disconnect()
                    print("some signals disconnnect")
                except Exception:
                    pass
            try:
                widget.disconnect()
                print("something disconnnect")
            except:
                pass
            widget.close
            # Schedule deletion safely
            substance_painter.ui.delete_ui_element(widget)
        except Exception as e:
            print(f"Error cleaning up widget {widget}: {e}")