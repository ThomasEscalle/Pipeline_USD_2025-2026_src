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
import shutil

class Prism_sync_media_Functions(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin

        self.supportedFormats = [
            ".jpg",
            ".jpeg",
            ".JPG",
            ".png",
            ".PNG",
            ".tif",
            ".tiff",
            ".tga",
            ".dpx",
            ".exr",
            ".hdr",
            ".mp4",
            ".mov",
            ".avi",
            ".m4v",
        ]
        self.videoFormats = [".mp4", ".mov", ".avi", ".m4v"]

        self.core.registerCallback("onProjectBrowserStartup", self.onProjectBrowserStartup, plugin=self)

    def onProjectBrowserStartup(self, origin):
        origin.syncMenu = QMenu("Sync Media")
        action = origin.syncMenu.addAction("Synchronize", self.onActionTriggered)
        action.setShortcut(QKeySequence("Ctrl+Shift+W"))
        origin.menubar.addMenu(origin.syncMenu)

    def onActionTriggered(self):
        print("Sync Media World action triggered")
        self.pipeline_path = self.core.projects.getResolvedProjectStructurePath("pipeline", context={})

        json_settings_path = os.path.join(self.pipeline_path, "sync_media_settings.json")
        if not os.path.exists(json_settings_path):
            # create default settings
            default_settings = {
                "rules" : [] 
            }
            with open(json_settings_path, "w") as f:
                json.dump(default_settings, f, indent=4)

            # If the file still does not exist, return
            if not os.path.exists(json_settings_path):
                QMessageBox.critical(None, "Error", f"Could not create default settings file at {json_settings_path}")
                return
            
        settings = {}
        with open(json_settings_path, "r") as f:
            settings = json.load(f)
        
        if "rules" not in settings:
            QMessageBox.critical(None, "Error", f"Settings file at {json_settings_path} is malformed. Missing 'rules' key.")
            return

        rules = settings["rules"]
        if not isinstance(rules, list):
            QMessageBox.critical(None, "Error", f"Settings file at {json_settings_path} is malformed. 'rules' key must be a list.")
            return
        
        for rule in rules:
            if not isinstance(rule, dict):
                QMessageBox.critical(None, "Error", f"Settings file at {json_settings_path} is malformed. Each rule must be a dictionary.")
                return
            
            self.processRule(rule)


    def processRule(self, rule):
        # Check if the key "source_media" exists
        # It can be an array of strings, or a single string
        if "source_media" not in rule:
            print(f"Invalid rule in settings file at {json_settings_path}: missing 'source_media' key.")
            return
        if isinstance(rule["source_media"], str):
            rule["source_media"] = [rule["source_media"]]
        elif not isinstance(rule["source_media"], list):
            print(f"Invalid rule in settings file at {json_settings_path}: 'source_media' must be a string or a list of strings.")
            return


        # Check if the key "destination" exists
        if "destination" not in rule or not isinstance(rule["destination"], dict):
            print(f"Invalid rule in settings file at {json_settings_path}: 'destination' must be a dictionary.")
            return
        
        source_media = rule["source_media"]
        destination = rule["destination"]

        # Check if destination has required keys
        if "images_destination" not in destination or "videos_destination" not in destination:
            print(f"Invalid rule in settings file at {json_settings_path}: 'destination' must contain 'images_destination' and 'videos_destination' keys.")
            return

        images_destination = destination["images_destination"]
        videos_destination = destination["videos_destination"]

        # 1.  Iterate over all the shots in the project
        # 2.  Iterate over all the medias in the shots
        # 3.  Check if the media source matches the source_media
        # 4.  If it matches, get the latest version of the media
        # 5.  Copy the media to the appropriate destination (images or videos)
        
        shots = self.core.entities.getShots()
        for shot in shots:
            print(f"Processing shot: {shot}")

            # Get shot details
            sequence = shot["sequence"]
            shot_name = shot["shot"]
            shot_display_name = sequence + "_" + shot_name

            path = shot.get("path", "")
            path = path.replace("\\", "/")

            path_playblasts = os.path.join(path, "Playblasts").replace("\\", "/")
            path_2dRender = os.path.join(path, "Renders/2dRender").replace("\\", "/")
            path_3dRender = os.path.join(path, "Renders/3dRender").replace("\\", "/")

            # List the subdirectories in all paths
            subdirs = []
            for p in [path_playblasts, path_2dRender, path_3dRender]:
                if os.path.exists(p):
                    for entry in os.listdir(p):
                        full_path = os.path.join(p, entry)
                        if os.path.isdir(full_path):
                            subdirs.append(full_path.replace("\\", "/"))

            for media_path in subdirs:
                print(f"  Checking media path: {media_path}")
                media_source = os.path.basename(media_path)
                
                # Check if the media source matches the source_media (all of them)
                match = True
                for sm in source_media:
                    if sm.lower() not in media_source.lower():
                        match = False
                        break
                if not match:
                    print(f"    Media source '{media_source}' does not match source_media {source_media}. Skipping.")
                    continue

                # Get the latest version of the media
                versions = []
                for entry in os.listdir(media_path):
                    full_path = os.path.join(media_path, entry)
                    if os.path.isdir(full_path) and entry.startswith("v"):
                        versions.append(full_path.replace("\\", "/"))

                if not versions:
                    print(f"    No versions found in media path: {media_path}. Skipping.")
                    continue

                versions.sort()
                latest_version_path = versions[-1]
                
                # Iterate over files in the latest version directory,
                # If one matches supported formats, copy it to the appropriate destination
                for entry in os.listdir(latest_version_path):
                    full_path = os.path.join(latest_version_path, entry)
                    if os.path.isfile(full_path):

                        _, ext = os.path.splitext(entry)
                        if ext in self.supportedFormats:
                            print(f"    Found media image file: {full_path}")
                            
                            if ext in self.videoFormats:
                                self.copyMediaFile(full_path, videos_destination, shot_display_name, ext, shot_name, sequence, video=True)
                            else:
                                self.copyMediaFile(full_path, images_destination, shot_display_name, ext, shot_name, sequence, video=False)
                            
    
    def copyMediaFile(self, source_file, destination_template, shot_display_name, ext, shot_name, sequence, video = False):
        print(f"      Copying media file: {source_file}")
        print(f"      Using destination template: {destination_template}")

        destination = destination_template

        # if we are copying a video, use the videos_destination template
        if video == False:
            frame_number = self.core.media.getFrameNumberFromFilename(source_file)
            destination = destination.replace("@frames@", f"{frame_number}")
            print(f"      Detected frame number: {frame_number}")

        # Cd up one the pipeline path for @pipeline@ variable
        pipeline_cd_up = os.path.dirname(self.pipeline_path)

        destination = destination.replace("@ext@", ext.lstrip("."))
        destination = destination.replace("@sht@", shot_name)
        destination = destination.replace("@seq@", sequence)
        destination = destination.replace("@shot_display_name@", shot_display_name)
        destination = destination.replace("@pipeline@", pipeline_cd_up.replace("\\", "/"))
        destination_dir = os.path.dirname(destination)

        # Check if destination directory exists, if not create it
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir, exist_ok=True)
            print(f"      Created destination directory: {destination_dir}")

        # Copy the file
        shutil.copy2(source_file, destination)

        print(f"      Resolved destination path: {destination}")


    # if returns true, the plugin will be loaded by Prism
    @err_catcher(name=__name__)
    def isActive(self):
        return True
