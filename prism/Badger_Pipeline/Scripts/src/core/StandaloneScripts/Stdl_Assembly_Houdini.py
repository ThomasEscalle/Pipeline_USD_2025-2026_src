import hou
import os


#  
#  # The way it is used in the pipeline :
#
#  output_hip_path = "C:/Users/Thomas/OneDrive/Bureau/Pipeline 2025/Pipeline_USD_2025-2026_src/prism/Badger_Pipeline/Scripts/src/core/FileTemplates/output.hip"
#  
#  assetName = "sq_010_sh_030"
#  assetType = "shot"
#  task_name = "Assembly"
#  department_name = "abl"
#  
#  shot_start = int("1001")
#  shot_end = int("1005")
#  shot_length = int("5")
#  shot_preroll = int("0")
#  shot_postroll = int("0")
#  
#  set_dress_filepath = "E:/3D/Projects/06_Ouyang/03_Production/02_Shots/sq_010/Master/Export/SetD_Publish/master/sq_010-Master_SetD_Publish_master.usd"
# 




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

# Create a "Assembly" subnet
assembly_subnet = stage.createNode("subnet", "Assembly")
assembly_subnet.setColor(hou.Color(0.273, 0.627, 0.278)) # Green
assembly_subnet.setUserData("nodeshape", "burst")

# Build the nodes inside the assembly subnet
def build_assembly_subnet():


    # Get the ouput0 node of the assembly subnet
    output0 = assembly_subnet.node("output0")
    # Get the input0 node of the assembly subnet
    inputs = assembly_subnet.indirectInputs()
    input_stage = inputs[0] if inputs else None

    # Create a "Null" node called "IN_ASSEMBLY"
    in_assembly = assembly_subnet.createNode("null", "IN_ASSEMBLY")
    in_assembly.setPosition(hou.Vector2(0, 0))


    # Create a Subnet called "SET_DRESS"
    set_dress_subnet = assembly_subnet.createNode("subnet", "SET_DRESS")
    set_dress_subnet.setColor(hou.Color(0.273, 0.627, 0.278)) # Green
    set_dress_subnet.setPosition(in_assembly.position() + hou.Vector2(0, -2))
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
            reference_node = set_dress_subnet.createNode("reference", "Set_Dress_Reference")
            reference_node.setPosition(in_set_dress.position() + hou.Vector2(0, -2))
            reference_node.parm("filepath1").set(set_dress_filepath.replace("\\", "/"))
            reference_node.parm("primpath1").set(f"/Set_Dress_grp")
            reference_node.setComment(f"Reference the Set Dress USD:\n{set_dress_filepath}")
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
    

    # Create a Subnet called "ITEMS"
    items_subnet = assembly_subnet.createNode("subnet", "ITEMS")
    items_subnet.setColor(hou.Color(0.273, 0.627, 0.278)) # Green
    items_subnet.setPosition(set_dress_subnet.position() + hou.Vector2(0, -2))
    items_subnet.setComment("Import the Aditional Items elements here")

    # Create a Subnet called "CHARACTERS_AND_PROPS"
    characters_and_props_subnet = assembly_subnet.createNode("subnet", "CHARACTERS_AND_PROPS")
    characters_and_props_subnet.setColor(hou.Color(0.273, 0.627, 0.278)) # Green
    characters_and_props_subnet.setPosition(items_subnet.position() + hou.Vector2(0, -2))
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

        last_node = in_characters_and_props
        for char_anim in eval(character_animations_filepaths):

            # Check if all the required keys are present
            required_keys = ['connected_entity', 'asset_file_path', 'product_file_path']
            if not all(key in char_anim for key in required_keys):
                print(f"Skipping invalid character animation entry: {char_anim}")
                continue

            # Create a "Bp_Anim_Import" node (custom node)
            asset_name_clean = char_anim['connected_entity']['asset_path'].split('//')[-1].replace(" ","_").replace("-","_")



            bp_anim_import = characters_and_props_subnet.createNode("Thomas::BP_Anim_Import::1.0", f"Anim_Import_{asset_name_clean}")
            bp_anim_import.setPosition(last_node.position() + hou.Vector2(0, -2))

            bp_anim_import.parm("import_method").set("method_0")

            ## Asset setup
            bp_anim_import.parm("filepath").set(char_anim['asset_file_path'].replace("\\", "/"))
            if "chars" in char_anim['connected_entity']['asset_path'].lower():
                bp_anim_import.parm("primpath").set(f"/Assets_grp/Characters_grp/{asset_name_clean}")
            elif "props" in char_anim['connected_entity']['asset_path'].lower():
                bp_anim_import.parm("primpath").set(f"/Assets_grp/Props_grp/{asset_name_clean}")
            
            ## Animation setup
            bp_anim_import.parm("filePathAnim").set(char_anim['product_file_path'].replace("\\", "/"))

            # Connect the nodes together
            bp_anim_import.setInput(0, last_node, 0)
            last_node = bp_anim_import

        # Connect the nodes together
        in_characters_and_props.setInput(0, char_input_stage, 0)
        char_output0.setInput(0, last_node, 0)

        # Place the input and output nodes
        char_input_stage.setPosition(hou.Vector2(0, 2))
        char_output0.setPosition(last_node.position() + hou.Vector2(0, -2))
        pass
    build_characters_and_props_subnet()



    # Create a Subnet called "CFX"
    cfx_subnet = assembly_subnet.createNode("subnet", "CFX")
    cfx_subnet.setColor(hou.Color(0.273, 0.627, 0.278)) # Green
    cfx_subnet.setPosition(characters_and_props_subnet.position() + hou.Vector2(0, -2))
    cfx_subnet.setComment("Import the CFX elements here")

    # Create a Subnet called "FX"
    fx_subnet = assembly_subnet.createNode("subnet", "FX")
    fx_subnet.setColor(hou.Color(0.273, 0.627, 0.278)) # Green
    fx_subnet.setPosition(cfx_subnet.position() + hou.Vector2(0, -2))
    fx_subnet.setComment("Import the FX elements here")

    # Create a Subnet called "CAMERA"
    camera_subnet = assembly_subnet.createNode("subnet", "CAMERA")
    camera_subnet.setColor(hou.Color(0.273, 0.627, 0.278)) # Green
    camera_subnet.setPosition(fx_subnet.position() + hou.Vector2(0, -2))
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
    out_assembly = assembly_subnet.createNode("null", "OUT_ASSEMBLY")
    out_assembly.setPosition(camera_subnet.position() + hou.Vector2(0, -2))


    # Place the input and output nodes
    input_stage.setPosition(hou.Vector2(0, 2))
    output0.setPosition( out_assembly.position() + hou.Vector2(0, -2))

    ####################################
    #### Connect the nodes together ####
    ####################################
    # Connect the input0 node to the in_assembly node
    in_assembly.setInput(0, input_stage, 0)
    # Connect the set_dress_subnet to the in_assembly node
    set_dress_subnet.setInput(0, in_assembly, 0)
    # Connect the items_subnet to the set_dress_subnet
    items_subnet.setInput(0, set_dress_subnet, 0)
    # Connect the characters_and_props_subnet to the items_subnet
    characters_and_props_subnet.setInput(0, items_subnet, 0)
    # Connect the cfx_subnet to the characters_and_props_subnet
    cfx_subnet.setInput(0, characters_and_props_subnet, 0)
    # Connect the fx_subnet to the cfx_subnet
    fx_subnet.setInput(0, cfx_subnet, 0)
    # Connect the camera_subnet to the fx_subnet
    camera_subnet.setInput(0, fx_subnet, 0)
    # Connect the output0 node to the fx_subnet
    out_assembly.setInput(0, camera_subnet, 0)
    # Connect the output0 node to the out_assembly node
    output0.setInput(0, out_assembly, 0)
    #####################################



build_assembly_subnet()




# Create a "Scene_Cleaning" subnet 
sceneCleaning_subnet = stage.createNode("subnet", "Scene_Cleaning")
sceneCleaning_subnet.setColor(hou.Color(0.776, 0.157, 0.157))  # Red
sceneCleaning_subnet.setPosition(assembly_subnet.position() + hou.Vector2(0, -2))
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

# assembly_subnet[0]->sceneCleaning_subnet[0]
sceneCleaning_subnet.setInput(0, assembly_subnet, 0)
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