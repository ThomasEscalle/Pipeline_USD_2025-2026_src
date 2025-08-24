

import os
import winreg
import re
import sys
import platform
import shutil

if platform.system() == "Windows":
    if sys.version[0] == "3":
        import winreg as _winreg
    else:
        import _winreg


# Search for the mayapy.exe executable for a specific version of Maya
def getMayaPyPath():

    base = getMayaPath()
    if not base:
        return None

    mayapy = os.path.join(base, "bin", "mayapy.exe")
    mayapy = mayapy.replace("/", "//")  # Normaliser le chemin pour Windows

    if os.path.exists(mayapy):
        return mayapy

    return None  # Rien trouvé


def getMayaPath():
    try:
        key = _winreg.OpenKey(
            _winreg.HKEY_LOCAL_MACHINE,
            "SOFTWARE\\Autodesk\\Maya",
            0,
            _winreg.KEY_READ | _winreg.KEY_WOW64_64KEY,
        )

        mayaVersions = []
        try:
            i = 0
            while True:
                mayaVers = _winreg.EnumKey(key, i)
                if sys.version[0] == "2":
                    mayaVers = unicode(mayaVers)
                if mayaVers.isnumeric():
                    mayaVersions.append(mayaVers)
                i += 1

        except WindowsError:
            pass

        validVersion = mayaVersions[-1]

        key = _winreg.OpenKey(
            _winreg.HKEY_LOCAL_MACHINE,
            "SOFTWARE\\Autodesk\\Maya\\%s\\Setup\\InstallPath" % validVersion,
            0,
            _winreg.KEY_READ | _winreg.KEY_WOW64_64KEY,
        )
        installDir = (_winreg.QueryValueEx(key, "MAYA_INSTALL_LOCATION"))[0]
        return installDir
    
    except:
        return ""




def getHoudiniPath():
    versions = {}
    try:
        # Print what is inside the Houdini key
        key = _winreg.OpenKey(
            _winreg.HKEY_LOCAL_MACHINE,
            "SOFTWARE\\Side Effects Software\\Houdini",
            0,
            _winreg.KEY_READ | _winreg.KEY_WOW64_64KEY,
        )
        i = 0
        while True:
            try:
                name, value, _ = _winreg.EnumValue(key, i)
                if name != "LicenseServer":
                    versions[name] = value
                i += 1
            except OSError:
                break

    except:
        print("WARNING : Houdini n'est pas installé ou la clé de registre est manquante.")
        return ""

    # Get the latest version from the versions dictionary
    if versions:
        latest_version = sorted(versions.keys(), key=lambda v: list(map(int, v.split("."))), reverse=True)[0]
        return versions[latest_version]

    return ""


def getHythonPath():
    # Get the path to the hython executable for the latest version of Houdini
    houdini_path = getHoudiniPath()
    if not houdini_path:
        return None

    hython_path = os.path.join(houdini_path, "bin", "hython.exe")
    hython_path = hython_path.replace("/", "//")  # Normaliser le chemin pour Windows

    if os.path.exists(hython_path):
        return hython_path

    return None  # Rien trouvé

# Search for the hython.exe executable for the latest version of Houdini
def find_latest_hython():
    """
    Cherche automatiquement la dernière version de Houdini installée
    et retourne le chemin vers hython.exe si trouvé.
    """
    base_path = r"C:/Program Files/Side Effects Software"
    possible_locations = [
        r"C:/Program Files/Side Effects Software",
        r"D:/Program Files/Side Effects Software",
        r"C:/Side Effects Software",
        r"D:/Side Effects Software",
        r"D:"
    ]

    if not os.path.exists(base_path):
        # Vérifier les emplacements alternatifs
        for loc in possible_locations:
            if os.path.exists(loc):
                base_path = loc
                break
        else:
            print("ERROR : Aucun dossier Side Effects Software trouvé.")
            return None



    try:
        # Trouver les dossiers Houdini avec une version
        houdini_dirs = [
            d for d in os.listdir(base_path)
            if re.match(r"Houdini /d+/./d+/./d+", d)
            and os.path.isdir(os.path.join(base_path, d))
        ]

        # Trier par numéro de version décroissant
        def version_key(name):
            numbers = re.findall(r"/d+", name)
            return tuple(map(int, numbers))  # ex: [20, 0, 547]

        houdini_dirs.sort(key=version_key, reverse=True)

        # Rechercher hython.exe dans les versions triées
        for version_dir in houdini_dirs:
            hython_path = os.path.join(base_path, version_dir, "bin", "hython.exe")
            if os.path.exists(hython_path):
                return hython_path
            
        return "D:/Houdini 20.5.370/bin/hython.exe"

    except Exception as e:
        print("ERROR : Erreur lors de la recherche de hython :", e)

    return None  # Rien trouvé
