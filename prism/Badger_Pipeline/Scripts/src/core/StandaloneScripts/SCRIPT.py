import maya.standalone
maya.standalone.initialize(name='python')

import maya.api.OpenMaya as om2
import maya.cmds as cmds
import random
import os

<<<<<<< HEAD
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
=======
# Lookdev scene script

output_hip_path = "C:/Program Files/Prism2/Plugins/Custom/Badger_Pipeline/Scripts/src/core/FileTemplates/output.hip"      # <-- Path where to save the scene

assetName = "Asset"             # <-- Name of the asset, string to be set by the user
assetType = "Chars"             # <-- Type of the asset, string to be set by the user, e.g. "character", "prop", etc.
taskName = "Surfacing"               # <-- Name of the task, string to be set by the user, e.g. "Modeling", "Rigging_v012", etc.
departmentName = "Surf"   # <-- Name of the department, string to be set by the user, e.g. "ModL", "ModH", etc.

variantsShareSameMaterials = "False"  # <-- If the variants share the same materials, string set to "True", otherwise "False"
creationMethod = "Modeling high first"   # <-- Method to use for creating, can be "Modeling high first" or "Number of variant first"
numberOfGroups = "01"  # <-- Number of output groups. Only used if creationMethod is "Number of variant first"

referencePath = "['//gandalf/3d3/FFE/04_Uptight/09_Dev/Project/ProjectTest/03_Production/01_Assets/Chars/Asset/Export/ModH_Publish_var001/master/Asset_ModH_Publish_var001_master.usd', '//gandalf/3d3/FFE/04_Uptight/09_Dev/Project/ProjectTest/03_Production/01_Assets/Chars/Asset/Export/ModH_Publish_var002/master/Asset_ModH_Publish_var002_master.usd']"       # <-- Path to the reference file if importReference is "True". It is a string.
importReference = "True"   # <-- If we want to import the reference, string set to "True", otherwise "False"

>>>>>>> 7d00a3614ea11d2b6998262d369daf216a0d9759


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


# Convert the importReferencePaths string to a list
importReferencePathsArray = eval(referencePath) if importReference == "True" else []

<<<<<<< HEAD

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
=======
# Convert the number of groups to integer
numberOfGroupsInt = int(numberOfGroups)

# If the creation method is "Modeling high first", set the number of groups to the number of import reference paths
if creationMethod == "Modeling high first":
    numberOfGroupsInt = len(importReferencePathsArray)
    if numberOfGroupsInt == 0:
        creationMethod = "Number of variant first"
        numberOfGroupsInt = int(numberOfGroups)

numberOfGroupsIntSaved = numberOfGroupsInt
if variantsShareSameMaterials == "True":
    numberOfGroupsInt = 1


# Create a node for each group
for i in range(numberOfGroupsInt):

    reference_index = i

    # Create a pagging for the created nodes. 
    # _<index> with 3 digits if numberOfGroupsInt > 1, otherwise no suffix
    nodes_suffix = f"_var{i+1:03d}" if numberOfGroupsInt > 1 else ""
>>>>>>> 7d00a3614ea11d2b6998262d369daf216a0d9759

    # If there is more than one group, create a subnet for each group
    # Set the parent node to the subnet if there is more than one group, otherwise set it to the stage
    parent_node = stage
    if numberOfGroupsInt > 1:
        group_subnet = stage.createNode("subnet", f"Surf{nodes_suffix}")
        group_subnet.setColor(hou.Color(0.157, 0.627, 0.776))
        group_subnet.setPosition(hou.Vector2(i * 3, 0))
        parent_node = group_subnet

        output_node_of_group = group_subnet.node("output0")
        if output_node_of_group:
            output_node_of_group.destroy()
    
<<<<<<< HEAD


    ####################################################################
    ####################################################################
    ####    I M P O R T    D U    S E T     D R E S S       USD  #######
    ####################################################################
    ####################################################################
=======
>>>>>>> 7d00a3614ea11d2b6998262d369daf216a0d9759

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
    

<<<<<<< HEAD
    ####################################################################
    ####################################################################
    ####################################################################
=======

    ###############################################
    #### Create the nodes in the Stage context ####
    ###############################################


    # If we share the same materials, we create one subnet import for each group
    import_subnet_position = hou.Vector2(0, 0)
    import_subnet_suffix = ""
    number_of_import_subnets = numberOfGroupsIntSaved if variantsShareSameMaterials == "True" else 1

    if variantsShareSameMaterials == "True":
        # Create a "switch" node to switch between the import subnets
        switch_import_node = parent_node.createNode("switch", "Switch_Import")
        switch_import_node.setColor(hou.Color(0.157, 0.627, 0.776)) # Cyan
        switch_import_node.setPosition(hou.Vector2(0, 0))


    # Iterate over the number of import subnets to create
    # If variants share same materials, we create one import subnet per group
    # Otherwise, we create only one import subnet
    for j in range(number_of_import_subnets):


        if variantsShareSameMaterials == "True":
            import_subnet_suffix = f"_var{j+1:03d}"
            import_subnet_position = hou.Vector2(j * 3, 3)
            reference_index = j

        # Create an "Import Subnet"
        import_subnet = parent_node.createNode("subnet", "Import" + import_subnet_suffix)
        import_subnet.setColor(hou.Color(0.776, 0.776, 0.157)) # Yellow
        import_subnet.setPosition(import_subnet_position)

        

        # Build the nodes inside the import subnet
        def build_import_subnet():
            # Get the ouput0 node of the import subnet
            output0 = import_subnet.node("output0")
            # Get the input0 node of the import subnet
            inputs = import_subnet.indirectInputs()
            input_stage = inputs[0] if inputs else None

            # Create a "Null" node called "IN_IMPORT"
            in_import = import_subnet.createNode("null", "IN_IMPORT")
            in_import.setPosition(hou.Vector2(0, 0))

            # Create a "Reference" node called "Reference"
            reference = import_subnet.createNode("reference::2.0", "Object_Reference")
            reference.setPosition(hou.Vector2(0, -1))
            reference.setColor(hou.Color(0.273, 0.627, 0.278)) # Green
            if importReference == "True" and creationMethod == "Modeling high first" :
                reference.setParms(
                    {
                        "filepath1": importReferencePathsArray[reference_index],
                        "primpath1": f"/{assetName}/geo/render"
                    }
                )
                import_subnet.setComment(f"Importing reference: {importReferencePathsArray[reference_index]}")
                import_subnet.setGenericFlag(hou.nodeFlag.DisplayComment,True)
            else:
                reference.setParms(
                    {
                        "filepath1": "", 
                        "primpath1": ""
                    }
                )

            # Create a Transform node called Transform_cm_to_m
            transform_cm_to_m = import_subnet.createNode("xform", "Transform_cm_to_m")
            transform_cm_to_m.setPosition(reference.position() + hou.Vector2(0, -1))
            transform_cm_to_m.parm("sx").set(0.01)  # Scale X to convert from cm to m
            transform_cm_to_m.parm("sy").set(0.01)  # Scale Y to convert from cm to m
            transform_cm_to_m.parm("sz").set(0.01)  # Scale Z to convert from cm to m
            transform_cm_to_m.parm("primpattern").set(f"/{assetName}")  # Apply to all children of the reference

            # Create a "mesh" node called "Mesh_edit"
            mesh_edit = import_subnet.createNode("mesh", "Mesh_edit")
            mesh_edit.setPosition(transform_cm_to_m.position() + hou.Vector2(0, -1))
            mesh_edit.parm("createprims").set(0)
            mesh_edit.parm("primpattern").set("%type:Boundable")  # Apply to all the geometries
            mesh_edit.parm("subdivisionScheme_control").set("set")
            mesh_edit.parm("subdivisionScheme").set("catmullClark")  # Set subdivision scheme to Catmull-Clark

            # Create a "layerbreak" node called "LayerBreak"
            layerbreak = import_subnet.createNode("layerbreak", "LayerBreak")
            layerbreak.setPosition(mesh_edit.position() + hou.Vector2(0, -1))

            # Create a "Null" node called "OUT_IMPORT"
            out_import = import_subnet.createNode("null", "OUT_IMPORT")
            out_import.setPosition(layerbreak.position() + hou.Vector2(0, -1))

            


            # Place the input and output nodes
            input_stage.setPosition(hou.Vector2(0, 1))
            output0.setPosition(out_import.position() + hou.Vector2(0, -1))

            ####################################
            #### Connect the nodes together ####
            ####################################

            # Connect the Input stage to the IN_IMPORT node
            in_import.setInput(0, input_stage, 0)
            # Connect the IN_IMPORT node to the Reference node
            reference.setInput(0, in_import, 0)
            # Connect the Reference node to the Transform node
            transform_cm_to_m.setInput(0, reference, 0)
            # Connect the Transform node to the Mesh_edit node
            mesh_edit.setInput(0, transform_cm_to_m, 0)
            # Connect the Transform node to the LayerBreak node
            layerbreak.setInput(0, mesh_edit, 0)
            # Connect the LayerBreak node to the OUT_IMPORT node
            out_import.setInput(0, layerbreak, 0)
            # Connect the OUT_IMPORT node to the output0 node
            output0.setInput(0, out_import, 0)

        build_import_subnet()

        if variantsShareSameMaterials == "True":
            # Connect the import subnet to the switch node
            switch_import_node.setInput(j, import_subnet, 0)
>>>>>>> 7d00a3614ea11d2b6998262d369daf216a0d9759




<<<<<<< HEAD

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
=======
    # Create a "MaterialLibrary" node called "Materials"
    material_library = parent_node.createNode("materiallibrary", "Materials")
    material_library.setColor(hou.Color(0.273, 0.627, 0.278)) # Green
    material_library.setPosition(hou.Vector2(0, -2))
    material_library.setParms({
        "matpathprefix": f"/{assetName}/mtl/"
    })

    # Create a "Assign Material" node called "Assign_Material"
    assign_material = parent_node.createNode("assignmaterial", "Assign_Material")
    assign_material.setColor(hou.Color(0.273, 0.627, 0.278)) # Green
    assign_material.setPosition(material_library.position() + hou.Vector2(0, -2))

    # Create a "SceneCleaning" subnet called "Scene_Cleaning"
    sceneCleaning_subnet = parent_node.createNode("subnet", "Scene_Cleaning")
    sceneCleaning_subnet.setColor(hou.Color(0.776, 0.157, 0.157)) # Red
    sceneCleaning_subnet.setPosition(assign_material.position() + hou.Vector2(0, -2))
    sceneCleaning_subnet.setComment("Ne pas toucher a ce node !")
    sceneCleaning_subnet.setGenericFlag(hou.nodeFlag.DisplayComment,True)

    # Create a null "OUT_SCENE_LOOKDEV" node
    out_scene_lookdev = parent_node.createNode("null", "OUT_SCENE_LOOKDEV")
    out_scene_lookdev.setPosition(sceneCleaning_subnet.position() + hou.Vector2(0, -2))

    def build_lookdev_scene():

        pass
    build_lookdev_scene()


    # Create a "Export" node
    export_node = parent_node.createNode("Thomas::BP_Export::1.0", "Publish")
    export_node.setColor(hou.Color(0.776, 0.776, 0.157))  # Yellow
    export_node.setPosition(out_scene_lookdev.position() + hou.Vector2(0, -2))
    export_node.parm("productName").set("Surf_Publish")
    if numberOfGroupsInt > 1:
        export_node.parm("productName").set(f"Surf_Publish{nodes_suffix}")
    export_node.parm("nextVersion").set(True)
    export_node.parm("updateMaster").set(True)
    export_node.parm("defaultprim").set(f"/{assetName}")
    export_node.setComment("Publier le surf lookdev")
    export_node.setGenericFlag(hou.nodeFlag.DisplayComment,True)


    # Create a "LOOKDEV_SCENE" subnet
    lookdev_scene = parent_node.createNode("subnet", "LOOKDEV_SCENE")
    lookdev_scene.setColor(hou.Color(0.776, 0.776, 0.157))  # Cyan
    lookdev_scene.setPosition(out_scene_lookdev.position() + hou.Vector2(-4, -2))



    #####################################
    #### Connect the nodes together #####
    #####################################
    
    # Materials -> Import
    if variantsShareSameMaterials == "True":
        import_subnet = switch_import_node
    material_library.setInput(0, import_subnet, 0)
    # Assign_Material -> Materials
    assign_material.setInput(0, material_library, 0)
    # SceneCleaning -> Assign_Material
    sceneCleaning_subnet.setInput(0, assign_material, 0)
    # OUT_SCENE_LOOKDEV -> SceneCleaning
    out_scene_lookdev.setInput(0, sceneCleaning_subnet, 0)
    # USD_OUTPUT -> OUT_SCENE_LOOKDEV
    export_node.setInput(0, out_scene_lookdev, 0)
    # LOOKDEV_SCENE -> OUT_SCENE_LOOKDEV
    lookdev_scene.setInput(0, out_scene_lookdev, 0)


    # Set the display flag on the "OUT_SCENE_LOOKDEV" node
    out_scene_lookdev.setDisplayFlag(True)
>>>>>>> 7d00a3614ea11d2b6998262d369daf216a0d9759



    cmds.file(rename=outputPath)
    cmds.file(save=True, type='mayaAscii')

build_template()