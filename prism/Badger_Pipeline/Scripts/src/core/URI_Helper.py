# Class that helps to create and manipulate URIs

import os
import re
import logging
from os.path import normpath

# Logger configuration
LOG = logging.getLogger(__name__)


# Class that helps to create and manipulate URIs
class URI_Helper:

    @staticmethod
    def createFromPath(path: str, latest_version: bool = True) -> str:
        """
        Convertit un chemin absolu d'asset ou de shot en URI logique compatible avec le resolver.
        Exemple :
            D:/Projects/Uptight/03_Production/01_Assets/Chars/Michel/Export/USD_Asset/asset.usda
            -> bp://Uptight?type=Chars&name=Michel&product=USD_Asset&version=latest
        """

        if not path or not os.path.exists(path):
            print(f"URI_Helper.createFromPath: Invalid path -> {path}")
            return path.replace("\\", "/")

        path = normpath(path)
        path = path.replace("\\", "/")

        # Découpe le chemin en segments
        parts = path.split("/")
        if len(parts) < 3:
            print(f"URI_Helper.createFromPath: Path too short -> {path}")
            return path

        # Recherche du projet (on suppose qu’il se trouve après un dossier Projects/)
        project_name = ""
        try:
            idx = next(i for i, p in enumerate(parts) if p.lower() == "projects")
            project_name = parts[idx + 1]
        except StopIteration:
            # Si on ne trouve pas "Projects", on prend le 2ème dossier comme fallback
            project_name = parts[1] if len(parts) > 1 else "UnknownProject"

        # Détecte si c’est un Asset ou un Shot
        type_param = ""
        name_param = ""
        product_param = ""
        version_param = ""

        if "01_Assets" in parts:
            type_index = parts.index("01_Assets") + 1
            if len(parts) > type_index:
                type_param = parts[type_index]
            if len(parts) > type_index + 1:
                name_param = parts[type_index + 1]

        elif "02_Shots" in parts:
            type_param = "Shot"
            try:
                seq_index = parts.index("02_Shots") + 1
                seq_param = parts[seq_index]
                shot_param = parts[seq_index + 1] if len(parts) > seq_index + 1 else "Master"
                name_param = f"{seq_param}/{shot_param}"
            except Exception:
                name_param = "UnknownShot"

        # Produit
        if "Export" in parts:
            export_index = parts.index("Export")
            if len(parts) > export_index + 1:
                product_param = parts[export_index + 1]

        # Version
        version_dirs = [p for p in parts if re.match(r"^v\\d+$", p.lower())]
        version_param = version_dirs[-1] if version_dirs else "latest" if latest_version else ""

        # Construit l’URI
        uri = f"bp://{project_name}?type={type_param}&name={name_param}"

        if product_param:
            uri += f"&product={product_param}"
        if version_param:
            uri += f"&version={version_param}"

        return uri

