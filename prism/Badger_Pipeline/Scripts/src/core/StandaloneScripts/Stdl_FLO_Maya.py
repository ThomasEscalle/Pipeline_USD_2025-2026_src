import maya.standalone
maya.standalone.initialize(name='python')

import maya.api.OpenMaya as om2
import maya.cmds as cmds
import random
import os

outputPath = "$$OUTPUT_PATH$$"

asset_type = "$$SEQUENCE_TYPE$$"
sequenceName = "$$ASSET_NAME$$"
task_name = "$$TASK$$"
department_name = "$$DEPARTMENT$$"

shot_range = "$$SHOT_RANGE$$"  # This is a string representation of a list ( start_frame, end_frame)
shot_length = "$$SHOT_LENGTH$$"  # This is an integer
shot_preroll = "$$SHOT_PREROLL$$"  # This is an integer
shot_postroll = "$$SHOT_POSTROLL$$"  # This is an integer



set_dress_path = "$$SET_DRESS_PATH$$"      # This is a string representation of a list of paths but that should only contain one item
save_path_edit_setD = "$$SAVE_PATH_EDIT_SETD$$"  # This is a path to the folder where the EditSetDress.usda should be saved
rigs_chars_paths = "$$RIGS_CHARS_PATHS$$"  # This is a string representation of a list of paths
rigs_props_paths = "$$RIGS_PROPS_PATHS$$"  # This is a string representation of a list of paths

create_bookmarks = "$$CREATE_BOOKMARKS$$"  # "True" or "False"



# Create a bookmark in the timeline
def createBookmark(name, start, stop, color):
    bm = cmds.createNode("timeSliderBookmark")
    cmds.setAttr(bm + ".name", name, type="string")
    cmds.setAttr(bm + ".color", *color)
    cmds.setAttr(bm + ".timeRangeStart", start)
    cmds.setAttr(bm + ".timeRangeStop", stop)
    return bm



def createOverrideLayer(asset_name, asset_path , prim_path):
        """
        Create a Maya USD layer with an override layer, referencing an asset. 
        This is used to non-destructively make edits (or add references to new sub-assets)
        without modifying the original USD layer.
        Args:
            asset_name (str): The name of the asset.
            asset_path (str): The filepath to the USD layer for the asset.
        Returns:
            tuple: The mayaUsdProxyShape node and layer created in it.
        """
        import mayaUsd.ufe as mayaUsdUfe #import this at runtime because otherwise maya crashes on startup

        node = cmds.createNode('mayaUsdProxyShape', name=asset_name)
        node_long = cmds.ls(node, long=True)[0]
        
        stage = mayaUsdUfe.getStage(node_long)

        # Create a new versioned override layer
        override_path = save_path_edit_setD
        
        layer = stage.CreateNew(override_path)
        asset_sdf_path = "/"+asset_name

        # Reference the asset at the root of the override layer
        xform = layer.DefinePrim(asset_sdf_path, 'Xform')
        xform.GetReferences().AddReference(asset_path , primPath = prim_path)
        layer.SetDefaultPrim(layer.GetPrimAtPath(asset_sdf_path))
        layer.GetRootLayer().Save()
        
        cmds.setAttr(node + ".filePath", override_path, type="string")
        cmds.connectAttr("time1.outTime", node + ".time")
        return node, layer



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
    shot_range_eval = eval(shot_range)
    start_frame = shot_range_eval[0]
    number_of_frames = int(shot_length)

    end_frame = int(start_frame) + int(number_of_frames) + int(shot_postroll) - 1
    start_frame = int(start_frame) - int(shot_preroll)

    # Set the playback options
    cmds.playbackOptions(min=start_frame, max=end_frame)
    cmds.playbackOptions(animationStartTime=start_frame, animationEndTime=end_frame)
    cmds.currentTime(start_frame)

    # If create_bookmarks is True, we create a bookmark for the shot's preroll, and postroll
    if create_bookmarks == "True":
        if int(shot_preroll) > 0:
            createBookmark("Preroll", start_frame, start_frame + int(shot_preroll) , (1, 0, 0))
        if int(shot_postroll) > 0:
            createBookmark("Postroll", end_frame - int(shot_postroll) + 1, end_frame +1, (1, 0, 0))


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












    ####################################################################
    ####################################################################
    ####    I M P O R T    D U    S E T     D R E S S       USD  #######
    ####################################################################
    ####################################################################

    # Import the set dress as a usd reference in the usd layer editor
    setDress_path_valid = eval(set_dress_path)
    data = createOverrideLayer("SetDress", setDress_path_valid[0], "/SetDress")

    proxy_shape_node = data[0]
    transform_proxy_node = cmds.listRelatives(proxy_shape_node, parent=True)[0]
    cmds.parent(transform_proxy_node, set_grp)
    setColor(proxy_shape_node, "#D4D400")  # RGB values for yellow
    # Set the scale of the group to 100
    cmds.setAttr(set_grp + ".scaleX", 100)
    cmds.setAttr(set_grp + ".scaleY", 100)
    cmds.setAttr(set_grp + ".scaleZ", 100)


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