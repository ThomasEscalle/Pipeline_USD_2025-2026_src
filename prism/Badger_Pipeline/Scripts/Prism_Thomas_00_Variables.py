# -*- coding: utf-8 -*-

import os


class Prism_Thomas_00_Variables(object):
    def __init__(self, core, plugin):
        self.version = "v2.0.0"
        self.pluginName = "Thomas_00"
        self.pluginType = "Custom"
        self.platforms = ["Windows"]
        self.pluginDirectory = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
