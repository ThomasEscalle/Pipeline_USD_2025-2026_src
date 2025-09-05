import hou
import os


output_hip_path = "$$OUTPUT_PATH$$"

assetName = "$$ASSET_NAME$$"
assetType = "$$TYPE_ASSET$$"
task = "$$TASK_NAME$$"
department = "$$DEPARTMENT_NAME$$"

import_reference = "$$IMPORT_REFERENCE$$"
reference_path = "$$REFERENCE_PATH$$"

# Convert the reference path to a list (eval), and take the first element if there are multiple paths
reference_paths_list = eval(reference_path) if reference_path else []
reference_pathstr = reference_paths_list[0] if reference_paths_list else ""

# Create a new Houdini scene
hou.hipFile.clear(suppress_save_prompt=True)

# Create the Stage node if it doesn't exist
stage = hou.node("/stage")
if stage is None:
    stage = hou.node("/").createNode("lopnet", "stage")



###############################################
#### Create the nodes in the Stage context ####
###############################################

# Create an "Import Subnet"
import_subnet = stage.createNode("subnet", "Import")
import_subnet.setColor(hou.Color(0.776, 0.776, 0.157)) # Yellow
import_subnet.setPosition(hou.Vector2(0, 2))

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
    if import_reference == "True" and reference_pathstr != "":
        
        # If we are importing a reference, set the reference path
        reference.setParms({
            "filepath1": reference_pathstr,
            "primpath1" : f"/setDress",
        })
    else:
        # If we are not importing a reference, set the reference path to an empty string
        reference.setParms({
            "filepath1": "",
            "primpath1" : f"/setDress",
        })
        # Set the color to red to indicate no reference
        reference.setColor(hou.Color(0.776, 0.157, 0.157)) # Red

    # Create a "layerbreak" node called "LayerBreak"
    layerbreak = import_subnet.createNode("layerbreak", "LayerBreak")
    layerbreak.setPosition(hou.Vector2(0, -2))

    # Create a "Null" node called "OUT_IMPORT"
    out_import = import_subnet.createNode("null", "OUT_IMPORT")
    out_import.setPosition(hou.Vector2(0, -3))

    # Place the input and output nodes
    input_stage.setPosition(hou.Vector2(0, 1))
    output0.setPosition(hou.Vector2(0, -4))

    ####################################
    #### Connect the nodes together ####
    ####################################

    # Connect the Input stage to the IN_IMPORT node
    in_import.setInput(0, input_stage, 0)
    # Connect the IN_IMPORT node to the Reference node
    reference.setInput(0, in_import, 0)
    # Connect the Reference node to the LayerBreak node
    layerbreak.setInput(0, reference, 0)
    # Connect the LayerBreak node to the OUT_IMPORT node
    out_import.setInput(0, layerbreak, 0)
    # Connect the OUT_IMPORT node to the output0 node
    output0.setInput(0, out_import, 0)

build_import_subnet()




# Create a "Assembly" subnet
assembly_subnet = stage.createNode("subnet", "Master_Light")
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


    ##################
    #### Comments ####
    ##################
    # Add a sticky note 
    sticky_note = assembly_subnet.createStickyNote("AssemblySubnet")
    sticky_note.setPosition(hou.Vector2(3, -4))
    sticky_note_text = "C'est ici que tu peux mettre tes lumières.\n"
    sticky_note.setText(sticky_note_text)
    sticky_note.resize(hou.Vector2(5, 2))
    sticky_note.setDrawBackground(False)
    sticky_note.setTextColor(hou.Color(1, 1, 1)) # White

build_assembly_subnet()


# Create a "LightMixer" node
light_mixer = stage.createNode("lightmixer", "Light_Mixer")
light_mixer.setColor(hou.Color(0.273, 0.627, 0.278)) # Green
light_mixer.setPosition(assembly_subnet.position() + hou.Vector2(0, -2))



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

    # Create a "graftstages" node 
    # graftstages = sceneCleaning_subnet.createNode("graftstages", "GRAFT_STAGES")
    # graftstages.setPosition(hou.Vector2(0, -2))
    # graftstages.setColor(hou.Color(0.776, 0.776, 0.157))  # Yellow
    # graftstages.setParms({
    #     "destpath" : f"/masterLight_{assetName}",
    # })

    # Create a "null" node called "OUT_SCENE_CLEANING"
    out_scene_cleaning = sceneCleaning_subnet.createNode("null", "OUT_SCENE_CLEANING")
    out_scene_cleaning.setPosition(hou.Vector2(0, -4))


    # Place the input and output nodes
    input_stage.setPosition(hou.Vector2(0, 2))
    output0.setPosition(hou.Vector2(0, -6))

    # Connect the nodes together
    # Connect the graftstages node to out_scene_cleaning node
    out_scene_cleaning.setInput(0, in_scene_cleaning, 0)
    # Connect the input0 node to the in_scene_cleaning node
    in_scene_cleaning.setInput(0, input_stage, 0)
    # Connect the output0 node to the out_scene_cleaning node
    output0.setInput(0, out_scene_cleaning, 0)

    return

build_sceneCleaning_subnet()



# Create a null "OUT_SCENE_BUILDING" node
out_scene_building = stage.createNode("null", "OUT_SCENE_MASTER_LIGHT")
out_scene_building.setPosition(sceneCleaning_subnet.position() + hou.Vector2(0, -2))
out_scene_building.setUserData("nodeshape", "diamond")


# Create a "Export" node
export_node = stage.createNode("Thomas::BP_Export::1.0", "Publish")
export_node.setColor(hou.Color(0.776, 0.776, 0.157))  # Yellow
export_node.setPosition(out_scene_building.position() + hou.Vector2(0, -2))
export_node.parm("productName").set("MLgt_Publish")
export_node.parm("nextVersion").set(True)
export_node.parm("updateMaster").set(True)



#####################################
#### Connect the nodes together #####
#####################################

# masterLight[0]->import_subnet[0]
assembly_subnet.setInput(0, import_subnet, 0)
# assembly_subnet[0]->sceneCleaning_subnet[0]
light_mixer.setInput(0, assembly_subnet, 0)
# light_mixer[0]->sceneCleaning_subnet[0]
sceneCleaning_subnet.setInput(0, light_mixer, 0)
# sceneCleaning_subnet[0]->out_scene_building[0]
out_scene_building.setInput(0, sceneCleaning_subnet, 0)
# out_scene_building[0]->usd_rop[0]
export_node.setInput(0, out_scene_building, 0)



# Set the display flag on the "OUT_SCENE_BUILDING" node
out_scene_building.setDisplayFlag(True)


# Save the Houdini file
hou.hipFile.save(output_hip_path)