

import os
import winreg
import re

# Search for the mayapy.exe executable for a specific version of Maya
def find_mayapy(version="2024"):
    """
    Tente de trouver le chemin vers mayapy.exe de Maya {version}
    en utilisant le registre Windows et des chemins d'installation standards.
    """
    # 1. Essai via le registre Windows
    try:
        reg_path = fr"SOFTWARE/Autodesk/Maya/{version}/Setup/InstallPath"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
            install_path, _ = winreg.QueryValueEx(key, "MAYA_INSTALL_LOCATION")
            mayapy = os.path.join(install_path, "bin", "mayapy.exe")
            if os.path.exists(mayapy):
                return mayapy
    except FileNotFoundError:
        pass  # Rien trouvé dans le registre

    # 2. Recherche dans les emplacements standards
    possible_locations = [
        fr"C:/Program Files/Autodesk/Maya{version}",
        fr"D:/Program Files/Autodesk/Maya{version}",
        fr"C:/Autodesk/Maya{version}",
        fr"D:/Autodesk/Maya{version}",
        fr"D:/Autodesk/Maya{version}/Maya{version}" # <-  Pour l'idiot qui sait pas installer 
    ]

    for base in possible_locations:
        mayapy = os.path.join(base, "bin", "mayapy.exe")
        mayapy = mayapy.replace("/", "//")  # Normaliser le chemin pour Windows
        print(f"Checking {mayapy}...")
        if os.path.exists(mayapy):
            return mayapy

    return None  # Rien trouvé

# Search for the mayapy.exe executable for Maya 2024
def find_mayapy_2024():
    """
    Find the path to mayapy.exe for Maya 2024.
    """
    return find_mayapy("2024")




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
