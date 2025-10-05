import hou
import os




output_hip_path = "$$OUTPUT_PATH$$"

assetName = "$$ASSET_NAME$$"
assetType = "$$TYPE_ASSET$$"
task_name = "$$TASK_NAME$$"
department_name = "$$DEPARTMENT_NAME$$"

shot_start = int("$$SHOT_START$$")
shot_end = int("$$SHOT_END$$")
shot_length = int("$$SHOT_LENGTH$$")
shot_preroll = int("$$SHOT_PREROLL$$")
shot_postroll = int("$$SHOT_POSTROLL$$")

camera_filepath = "$$CAMERA_FILEPATH$$"

set_dress_filepath = "$$SETDRESS_FILEPATH$$"

character_animations_filepaths = "$$CHARACTER_ANIMATIONS_FILEPATH$$"
"""
[
    {
        "hierarchy": "sq010/sh010",
        "itemType": "shot",
        "sequence": "sq010",
        "shot": "sh010",
        "type": "shot",
        "project_path": "C://Users//3D3//Desktop//Uptight",
        "project_name": "Uptight",
        "product": "Anim_Char_Albert_Publish",
        "path": "C://Users//3D3//Desktop//Uptight//03_Production//02_Shots//sq010//sh010//Export//Anim_Char_Albert_Publish",
        "locations": {
            "global": "C://Users//3D3//Desktop//Uptight//03_Production//02_Shots//sq010//sh010//Export//Anim_Char_Albert_Publish"
        },
        "product_file_path": "C:/Users/3D3/Desktop/Uptight/03_Production/02_Shots/sq010/sh010/Export/Anim_Char_Albert_Publish/master/sq010-sh010_Anim_Char_Albert_Publish_master.usd"
    }
]
"""




# Create a new Houdini scene
hou.hipFile.clear(suppress_save_prompt=True)

# Create the Stage node if it doesn't exist
stage = hou.node("/stage")
if stage is None:
    stage = hou.node("/").createNode("lopnet", "stage")



###############################################
#### Create the nodes in the Stage context ####
###############################################

# Create a "Import" subnet
import_subnet = stage.createNode("subnet", "Import")
import_subnet.setColor(hou.Color(0.273, 0.627, 0.278)) # Green
import_subnet.setUserData("nodeshape", "burst")

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


    # Create a Subnet called "SET_DRESS"
    set_dress_subnet = import_subnet.createNode("subnet", "SET_DRESS")
    set_dress_subnet.setColor(hou.Color(0.273, 0.627, 0.278)) # Green
    set_dress_subnet.setPosition(in_import.position() + hou.Vector2(0, -2))
    set_dress_subnet.setComment("Import the Set Dress elements here")

    def build_set_dress_subnet():
        # Get the ouput0 node of the set_dress subnet
        setD_output0 = set_dress_subnet.node("output0")
        # Get the input0 node of the set_dress subnet
        setD_inputs = set_dress_subnet.indirectInputs()
        setD_input_stage = setD_inputs[0] if setD_inputs else None

        # Create a "Null" node called "IN_SET_DRESS"
        in_set_dress = set_dress_subnet.createNode("null", "IN_SET_DRESS")
        in_set_dress.setPosition(hou.Vector2(0, 0))

        # Create a "Reference" node to import the set dress USD
        if set_dress_filepath and os.path.isfile(set_dress_filepath):
            reference_node = set_dress_subnet.createNode("sublayer", "SetDress_Sublayer")
            reference_node.setPosition(in_set_dress.position() + hou.Vector2(0, -2))
            reference_node.parm("filepath1").set(set_dress_filepath.replace("\\", "/"))
            reference_node.setComment(f"Sublayer the Set Dress USD:\n{set_dress_filepath}")
            reference_node.setGenericFlag(hou.nodeFlag.DisplayComment,True)

            # Connect the nodes together
            reference_node.setInput(0, in_set_dress, 0)
            setD_output0.setInput(0, reference_node, 0)
        else:
            # If no valid set dress filepath is provided, connect IN_SET_DRESS directly to output0
            setD_output0.setInput(0, in_set_dress, 0)

        # Place the input and output nodes
        setD_input_stage.setPosition(hou.Vector2(0, 2))
        setD_output0.setPosition(hou.Vector2(0, -4))

        pass

    build_set_dress_subnet()
    



    # Create a Subnet called "CHARACTERS_AND_PROPS"
    characters_and_props_subnet = import_subnet.createNode("subnet", "CHARACTERS_AND_PROPS")
    characters_and_props_subnet.setColor(hou.Color(0.273, 0.627, 0.278)) # Green
    characters_and_props_subnet.setPosition(set_dress_subnet.position() + hou.Vector2(0, -2))
    characters_and_props_subnet.setComment("Import the Characters and Props elements here")

    
    def build_characters_and_props_subnet():
        # Get the ouput0 node of the characters_and_props subnet
        char_output0 = characters_and_props_subnet.node("output0")
        # Get the input0 node of the characters_and_props subnet
        char_inputs = characters_and_props_subnet.indirectInputs()
        char_input_stage = char_inputs[0] if char_inputs else None

        # Create a "Null" node called "IN_CHARACTERS_AND_PROPS"
        in_characters_and_props = characters_and_props_subnet.createNode("null", "IN_CHARACTERS_AND_PROPS")
        in_characters_and_props.setPosition(hou.Vector2(0, 0))

        last_node = None
        first_node = None
        for char_anim in eval(character_animations_filepaths):

            # Create a "sublayer" node to import the character animation USD  # TODO FINISH THIS
            sublayer_node = characters_and_props_subnet.createNode("sublayer", f"{char_anim['shot']}_{char_anim['product']}_Sublayer")
            if last_node is None:
                sublayer_node.setPosition(hou.Vector2(4, 2))
            else:
                sublayer_node.setPosition(last_node.position() + hou.Vector2(4, 2))
            sublayer_node.parm("filepath1").set(char_anim['product_file_path'].replace("\\", "/"))

            sublayer_node.setComment(f"Sublayer the Character Animation USD:\n{char_anim['product_file_path']}")
            sublayer_node.setGenericFlag(hou.nodeFlag.DisplayComment,True)

            if last_node != None:
                sublayer_node.setInput(0, last_node, 0)
            else:
                first_node = sublayer_node

            last_node = sublayer_node

        if first_node is not None:
            # add a graftstages node to merge all the chars imports together
            graftstages_node = characters_and_props_subnet.createNode("graftstages", "Merge_Characters_Animations")
            graftstages_node.setPosition(first_node.position() + hou.Vector2(0, -2))
            graftstages_node.setComment("Merge all the Character Animation USDs together")
            graftstages_node.setGenericFlag(hou.nodeFlag.DisplayComment,True)
            graftstages_node.setInput(1, first_node, 0)
            graftstages_node.parm("destpath").set("/Chars_grp")

            # Add a transfor node to transform from cm to m to apply on all the chars at once
            transform_node = characters_and_props_subnet.createNode("xform", "Transform_cm_to_m")
            transform_node.setPosition(graftstages_node.position() + hou.Vector2(0, -2))
            transform_node.parm("scale").set(0.01)  # Scale down by a factor of 100 (cm to m)
            transform_node.parm("primpattern").set("/Chars_grp")
            transform_node.setInput(0, graftstages_node, 0)

            # Add a merge node to merge the transform node to the in_characters_and_props node
            merge_node = characters_and_props_subnet.createNode("merge", "Merge_Chars_and_Props")
            merge_node.setPosition(transform_node.position() + hou.Vector2(-3, -2))
            merge_node.setInput(0, in_characters_and_props, 0)
            merge_node.setInput(1, transform_node, 0)

        

            # Connect the nodes together
            in_characters_and_props.setInput(0, char_input_stage, 0)
            char_output0.setInput(0, merge_node, 0)

            # Place the input and output nodes
            char_input_stage.setPosition(hou.Vector2(0, 2))
            char_output0.setPosition(merge_node.position() + hou.Vector2(0, -2))
        else:
            # If no valid character animation filepaths are provided, connect IN_CHARACTERS_AND_PROPS directly to output0
            char_output0.setInput(0, in_characters_and_props, 0)
            in_characters_and_props.setInput(0, char_input_stage, 0)

            # Place the input and output nodes
            char_input_stage.setPosition(hou.Vector2(0, 2))
            char_output0.setPosition(hou.Vector2(0, -4))

        pass
    build_characters_and_props_subnet()


    # Create a Subnet called "CAMERA"
    camera_subnet = import_subnet.createNode("subnet", "CAMERA")
    camera_subnet.setColor(hou.Color(0.273, 0.627, 0.278)) # Green
    camera_subnet.setPosition(characters_and_props_subnet.position() + hou.Vector2(0, -2))
    camera_subnet.setComment("Import the Camera elements here")

    def build_camera_subnet():
        # Get the ouput0 node of the camera subnet
        cam_output0 = camera_subnet.node("output0")
        # Get the input0 node of the camera subnet
        cam_inputs = camera_subnet.indirectInputs()
        cam_input_stage = cam_inputs[0] if cam_inputs else None

        # Create a "Null" node called "IN_CAMERA"
        in_camera = camera_subnet.createNode("null", "IN_CAMERA")
        in_camera.setPosition(hou.Vector2(0, 0))

        # Create a "reference" node to import the camera USD
        if camera_filepath and os.path.isfile(camera_filepath):
            cam_reference_node = camera_subnet.createNode("reference", "Camera_Reference")
            cam_reference_node.setPosition(in_camera.position() + hou.Vector2(0, -2))
            cam_reference_node.parm("filepath1").set(camera_filepath.replace("\\", "/"))
            cam_reference_node.parm("primpath1").set(f"/Camera_grp")
            cam_reference_node.setComment(f"Reference the Camera USD:\n{camera_filepath}")
            cam_reference_node.setGenericFlag(hou.nodeFlag.DisplayComment,True)

            # Add a transform node to transform from cm to m
            transform_node = camera_subnet.createNode("xform", "Transform_cm_to_m")
            transform_node.setPosition(cam_reference_node.position() + hou.Vector2(0, -2))
            transform_node.parm("scale").set(0.01)  # Scale down by a factor of 100 (cm to m)
            transform_node.parm("primpattern").set("/Camera_grp")
            transform_node.setComment("Transform from cm to m")
            transform_node.setGenericFlag(hou.nodeFlag.DisplayComment,True)

            # Connect the nodes together
            cam_reference_node.setInput(0, in_camera, 0)
            transform_node.setInput(0, cam_reference_node, 0)
            cam_output0.setInput(0, transform_node, 0)

        else:
            # If no valid camera filepath is provided, connect IN_CAMERA directly to output0
            cam_output0.setInput(0, in_camera, 0)

        # Place the input and output nodes
        cam_input_stage.setPosition(hou.Vector2(0, 2))
        cam_output0.setPosition(hou.Vector2(0, -4))

        # Connect the nodes together
        in_camera.setInput(0, cam_input_stage, 0)

        pass

    build_camera_subnet()

    # Create a "Null" node called "OUT_ASSEMBLY"
    out_assembly = import_subnet.createNode("null", "OUT_ASSEMBLY")
    out_assembly.setPosition(camera_subnet.position() + hou.Vector2(0, -2))


    # Place the input and output nodes
    input_stage.setPosition(hou.Vector2(0, 2))
    output0.setPosition( out_assembly.position() + hou.Vector2(0, -2))

    ####################################
    #### Connect the nodes together ####
    ####################################
    # Connect the input0 node to the in_import node
    in_import.setInput(0, input_stage, 0)
    # Connect the set_dress_subnet to the in_import node
    set_dress_subnet.setInput(0, in_import, 0)
    # Connect the characters_and_props_subnet to the set_dress_subnet
    characters_and_props_subnet.setInput(0, set_dress_subnet, 0)
    # Connect the camera_subnet to the characters_and_props_subnet
    camera_subnet.setInput(0, characters_and_props_subnet, 0)
    # Connect the output0 node to the fx_subnet
    out_assembly.setInput(0, camera_subnet, 0)
    # Connect the output0 node to the out_assembly node
    output0.setInput(0, out_assembly, 0)
    #####################################




build_import_subnet()




# Create a "Scene_Cleaning" subnet 
sceneCleaning_subnet = stage.createNode("subnet", "Scene_Cleaning")
sceneCleaning_subnet.setColor(hou.Color(0.776, 0.157, 0.157))  # Red
sceneCleaning_subnet.setPosition(import_subnet.position() + hou.Vector2(0, -2))
# Add a comment to the Scene_Cleaning subnet
sceneCleaning_subnet.setComment("Ne pas toucher a ce node !")
sceneCleaning_subnet.setGenericFlag(hou.nodeFlag.DisplayComment,True)

def build_sceneCleaning_subnet():    # Get the ouput0 node of the sceneCleaning subnet
    output0 = sceneCleaning_subnet.node("output0")
    # Get the input0 node of the sceneCleaning subnet
    inputs = sceneCleaning_subnet.indirectInputs()
    input_stage = inputs[0] if inputs else None

    # Create a "Null" node called "IN_SCENE_CLEANING"
    in_scene_cleaning = sceneCleaning_subnet.createNode("null", "IN_SCENE_CLEANING")
    in_scene_cleaning.setPosition(hou.Vector2(0, 0))


    # Create a "null" node called "OUT_SCENE_CLEANING"
    out_scene_cleaning = sceneCleaning_subnet.createNode("null", "OUT_SCENE_CLEANING")
    out_scene_cleaning.setPosition(hou.Vector2(0, -4))


    # Place the input and output nodes
    input_stage.setPosition(hou.Vector2(0, 2))
    output0.setPosition(hou.Vector2(0, -6))

    # Connect the nodes together
    # Connect the IN_SCENE_CLEANING node to the graftstages node
    out_scene_cleaning.setInput(0, in_scene_cleaning, 0)
    # Connect the input0 node to the in_scene_cleaning node
    in_scene_cleaning.setInput(0, input_stage, 0)
    # Connect the output0 node to the out_scene_cleaning node
    output0.setInput(0, out_scene_cleaning, 0)

    return

build_sceneCleaning_subnet()



# Create a null "OUT_SCENE_ASSEMBLY" node
out_scene_building = stage.createNode("null", "OUT_SCENE_ASSEMBLY")
out_scene_building.setPosition(sceneCleaning_subnet.position() + hou.Vector2(0, -2))


# Create a "Export" node
export_node = stage.createNode("Thomas::BP_Export::1.0", "Publish")
export_node.setColor(hou.Color(0.776, 0.776, 0.157))  # Yellow
export_node.setPosition(out_scene_building.position() + hou.Vector2(0, -2))
export_node.parm("productName").set("Assembly_Publish")
export_node.parm("nextVersion").set(True)
export_node.parm("updateMaster").set(True)
export_node.parm("defaultprim").set(f"/{assetName}")
export_node.setComment("Publier le USD de l'assembly")
export_node.setGenericFlag(hou.nodeFlag.DisplayComment,True)




#####################################
#### Connect the nodes together #####
#####################################

# import_subnet[0]->sceneCleaning_subnet[0]
sceneCleaning_subnet.setInput(0, import_subnet, 0)
# sceneCleaning_subnet[0]->out_scene_building[0]
out_scene_building.setInput(0, sceneCleaning_subnet, 0)
# out_scene_building[0]->usd_rop[0]
export_node.setInput(0, out_scene_building, 0)


# Set the display flag on the "OUT_SCENE_BUILDING" node
out_scene_building.setDisplayFlag(True)



################################################
####  Set the frame range of the scene      ####
################################################
# Set the frame range of the Houdini scene
hou.playbar.setFrameRange(shot_start , shot_end )
hou.playbar.setPlaybackRange(shot_start , shot_end )
hou.setFrame(shot_start )



# Save the Houdini file
hou.hipFile.save(output_hip_path)