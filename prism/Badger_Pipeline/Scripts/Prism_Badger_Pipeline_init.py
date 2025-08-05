# -*- coding: utf-8 -*-

from Prism_Badger_Pipeline_Variables import Prism_Badger_Pipeline_Variables
from Prism_Badger_Pipeline_Functions import Prism_Badger_Pipeline_Functions


class Prism_Badger_Pipeline(Prism_Badger_Pipeline_Variables, Prism_Badger_Pipeline_Functions):
    def __init__(self, core):
        Prism_Badger_Pipeline_Variables.__init__(self, core, self)
        Prism_Badger_Pipeline_Functions.__init__(self, core, self)
