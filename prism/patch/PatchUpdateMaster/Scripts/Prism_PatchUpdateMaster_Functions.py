from PrismUtils.Decorators import err_catcher_plugin as err_catcher
import os
import json
import shutil

from PySide6 import QtWidgets, QtCore
import sys


class Prism_PatchUpdateMaster_Functions(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin

        self.core.plugins.monkeyPatch(self.core.products.updateMasterVersion, self.updateMasterVersion, self, force=True)
        self.core.registerCallback("masterVersionUpdated", self.fix_master_filename)

    def isActive(self):
        return True
    
    def updateMasterVersion(self, path, *args, **kwargs):
        #pre-hook code can go here
        productPath = path.replace("\\", "/")
        productPath = productPath.split("/")
        productPath.pop(-1)
        productPath = '/'.join(productPath)
        constructPath = productPath.split("/")
        constructPath.pop(-1)
        constructPath = "/".join(constructPath)
        masterPath = constructPath + "/master"
        masterPathData = masterPath + "/versioninfo.json"

        # Move the current master files back into the version folder to avoid losing them
        if os.path.exists(masterPathData) and len(os.listdir(masterPath))>5:
            with open(masterPathData, 'r') as file:
                context = json.load(file)
            oldVersion = context.get("version")

            if oldVersion in os.listdir(constructPath):
                versionFolder = os.path.join(constructPath, oldVersion)
                
                if not os.path.exists(versionFolder):
                    os.makedirs(versionFolder)
                
                for f in os.listdir(masterPath):
                    if f != "versioninfo.json":
                        shutil.move(os.path.join(masterPath, f), os.path.join(versionFolder, f))

        #call the original function
        result = self.core.plugins.callUnpatchedFunction(self.core.products.updateMasterVersion, path, *args, **kwargs)

        #post-hook code can go here
        #remove the file in the version folder that is now in master to avoid double files
        if os.path.exists(productPath) and len(os.listdir(masterPath))>5:
            for f in os.listdir(masterPath):
                if f != "versioninfo.json" and f in os.listdir(productPath):
                    os.remove(os.path.join(productPath, f))

        return result

    def fix_master_filename(self, path):
        folder = os.path.dirname(path)
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

        correct_name = list(set(correct_files) - set(files))


        if not correct_name:
            print("[FixMasterName] No differing files found between master and version folder.")
            return

        for f in files:
            if "master." in f:
                old_path = os.path.join(folder, f)
                new_path = os.path.join(folder, correct_name[0])
                print(f"[FixMasterName] Renaming {old_path} → {new_path}")
                try:
                    os.rename(old_path, new_path)
                except:
                    print("[FixMasterName] There was a .tex still in the version folder")
                    missingTex = os.listdir(version_folder)
                    for tex in missingTex:
                        if "versioninfo.json" not in tex:
                            shutil.move(version_folder+os.sep+tex, folder+os.sep+tex)
                            print(f"[FixMasterName] moving {version_folder+os.sep+tex} to {folder+os.sep+tex}")

