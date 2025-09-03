# -*- coding: utf-8 -*-
#
####################################################
#
# PRISM - Pipeline for animation and VFX projects
#
# www.prism-pipeline.com
#
# contact: contact@prism-pipeline.com
#
####################################################
#
#
# Copyright (C) 2016-2023 Richard Frangenberg
# Copyright (C) 2023 Prism Software GmbH
#
# Licensed under GNU LGPL-3.0-or-later
#
# This file is part of Prism.
#
# Prism is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Prism is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Prism.  If not, see <https://www.gnu.org/licenses/>.


from Prism_SubstancePainter_Variables import Prism_SubstancePainter_Variables
from Prism_SubstancePainter_externalAccess_Functions import (
    Prism_SubstancePainter_externalAccess_Functions,
)
from Prism_SubstancePainter_Functions import Prism_SubstancePainter_Functions
from Prism_SubstancePainter_Integration import Prism_SubstancePainter_Integration


class Prism_Plugin_SubstancePainter(
    Prism_SubstancePainter_Variables,
    Prism_SubstancePainter_externalAccess_Functions,
    Prism_SubstancePainter_Functions,
    Prism_SubstancePainter_Integration,
):
    def __init__(self, core):
        Prism_SubstancePainter_Variables.__init__(self, core, self)
        Prism_SubstancePainter_externalAccess_Functions.__init__(self, core, self)
        Prism_SubstancePainter_Functions.__init__(self, core, self)
        Prism_SubstancePainter_Integration.__init__(self, core, self)
