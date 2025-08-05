import maya.standalone
maya.standalone.initialize(name='python')

import maya.cmds as cmds
import os

assetName = "ASSET_NAME"   # <-- Name of the asset, string to be set by the user
outputPath = "OUTPUT_PATH" # <-- Path where to save the scene
assetType = "TYPE_ASSET"   # <-- Type of the asset, string to be set by the user, e.g. "character", "prop", etc.

importReference = "IMPORT_REFERENCE"   # <-- If we want to import the reference, string set to "True", otherwise "False"               
importReferencePath = "REFERENCE_PATH" # <-- Path to the reference file if importReference is "True"


def build_template():
    cmds.file(new=True, force=True)

    # Make sure the AbcImport plugin is loaded
    if not cmds.pluginInfo("AbcImport", query=True, loaded=True):
        cmds.loadPlugin("AbcImport")
    # Make sure the AbcExport plugin is loaded
    if not cmds.pluginInfo("AbcExport", query=True, loaded=True):
        cmds.loadPlugin("AbcExport")
    

    # Importe la référence si elle existe
    if importReference == "True":
        cmds.file(importReferencePath, reference=True, namespace="MOD_LOW")

    # Crée les groupes standards
    group_name = assetType + "_" + assetName + "_modh_grp"
    grp = cmds.group(empty=True, name=group_name)

    # Set the outliner color of the root group to blue
    cmds.setAttr(grp + ".useOutlinerColor", 1)
    cmds.setAttr(grp + ".outlinerColor", 0, 0.847, 0.813, type="double3")


    cmds.file(rename=outputPath)
    cmds.file(save=True, type='mayaAscii')


build_template()