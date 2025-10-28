import os
import re
import logging
from os.path import normpath

LOG = logging.getLogger(__name__)

class URI_Helper:

    @staticmethod
    def createFromPath(path: str, latest_version: bool = True) -> str:
        if not path or not os.path.exists(path):
            print(f"URI_Helper.createFromPath: Invalid path -> {path}")
            return path.replace("\\", "/")

        path = normpath(path).replace("\\", "/")
        parts = path.split("/")

        if len(parts) < 3:
            print(f"URI_Helper.createFromPath: Path too short -> {path}")
            return path

        # --- Détection du projet ---
        project_name = "UnknownProject"
        candidates = ["Projects", "03_Production", "01_Assets", "02_Shots"]

        found_idx = None
        for c in candidates:
            if c in parts:
                found_idx = parts.index(c)
                break

        if found_idx is not None and found_idx > 0:
            # On prend le dossier juste avant "03_Production" ou "01_Assets"
            project_name = parts[found_idx - 1]
        elif any(p.lower().startswith("proj") for p in parts):
            # Si un dossier contient "proj" dans son nom, on le prend
            project_name = next((p for p in parts if "proj" in p.lower()), "UnknownProject")

        # --- Détection du type / nom / produit / version ---
        type_param = ""
        name_param = ""
        product_param = ""
        version_param = ""

        if "01_Assets" in parts:
            assets_index = parts.index("01_Assets")
            # On cherche jusqu’à "Export" pour détecter la hiérarchie
            try:
                export_index = parts.index("Export")
            except ValueError:
                export_index = len(parts)
            sub_parts = parts[assets_index + 1:export_index]

            if len(sub_parts) > 0:
                type_param = "/".join(sub_parts[:-1]) if len(sub_parts) > 1 else sub_parts[0]
                name_param = sub_parts[-1]

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

        # Version (v001, v002, etc.)
        version_dirs = [p for p in parts if re.match(r"^v\d+$", p.lower())]
        version_param = version_dirs[-1] if version_dirs else "latest" if latest_version else ""

        # Construit l’URI finale
        uri = f"bp://{project_name}?type={type_param}&name={name_param}"
        if product_param:
            uri += f"&product={product_param}"
        if version_param:
            uri += f"&version={version_param}"

        return uri
