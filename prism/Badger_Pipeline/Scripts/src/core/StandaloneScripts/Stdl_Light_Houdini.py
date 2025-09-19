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

masterLightPath = "$$MASTER_LIGHT_PATH$$"
assemblyPath = "$$ASSEMBLY_PATH$$"


# Create a new Houdini scene
hou.hipFile.clear(suppress_save_prompt=True)

# Create the Stage node if it doesn't exist
stage = hou.node("/stage")
if stage is None:
    stage = hou.node("/").createNode("lopnet", "stage")



###############################################
#### Create the nodes in the Stage context ####
###############################################

# Create a "IMPORT" subnet
import_subnet = stage.createNode("subnet", "IMPORT")
import_subnet.setColor(hou.Color(0.776, 0.776, 0.157))  # Yellow

# Build the nodes inside the assembly subnet
def build_assembly_subnet():


    # Get the ouput0 node of the assembly subnet
    output0 = import_subnet.node("output0")
    # Get the input0 node of the assembly subnet
    inputs = import_subnet.indirectInputs()
    input_stage = inputs[0] if inputs else None

    # Create a "Null" node called "IN_IMPORT"
    in_import = import_subnet.createNode("null", "IN_IMPORT")
    in_import.setPosition(hou.Vector2(0, 0))


    
    # Create a reference node for the assembly
    assembly_ref = import_subnet.createNode("reference", "Assembly_Ref")
    assembly_ref.parm("filepath1").set( assemblyPath if assemblyPath != "" else "")
    assembly_ref.parm("primpath1").set(f"/{assetName}")
    assembly_ref.setPosition(in_import.position() + hou.Vector2(0, -2))


    # Create a reference node for the master light
    master_light_ref = import_subnet.createNode("reference", "Master_Light_Ref")
    master_light_ref.parm("filepath1").set(masterLightPath)
    master_light_ref.parm("primpath1").set("/Master_Light")
    master_light_ref.setPosition(assembly_ref.position() + hou.Vector2(0, -2))



    # Create a "Null" node called "OUT_IMPORT"
    out_import = import_subnet.createNode("null", "OUT_IMPORT")
    out_import.setPosition(master_light_ref.position() + hou.Vector2(0, -2))


    # Place the input and output nodes
    input_stage.setPosition(hou.Vector2(0, 2))
    output0.setPosition( out_import.position() + hou.Vector2(0, -2))

    ####################################
    #### Connect the nodes together ####
    ####################################
    # Connect the IN_IMPORT node to the input_stage node
    in_import.setInput(0, input_stage, 0)
    # Connect the input_stage node to the in_import node
    assembly_ref.setInput(0, in_import, 0)
    # Connect the assembly_ref node to the master_light_ref node
    master_light_ref.setInput(0, assembly_ref, 0)
    # Connect the last node (assembly or master light) to the out_import node
    out_import.setInput(0, master_light_ref, 0)
    # Connect the output0 node to the out_import node
    output0.setInput(0, out_import, 0)
    #####################################



build_assembly_subnet()

# Create a "Light" subnet
light_subnet = stage.createNode("subnet", "Light")
light_subnet.setColor(hou.Color(0.157, 0.776, 0.157))  # Green
light_subnet.setPosition(import_subnet.position() + hou.Vector2(0, -2))
light_subnet.setUserData("nodeshape", "burst")

def build_light_subnet():
    # Get the ouput0 node of the light subnet
    output0 = light_subnet.node("output0")
    # Get the input0 node of the light subnet
    inputs = light_subnet.indirectInputs()
    input_stage = inputs[0] if inputs else None

    # Create a "Null" node called "IN_LIGHT"
    in_light = light_subnet.createNode("null", "IN_LIGHT")
    in_light.setPosition(hou.Vector2(0, 0))



    # Create a "Null" node called "OUT_LIGHT"
    out_light = light_subnet.createNode("null", "OUT_LIGHT")
    out_light.setPosition(hou.Vector2(0, -4))


    # Place the input and output nodes
    input_stage.setPosition(hou.Vector2(0, 2))
    output0.setPosition(hou.Vector2(0, -6))

    # Connect the nodes together
    # Connect the IN_LIGHT node to the graftstages node
    out_light.setInput(0, in_light, 0)
    # Connect the input_stage node to the in_light node
    in_light.setInput(0, input_stage, 0)


    # Connect the output0 node to the out_light node
    output0.setInput(0, out_light, 0)

    return
build_light_subnet()


# Create a lightMixer node
light_mixer = stage.createNode("lightmixer", "Light_Mixer")
light_mixer.setColor(hou.Color(0.157, 0.776, 0.157))  # Green
light_mixer.setPosition(light_subnet.position() + hou.Vector2(0, -2))



# Create a "Scene_Cleaning" subnet 
sceneCleaning_subnet = stage.createNode("subnet", "Scene_Cleaning")
sceneCleaning_subnet.setColor(hou.Color(0.776, 0.157, 0.157))  # Red
sceneCleaning_subnet.setPosition(light_mixer.position() + hou.Vector2(0, -2))
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
export_node.parm("productName").set("Light_Publish")
export_node.parm("nextVersion").set(True)
export_node.parm("updateMaster").set(True)
export_node.parm("defaultprim").set(f"/{assetName}")
export_node.setComment("Publier le USD du lighting")
export_node.setGenericFlag(hou.nodeFlag.DisplayComment,True)

#####################################
#### Connect the nodes together #####
#####################################

# connect the IMPORT subnet to the Light subnet
light_subnet.setInput(0, import_subnet, 0)
# connect the Light subnet to the Light Mixer
light_mixer.setInput(0, light_subnet, 0)
# connect the Light Mixer to the Scene Cleaning subnet
sceneCleaning_subnet.setInput(0, light_mixer, 0)
# connect the Scene Cleaning subnet to the OUT_SCENE_ASSEMBLY node
out_scene_building.setInput(0, sceneCleaning_subnet, 0)
# connect the OUT_SCENE_ASSEMBLY node to the Export subnet
export_node.setInput(0, out_scene_building, 0)



##################
#### Comments ####
##################



# Set the display flag on the "OUT_SCENE_BUILDING" node
out_scene_building.setDisplayFlag(True)


# Save the Houdini file
hou.hipFile.save(output_hip_path)