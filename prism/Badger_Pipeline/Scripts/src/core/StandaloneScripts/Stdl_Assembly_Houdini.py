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

set_dress_filepath = "$$SETDRESS_FILEPATH$$"


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
            reference_node.parm("primpath1").set(f"/{assetName}/Set_Dress")
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