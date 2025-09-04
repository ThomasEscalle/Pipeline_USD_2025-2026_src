try: 			
    import maya.standalone 			
    maya.standalone.initialize() 		
except: 			
    pass

import maya.cmds as cmds
import os

assetName = "ASSET_NAME"   # <-- Name of the asset, string to be set by the user
outputPath = "OUTPUT_PATH" # <-- Path where to save the scene
assetType = "TYPE_ASSET"   # <-- Type of the asset, string to be set by the user, e.g. "character", "prop", etc.

importReference = "IMPORT_REFERENCE"    # <-- If we want to import the reference, string set to "True", otherwise "False"               
importReferencePaths = "REFERENCE_PATH" # <-- Path to the reference file if importReference is "True". It is a an array of paths contained into a string. Use eval() before to use it.

importMethod = "IMPORT_METHOD"            # <-- Method to use for importing, can be "Reference" or "Import"
doImportNamespace = "DO_IMPORT_NAMESPACE" # <-- Whether to import with namespace or not . Set to "True" or "False"
importNamespace = "IMPORT_NAMESPACE"      # <-- Namespace to use for importing

numberOfGroups = "NUMBER_OF_GROUPS" # <-- Number of output groups


def build_template():
    cmds.file(new=True, force=True)

    # Make sure the AbcImport plugin is loaded
    if not cmds.pluginInfo("AbcImport", query=True, loaded=True):
        cmds.loadPlugin("AbcImport")
        
    # Make sure the AbcExport plugin is loaded
    if not cmds.pluginInfo("AbcExport", query=True, loaded=True):
        cmds.loadPlugin("AbcExport")

    # Make sure the MayaUSD plugin is loaded
    try:
        if not cmds.pluginInfo("mayaUsdPlugin", query=True, loaded=True):
            cmds.loadPlugin("mayaUsdPlugin")
    except:
        pass

    # Importe la référence si elle existe
    if importReference == "True":
        references = eval(importReferencePaths)

        for reference in references:
            if importMethod == "Reference":
                if doImportNamespace == "True":
                    cmds.file(reference, reference=True, namespace=importNamespace)
                else:
                    cmds.file(reference, i=True)
            else:
                if doImportNamespace == "True":
                    cmds.file(reference, i=True, namespace=importNamespace)
                else:
                    cmds.file(reference, i=True)

    # Parse the number of output groups as an integer
    numberOfGroupsInt = int(numberOfGroups)

    if numberOfGroupsInt == 1:
        # Crée les groupes standards
        group_name = assetType + "_" + assetName + "_modh_grp"
        grp = cmds.group(empty=True, name=group_name)

        # Set the outliner color of the root group to blue
        cmds.setAttr(grp + ".useOutlinerColor", 1)
        cmds.setAttr(grp + ".outlinerColor", 0, 0.847, 0.813, type="double3")

    else :
        for i in range(numberOfGroupsInt):
            group_name = assetType + "_" + assetName + "_variant_" +  str(i + 1) + "_modh_grp"
            grp = cmds.group(empty=True, name=group_name)

            # Set the outliner color of the root group to blue
            cmds.setAttr(grp + ".useOutlinerColor", 1)
            cmds.setAttr(grp + ".outlinerColor", 0, 0.847, 0.813, type="double3")

    cmds.file(rename=outputPath)
    cmds.file(save=True, type='mayaAscii')


build_template()


try: 			
    maya.standalone.uninitialize() 		
except: 			
    pass