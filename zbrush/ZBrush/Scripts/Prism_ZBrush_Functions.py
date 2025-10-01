import os
import sys

import ctypes
import time
import json
import subprocess
import pathlib
import platform
from pathlib import Path
import shutil

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from PrismUtils.Decorators import err_catcher_plugin as err_catcher

from PrismUtils import PrismWidgets

#append the path of the UserInterfaces folder to sys.path
currentPath = os.path.dirname(os.path.abspath(__file__)) + os.sep + ".." + os.sep + "UserInterfaces" + os.sep
if currentPath not in sys.path:
    sys.path.append(currentPath)
from ZBrushStyleSheet.__init__ import load_stylesheet


class Prism_ZBrush_Functions(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin
        self.pb = None

        # Windows API setup
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32

        # Virtual key codes
        self.VK_CONTROL = 0x11
        self.VK_SHIFT = 0x10
        self.VK_P = 0x50

        self.SW_RESTORE = 9

        self.state = {
                "states": [
                    {
                        "statename": "publish",
                        "comment": "dummy publish state",
                        "description": ""
                    }
                ]
            }
        self.state = json.dumps(self.state)  # convert dict to JSON string



    @err_catcher(name=__name__)
    def startup(self, origin):
        stylesheet = load_stylesheet()
        if stylesheet:
            app = QApplication.instance()
            app.setStyleSheet(stylesheet)

        origin.timer.stop()

        #give a dummy parent to message boxes so they are on top of ZBrush
        origin.messageParent = QWidget()
        origin.messageParent.setWindowTitle("Prism")

        if self.core.useOnTop:
            origin.messageParent.setWindowFlags(
                origin.messageParent.windowFlags() ^ Qt.WindowStaysOnTopHint
            )

        origin.startAutosaveTimer()
        self.toolsWindow = self.Tools()

        pluginDir = os.path.dirname(os.path.abspath(__file__))
        watchdogZBrush = os.path.join(pluginDir, "Helpers/watchdogZBrush.py")

        python_exe = self.find_prism()

        subprocess.Popen([python_exe, watchdogZBrush])


    @err_catcher(name=__name__)
    def autosaveEnabled(self, origin):
        # get autosave enabled
        return False

    @err_catcher(name=__name__)
    def sceneOpen(self, origin):
        if self.core.shouldAutosaveTimerRun():
            origin.startAutosaveTimer()

    @err_catcher(name=__name__)
    def getCurrentFileName(self, origin=None, path=True):
        # get current scene file name
        tempPath = os.path.dirname(os.path.abspath(__file__)) + os.sep + "ZBrushTmp" + os.sep + "currentFileName.json"
        if not os.path.exists(tempPath):
            return ""
        with open(tempPath, "r", encoding="utf-8") as f:
            currentFileName = f.read().strip()
        if currentFileName is None:
            return ""
        return currentFileName

    @err_catcher(name=__name__)
    def getSceneExtension(self, origin):
        return self.sceneFormats[0]

    @err_catcher(name=__name__)
    def saveScene(self, origin, filepath, details={}):
        # save scenefile
        ext = os.path.splitext(filepath)[1]
        self.saveCurrentFileName(filepath.replace("\\", "/"))
        if ext == ".zpr" or ext == ".ZPR":
            command = "[FileNameSetNext, \"" + filepath.replace("\\", "/") + "\"]\n[RoutineDef, command,[IPress, File:Save as]]\n[RoutineCall,command]"
        elif ext == ".ztl" or ext == ".ZTL":    
            command = "[FileNameSetNext, \"" + filepath.replace("\\", "/") + "\"]\n[RoutineDef, command,[IPress, Tool:Save As]]\n[RoutineCall,command]"
        self.send_command_to_zbrush(command)
        self.activate_zbrush()

        self.exportThumbnail(origin, filepath)

    @err_catcher(name=__name__)
    def getImportPaths(self, origin):
        return []
    
    @err_catcher(name=__name__)
    def getAppVersion(self, origin):
        return "1.0"

    @err_catcher(name=__name__)
    def openScene(self, origin, filepath, force=False):
        # load scenefile
        self.saveCurrentFileName(filepath.replace("\\", "/"))
        ext = os.path.splitext(filepath)[1]
        if ext == ".zpr" or ext == ".ZPR":
            command = "[FileNameSetNext, \"" + filepath.replace("\\", "/") + "\"]\n[RoutineDef, command,[IPress, File:Open]]\n[RoutineCall,command]"
        else:
            command = "[FileNameSetNext, \"" + filepath.replace("\\", "/") + "\"]\n[RoutineDef, command,[IPress, Tool:Load Tool]]\n[RoutineCall,command]"
        self.send_command_to_zbrush(command)
        self.activate_zbrush()

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
    def sm_export_startup(self, origin):
        pass

    # 	@err_catcher(name=__name__)
    # 	def sm_export_setTaskText(self, origin, prevTaskName, newTaskName):
    # 		origin.l_taskName.setText(newTaskName)

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
    def sm_render_startup(self, origin):
        pass

    @err_catcher(name=__name__)
    def sm_render_getRenderLayer(self, origin):
        rlayerNames = []

        return rlayerNames

    @err_catcher(name=__name__)
    def sm_render_refreshPasses(self, origin):
        pass

    @err_catcher(name=__name__)
    def sm_render_openPasses(self, origin, item=None):
        pass

    @err_catcher(name=__name__)
    def sm_render_preSubmit(self, origin, rSettings):
        pass

    @err_catcher(name=__name__)
    def sm_render_startLocalRender(self, origin, outputName, rSettings):
        pass

    @err_catcher(name=__name__)
    def sm_render_undoRenderSettings(self, origin, rSettings):
        pass

    @err_catcher(name=__name__)
    def sm_render_getDeadlineParams(self, origin, dlParams, homeDir):
        pass

    @err_catcher(name=__name__)
    def getCurrentRenderer(self, origin):
        return "Renderer"

    @err_catcher(name=__name__)
    def getCurrentSceneFiles(self, origin):
        curFileName = self.core.getCurrentFileName()
        scenefiles = [curFileName]
        return scenefiles

    @err_catcher(name=__name__)
    def sm_render_getRenderPasses(self, origin):
        return []

    @err_catcher(name=__name__)
    def sm_render_addRenderPass(self, origin, passName, steps):
        pass

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
    def sm_import_disableObjectTracking(self, origin):
        self.deleteNodes(origin, [origin.setName])

    @err_catcher(name=__name__)
    def sm_import_importToApp(self, origin, doImport, update, impFileName):
        ext = os.path.splitext(impFileName)[1]

        if ext == ".abc" or ext == ".fbx":
            command = "[FileNameSetNext, \"" + impFileName.replace("\\", "/") + "\"]\n[RoutineDef, command,\n\t[IPress, Tool:Import:  Import]\n]\n[RoutineCall,command]"
        elif ext == ".obj":    
            command = "[FileNameSetNext, \"" + impFileName.replace("\\", "/") + "\"]\n[RoutineDef, command,\n\t[If,[IGetStatus, Transform:Edit],\n\t[IPress, Tool:Subtool:Duplicate]\n\t]\n\t[IPress, Tool:Import:  Import]\n]\n[RoutineCall,command]"
        self.send_command_to_zbrush(command)
        self.activate_zbrush()
        return {"result": True, "doImport": doImport}

    @err_catcher(name=__name__)
    def sm_import_updateObjects(self, origin):
        pass

    @err_catcher(name=__name__)
    def sm_import_removeNameSpaces(self, origin):
        pass

    @err_catcher(name=__name__)
    def sm_saveStates(self, origin, buf):
        pass

    @err_catcher(name=__name__)
    def sm_saveImports(self, origin, importPaths):
        pass

    @err_catcher(name=__name__)
    def sm_readStates(self, origin):
        return self.state

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
    def getCamNodes(self, origin):
        return []

    @err_catcher(name=__name__)
    def exportThumbnail(self, origin, filepath):
        #modify the filepath to remove the current ext and make it ends with preview.jpg
        #Create a thumbnail if it's not already done by save extended
        if hasattr(self.core, "savec") and not self.core.savec is None:
            preview = self.core.savec.previewDefined
        else:
            preview = False

        if  not preview:
            thumbnailPath = os.path.splitext(filepath)[0] + "preview.png"

            command = "[RoutineDef, command, [FileNameSetNext, \"" + thumbnailPath + "\"]\n[IPress, \"Document:Export\"]]\n[RoutineCall,command]"
            self.send_command_to_zbrush(command)
            self.activate_zbrush()

            newThumbnailPath = os.path.splitext(thumbnailPath)[0] + ".jpg"
            
            for t in range(5):
                if not os.path.exists(thumbnailPath):
                    time.sleep(0.5)

            # Load PNG
            image = QImage(thumbnailPath)
            # Save as JPG, with quality (0–100)
            image.save(newThumbnailPath, "JPG", 100)
            if os.path.exists(thumbnailPath):
                os.remove(thumbnailPath)
            

    def Tools(self):
        if hasattr(self, "tools_window") and self.tools_window is not None:
            # if it already exists, just bring it to front
            self.toolsWindow.raise_()
            self.toolsWindow.activateWindow()
            return self.toolsWindow
        #open tools window with a button for each function [Project Browser, Save Version, Save Comment, Import, Export, Settings]
        self.toolsWindow = QWidget()
        self.toolsWindow.setWindowTitle("Prism")
        layout = QVBoxLayout()
        extentionLayout = QFormLayout()
        self.ztlCheckBox = QCheckBox(".ztl")
        self.zprCheckBox = QCheckBox(".zpr")
        self.zprCheckBox.setChecked(True)
        def on_ztl_checked(state):
            if state:
                self.zprCheckBox.setChecked(False)
        def on_zpr_checked(state):
            if state:
                self.ztlCheckBox.setChecked(False)
        self.ztlCheckBox.stateChanged.connect(on_ztl_checked)
        self.zprCheckBox.stateChanged.connect(on_zpr_checked)
        extentionLayout.addRow(self.ztlCheckBox, self.zprCheckBox)
        layout.addLayout(extentionLayout)
        btn_save_version = QPushButton("Save")
        btn_save_version.clicked.connect(lambda: self.Save())
        layout.addWidget(btn_save_version)
        btn_save_version = QPushButton("Save Version")
        btn_save_version.clicked.connect(lambda: self.SaveVersion())
        layout.addWidget(btn_save_version)
        btn_save_comment = QPushButton("Save Extended")
        btn_save_comment.clicked.connect(lambda: self.SaveComment())
        layout.addWidget(btn_save_comment)
        btn_import = QPushButton("Import")
        btn_import.clicked.connect(lambda: self.Import())
        layout.addWidget(btn_import)
        btn_export = QPushButton("Export")
        btn_export.clicked.connect(lambda: self.Export())
        layout.addWidget(btn_export)
        btn_project_browser = QPushButton("Project Browser")
        btn_project_browser.clicked.connect(lambda: self.ProjectBrowser())
        layout.addWidget(btn_project_browser)
        btn_turntable = QPushButton("Turntable")
        btn_turntable.clicked.connect(lambda: self.Turntable())
        layout.addWidget(btn_turntable)
        btn_settings = QPushButton("Settings")
        btn_settings.clicked.connect(lambda: self.Settings())
        layout.addWidget(btn_settings)
        self.toolsWindow.setLayout(layout)
        self.toolsWindow.setAttribute(Qt.WA_StyledBackground, True)

        flags = Qt.Window | Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint
        self.toolsWindow.setWindowFlags(flags)
        self.toolsWindow.show()
        self.toolsWindow.raise_()
        self.toolsWindow.activateWindow()

        return self.toolsWindow

    def ProjectBrowser(self):
        if self.pb is not None:
            self.pb.show()
            self.pb.raise_()
            self.pb.activateWindow()
            return self.pb
        
        self.pb = self.core.projectBrowser()
        self.pb.setAttribute(Qt.WA_DeleteOnClose, False)  # prevent destruction
        self.pb.show()
        self.pb.raise_()
        self.pb.activateWindow()

        return self.pb
    
    def Save(self):
        oldFilePath = self.getCurrentFileName()
        if oldFilePath == "":
            command = "[RoutineDef,command,[Note, \"Please use Project Browser to create a new file before using 'Save' in Prism.\", 5]]\n[RoutineCall,command]"
            self.send_command_to_zbrush(command)
            self.activate_zbrush()
            return False
        filePath = self.getCurrentFileName()

        self.saveScene(self.core, filePath)

        #getting data
        data = self.core.getScenefileData(filePath)
        self.core.saveVersionInfo(filePath, data)


    def SaveVersion(self):
        print("Saving version...")
        oldFilePath = self.getCurrentFileName()
        if oldFilePath == "":
            command = "[RoutineDef,command,[Note, \"Please use Project Browser to create a new file before using 'Save Version' in Prism.\", 5]]\n[RoutineCall,command]"
            self.send_command_to_zbrush(command)
            self.activate_zbrush()
            return False
        
        if self.zprCheckBox.isChecked():
            ext = "zpr"
        else:
            ext = "ztl"
        version = int(oldFilePath[-8:-4])
        newVersion = version + 1
        filePath = oldFilePath[:-8] + str(newVersion).zfill(4) + "." + ext

        self.saveScene(self.core, filePath)

        #getting data
        data = self.core.getScenefileData(filePath)
        self.core.saveVersionInfo(filePath, data)

    def SaveComment(self):
        oldFilePath = self.getCurrentFileName()
        if oldFilePath == "":
            command = "[RoutineDef,command,[Note, \"Please use Project Browser to create a new file before using 'Save Extended' in Prism.\", 5]]\n[RoutineCall,command]"
            self.send_command_to_zbrush(command)
            self.activate_zbrush()
            return False
        #prevent it to open multiple times
        if hasattr(self.core, "savec") and self.core.savec is not None:
            self.core.savec.show()
            self.core.savec.raise_()
            self.core.savec.activateWindow()
            return False
        if not self.core.projects.ensureProject():
            return False

        if not self.core.users.ensureUser():
            return False
        
        if not self.core.fileInPipeline():
            self.core.showFileNotInProjectWarning()
            return False

        self.core.savec = PrismWidgets.SaveComment(core=self.core)
        self.core.savec.accepted.connect(lambda: self.core.saveWithCommentAccepted(self.core.savec))
        self.core.savec.destroyed.connect(lambda: setattr(self.core, "savec", None))
        self.core.savec.show()
        self.core.savec.activateWindow()
        self.core.savec.setAttribute(Qt.WA_DeleteOnClose)
        return True
    
    def Import(self):
        oldFilePath = self.getCurrentFileName()
        if oldFilePath == "":
            command = "[RoutineDef,command,[Note, \"Please use Project Browser to create a new file before using 'Import' in Prism.\", 5]]\n[RoutineCall,command]"
            self.send_command_to_zbrush(command)
            self.activate_zbrush()
            return False
        #create the state
        sm = self.core.getStateManager()

        self.state = sm.createState(
            "ImportFile",
            setActive=True,
            openProductsBrowser=False,
        )
        self.currentState = getattr(self.state, "state", None)

        # state is a QTreeWidgetItem — the UI object is on state.ui
        import_state = getattr(self.state, "ui", None)
        if import_state is None:
            print("State UI not found on the returned item. inspect state:", dir(self.state))
            return self.state

        # Save states to scene so PB finds them
        sm.saveStatesToScene()

        import_state.browse()

        return self.state

    def Export(self):
        #create the state
        sm = self.core.getStateManager()

        self.state = sm.createState(
            "Export",
            setActive=True,
        )
        self.currentState = getattr(self.state, "state", None)

        # state is a QTreeWidgetItem — the UI object is on state.ui
        export_state = getattr(self.state, "ui", None)
        if export_state is None:
            print("State UI not found on the returned item. inspect state:", dir(self.state))
            return self.state

        # Save states to scene so PB finds them
        sm.saveStatesToScene()

        # Show export window
        if hasattr(self, "export_window") and self.export_window is not None:
            self.export_window.resize(420, 350)
            self.export_window.show()
            return self.state
        
        self.export_window = ExportWindow(self.core, self.toolsWindow)
        self.export_window.resize(420, 350)
        self.export_window.show()

        return self.state
    
    def Turntable(self):
        oldFilePath = self.getCurrentFileName()
        if oldFilePath == "":
            command = "[RoutineDef,command,[Note, \"Please use Project Browser to create a new file before using 'Save Version' in Prism.\", 5]]\n[RoutineCall,command]"
            self.send_command_to_zbrush(command)
            self.activate_zbrush()
            return False
        #remove the extention of the old file path
        for letter in oldFilePath[::-1]:
            if letter == ".":
                oldFilePath = oldFilePath[:-1]
                break
            else:
                oldFilePath = oldFilePath[:-1]

        dataPath = oldFilePath + "versioninfo.json"
        print("dtata path :", dataPath)
        if os.path.exists(dataPath):
            with open(dataPath, 'r') as f:
                data = json.load(f)
        else:
            command = "[RoutineDef,command,[Note, \"The metadata isn't available.\", 5]]\n[RoutineCall,command]"
            self.send_command_to_zbrush(command)
            self.activate_zbrush()
            return False

        resolvedMediaPath = self.core.projects.getResolvedProjectStructurePath("renderVersions", data)

        path = resolvedMediaPath.replace("@identifier@", "sculpt")
        path = path.replace("3dRender", "2dRender")
        path = path[:-6]
        if not os.path.exists(path):
            os.makedirs(path)
        currentVersions = os.listdir(path)
        versionInt = len(currentVersions)
        version = "v" + str(versionInt+1).zfill(4)
        path += os.sep + version
        path += os.sep + data["asset"] + "_sculpt_" + version
        if not os.path.exists(os.path.dirname(os.path.abspath(path))):
            os.makedirs(os.path.dirname(os.path.abspath(path)))

        
        self.path = path

        if hasattr(self, "turntableWin"):
            self.turntableWin.show()
            self.turntableWin.raise_()
            self.turntableWin.activateWindow()
            return True
        self.turntableWin = TurntableWindow(self.toolsWindow, self.core)
        self.turntableWin.show()
        self.turntableWin.raise_()
        self.turntableWin.activateWindow()

    def Settings(self):
        print("Opening settings...")
        self.core.prismSettings()
    
    def find_prism(self):
        folders_to_scan = set()

        # Add Program Files and Home directories
        program_files = os.environ.get("ProgramW6432", "C:/Program Files")
        program_files_x86 = os.environ.get("ProgramFiles(x86)", "C:/Program Files (x86)")
        home_dir = str(Path.home())
        folders_to_scan.add(program_files.replace("\\", "/"))
        folders_to_scan.add(program_files_x86.replace("\\", "/"))
        folders_to_scan.add(home_dir.replace("\\", "/"))

        # Add all root drives (C:/, D:/, etc.)
        if platform.system() == "Windows":
            from string import ascii_uppercase
            import ctypes
            for letter in ascii_uppercase:
                drive = f"{letter}:/"
                if os.path.exists(drive):
                    folders_to_scan.add(drive.replace("\\", "/"))
                    folders_to_scan.add(os.path.join(drive, "Program Files").replace("\\", "/"))
                    folders_to_scan.add(os.path.join(drive, "Program Files (x86)").replace("\\", "/"))
        
        # Scan each folder
        for folder in folders_to_scan:
            for prism_variant in ["Prism", "Prism2"]:
                prism_path = os.path.join(folder, prism_variant).replace("\\", "/")
                prism_path = prism_path.replace("//", "/")
                if os.path.isdir(prism_path):
                    exe_path = os.path.join(prism_path, "Python311", "pythonw.exe").replace("\\", "/")
                    if os.path.isfile(exe_path):
                        return exe_path

        return ""


    @err_catcher(name=__name__)
    def send_command_to_zbrush(self, command):
        currentPath = os.path.dirname(os.path.abspath(__file__)) + os.sep
        #write a txt file with the command to be read by ZBrush in the same directory as this script
        zbrush_command_file = os.path.join(currentPath, "ZBrushTmp\\toZBrush.txt")

        if not os.path.exists(os.path.dirname(zbrush_command_file)):
            os.makedirs(os.path.dirname(zbrush_command_file))

        with open(zbrush_command_file, "w", encoding="utf-8") as f:
            f.write(command)
            f.flush()
            os.fsync(f.fileno())
        
    def activate_zbrush(self):
        # Find ZBrush window (adjust title to match your version, e.g. "ZBrush 2022")
        hwnd = self.user32.FindWindowW(None, "ZBrush")
        if hwnd == 0:
            print("ZBrush window not found.")
            return

        # Bring ZBrush to foreground
        self.user32.ShowWindow(hwnd, self.SW_RESTORE)
        self.user32.AllowSetForegroundWindow(-1)  # let any process set foreground
        self.user32.SetForegroundWindow(hwnd)
        time.sleep(0.2)

        # Press Ctrl+Shift+P
        self.user32.keybd_event(self.VK_CONTROL, 0, 0, 0)
        self.user32.keybd_event(self.VK_SHIFT, 0, 0, 0)
        self.user32.keybd_event(self.VK_P, 0, 0, 0)
        time.sleep(0.1)
        self.user32.keybd_event(self.VK_P, 0, 2, 0)
        self.user32.keybd_event(self.VK_SHIFT, 0, 2, 0)
        self.user32.keybd_event(self.VK_CONTROL, 0, 2, 0)

        print("Sent Ctrl+Shift+P to ZBrush.")
    

    @err_catcher(name=__name__)
    def saveCurrentFileName(self, filename):
        currentFileName = filename.replace("\\", "/")
        path = os.path.dirname(os.path.abspath(__file__)) + os.sep + "ZBrushTmp" + os.sep + "currentFileName.json"
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        with open(path, "w", encoding="utf-8") as f:
            f.write(currentFileName)
            f.flush()
    

class ExportWindowUI(QDialog):
    def __init__(self, core, parent=None):
        super().__init__(parent)
        self.core = core
        self.setWindowTitle("Prism - Export")


        layout = QVBoxLayout(self)


        # --- Productname + Comment in a form layout ---
        form_layout = QFormLayout()
        self.prodname_edit = QComboBox()
        self.prodname_edit.setEditable(True)
        self.prodname_edit.setCurrentText("geo")
        currentFileName = self.core.appPlugin.getCurrentFileName(self.core)
        dataPath = currentFileName[:-4] + "versioninfo.json"
        if os.path.exists(dataPath):
            with open(dataPath, 'r') as f:
                data = json.load(f)
        else:
            data = {}
        products = self.core.products.getProductNamesFromEntity(data)
        for product in products:
            self.prodname_edit.addItem(product)
        form_layout.addRow("Productname:", self.prodname_edit)


        self.comment_edit = QLineEdit()
        form_layout.addRow("Comment (optional):", self.comment_edit)


        layout.addLayout(form_layout)


        # Separator line
        layout.addWidget(self._separator())


        # --- Export Geometry section ---
        self.export_geo_cb = QCheckBox("Export Geometry")
        self.export_geo_cb.setChecked(True)
        layout.addWidget(self.export_geo_cb)


        # Format
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Format:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems([".abc", ".obj", ".fbx"])
        format_layout.addWidget(self.format_combo)
        layout.addLayout(format_layout)


        # Version Up
        version_layout = QHBoxLayout()
        self.version_up_cb = QCheckBox("Version Up")
        self.version_up_cb.setChecked(True)
        version_layout.addWidget(self.version_up_cb)


        self.version_combo = QComboBox()
        self.create_version_list()
        self.version_combo.setEnabled(False)  # hidden if Version Up checked
        version_layout.addWidget(self.version_combo)


        layout.addLayout(version_layout)


        # Location
        location_layout = QHBoxLayout()
        location_layout.addWidget(QLabel("Location:"))
        self.location_combo = QComboBox()
        self.location_combo.addItems(["global", "local"])
        location_layout.addWidget(self.location_combo)
        layout.addLayout(location_layout)


        # Separator line
        layout.addWidget(self._separator())


        # --- Export Maps section ---
        self.export_maps_cb = QCheckBox("Export Maps")
        layout.addWidget(self.export_maps_cb)


        self.udim_cb = QCheckBox("Export folders as UDIMs")
        self.udim_cb.setEnabled(False)
        layout.addWidget(self.udim_cb)

        # map size
        map_size_layout = QHBoxLayout()
        map_size_layout.addWidget(QLabel("Map Size:"))
        self.map_size_combo = QComboBox()
        self.map_size_combo.addItems(["512", "1024", "2048", "4096"])


        # Spacer pushes button to bottom
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))


        # Export button
        self.export_btn = QPushButton("Export")
        layout.addWidget(self.export_btn)


        # connections
        self.export_geo_cb.toggled.connect(self.toggle_geo_options)
        self.export_maps_cb.toggled.connect(self.toggle_maps_options)
        self.version_up_cb.toggled.connect(self.toggle_version_combo)


        # init states
        self.toggle_geo_options(self.export_geo_cb.isChecked())
        self.toggle_maps_options(self.export_maps_cb.isChecked())
        self.toggle_version_combo(self.version_up_cb.isChecked())


    def _separator(self):
        """Return a horizontal line separator"""
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Plain)
        line.setLineWidth(1)
        return line

    def create_version_list(self):
        #clear the combo
        self.version_combo.clear()
        #read the json file of the current scene to get the next available version
        currentFileName = self.core.appPlugin.getCurrentFileName()
        jsonPath = os.path.splitext(currentFileName)[0] + "versioninfo.json"
        with open(jsonPath, "r") as f:
            entity = json.load(f)


        nextVersion = self.core.products.getNextAvailableVersion(entity, self.prodname_edit.currentText()) #always Modeling because it's for sculpt
        version = int(nextVersion[1:]) -1 # remove the "v" prefix and convert to int


        items = []
        for i in range(version):
            items.append("v" + str(i+1).zfill(4))
        self.version_combo.addItems(items)

    def toggle_geo_options(self, checked):
        self.format_combo.setEnabled(checked)
        self.version_up_cb.setEnabled(checked)
        self.version_combo.setEnabled(checked and not self.version_up_cb.isChecked())
        self.location_combo.setEnabled(checked)


    def toggle_maps_options(self, checked):
        self.udim_cb.setEnabled(checked)


    def toggle_version_combo(self, checked):
        self.version_combo.setEnabled(not checked and self.export_geo_cb.isChecked())


class ExportWindow(ExportWindowUI):
    def __init__(self, core, parent=None):
        super().__init__(core, parent)
        self.core = core
        self.export_btn.clicked.connect(self.export)
        self.version_up_cb.stateChanged.connect(self.create_version_list)
        self.prodname_edit.currentIndexChanged.connect(self.create_version_list)

    @err_catcher(name=__name__)
    def export(self):
        currentFileName = self.core.appPlugin.getCurrentFileName()
        if currentFileName == "":
            command = "[RoutineDef,command,[Note, \"Please use Project Browser to create a new file before using 'Export' in Prism.\", 5]]\n[RoutineCall,command]"
            self.core.appPlugin.send_command_to_zbrush(command)
            self.core.appPlugin.activate_zbrush()
            return False


        #export Geometry
        if self.export_geo_cb.isChecked():
            directory = ""
            productname = self.prodname_edit.currentText()
            comment = self.comment_edit.text()
            location = self.location_combo.currentText()
            task = self.prodname_edit.currentText()
            if productname == "":
                task = "Modeling"
           
            #read the json file of the current scene to get the next available version
            currentFileName = self.core.appPlugin.getCurrentFileName()
            jsonPath = os.path.splitext(currentFileName)[0] + "versioninfo.json"
            with open(jsonPath, "r") as f:
                entity = json.load(f)


            if self.version_up_cb.isChecked():
                version =  self.core.products.getNextAvailableVersion(entity, task)
            else:
                version = self.version_combo.currentText()
                if version == "":
                    version = "v0001"
            ext = self.format_combo.currentText()


            #read the json file of the current scene
            currentFileName = self.core.appPlugin.getCurrentFileName()
            jsonPath = os.path.splitext(currentFileName)[0] + "versioninfo.json"
            with open(jsonPath, "r") as f:
                entity = json.load(f)
            entity["ProductName"] = productname


            exportPath = self.core.products.generateProductPath(
                task=task,
                entity=entity,
                extension=ext,
                comment=comment,
                version=version,
                location=location,
            )

            #check if the exportpath exists and create it if not
            if not os.path.exists(os.path.dirname(exportPath)):
                os.makedirs(os.path.dirname(exportPath))

            #Check what's in the export path if not new version and clear the folder
            exportPathInfo = exportPath.replace("\\", "/")
            exportPathInfo = exportPathInfo.split("/")
            exportPathInfo.pop(-1)
            exportPathInfo = '/'.join(exportPathInfo)


            if not self.version_up_cb.isChecked():
                files = os.listdir(exportPathInfo)
                for file in files:
                    os.remove(exportPathInfo + "/" + file)
           
            #send command to zbrush
            command = "[FileNameSetNext, \"" + exportPath.replace("\\", "/") + "\"]\n[RoutineDef, command,[IPress, Tool:Export]]\n[RoutineCall,command]"
            self.core.appPlugin.send_command_to_zbrush(command)
            self.core.appPlugin.activate_zbrush()


            #save json info
            productContext = entity
            productContext["product"] = task
            productContext["version"] = version
            productContext["comment"] = comment
            productContext["ProductName"] = productname
            productContext["sourceScene"] = self.core.getCurrentFileName()
            self.core.saveVersionInfo(exportPathInfo, productContext)


            #update master version
            while not os.path.exists(exportPath):
                time.sleep(1)
            self.core.products.updateMasterVersion(exportPath)


        #Export Maps
        if self.export_maps_cb.isChecked():
            # find if there is any subtool with subdivision levels
            #TO DO

            #export maps
            command = "[RoutineDef, command,[IPress, Zplugin:Multi Map Exporter:Create All Maps]]\n[RoutineCall,command]"


        self.accept()

class TurntableWindow(QDialog):
    def __init__(self, parent, core):
        super().__init__(parent)
        self.setWindowTitle("Turntable Options")
        self.core = core
        self.path = self.core.appPlugin.path
        self.setup_ui()

    def setup_ui(self):
        # Layouts
        main_layout = QVBoxLayout()
        padding_layout = QHBoxLayout()

        # Padding label and spinbox
        padding_label = QLabel("Padding:")
        self.padding_input = QSpinBox()
        self.padding_input.setRange(0, 360)
        self.padding_input.setValue(45)  # Default value

        padding_layout.addWidget(padding_label)
        padding_layout.addWidget(self.padding_input)

        # Turntable button
        self.turntable_button = QPushButton("Turntable")
        self.turntable_button.clicked.connect(self.on_turntable_clicked)

        # Add widgets to main layout
        main_layout.addLayout(padding_layout)
        main_layout.addWidget(self.turntable_button)

        self.setLayout(main_layout)
    
    def on_turntable_clicked(self):
        if self.path == None:
            self.path = self.core.appPlugin.path
        command = f"[VarSet, padding, {self.padding_input.value()}]\n[VarSet, gTotalFrames, 360/padding]\n[VarSet, fileName, \"{self.path}\"]\n[VarSet, ext, \".png\"]\n[VarSet, gFrameCount, 0]\n\n[RoutineDef, command,\n[VarSet, path, fileName]\n\n[Loop, gTotalFrames,\n[VarSet, curAngle, padding]\n[VarSet, n, 0]\n[Loop, [SubToolGetCount],\n[SubToolSelect, n]\n[VarSet, n, n+1]\n[IModSet, Tool:Deformation:Rotate, 2]   // Y axis only\n[ISet, Tool:Deformation:Rotate, curAngle]\n]\n\n// Force redraw / update\n[IUpdate, 1]\n\n// Export image\n[VarSet, frame, gFrameCount/padding]\n[VarSet, fill, 4-[StrLength, frame]]\n[VarSet, strFill, ""]\n[Loop, fill,\n[VarSet, strFill, [StrMerge, strFill, \"0\"]]\n]\n[VarSet, path, [StrMerge, fileName, \"_\", strFill, frame, ext]]\n[FileNameSetNext, path]\n[IPress, Document:Export]\n\n[VarSet, gFrameCount, gFrameCount + padding]\n]\n]\n[RoutineCall, command]"
        self.core.appPlugin.send_command_to_zbrush(command)
        self.core.appPlugin.activate_zbrush()

        for i in range(int(360/self.padding_input.value())+1):
            print("i :", i)
            thumbnailPath = self.path + "_" + str((i)).zfill(4) + ".png"
            newThumbnailPath = self.path + "_" + str((i)).zfill(4) + ".jpg"

            # Wait until file exists (up to e.g. 1 seconds)
            for attempt in range(5):
                if os.path.exists(thumbnailPath):
                    break
                time.sleep(0.2)

            if os.path.exists(thumbnailPath):
                print("it exists for i :", i)
                # Load PNG
                image = QImage(thumbnailPath).copy()
                # Save as JPG, with quality (0–100)
                image.save(newThumbnailPath, "JPG", 100)
                try:
                    os.remove(thumbnailPath)
                except PermissionError:
                    time.sleep(0.2)
                    try:
                        os.remove(thumbnailPath)
                    except PermissionError:
                        print("not the rigth way to do it")
        self.path = None
        self.accept()