import os


class Prism_SubstancePainter_Variables(object):
    def __init__(self, core, plugin):
        self.version = "v2.0.0"
        self.pluginName = "SubstancePainter"
        self.pluginType = "App"
        self.appShortName = "SubstancePainter"
        self.appType = "3d"
        self.hasQtParent = True
        self.sceneFormats = [".spp", ".exr", ".png", ".jpg", "tiff"]
        self.appSpecificFormats = self.sceneFormats
        self.outputFormats = [".exr", ".png", ".jpg", "tiff"]
        self.appColor = [255, 255, 255]
        self.renderPasses = []
        self.hasFrameRange = False
        self.platforms = ["Windows"]
        self.pluginDirectory = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        self.appIcon = os.path.join(self.pluginDirectory, "Resources", "Substance.ico")
