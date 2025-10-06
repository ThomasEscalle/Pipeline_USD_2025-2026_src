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


import os
import glob

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from PrismUtils.Decorators import err_catcher_plugin as err_catcher


class Prism_ZBrush_externalAccess_Functions(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin
        self.core.registerCallback("getPresetScenes", self.getPresetScenes, plugin=self.plugin)
        ssheetPath = os.path.join(
            self.pluginDirectory,
            "UserInterfaces",
            "ZBrushStyleSheet"
        )
        self.core.registerStyleSheet(ssheetPath)
        self.core.registerCallback(
            "userSettings_saveSettings",
            self.userSettings_saveSettings,
            plugin=self.plugin,
        )
        self.core.registerCallback(
            "userSettings_loadSettings",
            self.userSettings_loadSettings,
            plugin=self.plugin,
        )

    @err_catcher(name=__name__)
    def userSettings_loadUI(self, origin, tab):
        tab.lo_settings = QGridLayout()
        tab.layout().addLayout(tab.lo_settings)
        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
        tab.lo_settings.addItem(spacer, 0, 0)

        origin.l_sceneType = QLabel("Save scene as:")
        origin.cb_sceneType = QComboBox()
        tab.lo_settings.addWidget(origin.l_sceneType, 1, 1)
        tab.lo_settings.addWidget(origin.cb_sceneType, 1, 2)

        origin.chb_zbrushSendToHoudini = QCheckBox("Enable Send To Houdini")
        tab.lo_settings.addWidget(origin.chb_zbrushSendToHoudini, 2, 1)

        origin.chb_zbrushSendToMaya = QCheckBox("Enable Send To Maya")
        tab.lo_settings.addWidget(origin.chb_zbrushSendToMaya, 3, 1)

        origin.chb_zbrushSendToBlender = QCheckBox("Enable Send To Blender")
        tab.lo_settings.addWidget(origin.chb_zbrushSendToBlender, 4, 1)

        self.saveSceneTypes = [
            ".zpr",
            ".ztl",
        ]

        origin.cb_sceneType.addItems(self.saveSceneTypes)

    @err_catcher(name=__name__)
    def userSettings_saveSettings(self, origin, settings):
        if "zbrush" not in settings:
            settings["zbrush"] = {}

        settings["zbrush"]["saveSceneType"] = origin.cb_sceneType.currentText()
        settings["zbrush"]["enableSendToHoudini"] = origin.chb_zbrushSendToHoudini.isChecked()
        settings["zbrush"]["enableSendToMaya"] = origin.chb_zbrushSendToMaya.isChecked()
        settings["zbrush"]["enableSendToBlender"] = origin.chb_zbrushSendToBlender.isChecked()

    @err_catcher(name=__name__)
    def userSettings_loadSettings(self, origin, settings):
        if "zbrush" in settings:
            if "saveSceneType" in settings["zbrush"]:
                saveType = settings["zbrush"]["saveSceneType"]
                idx = origin.cb_sceneType.findText(saveType)
                if idx != -1:
                    origin.cb_sceneType.setCurrentIndex(idx)

            if "enableSendToHoudini" in settings["zbrush"]:
                enabled = settings["zbrush"]["enableSendToHoudini"]
                origin.chb_zbrushSendToHoudini.setChecked(enabled)

            if "enableSendToMaya" in settings["zbrush"]:
                enabled = settings["zbrush"]["enableSendToMaya"]
                origin.chb_zbrushSendToMaya.setChecked(enabled)

            if "enableSendToBlender" in settings["zbrush"]:
                enabled = settings["zbrush"]["enableSendToBlender"]
                origin.chb_zbrushSendToBlender.setChecked(enabled)

    @err_catcher(name=__name__)
    def getAutobackPath(self, origin):
        autobackpath = ""

        fileStr = "ZBrush Script ("
        for i in self.sceneFormats:
            fileStr += "*%s " % i

        fileStr += ")"

        return autobackpath, fileStr

    @err_catcher(name=__name__)
    def getZPrefDirs(self):
        pubuser = os.environ["PUBLIC"]
        prefDir = os.path.join(pubuser, "Documents", "ZBrushData*")
        prefDirs = glob.glob(prefDir)
        return prefDirs

    @err_catcher(name=__name__)
    def customizeExecutable(self, origin, appPath, filepath):
        msg = "The Prism features will be limited when opening a ZBrush project from Prism standalone.\nSave or load your ZBrush project using Prism inside of ZBrush to avoid any limitations."
        self.core.popup(msg)
        return False

    @err_catcher(name=__name__)
    def getPresetScenes(self, presetScenes):
        presetDir = os.path.join(self.pluginDirectory, "Presets")
        scenes = self.core.entities.getPresetScenesFromFolder(presetDir)
        presetScenes += scenes
