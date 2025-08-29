### Command : ./pyside2-uic.exe -o S:/3D/ScriptsMaya/SaveAs/generatedUi.py S:/3D/ScriptsMaya/SaveAs/save_as.ui

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import sys
import os

import maya.OpenMayaUI as omui
import shiboken2
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.cmds as cmds
from maya.OpenMayaUI import MQtUtil




def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(int(main_window_ptr), QtWidgets.QWidget)







# A dialog to ask the user for the variation name
class AskVariation(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AskVariation, self).__init__(parent)
        self.setWindowTitle("Enter Variation Name")
        self.setMinimumWidth(300)

        # Create a vertical layout
        layout = QtWidgets.QVBoxLayout(self)

        # Create a label
        label = QtWidgets.QLabel("Select a variation for your publish:")
        layout.addWidget(label)

        # Create a combo box
        self.combo_box = QtWidgets.QComboBox(self)
        self.combo_box.addItems(["var001", "var002", "var003", "var004", "var005", "var006", "var007", "var008", "var009", "var010",
                                 "var011", "var012", "var013", "var014", "var015", "var016", "var017", "var018", "var019", "var020"])
        layout.addWidget(self.combo_box)
        
        # Add a spacer
        spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        layout.addItem(spacer)
        
        # Create a button box
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        # Set the layout
        self.setLayout(layout)






# Function to publish RLO
def publishRLO(state, pcore):
    
    #### ENTITY : 
    # { 
    # "project_path": "E:\\3D\\PIPELINE\\USD_Uptight_2025_v001\\00_Template\\Uptight",
    # "sequence": "sq_010",
    # "shot": "master",
    # "department": "rlo",
    # "task": "zdq",
    # "version": "v0002",
    # "type": "shot",
    # "locations": {
    #     "global": "E:\\3D\\PIPELINE\\USD_Uptight_2025_v001\\00_Template\\Uptight\\03_Production\\02_Shots\\sq_010\\master\\Scenefiles\\rlo\\zdq\\sq_010-master_zdq_v0002.ma"
    # },
    # "comment": "",
    # "project_name": "Uptight",
    # "username": "Thomas",
    # "user": "tho",
    # "filename": "E:/3D/PIPELINE/USD_Uptight_2025_v001/00_Template/Uptight/03_Production/02_Shots/sq_010/master/Scenefiles/rlo/zdq/sq_010-master_zdq_v0002.ma",
    # "extension": ".ma"
    # }

    # Get the current file path and split it
    filePath = pcore.getCurrentFileName()
    filePath = filePath.replace("\\", "/")
    splitedPath = filePath.split("/")
    # Get the entity data
    entity = pcore.getScenefileData(filePath)

    # Prepare the name
    department = entity["department"]
    taskName = entity["task"]

    # In RLO (rough layout), we have to export multiple things : 
    # - The cameras 
    #   - We mush check for their name and export them in the corresponding shot
    # - The RIG's abc files
    #   - We must go through all the animated mesh and export them as abc files
    # - The USD edits


    #### 1. Export the cameras
    # Get all the cameras in the scene
    cameras = cmds.ls(type="camera")
    # Filter the cameras to keep only the ones that are in the current shot
    shot_cameras = [cam for cam in cameras if cam.startswith("camera_" )]

    # print the cameras
    if not shot_cameras:
        msg = QMessageBox(QMessageBox.Warning, "Prism Warning", "No cameras found in the current shot.")
        msg.addButton("Close", QMessageBox.RejectRole)
        msg.exec_()
        return
    
    # This cameras are shape, we want to get the transform nodes
    shot_cameras_shapes = shot_cameras.copy()
    shot_cameras = [cmds.listRelatives(cam, parent=True)[0] for cam in shot_cameras if cmds.listRelatives(cam, parent=True)]
    for cam in shot_cameras:
        print("Camera found: ", cam)

    pass







class SaveAsWindow(MayaQWidgetDockableMixin, QtWidgets.QDialog):
    
    def __init__(self, parent=maya_main_window()):
        super(SaveAsWindow, self).__init__(parent)
        self.setWindowTitle("Badger Pipeline")
        self.setMinimumWidth(400)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        # Setup the User Interface
        self.setupUi()

        # Setup the connections
        self.setupConnections()

    # Setup the User Interface
    def setupUi(self):

        # Main vertical layout
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.main_layout)

        # Row 1: Save, Save As, Save As Comm
        row1 = QtWidgets.QHBoxLayout()
        row1.setSpacing(0)

        # Save button
        self.save_btn = QtWidgets.QPushButton("")
        self.save_btn.setIcon(self.getIcon("save"))
        self.save_btn.setIconSize(QtCore.QSize(38, 38))
        self.save_btn.setToolTip("Save")
        self.save_btn.setFlat(True)

        # Save as button
        self.saveas_btn = QtWidgets.QPushButton("")
        self.saveas_btn.setIcon(self.getIcon("saveas"))
        self.saveas_btn.setIconSize(QtCore.QSize(38, 38))
        self.saveas_btn.setToolTip("Save As")
        self.saveas_btn.setFlat(True)

        # Save as with comment button
        self.saveascomm_btn = QtWidgets.QPushButton("")
        self.saveascomm_btn.setIcon(self.getIcon("comment"))
        self.saveascomm_btn.setIconSize(QtCore.QSize(38, 38))
        self.saveascomm_btn.setToolTip("Save As with a comment")
        self.saveascomm_btn.setFlat(True)

        for btn in [self.save_btn, self.saveas_btn, self.saveascomm_btn]:
            btn.setMinimumHeight(40)
            row1.addWidget(btn)
        self.main_layout.addLayout(row1)



        # Row 2: Export Publish , Playblast
        row2 = QtWidgets.QHBoxLayout()

        # Export button
        self.export_btn = QtWidgets.QPushButton("Export")
        self.export_btn.setIcon(self.getIcon("export"))
        self.export_btn.setIconSize(QtCore.QSize(32, 32))
        self.export_btn.setToolTip("Export")
        self.export_btn.setMinimumHeight(40)

        # Publish button
        self.publish_btn = QtWidgets.QPushButton("Publish")
        self.publish_btn.setIcon(self.getIcon("publish"))
        self.publish_btn.setIconSize(QtCore.QSize(32, 32))
        self.publish_btn.setToolTip("Publish")

        # Playblast button
        self.playblast_btn = QtWidgets.QPushButton("Playblast")
        self.playblast_btn.setIcon(self.getIcon("turn"))
        self.playblast_btn.setIconSize(QtCore.QSize(32, 32))
        self.playblast_btn.setToolTip("Playblast")


        for btn in [self.export_btn,self.publish_btn, self.playblast_btn]:
            btn.setMinimumHeight(40)
            row2.addWidget(btn)
        self.main_layout.addLayout(row2)




        # Row 3: Playblast
        row3 = QtWidgets.QHBoxLayout()

        # Import button
        self.import_btn = QtWidgets.QPushButton("Import")
        self.import_btn.setIcon(self.getIcon("import"))
        self.import_btn.setIconSize(QtCore.QSize(32, 32))
        self.import_btn.setToolTip("Import a file")
        row3.addWidget(self.import_btn)



        # Row 4: Stage, Window
        row4 = QtWidgets.QHBoxLayout()

        # Stage button
        self.stage_btn = QtWidgets.QPushButton("")
        self.stage_btn.setIcon(self.getIcon("settings"))
        self.stage_btn.setIconSize(QtCore.QSize(32, 32))
        self.stage_btn.setToolTip("Stage")

        # Window button
        self.window_btn = QtWidgets.QPushButton("")
        self.window_btn.setIcon(self.getIcon("window"))
        self.window_btn.setIconSize(QtCore.QSize(32, 32))
        self.window_btn.setToolTip("Window")


        for btn in [self.stage_btn, self.window_btn]:
            btn.setMinimumHeight(40)
            row4.addWidget(btn)

        row3.addLayout(row4)
        self.main_layout.addLayout(row3)


    # Setup the connections
    def setupConnections(self):
        # Connect buttons to functions
        self.save_btn.clicked.connect(self.save_btn_clicked)
        self.saveas_btn.clicked.connect(self.saveas_btn_clicked)
        self.saveascomm_btn.clicked.connect(self.saveascomm_btn_clicked)
        self.publish_btn.clicked.connect(self.publish_btn_clicked)
        self.playblast_btn.clicked.connect(self.playblast_btn_clicked)
        self.import_btn.clicked.connect(self.import_btn_clicked)
        self.stage_btn.clicked.connect(self.stage_btn_clicked)
        self.window_btn.clicked.connect(self.window_btn_clicked)
        self.export_btn.clicked.connect(self.export_btn_clicked)


    # Show window with docking ability
    def run(self):
        self.show(dockable=True)


    def showPrismWarningMessage(self):
        msg = QMessageBox(QMessageBox.Warning, "Prism Warning", "Failed to load Prism.")
        msg.addButton("Details", QMessageBox.YesRole)
        msg.addButton("Close", QMessageBox.RejectRole)
        msg.exec_()

    # Save button clicked
    def save_btn_clicked(self):
        cmds.file(save=True, force=True)
        pass

    # Save As button clicked
    def saveas_btn_clicked(self):
        try:
            pcore.saveScene()
        except:
            self.showPrismWarningMessage()

    def saveascomm_btn_clicked(self):
        try:
            pcore.saveWithComment()
        except:
            self.showPrismWarningMessage()

    # Get the state manager
    def getState(self):
        # Get the state manager
        sm = pcore.getStateManager()
        if not pcore.fileInPipeline():
            pcore.showFileNotInProjectWarning(title="Warning")
            return False

        for state in sm.states:
            if state.ui.className == "Export" and state.ui.e_name.text() == "Default Export ({product})":
                break
        else:
            parent = self.getDftStateParent()
            state = sm.createState("Export", stateData={"stateName": "Default Export ({product})"}, parent=parent)
            if not state:
                msg = "Failed to create export state. Please contact the support."
                pcore.popup(msg)
                return

            state.ui.initializeContextBasedSettings()
        return state


    # region PUBLISH
    def publish_btn_clicked(self):

        # Get the state manager
        state = self.getState()

        if not state:
            msg = "Failed to create publish state. Please contact the support."
            pcore.popup(msg)
            return

        # Get the current file path and split it
        filePath = pcore.getCurrentFileName()
        filePath = filePath.replace("\\", "/")
        splitedPath = filePath.split("/")

        # Prepare the name
        department = splitedPath[-3]
        taskName = splitedPath[-2]
        variation = ""
        outputType = ".usd"
        
        # If the department is RigL or RigH
        if department == "RigL" or department == "RigH":
            print("Rig department detected, asking for variation name.")
            
            # Export as a .ma
            outputType = ".ma" 

        if department.lower() == "rlo":
            print("RLO department detected, asking for variation name.")
            publishRLO(state, pcore)
            return


        # The name is : "<department>_Publish"
        name = department + "_Publish"
        state.ui.l_taskName.setText(name)
        state.ui.cb_outType.setCurrentText(outputType)
        state.ui.typeChanged(state.ui.getOutputType())
        

        try:
            pcore.getPlugin("Maya").onShelfClickedExport()
        except:
            self.showPrismWarningMessage()





    # endregion
    # region EXPORT
    def export_btn_clicked(self):
        sm = pcore.getStateManager()
        
        # Get the state manager
        state = self.getState()

        if not state:
            msg = "Failed to create publish state. Please contact the support."
            pcore.popup(msg)
            return

        # Get the current file path and split it
        filePath = pcore.getCurrentFileName()
        filePath = filePath.replace("\\", "/")
        splitedPath = filePath.split("/")

        # Prepare the name
        department = splitedPath[-3]
        taskName = splitedPath[-2]
        variation = ""
        outputType = ".usd"
        
        # If the department is RigL or RigH
        if department == "RigL" or department == "RigH":
            print("Rig department detected, asking for variation name.")
            
            # Export as a .ma
            outputType = ".ma" 


        state.ui.cb_outType.setCurrentText(outputType)
        state.ui.typeChanged(state.ui.getOutputType())
        


        if not pcore.fileInPipeline():
            pcore.showFileNotInProjectWarning(title="Warning")
            return False

        for state in sm.states:
            if state.ui.className == "Export" and state.ui.e_name.text() == "Default Export ({product})":
                break
        else:
            parent = self.getDftStateParent()
            state = sm.createState("Export", stateData={"stateName": "Default Export ({product})"}, parent=parent)
            if not state:
                msg = "Failed to create export state. Please contact the support."
                pcore.popup(msg)
                return

            state.ui.initializeContextBasedSettings()

        # If we are in "Export", the default name is : "<department>_Export_<taskName>"
        filePath = pcore.getCurrentFileName()
        # Exemple : E:\3D\PIPELINE\USD_Uptight_2025_v001\00_Template\Uptight\03_Production\01_Assets\Chars\Vinnie\Scenefiles\ModL\v001_UVs\Vinnie_v001_UVs_v0005.ma
        filePath = filePath.replace("\\", "/")
        splitedPath = filePath.split("/")

        department = splitedPath[-3]
        taskName = splitedPath[-2]

        name = department + "_Export_" + taskName
        state.ui.l_taskName.setText(name)

        try:
            pcore.getPlugin("Maya").onShelfClickedExport()
        except:
            self.showPrismWarningMessage()

    def playblast_btn_clicked(self):
        try:
            pcore.getPlugin("Maya").onShelfClickedPlayblast()
        except:
            self.showPrismWarningMessage()

    def import_btn_clicked(self):
        try:
            pcore.getPlugin("Maya").onShelfClickedImport()
        except:
            self.showPrismWarningMessage()

    def stage_btn_clicked(self):
        try:
            pcore.stateManager()
        except:
            self.showPrismWarningMessage()


    def window_btn_clicked(self):
        try:
            pcore.projectBrowser()
        except:
            self.showPrismWarningMessage()

    # endregion
    
    # region UTILS
    def getDftStateParent(self, create=True):
        sm = pcore.getStateManager()
        if not sm:
            return

        for state in sm.states:
            if state.ui.listType != "Export" or state.ui.className != "Folder":
                continue

            if state.ui.e_name.text() != "Default States":
                continue

            return state

        if create:
            stateData = {
                "statename": "Default States",
                "listtype": "Export",
                "stateenabled": 2,
                "stateexpanded": False,
            }
            state = sm.createState("Folder", stateData=stateData)
            return state
        

    def getIcon(self, iconName):
        currentPath = "C:/Users/Thomas/OneDrive/Bureau/Pipeline 2025/Pipeline_USD_2025-2026_src/maya/scripts/SaveAs"
        iconPath = os.path.join( currentPath, "icons", iconName + ".png")
        icon = QtGui.QIcon(iconPath)
        return icon
    
    # endregion





if __name__ == "__main__":
    try:
        window.close() # pylint: disable=E0601
        window.deleteLater()
    except:
        pass
    window = SaveAsWindow()
    window.run()




