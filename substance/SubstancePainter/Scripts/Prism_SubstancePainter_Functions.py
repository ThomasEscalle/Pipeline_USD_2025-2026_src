import os
import traceback
import json

os.environ["QT_API"] = "pyside6"   # force qtpy to use PySide6
import qtpy

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

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
        self.susMainWin = substance_painter.ui.get_main_window()
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

        self.hasQtParent = True

        # Add tracking lists for cleanup
        self._actions = []
        self._qt_objects = []
        self._dock_widgets = []
        self._timers = []
        self._threads = []
        self._event_tokens = []

        for widget in QApplication.allWidgets():
            # Replace 'PrismProjectBrowser' with the actual class name if different
            if widget.__class__.__name__ == "mv_ProjectBrowser" and widget.isVisible():
                self._project_browser = widget
                print("Tracked existing Prism Project Browser:", widget)
                break

        self.core.registerCallback("masterVersionUpdated", self.fix_master_filename)
        self.core.registerCallback("onStateManagerOpen", self.onStateManagerOpen, plugin=self)

    @err_catcher(name=__name__)
    def startup(self, origin):
        #origin.startAutosaveTimer()
        origin.messageParent = self.susMainWin
        self.createMenu(origin)

    @err_catcher(name=__name__)
    def createMenu(self, origin):
        # Create or get the top menu bar
        for menu in self.susMainWin.menuBar().findChildren(QMenu):
            if menu.title() == "Prism":
                self.prism_menu = menu
                break
        else:
            menu_bar = self.susMainWin.menuBar()

            # Create the Prism menu
            self.prism_menu = QMenu("Prism", self.susMainWin)
            #menu_bar.addMenu(self.prism_menu)
            substance_painter.ui.add_menu(self.prism_menu)

            iconPath = self.core.getConfig("globals", "current project").replace("\\", "/")[:-13]  + "Icons/TOPHIT.png"
            print(iconPath)

            icon = QIcon(iconPath)

            self.prism_menu.setTitle("")
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
        action = QAction(name, self.susMainWin)
        action.triggered.connect(callback)
        self.prism_menu.addAction(action)
        #substance_painter.ui.add_action(self.prism_menu, action)

    def onStateManagerOpen(self, origin):
        origin.loadState(ExportTextureClass)

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
            _textureUI = TextureExportController(core=self.core, parent=self.susMainWin)
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
        self._textureUI = TextureExportController(self.susMainWin)
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

            rect = self.susMainWin.findChild(QWidget, "Viewer3D").rect()

            pixmap = QPixmap(rect.size())
            self.susMainWin.findChild(QWidget, "Viewer3D").render(pixmap, QPoint(), QRegion(rect))

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
        # --- 1. Remove menu actions ---
        try:
            if hasattr(self, "prism_menu") and self.prism_menu:
                self.prism_menu.removeAction(self.prism_menu.menuAction())
                self.prism_menu.deleteLater()
                self.prism_menu = None
                print("Removed Prism menu action.")
        except Exception as e:
            print("Error removing menu action:", e)
            traceback.print_exc()

        # --- 6. Clear remaining references ---
        self.core = None
        self.plugin = None
        self.susMainWin = None
        self.currentState = None


class ExportTextureClass(QWidget):
    className = "ExportTexture"
    listType = "Export"

    def setup(self, state, core, stateManager, stateData=None):
        self.core = core
        self.state = state
        self.stateManager = stateManager
        self.canSetVersion = True
        self.setupUi()
        self.connectEvents()

        if stateData is not None:
            self.loadData(stateData)

    @err_catcher(name=__name__)
    def loadData(self, data):
        if "statename" in data:
            self.e_name.setText(data["statename"])
        if "option1" in data:
            self.chb_option1.setChecked(data["option1"])
        if "fileFormat" in data:
            idx = self.cb_format.find(data["fileFormat"])
            if idx != -1:
                self.cb_format.setCurrentIndex(idx)
        if "stateenabled" in data and self.listType == "Export":
            self.state.setCheckState(
                0,
                eval(
                    data["stateenabled"]
                    .replace("PySide.QtCore.", "")
                    .replace("PySide2.QtCore.", "")
                ),
            )

        self.core.callback("onStateSettingsLoaded", self, data)

    @err_catcher(name=__name__)
    def setupUi(self):
        self.lo_main = QVBoxLayout(self)
        self.w_name = QWidget()
        self.lo_name = QHBoxLayout(self.w_name)
        self.l_name = QLabel("Name:")
        self.e_name = QLineEdit()
        self.e_name.setText(self.state.text(0))
        self.l_name.setVisible(False)
        self.e_name.setVisible(False)
        self.lo_name.addWidget(self.l_name)
        self.lo_name.addWidget(self.e_name)

        self.gb_general = QGroupBox("General")
        self.lo_general = QVBoxLayout(self.gb_general)

        self.w_option1 = QWidget()
        self.lo_option1 = QHBoxLayout(self.w_option1)
        self.l_option1 = QLabel("Option1:")
        self.chb_option1 = QCheckBox()
        self.lo_option1.addWidget(self.l_option1)
        self.lo_option1.addStretch()
        self.lo_option1.addWidget(self.chb_option1)

        self.w_format = QWidget()
        self.lo_format = QHBoxLayout(self.w_format)
        self.l_format = QLabel("Format:")
        self.cb_format = QComboBox()
        self.cb_format.addItems([".f1", "f2"])
        self.lo_format.addWidget(self.l_format)
        self.lo_format.addStretch()
        self.lo_format.addWidget(self.cb_format)

        self.lo_general.addWidget(self.w_option1)
        self.lo_general.addWidget(self.w_format)

        self.lo_main.addWidget(self.w_name)
        self.lo_main.addWidget(self.gb_general)

    @err_catcher(name=__name__)
    def connectEvents(self):
        self.e_name.textChanged.connect(self.nameChanged)
        self.e_name.editingFinished.connect(self.stateManager.saveStatesToScene)
        self.chb_option1.toggled.connect(self.stateManager.saveStatesToScene)
        self.cb_format.currentIndexChanged.connect(self.stateManager.saveStatesToScene)

    @err_catcher(name=__name__)
    def nameChanged(self, text):
        self.state.setText(0, text)

    @err_catcher(name=__name__)
    def updateUi(self):
        return True

    @err_catcher(name=__name__)
    def preExecuteState(self):
        warnings = []

        if not self.chb_option1.isChecked():
            warnings.append(["Option1 not checked.", "", 2])

        return [self.state.text(0), warnings]

    @err_catcher(name=__name__)
    def executeState(self, parent, useVersion="next"):
        fileName = self.core.getCurrentFileName()
        context = self.core.getScenefileData(fileName)
        outputPath = self.core.products.generateProductPath(
            entity=context,
            task="myProduct",
            extension=self.cb_format.currentText(),
        )

        if not os.path.exists(os.path.dirname(outputPath)):
            os.makedirs(os.path.dirname(outputPath))

        with open(outputPath, "w") as f:
            f.write("custom export")

        self.core.popup("Custom export to: %s" % outputPath, severity="info")
        result = {"result": "success"}
        if result["result"] == "success":
            return [self.state.text(0) + " - success"]
        else:
            return [
                self.state.text(0)
                + " - error - %s" % result["error"]
            ]

    @err_catcher(name=__name__)
    def getStateProps(self):
        stateProps = {}
        stateProps.update(
            {
                "statename": self.e_name.text(),
                "option1": self.chb_option1.isChecked(),
                "cb_format": self.cb_format.currentText(),
                "stateenabled": str(self.state.checkState(0)),
            }
        )
        return stateProps