import maya.standalone
maya.standalone.initialize(name='python')

import maya.cmds as cmds
import os

assetName = "Albane"  # <-- Name of the asset, string to be set by the user
typeAsset = "Chars" # <-- Type of the asset, string to be set by the user, e.g. "character", "prop", etc.
outputPath = "C:/Users/Thomas/OneDrive/Bureau/Pipeline 2025/Pipeline_USD_2025-2026_src/prism/Badger_Pipeline/Scripts/src/core/FileTemplates/output.ma"  # <-- Path where to save the scene

importReference = "True"    # <-- If we want to import the reference, string set to "True", otherwise "False"
importReferencePath = "E:/3D/Projects/06_Ouyang/03_Production/01_Assets/Chars/Albane/Export/ModH_Publish/master/Albane_ModH_Publish_master.usda"  # <-- Path to the reference file if importReference is "True". It is a an array of paths contained into a string. Use eval() before to use it.

importMethod = "Reference"            # <-- Method to use for importing, can be "Reference" or "Import"
doImportNamespace = "False" # <-- Whether to import with namespace or not . Set to "True" or "False"
importNamespace = "MOD_LOW"      # <-- Namespace to use for importing


createRiggingGroups = "True"

# Hierarchy de groupes :
# - char_chaise_righ_grp
#     - char_chaise_righ_geo
#     - GlobalMove_01
#          - Joints_01
#          - CTRLs_01
#          - IKs_01
#     - RelaySystem_01
#     - ExtraNodes_01
#          - ExtraNodes_To_Show_01
#          - ExtraNodes_To_Hide_01

def build_template():
    cmds.file(new=True, force=True)

    # Make sure the AbcImport plugin is loaded
    if not cmds.pluginInfo("AbcImport", query=True, loaded=True):
        cmds.loadPlugin("AbcImport")
    # Make sure the AbcExport plugin is loaded
    if not cmds.pluginInfo("AbcExport", query=True, loaded=True):
        cmds.loadPlugin("AbcExport")
    # Make sure the mayaUsdPlugin plugin is loaded
    if not cmds.pluginInfo("mayaUsdPlugin", query=True, loaded=True):
        cmds.loadPlugin("mayaUsdPlugin")

    # Importe la référence si elle existe
    imported_nodes = []
    if importReference == "True" and importReferencePath and importReferencePath != "[]" and importReferencePath != '""':
        if importMethod == "Reference":
            if doImportNamespace == "True":
                result = cmds.file(importReferencePath, reference=True, namespace=importNamespace, returnNewNodes=True)
            else:
                result = cmds.file(importReferencePath, i=True, returnNewNodes=True)
        else:
            if doImportNamespace == "True":
                result = cmds.file(importReferencePath, i=True, namespace=importNamespace, returnNewNodes=True)
            else:
                result = cmds.file(importReferencePath, i=True, returnNewNodes=True)
        imported_nodes = result if result else []

    # Crée les groupes standards
    group_name = typeAsset + "_" + assetName + "_righ_grp"
    grp = cmds.group(empty=True, name=group_name)

    if createRiggingGroups == "True":
        # Crées les groupes standards
        grp_geo = cmds.group(empty=True, name=typeAsset + "_" + assetName + "_righ_geo")
        grp_globalMove = cmds.group(empty=True, name="GlobalMove_01")
        grp_joints = cmds.group(empty=True, name="Joints_01")
        grp_ctrls = cmds.group(empty=True, name="CTRLs_01")
        grp_IKs = cmds.group(empty=True, name="IKs_01")
        grp_relaySystem = cmds.group(empty=True, name="RelaySystem_01")
        grp_extraNodes = cmds.group(empty=True, name="ExtraNodes_01")
        grp_extraNodesToShow = cmds.group(empty=True, name="ExtraNodes_To_Show_01")
        grp_extraNodesToHide = cmds.group(empty=True, name="ExtraNodes_To_Hide_01")

        # Parent les groupes
        cmds.parent(grp_geo, grp)
        cmds.parent(grp_globalMove, grp)
        cmds.parent(grp_joints, grp_globalMove)
        cmds.parent(grp_ctrls, grp_globalMove)
        cmds.parent(grp_IKs, grp_globalMove)
        cmds.parent(grp_relaySystem, grp)
        cmds.parent(grp_extraNodes, grp)
        cmds.parent(grp_extraNodesToShow, grp_extraNodes)
        cmds.parent(grp_extraNodesToHide, grp_extraNodes)

        # Si on a importé une référence, on met les nodes importés dans grp_geo
        if importReference == "True" and imported_nodes:
            # On ne veut reparenter que les transform nodes de top-level
            import maya.api.OpenMaya as om2
            def is_top_level_transform(node):
                if not cmds.objectType(node, isType='transform'):
                    return False
                parents = cmds.listRelatives(node, parent=True)
                return not parents
            top_level_transforms = [n for n in imported_nodes if is_top_level_transform(n)]
            for node in top_level_transforms:
                try:
                    cmds.parent(node, grp_geo)
                except Exception:
                    pass

    # Set the outliner color of the root group to blue
    cmds.setAttr(grp + ".useOutlinerColor", 1)
    cmds.setAttr(grp + ".outlinerColor", 0, 0.847, 0.813, type="double3")

    cmds.file(rename=outputPath)
    cmds.file(save=True, type='mayaAscii')

build_template()