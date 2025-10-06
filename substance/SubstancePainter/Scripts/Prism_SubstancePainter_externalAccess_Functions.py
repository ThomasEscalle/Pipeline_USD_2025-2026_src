import os
import platform

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from PrismUtils.Decorators import err_catcher_plugin as err_catcher


class Prism_SubstancePainter_externalAccess_Functions(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin

    @err_catcher(name=__name__)
    def getAutobackPath(self, origin):
        autobackpath = ""
        if platform.system() == "Windows":
            autobackpath = os.path.join(
                self.core.getWindowsDocumentsPath(), "SubstancePainter"
            )

        fileStr = "SubstancePainter Scene File ("
        for i in self.sceneFormats:
            fileStr += "*%s " % i

        fileStr += ")"

        return autobackpath, fileStr

    @err_catcher(name=__name__)
    def copySceneFile(self, origin, origFile, targetPath, mode="copy"):
        pass
