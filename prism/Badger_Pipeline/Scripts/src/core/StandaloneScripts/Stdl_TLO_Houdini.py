import hou
import os


output_hip_path = "$$OUTPUT_PATH$$"
assetName = "seq_010_shot_010"
assetType = "tlo"
lightPath = "$$LIGHT_PATH$$"

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

# Set the path to the output file in the temp directory/temporary_tlo.usda
output_path = os.path.join(QStandardPaths.writableLocation(QStandardPaths.TempLocation), "temporary_tlo.usda")
rop.parm("lopoutput").set(output_path)
rop.parm("execute").pressButton()

# Create a new product in Prism
fnameData = core.getScenefileData(core.getCurrentFileName(), getEntityFromPath=True)
core.products.createProduct(fnameData, "TLO_Publish", "global")

# Ingest the new version into prism
result = core.products.ingestProductVersion([output_path], fnameData,"TLO_Publish")

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



    # Create a "Null" node called "OUT_IMPORT"
    out_import = import_subnet.createNode("null", "OUT_IMPORT")
    out_import.setPosition(in_import.position() + hou.Vector2(0, -2))


    # Place the input and output nodes
    input_stage.setPosition(hou.Vector2(0, 2))
    output0.setPosition( out_import.position() + hou.Vector2(0, -2))

    ####################################
    #### Connect the nodes together ####
    ####################################
    # Connect the IN_IMPORT node to the input_stage node
    in_import.setInput(0, input_stage, 0)
    # Connect the out_import to the in_import node
    out_import.setInput(0, in_import, 0)
    # Connect the output0 node to the out_import node
    output0.setInput(0, out_import, 0)
    #####################################



build_assembly_subnet()


# Create a "TLO" subnet
TLO_subnet = stage.createNode("subnet", "TLO")
TLO_subnet.setColor(hou.Color(0.157, 0.776, 0.157))  # Green
TLO_subnet.setPosition(import_subnet.position() + hou.Vector2(0, -2))
TLO_subnet.setUserData("nodeshape", "burst")

def build_TLO_subnet():
    # Get the ouput0 node of the TLO subnet
    output0 = TLO_subnet.node("output0")
    # Get the input0 node of the TLO subnet
    inputs = TLO_subnet.indirectInputs()
    input_stage = inputs[0] if inputs else None

    # Create a "Null" node called "IN_TLO"
    in_tlo = TLO_subnet.createNode("null", "IN_TLO")
    in_tlo.setPosition(hou.Vector2(0, 0))


    # Create a "Null" node called "OUT_TLO"
    out_tlo = TLO_subnet.createNode("null", "OUT_TLO")
    out_tlo.setPosition(hou.Vector2(0, -4))


    # Place the input and output nodes
    input_stage.setPosition(hou.Vector2(0, 2))
    output0.setPosition(hou.Vector2(0, -6))

    # Connect the nodes together
    # Connect the IN_TLO node to the graftstages node
    out_tlo.setInput(0, in_tlo, 0)
    # Connect the input_stage node to the in_tlo node
    in_tlo.setInput(0, input_stage, 0)
    # Connect the output0 node to the out_tlo node
    output0.setInput(0, out_tlo, 0)

    return
build_TLO_subnet()




# Create a "Scene_Cleaning" subnet 
sceneCleaning_subnet = stage.createNode("subnet", "Scene_Cleaning")
sceneCleaning_subnet.setColor(hou.Color(0.776, 0.157, 0.157))  # Red
sceneCleaning_subnet.setPosition(TLO_subnet.position() + hou.Vector2(0, -2))
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
        "defaultprim": f"/setD_{assetName}"
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

# connect the IMPORT subnet to the TLO subnet
TLO_subnet.setInput(0, import_subnet, 0)
# connect the TLO  to the Scene Cleaning subnet
sceneCleaning_subnet.setInput(0, TLO_subnet, 0)
# connect the Scene Cleaning subnet to the OUT_SCENE_ASSEMBLY node
out_scene_building.setInput(0, sceneCleaning_subnet, 0)
# connect the OUT_SCENE_ASSEMBLY node to the Export subnet
export_subnet.setInput(0, out_scene_building, 0)



##################
#### Comments ####
##################

# Add a sticky note 
sticky_note = stage.createStickyNote("stage_comment")
sticky_note.setPosition(hou.Vector2(3, -4))
sticky_note_text = "Cette scene sert a preparer les render settings.\n"
sticky_note_text += "C'est ici que l'on vas gerer les Render Layers, AOVS, render settings...\n"
sticky_note_text += "Une fois finis, utilise le node \"Export\" pour exporter ta scène.\n\n"
sticky_note.setText(sticky_note_text)
sticky_note.resize(hou.Vector2(5, 2))
sticky_note.setDrawBackground(False)
sticky_note.setTextColor(hou.Color(1, 1, 1)) # White


# Set the display flag on the "OUT_SCENE_BUILDING" node
out_scene_building.setDisplayFlag(True)


# Save the Houdini file
hou.hipFile.save(output_hip_path)