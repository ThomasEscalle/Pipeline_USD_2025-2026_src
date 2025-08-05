import hou
import os


output_hip_path = "$$OUTPUT_PATH$$"
assetName = "seq_010_shot_010"
assetType = "assembly"

setDressingPath = "$$SET_DRESSING_PATH$$"


script = """
import PrismInit
import os
from PySide2.QtCore import QStandardPaths
core = PrismInit.pcore

# Use the drop down menu to select example code snippets.
node = hou.pwd()
stage = node.editableStage()

# Get the "USD_ROP" node from the current path
rop = node.parent().node("USD_ROP")

# Set the path to the output file in the temp directory/temporary_assembly.usda
output_path = os.path.join(QStandardPaths.writableLocation(QStandardPaths.TempLocation), "temporary_assembly.usda")
rop.parm("lopoutput").set(output_path)
rop.parm("execute").pressButton()

# Create a new product in Prism
fnameData = core.getScenefileData(core.getCurrentFileName(), getEntityFromPath=True)
core.products.createProduct(fnameData, "Assembly_Publish", "global")

# Ingest the new version into prism
result = core.products.ingestProductVersion([output_path], fnameData,"Assembly_Publish")

path = result["createdFiles"][0]
folder = os.path.dirname(path)

# Update the product with the new version
core.products.updateMasterVersion(result["createdFiles"][0])

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



# Create a "Export" subnet
export_subnet = stage.createNode("subnet", "Export")
export_subnet.setColor(hou.Color(0.776, 0.776, 0.157))  # Yellow
export_subnet.setPosition(out_scene_building.position() + hou.Vector2(0, -2))
# Add a button parameter to the export subnet
export_subnet_button_parm = hou.ButtonParmTemplate("publish", "PUBLISH")
export_subnet_button_parm.setScriptCallback("hou.pwd().node('Python_Script').cook(force=True)")
export_subnet_button_parm.setScriptCallbackLanguage(hou.scriptLanguage.Python)
export_subnet.addSpareParmTuple(export_subnet_button_parm)


def build_export_subnet():
    print("Building Export Subnet...")
    # Get the ouput0 node of the export subnet
    output0 = export_subnet.node("output0")
    # Get the input0 node of the export subnet
    inputs = export_subnet.indirectInputs()
    input_stage = inputs[0] if inputs else None

    # Create a USD_ROP node inside the export subnet
    usd_rop_export = export_subnet.createNode("usd_rop", "USD_ROP")
    usd_rop_export.setPosition(hou.Vector2(2, -1))
    usd_rop_export.setColor(hou.Color(0.776, 0.776, 0.157))  # Yellow
    usd_rop_export.setParms({
        "defaultprim": f"/assembly_{assetName}"
    })

    # Create a pythonscript node inside the export subnet
    python_script = export_subnet.createNode("pythonscript", "Python_Script")
    python_script.setPosition(hou.Vector2(-3, 0))
    python_script.setColor(hou.Color(0.776, 0.776, 0.157))  # Yellow
    python_script.setParms({
        "python": script
    })

    # Place the input and output nodes
    input_stage.setPosition(hou.Vector2(0, 0))
    output0.setPosition(hou.Vector2(0, -4))

    # Connect the nodes together
    # Connect the Input stage to the USD_ROP node
    usd_rop_export.setInput(0, input_stage, 0)

build_export_subnet()




#####################################
#### Connect the nodes together #####
#####################################

# assembly_subnet[0]->sceneCleaning_subnet[0]
sceneCleaning_subnet.setInput(0, assembly_subnet, 0)
# sceneCleaning_subnet[0]->out_scene_building[0]
out_scene_building.setInput(0, sceneCleaning_subnet, 0)
# out_scene_building[0]->usd_rop[0]
export_subnet.setInput(0, out_scene_building, 0)



##################
#### Comments ####
##################

# Add a sticky note 
sticky_note = stage.createStickyNote("stage_comment")
sticky_note.setPosition(hou.Vector2(3, -4))
sticky_note_text = "Cette scène sert a importer l'ensemble des éléments qui ont été crées jusqu'ici.\n"
sticky_note_text += "Rends toi dans le subnet \"Assembly\" pour importer les elements manquants.\n"
sticky_note_text += "Une fois finis, utilise le node \"Export\" pour exporter ta scène.\n\n"
sticky_note.setText(sticky_note_text)
sticky_note.resize(hou.Vector2(5, 2))
sticky_note.setDrawBackground(False)
sticky_note.setTextColor(hou.Color(1, 1, 1)) # White


# Set the display flag on the "OUT_SCENE_BUILDING" node
out_scene_building.setDisplayFlag(True)


# Save the Houdini file
hou.hipFile.save(output_hip_path)