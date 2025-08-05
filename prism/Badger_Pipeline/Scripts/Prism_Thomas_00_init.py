# -*- coding: utf-8 -*-

from Prism_Thomas_00_Variables import Prism_Thomas_00_Variables
from Prism_Thomas_00_Functions import Prism_Thomas_00_Functions


class Prism_Thomas_00(Prism_Thomas_00_Variables, Prism_Thomas_00_Functions):
    def __init__(self, core):
        Prism_Thomas_00_Variables.__init__(self, core, self)
        Prism_Thomas_00_Functions.__init__(self, core, self)
