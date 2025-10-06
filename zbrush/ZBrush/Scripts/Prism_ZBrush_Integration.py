import os
import sys
import platform

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

if platform.system() == "Windows":
    if sys.version[0] == "3":
        import winreg as _winreg
    else:
        import _winreg

from PrismUtils.Decorators import err_catcher_plugin as err_catcher


class Prism_ZBrush_Integration(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin

        self.examplePath = str(self.getZBrushPath())

    @err_catcher(name=__name__)
    def getZBrushPath(self, single=True):
        try:
            zPaths = []
            if platform.system() == "Windows":
                key = _winreg.OpenKey(
                    _winreg.HKEY_LOCAL_MACHINE,
                    "SOFTWARE\\Pixologic",
                    0,
                    _winreg.KEY_READ | _winreg.KEY_WOW64_64KEY,
                )
                idx = 0
                while True:
                    try:
                        zVersion = _winreg.EnumKey(key, idx)
                        zKey = _winreg.OpenKey(
                            _winreg.HKEY_LOCAL_MACHINE,
                            "SOFTWARE\\Pixologic\\" + zVersion,
                            0,
                            _winreg.KEY_READ | _winreg.KEY_WOW64_64KEY,
                        )
                        path = _winreg.QueryValueEx(zKey, "Location")[0]
                        path = os.path.normpath(path)
                        zPaths.append(path)
                        idx += 1
                    except:
                        break

                key = _winreg.OpenKey(
                    _winreg.HKEY_LOCAL_MACHINE,
                    "SOFTWARE\\Maxon",
                    0,
                    _winreg.KEY_READ | _winreg.KEY_WOW64_64KEY,
                )
                idx = 0
                while True:
                    try:
                        zVersion = _winreg.EnumKey(key, idx)
                        if "zbrush" not in zVersion.lower():
                            idx += 1
                            continue

                        zKey = _winreg.OpenKey(
                            _winreg.HKEY_LOCAL_MACHINE,
                            "SOFTWARE\\Maxon\\" + zVersion,
                            0,
                            _winreg.KEY_READ | _winreg.KEY_WOW64_64KEY,
                        )
                        path = _winreg.QueryValueEx(zKey, "Location")[0]
                        path = os.path.normpath(path)
                        zPaths.append(path)
                        idx += 1
                    except:
                        break

            if single:
                return zPaths[-1] if zPaths else None
            else:
                return zPaths if zPaths else []
        except:
            return None

    def addIntegration(self, installPath):
        try:
            pluginPath = os.path.join(installPath, "ZStartup", "ZPlugs64")
            if not os.path.exists(pluginPath):
                msg = (
                    "Invalid ZBrush path: %s.\nThe path doesn't exist."
                    % pluginPath
                )
                self.core.popup(msg, "Prism Integration")
                return False

            integrationBase = os.path.join(self.pluginDirectory, "Integration")

            cmds = []
            for file in ["prism_menu.txt", "prism_menu.zsc"]:
                origFile = os.path.join(integrationBase, file)
                targetFile = os.path.join(pluginPath, file)

                if os.path.exists(targetFile):
                    cmd = {"type": "removeFile", "args": [targetFile], "validate": False}
                    cmds.append(cmd)

                cmd = {"type": "copyFile", "args": [origFile, targetFile]}
                cmds.append(cmd)

                _, ext = os.path.splitext(file)
                if ext == ".txt":
                    with open(origFile, "r") as init:
                        initStr = init.read()

                    initStr = initStr.replace("PRISMROOT", "%s" % self.core.prismRoot.replace("\\", "/"))
                    initStr = initStr.replace("PYTHONEXE", "%s" % self.core.getPythonPath(executable="pythonw").replace("\\", "/"))
                    initStr = initStr.replace("PRISMPLUGINROOT", "%s" % self.pluginDirectory.replace("\\", "/"))
                    prefDir = os.path.dirname(self.core.userini)
                    initStr = initStr.replace("PRISMPREFS", "%s" % prefDir)

                    cmd = {"type": "writeToFile", "args": [targetFile, initStr]}
                    cmds.append(cmd)

            version = os.path.basename(installPath).split(" ")[-1].split(".")[0]
            try:
                int(version)
            except:
                version = None

            origHotkeyFile = os.path.join(integrationBase, "StartupHotkeys.TXT")
            dftHotkeyPath = os.path.join(installPath, "ZStartup/HotKeys/StartupHotkeys.TXT")
            if os.path.exists(dftHotkeyPath):
                with open(dftHotkeyPath, "r") as f:
                    dftHotkeys = f.read()
            else:
                dftHotkeys = ""

            foundPrefDir = False
            for prefDir in self.getZPrefDirs():
                if version and prefDir.endswith(version):
                    foundPrefDir = True

                hkdir = os.path.join(prefDir, "ZStartup", "Hotkeys")
                hkfile = os.path.join(hkdir, "StartupHotkeys.TXT")
                if not os.path.exists(hkdir):
                    cmd = {"type": "createFolder", "args": [hkdir]}
                    cmds.append(cmd)

                with open(origHotkeyFile, "r") as f:
                    hotkeyString = f.read()

                hotkeyString = hotkeyString.replace("ZBRUSH_DEFAULT_HOTKEYS", dftHotkeys)

                if os.path.exists(hkfile):
                    with open(hkfile, "r") as f:
                        hkcontent = f.read()
                else:
                    hkcontent = ""

                searchStrings = [["// >>>PrismStart", "// <<<PrismEnd"]]
                cleanHkContent = self.core.integration.removeIntegrationData(content=hkcontent, searchStrings=searchStrings)

                newHkContent = cleanHkContent + hotkeyString
                cmd = {"type": "writeToFile", "args": [hkfile, newHkContent]}
                cmds.append(cmd)

            result = self.core.runFileCommands(cmds)
            if result is True:
                if version and not foundPrefDir:
                    msg = "ZBrush needs to be launched at least once before the Prism integration gets added. It seems like this didn't happen in this case. If you experience problems when using Prism in ZBrush please add the Prism integration to ZBrush again.\n\n(%s)" % installPath
                    self.core.popup(msg)

                return True
            else:
                raise Exception(result)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            msgStr = (
                "Errors occurred during the installation of the ZBrush integration.\nThe installation is possibly incomplete.\n\n%s\n%s\n%s"
                % (str(e), exc_type, exc_tb.tb_lineno)
            )
            msgStr += "\n\nRunning this application as administrator could solve this problem eventually."
            self.core.popup(msgStr, title="Prism Integration")
            return False

    def removeIntegration(self, installPath):
        try:
            cmds = []
            pluginPath = os.path.join(installPath, "ZStartup", "ZPlugs64")
            for file in ["prism_menu.txt", "prism_menu.zsc"]:
                fPath = os.path.join(pluginPath, file)
                if os.path.exists(fPath):
                    cmd = {"type": "removeFile", "args": [fPath], "validate": True}
                    cmds.append(cmd)

            for prefDir in self.getZPrefDirs():
                hkfile = os.path.join(prefDir, "ZStartup", "Hotkeys", "StartupHotkeys.TXT")

                if not os.path.exists(hkfile):
                    continue

                with open(hkfile, "r") as f:
                    hkcontent = f.read()

                searchStrings = [["// >>>PrismStart", "// <<<PrismEnd"]]
                cleanHkContent = self.core.integration.removeIntegrationData(content=hkcontent, searchStrings=searchStrings)
                if cleanHkContent == hkcontent:
                    continue

                if cleanHkContent.replace(" ", "").replace("\n", ""):
                    cmd = {"type": "writeToFile", "args": [hkfile, cleanHkContent]}
                else:
                    cmd = {"type": "removeFile", "args": [hkfile]}

                cmds.append(cmd)

            result = self.core.runFileCommands(cmds)
            if result is True:
                return True
            else:
                raise Exception(result)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            msgStr = (
                "Errors occurred during the removal of the ZBrush integration.\n\n%s\n%s\n%s"
                % (str(e), exc_type, exc_tb.tb_lineno)
            )
            msgStr += "\n\nRunning this application as administrator could solve this problem eventually."
            self.core.popup(msgStr, title="Prism Integration")
            return False

    def updateInstallerUI(self, userFolders, pItem):
        try:
            zItem = QTreeWidgetItem(["ZBrush"])
            zItem.setCheckState(0, Qt.Checked)
            pItem.addChild(zItem)

            zPaths = self.getZBrushPath(single=False) or []
            zCustomItem = QTreeWidgetItem(["Custom"])
            zCustomItem.setToolTip(0, 'e.g. "%s"' % self.examplePath)
            zCustomItem.setToolTip(1, 'e.g. "%s"' % self.examplePath)
            zCustomItem.setText(1, "< doubleclick to browse path >")
            zCustomItem.setCheckState(0, Qt.Unchecked)
            zItem.addChild(zCustomItem)
            zItem.setExpanded(True)

            activeVersion = False
            for zPath in reversed(zPaths):
                zVersion = os.path.basename(zPath).split(" ")[-1]
                zVItem = QTreeWidgetItem([zVersion])
                zItem.addChild(zVItem)

                if os.path.exists(zPath):
                    zVItem.setCheckState(0, Qt.Checked)
                    zVItem.setText(1, zPath)
                    zVItem.setToolTip(0, zPath)
                    zVItem.setText(1, zPath)
                    activeVersion = True
                else:
                    zVItem.setCheckState(0, Qt.Unchecked)
                    zVItem.setFlags(~Qt.ItemIsEnabled)

            if not activeVersion:
                zItem.setCheckState(0, Qt.Unchecked)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            msg = (
                "Errors occurred during the installation.\n The installation is possibly incomplete.\n\n%s\n%s\n%s\n%s"
                % (__file__, str(e), exc_type, exc_tb.tb_lineno),
            )
            self.core.popup(msg, "Prism Installation")
            return False

    def installerExecute(self, zbrushItem, result):
        try:
            zPaths = []
            installLocs = []

            if zbrushItem.checkState(0) != Qt.Checked:
                return installLocs

            for i in range(zbrushItem.childCount()):
                item = zbrushItem.child(i)
                if item.checkState(0) == Qt.Checked and os.path.exists(item.text(1)):
                    zPaths.append(item.text(1))

            for i in zPaths:
                result["ZBrush integration"] = self.core.integration.addIntegration(self.plugin.pluginName, path=i, quiet=True)
                if result["ZBrush integration"]:
                    installLocs.append(i)

            return installLocs
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            msg = (
                "Errors occurred during the installation.\n The installation is possibly incomplete.\n\n%s\n%s\n%s\n%s"
                % (__file__, str(e), exc_type, exc_tb.tb_lineno)
            )
            self.core.popup(msg, "Prism Installation")
            return False
