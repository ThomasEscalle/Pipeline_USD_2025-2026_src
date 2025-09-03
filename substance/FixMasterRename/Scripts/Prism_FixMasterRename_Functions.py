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


from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from PrismUtils.Decorators import err_catcher_plugin as err_catcher
    
import os
import json


class Prism_FixMasterRename_Functions(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin
        # Register our callback
        self.core.registerCallback("masterVersionUpdated", self.fix_master_filename)

    # if returns true, the plugin will be loaded by Prism
    @err_catcher(name=__name__)
    def isActive(self):
        return True

    def fix_master_filename(self, master_path):
        folder = os.path.dirname(master_path)
        files = os.listdir(folder)

        json_file = os.path.join(folder, "versioninfo.json")
        if not os.path.exists(json_file):
            print("[FixMasterName] No versioninfo.json found in:", folder)
            return

        with open(json_file, 'r') as file:
            context = json.load(file)

        version = context.get("version")
        if not version:
            print("[FixMasterName] No version found in versioninfo.json")
            return

        version_base = folder.replace("\\", "/").split("/")
        version_base.pop(-1)
        version_folder = "/".join(version_base) + "/" + version

        if not os.path.exists(version_folder):
            print("[FixMasterName] Version folder not found:", version_folder)
            return

        correct_files = os.listdir(version_folder)
        if not correct_files:
            print("[FixMasterName] No files in version folder:", version_folder)
            return
        if len(correct_files)<5:
            return

        correct_name = correct_files[0]

        for f in files:
            if "master." in f:
                old_path = os.path.join(folder, f)
                new_path = os.path.join(folder, correct_name)
                print(f"[FixMasterName] Renaming {old_path} → {new_path}")
                os.rename(old_path, new_path)

