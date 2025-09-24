import sys
import os
import importlib
import traceback
import platform
import pathlib
from pathlib import Path

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import substance_painter.ui

pcore = None

def start_plugin():
    prismInit()


def close_plugin():
    global pcore
    if pcore is None:
        print("Plugin core already None; cannot unregister")
        return

    # Only unregister if the attributes exist
    if hasattr(pcore, "appPlugin") and pcore.appPlugin is not None:
        pcore.appPlugin.unregister()

    # Clear the reference last
    pcore = None
    print("Plugin safely unregistered")


def prismInit():
    prismRoot = os.getenv("PRISM_ROOT")
    if not prismRoot:
        prismRoot = find_prism()

    scriptDir = os.path.join(prismRoot, "Scripts")

    if scriptDir not in sys.path:
        sys.path.append(scriptDir)
    global pcore
    # Import PrismCore from the Prism Scripts folder
    import PrismCore
    importlib.reload(PrismCore)

    pcore = PrismCore.create(
        app="SubstancePainter",
        prismArgs=["noProjectBrowser"]
    )


def find_prism():
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
                    return prism_path

    return ""
