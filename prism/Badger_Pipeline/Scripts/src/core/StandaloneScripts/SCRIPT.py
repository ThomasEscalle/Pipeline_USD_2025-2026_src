import maya.standalone
maya.standalone.initialize(name='python')

import maya.cmds as cmds
import os

assetName = "Albane"    # <-- Name of the asset, string to be set by the user
outputPath = "C:/Users/Thomas/OneDrive/Bureau/Pipeline 2025/Pipeline_USD_2025-2026_src/prism/Badger_Pipeline/Scripts/src/core/FileTemplates/output.ma"  # <-- Path where to save the scene
assetType = "Chars"    # <-- Type of the asset, string to be set by the user, e.g. "character", "prop", etc.

numberOfGroups = "01" # <-- Number of output groups to create


def build_template():
    cmds.file(new=True, force=True)
    
    # Parse the number of output groups as an integer
    numberOfGroupsInt = int(numberOfGroups)



    if numberOfGroupsInt == 1:
        # Crée les groupes standards
        group_name = assetType + "_" + assetName + "_modl_grp"
        grp = cmds.group(empty=True, name=group_name)

        # Set the outliner color of the root group to blue
        cmds.setAttr(grp + ".useOutlinerColor", 1)
        cmds.setAttr(grp + ".outlinerColor", 0, 0.847, 0.813, type="double3")

    else :
        for i in range(numberOfGroupsInt):
            group_name = assetType + "_" + assetName + "_variant_" +  str(i + 1) + "_modl_grp"
            grp = cmds.group(empty=True, name=group_name)

            # Set the outliner color of the root group to blue
            cmds.setAttr(grp + ".useOutlinerColor", 1)
            cmds.setAttr(grp + ".outlinerColor", 0, 0.847, 0.813, type="double3")

    cmds.file(rename=outputPath)
    cmds.file(save=True, type='mayaAscii')

build_template()