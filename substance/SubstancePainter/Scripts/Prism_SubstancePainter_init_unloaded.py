from Prism_SubstancePainter_Variables import Prism_SubstancePainter_Variables
from Prism_SubstancePainter_externalAccess_Functions import (
    Prism_SubstancePainter_externalAccess_Functions,
)
from Prism_SubstancePainter_Integration import Prism_SubstancePainter_Integration


class Prism_SubstancePainter_unloaded(
    Prism_SubstancePainter_Variables,
    Prism_SubstancePainter_externalAccess_Functions,
    Prism_SubstancePainter_Integration,
):
    def __init__(self, core):
        Prism_SubstancePainter_Variables.__init__(self, core, self)
        Prism_SubstancePainter_externalAccess_Functions.__init__(self, core, self)
        Prism_SubstancePainter_Integration.__init__(self, core, self)
