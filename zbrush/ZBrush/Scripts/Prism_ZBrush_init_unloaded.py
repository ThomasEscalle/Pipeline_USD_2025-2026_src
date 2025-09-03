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
# Licensed under proprietary license. See license file in the directory of this plugin for details.
#
# This file is part of Prism-Plugin-ZBrush.
#
# Prism-Plugin-ZBrush is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.


from Prism_ZBrush_Variables import Prism_ZBrush_Variables
from Prism_ZBrush_externalAccess_Functions import (
    Prism_ZBrush_externalAccess_Functions,
)
from Prism_ZBrush_Integration import Prism_ZBrush_Integration


class Prism_ZBrush_unloaded(
    Prism_ZBrush_Variables,
    Prism_ZBrush_externalAccess_Functions,
    Prism_ZBrush_Integration,
):
    def __init__(self, core):
        Prism_ZBrush_Variables.__init__(self, core, self)
        Prism_ZBrush_externalAccess_Functions.__init__(self, core, self)
        Prism_ZBrush_Integration.__init__(self, core, self)
