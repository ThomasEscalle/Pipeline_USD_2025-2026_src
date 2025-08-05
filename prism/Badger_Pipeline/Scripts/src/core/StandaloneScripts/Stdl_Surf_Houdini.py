import hou
import os

# Lookdev scene script


output_hip_path = "$$OUTPUT_PATH$$"
assetName = "$$ASSET_NAME$$"
assetType = "$$TYPE_ASSET$$"
referencePath = "$$REFERENCE_PATH$$"
importReference = "$$IMPORT_REFERENCE$$"

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

# Set the path to the output file in the temp directory/temporary_surfacing.usda
output_path = os.path.join(QStandardPaths.writableLocation(QStandardPaths.TempLocation), "temporary_surfacing.usda")
rop.parm("lopoutput").set(output_path)
rop.parm("execute").pressButton()

# Create a new product in Prism
fnameData = core.getScenefileData(core.getCurrentFileName(), getEntityFromPath=True)
core.products.createProduct(fnameData, "Surf_Publish_v001", "global")

# Ingest the new version into prism
result = core.products.ingestProductVersion([output_path], fnameData,"Surf_Publish_v001")

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

# Create an "Import Subnet"
import_subnet = stage.createNode("subnet", "Import")
import_subnet.setColor(hou.Color(0.776, 0.776, 0.157)) # Yellow
import_subnet.setPosition(hou.Vector2(0, 0))

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
    if importReference == "True":
        reference.setParms(
            {
                "filepath1": referencePath , 
                "primpath1": f"/{assetName}/geo/render"
            }
        )
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



# Create a "MaterialLibrary" node called "Materials"
material_library = stage.createNode("materiallibrary", "Materials")
material_library.setColor(hou.Color(0.273, 0.627, 0.278)) # Green
material_library.setPosition(import_subnet.position() + hou.Vector2(0, -2))
material_library.setParms({
    "matpathprefix": f"/{assetName}/mtl/"
})

# Create a "Assign Material" node called "Assign_Material"
assign_material = stage.createNode("assignmaterial", "Assign_Material")
assign_material.setColor(hou.Color(0.273, 0.627, 0.278)) # Green
assign_material.setPosition(material_library.position() + hou.Vector2(0, -2))

# Create a "SceneCleaning" subnet called "Scene_Cleaning"
sceneCleaning_subnet = stage.createNode("subnet", "Scene_Cleaning")
sceneCleaning_subnet.setColor(hou.Color(0.776, 0.157, 0.157)) # Red
sceneCleaning_subnet.setPosition(assign_material.position() + hou.Vector2(0, -2))
sceneCleaning_subnet.setComment("Ne pas toucher a ce node !")
sceneCleaning_subnet.setGenericFlag(hou.nodeFlag.DisplayComment,True)

# Create a null "OUT_SCENE_LOOKDEV" node
out_scene_lookdev = stage.createNode("null", "OUT_SCENE_LOOKDEV")
out_scene_lookdev.setPosition(sceneCleaning_subnet.position() + hou.Vector2(0, -2))

def build_lookdev_scene():

    pass
build_lookdev_scene()



# Create a "Export" node
export_subnet = stage.createNode("subnet", "Export")
export_subnet.setColor(hou.Color(0.776, 0.776, 0.157))  # Yellow
export_subnet.setPosition(out_scene_lookdev.position() + hou.Vector2(0, -2))
# Add a button parameter to the export subnet
export_subnet_button_parm = hou.ButtonParmTemplate("publish", "PUBLISH")
export_subnet_button_parm.setScriptCallback("hou.pwd().node('Python_Script').cook(force=True)")
export_subnet_button_parm.setScriptCallbackLanguage(hou.scriptLanguage.Python)
export_subnet.addSpareParmTuple(export_subnet_button_parm)


def build_export_subnet():
    print("Building Export Subnet...")
    # Get the ouput0 node of the import subnet
    output0 = export_subnet.node("output0")
    # Get the input0 node of the import subnet
    inputs = export_subnet.indirectInputs()
    input_stage = inputs[0] if inputs else None


    # Create a USD_ROP node inside the export subnet
    usd_rop_export = export_subnet.createNode("usd_rop", "USD_ROP")
    usd_rop_export.setPosition(hou.Vector2(2, -1))
    usd_rop_export.setColor(hou.Color(0.776, 0.776, 0.157))  # Yellow
    usd_rop_export.setParms({
        "defaultprim": f"/{assetName}",
    })

    # Create a pythonscript1 node inside the export subnet
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







# Create a "LOOKDEV_SCENE" subnet
lookdev_scene = stage.createNode("subnet", "LOOKDEV_SCENE")
lookdev_scene.setColor(hou.Color(0.776, 0.776, 0.157))  # Cyan
lookdev_scene.setPosition(out_scene_lookdev.position() + hou.Vector2(-4, -2))







#####################################
#### Connect the nodes together #####
#####################################
# Materials -> Import
material_library.setInput(0, import_subnet, 0)
# Assign_Material -> Materials
assign_material.setInput(0, material_library, 0)
# SceneCleaning -> Assign_Material
sceneCleaning_subnet.setInput(0, assign_material, 0)
# OUT_SCENE_LOOKDEV -> SceneCleaning
out_scene_lookdev.setInput(0, sceneCleaning_subnet, 0)
# USD_OUTPUT -> OUT_SCENE_LOOKDEV
export_subnet.setInput(0, out_scene_lookdev, 0)
# LOOKDEV_SCENE -> OUT_SCENE_LOOKDEV
lookdev_scene.setInput(0, out_scene_lookdev, 0)


##################
#### Comments ####
##################

# Add a sticky note
sticky_note = stage.createStickyNote("lookdev_comment")
sticky_note.setPosition((hou.Vector2(3, -4)))
sticky_note_text = "Cette scène sert a créer le lookdev de la scène.\n"
sticky_note_text += "Tu peux créer tes shaders dans le sous-réseau \"Materials\".\n"
sticky_note_text += "Tu peux assigner tes shaders dans le node \"Assign_Material\".\n"
sticky_note_text += "Le node \"LOOKDEV_SCENE\" permet de visualiser ta scène avec des lights. Elle n'est pas exportée dans le fichier USD. C'est juste pour le viewport.\n"
sticky_note.setText(sticky_note_text)
sticky_note.resize(hou.Vector2(5, 2))
sticky_note.setDrawBackground(False)
sticky_note.setTextColor(hou.Color(1, 1, 1))

# Set the display flag on the "OUT_SCENE_BUILDING" node
out_scene_lookdev.setDisplayFlag(True)


# Save the Houdini file
hou.hipFile.save(output_hip_path)