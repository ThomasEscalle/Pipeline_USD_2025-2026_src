import hou
import os


output_hip_path = "C:/Users/Thomas/OneDrive/Bureau/Pipeline 2025/Pipeline_USD_2025-2026_src/prism/Badger_Pipeline/Scripts/src/core/FileTemplates/output.hip"
assetName = "sq_010_Master"
assetType = "shot"
taskName = "SetDress"
departmentName = "SetD"


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

    # Place the input and output nodes
    input_stage.setPosition(hou.Vector2(0, 2))
    output0.setPosition(hou.Vector2(0, -12))

    ####################################
    #### Connect the nodes together ####
    ####################################
    # Connect the IN_ASSEMBLY node to the output0 node
    output0.setInput(0, in_assembly, 0)
    # Connect the input0 node to the in_assembly node
    in_assembly.setInput(0, input_stage, 0)

build_assembly_subnet()




# Create a "Scene_Cleaning" subnet 
sceneCleaning_subnet = stage.createNode("subnet", "Scene_Cleaning")
sceneCleaning_subnet.setColor(hou.Color(0.776, 0.157, 0.157))  # Red
sceneCleaning_subnet.setPosition(assembly_subnet.position() + hou.Vector2(0, -4))
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

    # Create a "graftstages" node 
    graftstages = sceneCleaning_subnet.createNode("graftstages", "GRAFT_STAGES")
    graftstages.setPosition(hou.Vector2(0, -2))
    graftstages.setColor(hou.Color(0.776, 0.776, 0.157))  # Yellow
    graftstages.setParms({
        "destpath" : f"/setD_{assetName}",
    })

    # Create a "null" node called "OUT_SCENE_CLEANING"
    out_scene_cleaning = sceneCleaning_subnet.createNode("null", "OUT_SCENE_CLEANING")
    out_scene_cleaning.setPosition(hou.Vector2(0, -4))


    # Place the input and output nodes
    input_stage.setPosition(hou.Vector2(0, 2))
    output0.setPosition(hou.Vector2(0, -6))

    # Connect the nodes together
    # Connect the IN_SCENE_CLEANING node to the graftstages node
    graftstages.setInput(1, in_scene_cleaning, 0)
    # Connect the graftstages node to out_scene_cleaning node
    out_scene_cleaning.setInput(0, graftstages, 0)
    # Connect the input0 node to the in_scene_cleaning node
    in_scene_cleaning.setInput(0, input_stage, 0)
    # Connect the output0 node to the out_scene_cleaning node
    output0.setInput(0, out_scene_cleaning, 0)

    return

build_sceneCleaning_subnet()



# Create a null "OUT_SCENE_BUILDING" node
out_scene_building = stage.createNode("null", "OUT_SCENE_BUILDING")
out_scene_building.setPosition(sceneCleaning_subnet.position() + hou.Vector2(0, -2))
out_scene_building.setUserData("nodeshape", "diamond")




# Create a "Export" node
export_node = stage.createNode("Thomas::BP_Export::1.0", "Publish")
export_node.setColor(hou.Color(0.776, 0.776, 0.157))  # Yellow
export_node.setPosition(out_scene_building.position() + hou.Vector2(0, -2))
export_node.parm("productName").set("SetD_Publish")
export_node.parm("nextVersion").set(True)
export_node.parm("updateMaster").set(True)




# Create a "LOOKDEV_SCENE" subnet
lookdev_scene = stage.createNode("subnet", "LOOKDEV_SCENE")
lookdev_scene.setColor(hou.Color(0.776, 0.776, 0.157))  # Cyan
lookdev_scene.setPosition(out_scene_building.position() + hou.Vector2(-4, -2))




#####################################
#### Connect the nodes together #####
#####################################

# assembly_subnet[0]->sceneCleaning_subnet[0]
sceneCleaning_subnet.setInput(0, assembly_subnet, 0)
# sceneCleaning_subnet[0]->out_scene_building[0]
out_scene_building.setInput(0, sceneCleaning_subnet, 0)
# out_scene_building[0]->usd_rop[0]
export_node.setInput(0, out_scene_building, 0)
# out_scene_building[0]->lookdev_scene[0]
lookdev_scene.setInput(0, out_scene_building, 0)



##################
#### Comments ####
##################

# Set the display flag on the "OUT_SCENE_BUILDING" node
out_scene_building.setDisplayFlag(True)


# Save the Houdini file
hou.hipFile.save(output_hip_path)