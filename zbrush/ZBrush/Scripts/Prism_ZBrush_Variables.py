import os


class Prism_ZBrush_Variables(object):
    def __init__(self, core, plugin):
        self.version = "v2.0.10"
        self.pluginName = "ZBrush"
        self.pluginType = "App"
        self.appShortName = "ZBrush"
        self.appType = "3d"
        self.hasQtParent = False
        self.sceneFormats = [".ZPR", ".zpr", ".ZTL", ".ztl"]
        self.appSpecificFormats = self.sceneFormats
        self.appColor = [255, 180, 40]
        self.hasFrameRange = False
        self.canOverrideExecuteable = True
        self.platforms = ["Windows"]
        self.pluginDirectory = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        self.appIcon = os.path.join(self.pluginDirectory, "Resources", "ZLogo.ico")
