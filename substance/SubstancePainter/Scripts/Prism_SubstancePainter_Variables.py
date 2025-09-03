import os


class Prism_SubstancePainter_Variables(object):
    def __init__(self, core, plugin):
        self.version = "v2.0.0"
        self.pluginName = "SubstancePainter"
        self.pluginType = "App"
        self.appShortName = "SubstancePainter"
        self.appType = "3d"
        self.hasQtParent = True
        self.sceneFormats = [".format"]
        self.appSpecificFormats = self.sceneFormats
        self.outputFormats = [".abc", ".obj", ".fbx", "ShotCam"]
        self.appColor = [255, 255, 255]
        self.renderPasses = []
        self.platforms = ["Windows"]
        self.pluginDirectory = os.path.abspath(
            os.path.dirname(os.path.dirname(__file__))
        )
