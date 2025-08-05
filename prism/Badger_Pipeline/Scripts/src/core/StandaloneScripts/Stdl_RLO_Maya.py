import maya.standalone
maya.standalone.initialize(name='python')

import maya.cmds as cmds
import os

assetName = "$$ASSET_NAME$$"
outputPath = "$$OUTPUT_PATH$$"
sequenceName = "$$SEQUENCE_NAME$$"

rig_paths_props = $$RIG_PATHS_PROPS$$
rig_paths_chars = $$RIG_PATHS_CHARS$$

set_dress_path = "$$SET_DRESS_PATH$$"

shots = $$SHOTS$$

def build_template():
    cmds.file(new=True, force=True)

    # Make sure the AbcImport plugin is loaded
    if not cmds.pluginInfo("AbcImport", query=True, loaded=True):
        cmds.loadPlugin("AbcImport")
    # Make sure the AbcExport plugin is loaded
    if not cmds.pluginInfo("AbcExport", query=True, loaded=True):
        cmds.loadPlugin("AbcExport")
    # Make sure the MayaUSD plugin is loaded
    if not cmds.pluginInfo("mayaUsdPlugin", query=True, loaded=True):
        cmds.loadPlugin("mayaUsdPlugin")

    # Create a 'cameras_grp' group
    camera_grp_name = "cameras_grp"
    cam_grp = cmds.group(empty=True, name=camera_grp_name)
    cmds.setAttr(cam_grp + ".useOutlinerColor", 1)
    cmds.setAttr(cam_grp + ".outlinerColor", 0.0, 0.762,0.719)  # RGB values for teal

    # For each shot, create a camera and place it in the cameras group
    for shot in shots:
        # TODO : Mettre le rig de cam au lieu d'une cam basique
        camera_name = f"camera_{sequenceName}_{shot}"
        camera_name = camera_name.replace("_sh_", "_sht_") 
        camera_name = camera_name.replace("_sq_", "_seq_")
        camera = cmds.camera(name=camera_name)[0]
        camera = cmds.rename(camera, camera_name)
        cmds.parent(camera, cam_grp)

    # Create a ('assets_grp') group
    assets_grp_name = "assets_grp"
    assets_grp = cmds.group(empty=True, name=assets_grp_name)
    cmds.setAttr(assets_grp + ".useOutlinerColor", 1)
    cmds.setAttr(assets_grp + ".outlinerColor", 0.0, 0.762,0.591)  # RGB values for green

    # Create a ('props_grp') group inside the assets group
    props_grp_name = "props_grp"
    props_grp = cmds.group(empty=True, name=props_grp_name, parent=assets_grp)

    # For each prop path, import the reference and place it in the props group
    for rig_path in rig_paths_props:
        if os.path.exists(rig_path):
            nodes = cmds.file(
                rig_path, 
                reference=True, 
                namespace="RIG",
                returnNewNodes=True
                )
            top_groups = [n for n in nodes if cmds.objectType(n) == "transform" and not cmds.listRelatives(n, parent=True)]
            if top_groups:
                for group in top_groups:
                    cmds.parent(group, props_grp)

        else:
            print(f"Rig path does not exist: {rig_path}")




    # Create a ('characters_grp') group inside the assets group
    characters_grp_name = "characters_grp"
    characters_grp = cmds.group(empty=True, name=characters_grp_name, parent=assets_grp)

    # For each character path, import the reference and place it in the characters group
    for rig_path in rig_paths_chars:
        if os.path.exists(rig_path):
            nodes = cmds.file(
                rig_path, 
                reference=True,
                namespace="RIG",
                returnNewNodes=True
                )
            top_groups = [n for n in nodes if cmds.objectType(n) == "transform" and not cmds.listRelatives(n, parent=True)]
            if top_groups:
                for group in top_groups:
                    cmds.parent(group, characters_grp)
        else:
            print(f"Rig path does not exist: {rig_path}")



    # Import the set dress as a usd reference in the usd layer editor
    shape_node = cmds.createNode('mayaUsdProxyShape')
    shape_node = cmds.rename(shape_node, "usd_setDress")
    cmds.setAttr('{}.filePath'.format(shape_node), set_dress_path, type='string')
    cmds.setAttr(shape_node + ".useOutlinerColor", 1)
    cmds.setAttr(shape_node + ".outlinerColor", 0.8,0.75,0.9)  # RGB values for yellow
    # cmds.parent(shape_node, scene_grp)

    cmds.file(rename=outputPath)
    cmds.file(save=True, type='mayaAscii')

build_template()