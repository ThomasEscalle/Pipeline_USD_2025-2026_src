import maya.standalone
maya.standalone.initialize(name='python')

import maya.api.OpenMaya as om2
import maya.cmds as cmds
import random
import os

outputPath = "C:/Program Files/Prism2/Plugins/Custom/Badger_Pipeline/Scripts/src/core/FileTemplates/output.ma"

asset_type = "shot"
sequenceName = "sq010_Master"
task_name = "RLO"
department_name = "rlo"

number_of_frames_str = "150"
first_frame_str = "1001"

set_dress_path = "['C:/Users/3D3/Desktop/Fool/03_Production/02_Shots/sq010/Master/Export/SetD_Publish/master/sq010-Master_SetD_Publish_master.usd']"      # This is a string representation of a list of paths but that should only contain one item
rigs_chars_paths = "['C:/Users/3D3/Desktop/Fool/03_Production/01_Assets/Chars/Alexis/Export/RigL_Publish/master/Alexis_RigL_Publish_master.ma']"  # This is a string representation of a list of paths
rigs_props_paths = "[]"  # This is a string representation of a list of paths

create_bookmarks = "True"  # "True" or "False"


camera_rig_path = "C:/Users/3D3/Desktop/Fool/00_Pipeline/Templates/camera_template.ma"
import_camera_rig = "True"  # "True" or "False"
auto_hide_cameras = "True"  # "True" or "False"

# shots_str looks something like this : "[{'sequence': 'sq_010', 'shot': 'sh_010', 'path': 'E:\\3D\\Projects\\06_Ouyang\\03_Production\\02_Shots\\sq_010\\sh_010', 'location': 'global', 'type': 'shot', 'paths': [{'location': 'global', 'path': 'E:\\3D\\Projects\\06_Ouyang\\03_Production\\02_Shots\\sq_010\\sh_010'}], 'range': [1001, 1100], 'length': 100, 'metadata': {}}, {'sequence': 'sq_010', 'shot': 'sh_020', 'path': 'E:\\3D\\Projects\\06_Ouyang\\03_Production\\02_Shots\\sq_010\\sh_020', 'location': 'global', 'type': 'shot', 'paths': [{'location': 'global', 'path': 'E:\\3D\\Projects\\06_Ouyang\\03_Production\\02_Shots\\sq_010\\sh_020'}], 'range': [1001, 1080], 'length': 80, 'metadata': {'preroll': {'value': '50', 'show': True}, 'postroll': {'value': '50', 'show': True}}}]" 
shots_str = "[{'shot': 'sh010', 'path': 'C://Users//3D3//Desktop//Fool//03_Production//02_Shots//sq010//sh010', 'sequence': 'sq010', 'location': 'global', 'type': 'shot', 'paths': [{'location': 'global', 'path': 'C://Users//3D3//Desktop//Fool//03_Production//02_Shots//sq010//sh010'}], 'range': [1001, 1100], 'length': 100, 'metadata': {}}, {'shot': 'sh020', 'path': 'C://Users//3D3//Desktop//Fool//03_Production//02_Shots//sq010//sh020', 'sequence': 'sq010', 'location': 'global', 'type': 'shot', 'paths': [{'location': 'global', 'path': 'C://Users//3D3//Desktop//Fool//03_Production//02_Shots//sq010//sh020'}], 'range': [1001, 1050], 'length': 50, 'metadata': {}}]" 


# Create a bookmark in the timeline
def createBookmark(name, start, stop, color):
    bm = cmds.createNode("timeSliderBookmark")
    cmds.setAttr(bm + ".name", name, type="string")
    cmds.setAttr(bm + ".color", *color)
    cmds.setAttr(bm + ".timeRangeStart", start)
    cmds.setAttr(bm + ".timeRangeStop", stop)
    return bm

# Get a random color from a predefined list
def getRandomColor():
   colors = [
      "#F9BFCB",
      "#DD1E3F",
      "#ED1E24",
      "#FCE3DF",
      "#F57F73",
      "#F47D52",
      "#F14924",
      "#D36A28",
      "#AAAAAA",
      "#FFA419",
      "#E4BD20",
      "#FAF9E5",
      "#F7EC14",
      "#9AC93B",
      "#91C73E",
      "#69BD44",
      "#10813F",
      "#71C16A",
      "#99D4C0",
      "#63C6C1",
      "#DEF2F3",
      "#6FCCDD",
      "#D9D7EC",
      "#3853A4",
      "#7651A1",
      "#80469B",
      "#D4A2C8" ,
      "#B9539F",
      "#7D277E",
      "#D1B48C",
   ]
   color = random.choice(colors)
   color_tuple = (int(color[1:3], 16) / 255, int(color[3:5], 16) / 255, int(color[5:7], 16) / 255)
   return color_tuple


# Set the color of a given object
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


# Check if a node is a top level transform (no parent)
def is_top_level_transform(node):
    if not cmds.objectType(node, isType='transform'):
        return False
    parents = cmds.listRelatives(node, parent=True)
    return not parents




# Main function to build the template
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
    
    # Create a ('set_grp') group
    set_grp_name = "Set_grp"
    set_grp = cmds.group(empty=True, name=set_grp_name)
    setColor(set_grp, "#D4D400")  # RGB values for yellow





    # Iterate over all the shots
    current_frame = first_frame
    created_cameras = []
    last_random_color = None
    for shot in shots_in_sequence:
        
        # Range is relative (it always starts at 1001)
        # We want to convert it to absolute range in the timeline
        absolute_start = shot['range'][0] + (current_frame - 1001)
        absolute_stop  = shot['range'][1] + (current_frame - 1001) + 1  # +1 to include the last frame of the shot

        # Create a random color for the bookmark
        random_color = getRandomColor()
        while random_color == last_random_color: # Avoid having the same color as the last one
            random_color = getRandomColor()
        last_random_color = random_color

        if create_bookmarks == "True":
            # Create a bookmark for the shot
            createBookmark(name=shot['shot'], start=absolute_start, stop=absolute_stop, color=random_color)

        if import_camera_rig == "True" and camera_rig_path != "":
            # Import the camera rig
            imported_nodes = cmds.file(camera_rig_path, i=True, returnNewNodes=True)
            if imported_nodes is None:
                imported_nodes = []

            # Parent the top level transform nodes to the cam_grp
            top_level_transforms = [n for n in imported_nodes if is_top_level_transform(n)]
            for node in top_level_transforms:
                # Skip if the node is not a transform
                # Create a parent node with the shot name _grp
                parent_node = cmds.group(empty=True, name="cam_" + shot['shot'] + "_grp")

                # Put the node under the parent node and rename it to shot name + original name
                node = cmds.rename(node, shot['shot'] + "_" + node)
                cmds.parent(node, parent_node)

                if auto_hide_cameras == "True":
                    # Add a key on the visibility of the camera at the start and end of the shot
                    cmds.setAttr(parent_node + ".visibility", 0)
                    cmds.setKeyframe(parent_node, attribute="visibility", time=0, value=0)
                    cmds.setKeyframe(parent_node, attribute="visibility", time=absolute_start, value=1)
                    cmds.setKeyframe(parent_node, attribute="visibility", time=absolute_stop, value=0)
                cmds.parent(parent_node, cam_grp)
                setColor(parent_node, random_color)

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
    # We need to do this in a second time
    for cam in created_cameras:
        cmds.rename(cam['transform'], cam['shot'] + "_cam")

    


    ####################################################################
    ####################################################################
    ####    I M P O R T    D U    S E T     D R E S S       USD  #######
    ####################################################################
    ####################################################################

    # Import the set dress as a usd reference in the usd layer editor
    shape_node = cmds.createNode('mayaUsdProxyShape')
    shape_node = cmds.rename(shape_node, "usd_setDress")
    
    setDress_path_valid = eval(set_dress_path)
    if len(setDress_path_valid) > 0:
        stdPath = setDress_path_valid[0]
        cmds.setAttr('{}.filePath'.format(shape_node), stdPath, type='string')
    
    # Get the transform node of the shape
    transform_node_usd = cmds.listRelatives(shape_node, parent=True)[0]
    cmds.parent(transform_node_usd, set_grp)
    # Scale the set_grp by 100 to convert from meters to centimeters
    cmds.setAttr(set_grp + ".scale", 100, 100, 100)
    

    ####################################################################
    ####################################################################
    ####################################################################





    ###################################################
    ###################################################
    ####    I M P O R T    D E S    R I G S     #######
    ###################################################
    ###################################################

    # Import the characters rigs
    rigs_eval_chars = eval(rigs_chars_paths)
    for rig_path in rigs_eval_chars:
        if os.path.exists(rig_path):

            imported_nodes = cmds.file(rig_path, reference=True, returnNewNodes=True, namespace ="chars")

            if imported_nodes is None:
                imported_nodes = []

            # Parent the top level transform nodes to the characters_grp
            top_level_transforms = [n for n in imported_nodes if is_top_level_transform(n)]
            for node in top_level_transforms:
                cmds.parent(node, characters_grp)

    # Import the props rigs
    rigs_eval_props = eval(rigs_props_paths)
    for rig_path in rigs_eval_props:
        if os.path.exists(rig_path):
            imported_nodes = cmds.file(rig_path, reference=True, returnNewNodes=True, namespace ="props")
            if imported_nodes is None:
                imported_nodes = []

            # Parent the top level transform nodes to the props_grp
            top_level_transforms = [n for n in imported_nodes if is_top_level_transform(n)]
            for node in top_level_transforms:
                cmds.parent(node, props_grp)



    ###################################################



    cmds.file(rename=outputPath)
    cmds.file(save=True, type='mayaAscii')

build_template()