import maya.standalone
maya.standalone.initialize(name='python')

import maya.cmds as cmds
import os

assetName = "ASSET_NAME"  # <-- Name of the asset, string to be set by the user
typeAsset = "TYPE_ASSET" # <-- Type of the asset, string to be set by the user, e.g. "character", "prop", etc.
outputPath = "OUTPUT_PATH"  # <-- Path where to save the scene

importReference = "IMPORT_REFERENCE"    # <-- If we want to import the reference, string set to "True", otherwise "False"
importReferencePath = "REFERENCE_PATH"  # <-- Path to the reference file if importReference is "True". It is a an array of paths contained into a string. Use eval() before to use it.

importMethod = "IMPORT_METHOD"            # <-- Method to use for importing, can be "Reference" or "Import"
doImportNamespace = "DO_IMPORT_NAMESPACE" # <-- Whether to import with namespace or not . Set to "True" or "False"
importNamespace = "IMPORT_NAMESPACE"      # <-- Namespace to use for importing


createRiggingGroups = "CREATE_RIGGING_GROUPS"

# Hierarchy de groupes :
# - chaise
#     - Asset_root
#       - geo
#         - render
#            - <Les geos viennent ici, sans leurs groupes parent.. A voir comment gerer les references ?? > 
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
    group_name = assetName
    grp = cmds.group(empty=True, name=group_name)

    if createRiggingGroups == "True":
        # Crées les groupes standards
        grp_asset_root = cmds.group(empty=True, name="Asset_root")
        grp_geo = cmds.group(empty=True, name="geo")
        grp_render = cmds.group(empty=True, name="proxy")  # Proxy because we are in Riggin 'LOW'

        grp_globalMove = cmds.group(empty=True, name="GlobalMove_01")
        grp_joints = cmds.group(empty=True, name="Joints_01")
        grp_ctrls = cmds.group(empty=True, name="CTRLs_01")
        grp_IKs = cmds.group(empty=True, name="IKs_01")
        grp_relaySystem = cmds.group(empty=True, name="RelaySystem_01")
        grp_extraNodes = cmds.group(empty=True, name="ExtraNodes_01")
        grp_extraNodesToShow = cmds.group(empty=True, name="ExtraNodes_To_Show_01")
        grp_extraNodesToHide = cmds.group(empty=True, name="ExtraNodes_To_Hide_01")

        # Parent les groupes
        
        cmds.parent(grp_asset_root, grp)
        cmds.parent(grp_geo, grp_asset_root)
        cmds.parent(grp_render, grp_geo)
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
                    cmds.parent(node, grp_render)
                except Exception:
                    pass

    # Set the outliner color of the root group to blue
    cmds.setAttr(grp + ".useOutlinerColor", 1)
    cmds.setAttr(grp + ".outlinerColor", 0, 0.847, 0.813, type="double3")

    cmds.file(rename=outputPath)
    cmds.file(save=True, type='mayaAscii')

build_template()