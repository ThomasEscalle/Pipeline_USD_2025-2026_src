import maya.standalone
maya.standalone.initialize(name='python')

import maya.cmds as cmds
import os

assetName = "ASSET_NAME"
outputPath = "OUTPUT_PATH"
typeAsset = "TYPE_ASSET"
importReference = "IMPORT_REFERENCE"
importReferencePath = "REFERENCE_PATH"

# Hierarchy de groupes :
# - char_chaise_rigl_grp
#     - char_chaise_rigl_geo
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

    # Importe la référence si elle existe
    if importReference == "True":
        cmds.file(importReferencePath, reference=True, namespace="MOD_LOW")
        # Create a layer and add the objects to the layer

    # Crée les groupes standards
    group_name = typeAsset + "_" + assetName + "_rigl_grp"
    grp = cmds.group(empty=True, name=group_name)

    # Crées les groupes standards
    grp_geo = cmds.group(empty=True, name=typeAsset + "_" + assetName + "_rigl_geo")
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


    # Ajoute la nomenclature au groupe
    cmds.addAttr(grp, longName="notes", dataType="string")
    nomenclature = "Cette scène sert de base pour le rigging low.\n"
    nomenclature += "------------------------------------------\n"
    nomenclature += "    Nomenclature :\n"
    nomenclature += "Pour les groupes : " + typeAsset + "_" + assetName +"_<nomDuGroupe>_grp\n"
    nomenclature += "Pour les meshes : " + typeAsset + "_" + assetName +"_<nomDuMesh>_geo\n"
    cmds.setAttr(grp + ".notes", nomenclature, type="string")



    # Set the outliner color of the root group to blue
    cmds.setAttr(grp + ".useOutlinerColor", 1)
    cmds.setAttr(grp + ".outlinerColor", 0, 0.847, 0.813, type="double3")

    cmds.file(rename=outputPath)
    cmds.file(save=True, type='mayaAscii')

build_template()