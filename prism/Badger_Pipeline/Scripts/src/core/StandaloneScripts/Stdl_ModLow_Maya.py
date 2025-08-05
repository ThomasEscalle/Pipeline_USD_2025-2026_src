import maya.standalone
maya.standalone.initialize(name='python')

import maya.cmds as cmds
import os

assetName = "ASSET_NAME"
outputPath = "OUTPUT_PATH"
typeAsset = "TYPE_ASSET"


def build_template():
    cmds.file(new=True, force=True)
    
    # Crée les groupes standards
    group_name = typeAsset + "_" + assetName + "_modl_grp"
    grp = cmds.group(empty=True, name=group_name)

    # Ajoute la nomenclature au groupe
    cmds.addAttr(grp, longName="notes", dataType="string")
    nomenclature = "Cette scène sert de base pour le modeling low.\n"
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