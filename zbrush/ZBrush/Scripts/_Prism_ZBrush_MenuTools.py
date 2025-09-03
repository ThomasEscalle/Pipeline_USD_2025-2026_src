import os
import sys



#import Prism_ZBrush_Functions as functions


def Tools(core):
    #open tools window with a button for each function [Project Browser, Save Version, Save Comment, Import, Export, Settings]
    tools_window = QWidget()
    tools_window.setWindowTitle("Prism")
    layout = QVBoxLayout()
    btn_save_version = QPushButton("Save Version")
    btn_save_version.clicked.connect(lambda: SaveVersion(core))
    layout.addWidget(btn_save_version)
    btn_save_comment = QPushButton("Save Extended")
    btn_save_comment.clicked.connect(lambda: SaveComment(core))
    layout.addWidget(btn_save_comment)
    btn_import = QPushButton("Import")
    btn_import.clicked.connect(lambda: Import(core))
    layout.addWidget(btn_import)
    btn_export = QPushButton("Export")
    btn_export.clicked.connect(lambda: Export(core))
    layout.addWidget(btn_export)
    btn_project_browser = QPushButton("Project Browser")
    btn_project_browser.clicked.connect(lambda: ProjectBrowser(core))
    layout.addWidget(btn_project_browser)
    btn_settings = QPushButton("Settings")
    btn_settings.clicked.connect(lambda: Settings(core))
    layout.addWidget(btn_settings)

    tools_window.setLayout(layout)
    tools_window.show()
    tools_window.raise_()
    tools_window.activateWindow()
    tools_window.setWindowFlags(tools_window.windowFlags() | Qt.WindowStaysOnTopHint)
    tools_window.setAttribute(Qt.WA_DeleteOnClose)

    return tools_window

def ProjectBrowser(core):
    pb = core.ProjectBrowser()

    pb.show()
    pb.raise_()
    pb.activateWindow()

    return pb

def SaveVersion(core):
    filePath = ""
    #functions.saveScene(core, filePath)

def SaveComment(core):
    path = core.saveWithComment()

def Import(core):

    filepath = core.importDialog()

def Export(core):
    filepath = core.exportDialog()
    # Then trigger ZBrush export if needed

def Settings(core):
    core.openSettings()




