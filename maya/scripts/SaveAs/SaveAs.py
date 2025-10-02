from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import PrismInit
from PySide6 import QtCore, QtGui, QtWidgets

import sys
import os

import maya.OpenMayaUI as omui

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.cmds as cmds
from maya.OpenMayaUI import MQtUtil


from SaveAs.IconLoader import loadIcon
from SaveAs.ExecuteDepartment import ExecuteDepartment_ModL, ExecuteDepartment_ModH, ExecuteDepartment_RigL, ExecuteDepartment_RigH, ExecuteDepartment_RLO, ExecuteDepartment_FLO, ExecuteDepartment_Animation


def maya_main_window():
    # main_window_ptr = omui.MQtUtil.mainWindow()
    return None


# Links the department keys to their corresponding execute department class
ExecuteDepartments_Keys = {
    "modl" : ExecuteDepartment_ModL(),     # <- Modelisation Low
    "modh" : ExecuteDepartment_ModH(),     # <- Modelisation High
    "rigl" : ExecuteDepartment_RigL(),     # <- Rig Low
    "righ" : ExecuteDepartment_RigH(),     # <- Rig High
    "rlo"  : ExecuteDepartment_RLO(),      # <- Rough Layout
    "flo"  : ExecuteDepartment_FLO(),      # <- Final Layout
    "anim" : ExecuteDepartment_Animation() # <- Animation  
}









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
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        
        self.pcore = PrismInit.pcore

        # Setup the User Interface
        self.setupUi()

        # Setup the connections
        self.setupConnections()

        # Setup the current department
        self.setupCurrentDepartment()

    # Setup the User Interface
    def setupUi(self):

        # Main vertical layout
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.main_layout)

        # --- Menu Bar ---
        self.menu_bar = QtWidgets.QMenuBar(self)

        self.setupMenuBar()

        # Ajout du menu bar en haut du layout
        self.main_layout.setMenuBar(self.menu_bar)

        # Row 1: Save, Save As, Save As Comm
        row1 = QtWidgets.QHBoxLayout()
        row1.setSpacing(0)

        # Save button
        self.save_btn = QtWidgets.QPushButton("")
        self.save_btn.setIcon(loadIcon("save.png"))
        self.save_btn.setIconSize(QtCore.QSize(24, 24))
        self.save_btn.setToolTip("Save")
        self.save_btn.setFlat(True)

        # Save as button
        self.saveas_btn = QtWidgets.QPushButton("")
        self.saveas_btn.setIcon(loadIcon("saveas.png"))
        self.saveas_btn.setIconSize(QtCore.QSize(24, 24))
        self.saveas_btn.setToolTip("Save As")
        self.saveas_btn.setFlat(True)

        # Save as with comment button
        self.saveascomm_btn = QtWidgets.QPushButton("")
        self.saveascomm_btn.setIcon(loadIcon("comment.png"))
        self.saveascomm_btn.setIconSize(QtCore.QSize(24, 24))
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
        self.export_btn.setIcon(loadIcon("export.png"))
        self.export_btn.setIconSize(QtCore.QSize(24, 24))
        self.export_btn.setToolTip("Export")
        self.export_btn.setMinimumHeight(40)

        # Publish button
        self.publish_btn = QtWidgets.QPushButton("Publish")
        self.publish_btn.setIcon(loadIcon("publish.png"))
        self.publish_btn.setIconSize(QtCore.QSize(24, 24))
        self.publish_btn.setToolTip("Publish")

        # Playblast button
        self.playblast_btn = QtWidgets.QPushButton("Playblast")
        self.playblast_btn.setIcon(loadIcon("turn.png"))
        self.playblast_btn.setIconSize(QtCore.QSize(24, 24))
        self.playblast_btn.setToolTip("Playblast")

        for btn in [self.export_btn,self.publish_btn, self.playblast_btn]:
            btn.setMinimumHeight(40)
            row2.addWidget(btn)
        self.main_layout.addLayout(row2)

        # Row 3: Playblast
        row3 = QtWidgets.QHBoxLayout()

        # Import button
        self.import_btn = QtWidgets.QPushButton("Import")
        self.import_btn.setIcon(loadIcon("import.png"))
        self.import_btn.setIconSize(QtCore.QSize(24, 24))
        self.import_btn.setToolTip("Import a file")
        row3.addWidget(self.import_btn)

        # Row 4: Stage, Window
        row4 = QtWidgets.QHBoxLayout()

        # Stage button
        self.stage_btn = QtWidgets.QPushButton("")
        self.stage_btn.setIcon(loadIcon("settings.png"))
        self.stage_btn.setIconSize(QtCore.QSize(24, 24))
        self.stage_btn.setToolTip("Stage")

        # Window button
        self.window_btn = QtWidgets.QPushButton("")
        self.window_btn.setIcon(loadIcon("window.png"))
        self.window_btn.setIconSize(QtCore.QSize(24, 24))
        self.window_btn.setToolTip("Window")

        for btn in [self.stage_btn, self.window_btn]:
            btn.setMinimumHeight(40)
            row4.addWidget(btn)

        row3.addLayout(row4)
        self.main_layout.addLayout(row3)


    # Setup the menu bar
    def setupMenuBar(self):
        # Add a "Department menu"
        department_menu = self.menu_bar.addMenu("&Departement")

        # Créer un QActionGroup exclusif
        self.dept_action_group = QtGui.QActionGroup(self)
        self.dept_action_group.setExclusive(True)

        self.action_modeling_low = department_menu.addAction("Modeling Low")
        self.action_modeling_low.setCheckable(True)
        self.action_modeling_low.setToolTip("ModL")
        self.action_modeling_low.setChecked(True)  # Set default checked
        self.dept_action_group.addAction(self.action_modeling_low)

        self.action_modeling_high = department_menu.addAction("Modeling High")
        self.action_modeling_high.setCheckable(True)
        self.action_modeling_high.setToolTip("ModH")
        self.dept_action_group.addAction(self.action_modeling_high)

        self.action_rig_low = department_menu.addAction("Rig Low")
        self.action_rig_low.setCheckable(True)
        self.action_rig_low.setToolTip("RigL")
        self.dept_action_group.addAction(self.action_rig_low)

        self.action_rig_high = department_menu.addAction("Rig High")
        self.action_rig_high.setCheckable(True)
        self.action_rig_high.setToolTip("RigH")
        self.dept_action_group.addAction(self.action_rig_high)

        self.action_rlo = department_menu.addAction("RLO")
        self.action_rlo.setCheckable(True)
        self.action_rlo.setToolTip("RLO")
        self.dept_action_group.addAction(self.action_rlo)

        self.action_flo = department_menu.addAction("FLO")
        self.action_flo.setCheckable(True)
        self.action_flo.setToolTip("FLO")
        self.dept_action_group.addAction(self.action_flo)

        self.action_animation = department_menu.addAction("Animation")
        self.action_animation.setCheckable(True)
        self.action_animation.setToolTip("Anim")
        self.dept_action_group.addAction(self.action_animation)

        # Add a "View" menu
        view_menu = self.menu_bar.addMenu("&View")
        
        self.action_pro_mode = view_menu.addAction("Pro Mode")
        self.action_pro_mode.setCheckable(True)
        self.action_pro_mode.setChecked(False)
        self.action_pro_mode.setToolTip("Hide basic save buttons for advanced users")
        self.action_pro_mode.setShortcut(QtGui.QKeySequence("Ctrl+P"))
        self.action_pro_mode.triggered.connect(self.toggle_pro_mode)

        # Add a "Help" menu
        help_menu = self.menu_bar.addMenu("&Help")
        help_menu.addAction("Documentation", self.show_documentation)

    # Setup the current department
    def setupCurrentDepartment(self):
        # Get the current file path and split it
        try:
            filePath = self.pcore.getCurrentFileName()

            filePath = filePath.replace("\\", "/")
            splitedPath = filePath.split("/")

            # Prepare the name
            department = splitedPath[-3]

            for action in self.dept_action_group.actions():
                if action.toolTip().lower() == department.lower():
                    action.setChecked(True)
                    print("The department ID is : ", action.text())

                    # Set the window title to include the department
                    self.setWindowTitle(f"Badger Pipeline - {action.text()}")
        except:
            return
        if not filePath or filePath == "":
            return
        


    # Get the selected department
    def getDepartment(self):
        for action in self.dept_action_group.actions():
            if action.isChecked():
                return action.toolTip()
        return ""

    # Show the documentation
    def show_documentation(self):
        print("Opening documentation...")
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://thomasescalle.github.io/Pipeline_USD_2025/"))

    # Toggle pro mode - hide/show basic save buttons
    def toggle_pro_mode(self, checked):
        """Hide or show the basic save buttons based on pro mode state"""
        # Hide/show the save buttons when pro mode is toggled
        self.save_btn.setVisible(not checked)
        self.saveas_btn.setVisible(not checked)
        self.saveascomm_btn.setVisible(not checked)
        
        if checked:
            print("Pro Mode activated - basic save buttons hidden")
        else:
            print("Pro Mode deactivated - basic save buttons visible")

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
        msg.addButton("Close", QMessageBox.RejectRole)
        msg.exec_()

    # Save button clicked
    def save_btn_clicked(self):
        cmds.file(save=True, force=True)
        pass

    # Save As button clicked
    def saveas_btn_clicked(self):
        try:
            self.pcore.saveScene()
        except:
            self.showPrismWarningMessage()

    def saveascomm_btn_clicked(self):
        try:
            self.pcore.saveWithComment()
        except:
            self.showPrismWarningMessage()

    # Get the state manager
    def getState(self):
        # Get the state manager
        sm = self.pcore.getStateManager()
        if not self.pcore.fileInPipeline():
            self.pcore.showFileNotInProjectWarning(title="Warning")
            return False

        for state in sm.states:
            if state.ui.className == "Export" and state.ui.e_name.text() == "Default Export ({product})":
                break
        else:
            parent = self.getDftStateParent()
            state = sm.createState("Export", stateData={"stateName": "Default Export ({product})"}, parent=parent)
            if not state:
                msg = "Failed to create export state. Please contact the support."
                self.pcore.popup(msg)
                return

            state.ui.initializeContextBasedSettings()
        return state


    # region PUBLISH
    def publish_btn_clicked(self):

        # Get the current department
        current_department = self.getDepartment()
        if not current_department:
            print("No department selected.")
            return

        # Get the execute department class
        current_department = current_department.lower()
        print("Current department is : ", current_department)
        execute_department = ExecuteDepartments_Keys.get(current_department.lower())
        if not execute_department:
            print("No execute department found.")
            return

        print("1")
        execute_department.publish(self.pcore)




    # endregion
    # region EXPORT
    def export_btn_clicked(self):
        # Get the current department
        current_department = self.getDepartment()
        if not current_department:
            print("No department selected.")
            return

        # Get the execute department class
        current_department = current_department.lower()
        print("Current department is : ", current_department)
        execute_department = ExecuteDepartments_Keys.get(current_department.lower())

        if not execute_department:
            print("No execute department found.")
            return

        # Call the export method from the selected execute department
        execute_department.export(self.pcore)





    def playblast_btn_clicked(self):
        try:
            self.pcore.getPlugin("Maya").onShelfClickedPlayblast()
        except:
            self.showPrismWarningMessage()

    def import_btn_clicked(self):
        try:
            self.pcore.getPlugin("Maya").onShelfClickedImport()
        except:
            self.showPrismWarningMessage()

    def stage_btn_clicked(self):
        try:
            self.pcore.stateManager()
        except:
            self.showPrismWarningMessage()


    def window_btn_clicked(self):
        try:
            self.pcore.projectBrowser()
        except:
            self.showPrismWarningMessage()

    # endregion
    
    # region UTILS
    def getDftStateParent(self, create=True):
        sm = self.pcore.getStateManager()
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


def main():
    try:
        window.close() # pylint: disable=E0601
        window.deleteLater()
    except:

        pass
    window = SaveAsWindow()
    window.run()


if __name__ == "__main__":
    main()




