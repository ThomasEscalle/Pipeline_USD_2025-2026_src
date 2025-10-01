

import os
from PySide6.QtGui import QIcon


def loadIcon(name):
    # Get the path of the script
    scriptPath = os.path.realpath(__file__)
    scriptPath = scriptPath.replace("\\", "/")
    scriptPath = scriptPath.replace("/IconLoader.py" , "")
    scriptPath += "/icons/" + name 
    return QIcon(scriptPath)