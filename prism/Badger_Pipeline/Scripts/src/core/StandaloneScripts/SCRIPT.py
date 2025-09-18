import maya.standalone
maya.standalone.initialize(name='python')

import maya.api.OpenMaya as om2
import maya.cmds as cmds
import random
import os

outputPath = "C:/Users/Thomas/OneDrive/Bureau/Pipeline 2025/Pipeline_USD_2025-2026_src/prism/Badger_Pipeline/Scripts/src/core/FileTemplates/output.ma"

asset_type = "shot"
sequenceName = "sq_010_Master"
task_name = "RLO"
department_name = "rlo"

number_of_frames_str = "15"
first_frame_str = "1001"

set_dress_path = "E:/3D/Projects/06_Ouyang/03_Production/02_Shots/sq_010/Master/Export/SetD_Publish/master/sq_010-Master_SetD_Publish_master.usd"

camera_rig_path = "E:/3D/Projects/06_Ouyang/00_Pipeline/Templates/camera_template.ma"
import_camera_rig = "True"  # "True" or "False"

# shots_str = "[{'sequence': 'sq_010', 'shot': 'sh_010', 'path': 'E:\\3D\\Projects\\06_Ouyang\\03_Production\\02_Shots\\sq_010\\sh_010', 'location': 'global', 'type': 'shot', 'paths': [{'location': 'global', 'path': 'E:\\3D\\Projects\\06_Ouyang\\03_Production\\02_Shots\\sq_010\\sh_010'}], 'range': [1001, 1100], 'length': 100, 'metadata': {}}, {'sequence': 'sq_010', 'shot': 'sh_020', 'path': 'E:\\3D\\Projects\\06_Ouyang\\03_Production\\02_Shots\\sq_010\\sh_020', 'location': 'global', 'type': 'shot', 'paths': [{'location': 'global', 'path': 'E:\\3D\\Projects\\06_Ouyang\\03_Production\\02_Shots\\sq_010\\sh_020'}], 'range': [1001, 1080], 'length': 80, 'metadata': {'preroll': {'value': '50', 'show': True}, 'postroll': {'value': '50', 'show': True}}}]" 
shots_str = "[{'sequence': 'sq_010', 'shot': 'sh_010', 'path': 'E:\\3D\\Projects\\06_Ouyang\\03_Production\\02_Shots\\sq_010\\sh_010', 'location': 'global', 'type': 'shot', 'paths': [{'location': 'global', 'path': 'E:\\3D\\Projects\\06_Ouyang\\03_Production\\02_Shots\\sq_010\\sh_010'}], 'range': [1001, 1005], 'length': 5, 'metadata': {}}, {'sequence': 'sq_010', 'shot': 'sh_020', 'path': 'E:\\3D\\Projects\\06_Ouyang\\03_Production\\02_Shots\\sq_010\\sh_020', 'location': 'global', 'type': 'shot', 'paths': [{'location': 'global', 'path': 'E:\\3D\\Projects\\06_Ouyang\\03_Production\\02_Shots\\sq_010\\sh_020'}], 'range': [1001, 1005], 'length': 5, 'metadata': {'preroll': {'value': '50', 'show': True}, 'postroll': {'value': '50', 'show': True}}}, {'sequence': 'sq_010', 'shot': 'sh_030', 'path': 'E:\\3D\\Projects\\06_Ouyang\\03_Production\\02_Shots\\sq_010\\sh_030', 'location': 'global', 'type': 'shot', 'paths': [{'location': 'global', 'path': 'E:\\3D\\Projects\\06_Ouyang\\03_Production\\02_Shots\\sq_010\\sh_030'}], 'range': [1001, 1005], 'length': 5, 'metadata': {}}]" 


def createBookmark(name, start, stop, color):
    bm = cmds.createNode("timeSliderBookmark")
    cmds.setAttr(bm + ".name", name, type="string")
    cmds.setAttr(bm + ".color", *color)
    cmds.setAttr(bm + ".timeRangeStart", start)
    cmds.setAttr(bm + ".timeRangeStop", stop)
    return bm


def setColor(obj, color ):

    # If the color is a tuple, we convert it to a hex string
    if type(color) == tuple and len(color) == 3:
        r = int(color[0] * 255)
        g = int(color[1] * 255)
        b = int(color[2] * 255)
        color = "#{:02X}{:02X}{:02X}".format(r, g, b)

    # If the color is empty, we return
    if color == "":
        print("Invalid color : " + color)
        return


    # If the color is not valid (size != 7), we return
    if len(color) != 7:
        print("Invalid color : " + color)
        return
    
    # If the object is a list, we iterate over it
    # and call the function recursively
    if type(obj) == list:
        for o in obj:
            setColor(o, color)
        return
    
    # Get the color as RGB
    r = int(color[1:3], 16) / 255
    g = int(color[3:5], 16) / 255
    b = int(color[5:7], 16) / 255

    # Round the values
    r = round(r, 3)
    g = round(g, 3)
    b = round(b, 3)

    # Convert the color to display space
    colorV = [r , g , b]
    colorVdp = cmds.colorManagementConvert(toDisplaySpace=[colorV[0], colorV[1], colorV[2]])


    # Set the color in the viewport
    cmds.setAttr(obj + ".overrideEnabled", 1)
    cmds.setAttr(obj + ".overrideRGBColors", 1)
    cmds.setAttr(obj + ".overrideColorRGB", colorV[0], colorV[1], colorV[2])

    # Color in the outliner
    cmds.setAttr(obj + ".useOutlinerColor", 1)
    cmds.setAttr(obj + ".outlinerColor", colorVdp[0], colorVdp[1], colorVdp[2])


    # Get the shapes of the object
    shapes = cmds.listRelatives(obj, shapes=True)

    # If the object has shapes, we color them
    if shapes is not None:
        for shape in shapes:
            cmds.setAttr(shape + ".overrideEnabled", 1)
            cmds.setAttr(shape + ".overrideRGBColors", 1)
            cmds.setAttr(shape + ".overrideColorRGB", colorV[0], colorV[1], colorV[2])

def is_top_level_transform(node):
    if not cmds.objectType(node, isType='transform'):
        return False
    parents = cmds.listRelatives(node, parent=True)
    return not parents

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
    # Make sure the timeSliderBookmark plugin is loaded
    if not cmds.pluginInfo("timeSliderBookmark", query=True, loaded=True):
        cmds.loadPlugin("timeSliderBookmark")


    # Set the framerange from first_frame to first_frame + number_of_frames - 1
    try:
        first_frame = int(first_frame_str)
        number_of_frames = int(number_of_frames_str)
    except ValueError:
        first_frame = 1001
        number_of_frames = 100
    last_frame = first_frame + number_of_frames - 1

    # Convert the shots string to a list of dictionaries
    shots_in_sequence = eval(shots_str)


    # Set the playback options
    cmds.playbackOptions(min=first_frame, max=last_frame)
    cmds.playbackOptions(animationStartTime=first_frame, animationEndTime=last_frame)
    cmds.currentTime(first_frame)
    


    # Create a 'Cameras_grp' group
    camera_grp_name = "Cameras_grp"
    cam_grp = cmds.group(empty=True, name=camera_grp_name)
    setColor(cam_grp, "#00C2B7")  # RGB values for teal


    # Create a ('assets_grp') group
    assets_grp_name = "Assets_grp"
    assets_grp = cmds.group(empty=True, name=assets_grp_name)
    setColor(assets_grp, "#6B2DBB")  # RGB values for Blue

    # Create a ('props_grp') group inside the assets group
    props_grp_name = "Props_grp"
    props_grp = cmds.group(empty=True, name=props_grp_name, parent=assets_grp)

    # Create a ('characters_grp') group inside the assets group
    characters_grp_name = "Characters_grp"
    characters_grp = cmds.group(empty=True, name=characters_grp_name, parent=assets_grp)
    
    # Create a ('sets_grp') group
    sets_grp_name = "Sets_grp"
    sets_grp = cmds.group(empty=True, name=sets_grp_name)
    setColor(sets_grp, "#D4D400")  # RGB values for yellow

    # Iterate over all the shots
    current_frame = first_frame
    created_cameras = []
    for shot in shots_in_sequence:
        
        # Range is relative (it always starts at 1001)
        # We want to convert it to absolute range in the timeline
        absolute_start = shot['range'][0] + (current_frame - 1001)
        absolute_stop  = shot['range'][1] + (current_frame - 1001) + 1  # +1 to include the last frame of the shot

        # Create a random color for the bookmark
        random_color = (random.random(), random.random(), random.random())
        createBookmark(name=shot['shot'], start=absolute_start, stop=absolute_stop, color=random_color)

        if import_camera_rig == "True" and camera_rig_path != "":
            # Import the camera rig
            imported_nodes = cmds.file(camera_rig_path, i=True, returnNewNodes=True)
            if imported_nodes is None:
                imported_nodes = []

            # Parent the top level transform nodes to the cam_grp
            top_level_transforms = [n for n in imported_nodes if is_top_level_transform(n)]
            for node in top_level_transforms:

                
                # Create a parent node with the shot name _grp
                parent_node = cmds.group(empty=True, name="cam_" + shot['shot'] + "_grp")

                node = cmds.rename(node, shot['shot'] + "_" + node)
                cmds.parent(node, parent_node)

                setColor(parent_node, random_color)
                
                # Add a key on the visibility of the camera at the start and end of the shot
                cmds.parent(parent_node, cam_grp)
                cmds.setAttr(parent_node + ".visibility", 0)
                cmds.setKeyframe(parent_node, attribute="visibility", time=0, value=0)
                cmds.setKeyframe(parent_node, attribute="visibility", time=absolute_start, value=1)
                cmds.setKeyframe(parent_node, attribute="visibility", time=absolute_stop, value=0)

                # Iterate over the children of the node to find the camera and set its color and rename it's transform node
                childrens = cmds.listRelatives(node, allDescendents=True, fullPath=True)
                if childrens is not None:
                    for child in childrens:
                        if cmds.objectType(child) == "camera":
                            # Get the transform no²de of the camera
                            transform = cmds.listRelatives(child, parent=True, fullPath=True)[0]
                            created_cameras.append({"shot": shot['shot'], "transform": transform})

        # Update the bookmark current frame for the next shot
        current_frame += shot['length']

    # Iterate over the created cameras and rename them to shot name + _cam
    for cam in created_cameras:
        cmds.rename(cam['transform'], cam['shot'] + "_cam")

    
    # Import the set dress as a usd reference in the usd layer editor
    shape_node = cmds.createNode('mayaUsdProxyShape')
    shape_node = cmds.rename(shape_node, "usd_setDress")
    cmds.setAttr('{}.filePath'.format(shape_node), set_dress_path, type='string')
    
    # Get the transform node of the shape
    transform_node_usd = cmds.listRelatives(shape_node, parent=True)[0]
    cmds.parent(transform_node_usd, sets_grp)
    # Scale the sets_grp by 100 to convert from meters to centimeters
    cmds.setAttr(sets_grp + ".scale", 100, 100, 100)
    

    cmds.file(rename=outputPath)
    cmds.file(save=True, type='mayaAscii')

build_template()