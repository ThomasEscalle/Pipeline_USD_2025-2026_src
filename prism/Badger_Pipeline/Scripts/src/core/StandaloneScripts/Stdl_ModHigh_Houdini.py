import hou
import os

# Template to create houdini low geo

output_hip_path = "$$OUTPUT_PATH$$"
assetName = "$$ASSET_NAME$$"
assetType = "$$TYPE_ASSET$$"

import_reference = "$$IMPORT_REFERENCE$$"
reference_path = "$$REFERENCE_PATH$$"

# Create a new Houdini scene
hou.hipFile.clear(suppress_save_prompt=True)

# Create the Stage node if it doesn't exist
obj = hou.node("/obj")
if obj is None:
    obj = hou.node("/").createNode("geo", "stage")


###############################################
#### Create the nodes in the OBJ   context ####
###############################################

# Create a geo node
geo_node = obj.createNode("geo", "ModH_Main")

# Create a "Import" subnet node
import_subnet = geo_node.createNode("subnet", "Import")
import_subnet.setColor(hou.Color(0.776, 0.776, 0.157)) # Yellow
import_subnet.setPosition(hou.Vector2(0, 2))
def buildImportSubnet():
    # Get the ouput0 node of the import subnet
    output0 = import_subnet.node("output0")
    if output0 is None:
        output0 = import_subnet.createNode("output", "output0")
        output0.setColor(hou.Color(0.776, 0.776, 0.157))

    # Get the input0 node of the import subnet
    inputs = import_subnet.indirectInputs()
    input_stage = inputs[0] if inputs else None

    # Place the input and output nodes
    input_stage.setPosition(hou.Vector2(0, 2))
    output0.setPosition(hou.Vector2(0, -4))

    # Create a "File" node inside the import subnet
    file_node = import_subnet.createNode("file", "Import_File")
    file_node.setColor(hou.Color(0.776, 0.776, 0.157))  # Yellow
    file_node.setPosition(hou.Vector2(0, 0))
    if import_reference == "True":
        file_node.parm("file").set(reference_path)

    # Create a "Transform_Cm_To_M" node inside the import subnet
    transform_node = import_subnet.createNode("xform", "Transform_Cm_To_M")
    transform_node.setColor(hou.Color(0.776, 0.157, 0.157))  # Red
    transform_node.setPosition(hou.Vector2(0, -2))
    transform_node.parm("sx").set(0.01)  # Convert cm to m
    transform_node.parm("sy").set(0.01)  # Convert cm to m
    transform_node.parm("sz").set(0.01)  # Convert cm to




    # Connect the nodes together
    if input_stage:
        file_node.setInput(0, input_stage)
    transform_node.setInput(0, file_node)
    output0.setInput(0, transform_node)
buildImportSubnet()



# Create a "ModL" subnet node
modl_subnet = geo_node.createNode("subnet", "ModH")
modl_subnet.setColor(hou.Color(0.273, 0.627, 0.278)) # Green
modl_subnet.setUserData("nodeshape", "burst")
modl_subnet.setPosition(hou.Vector2(0, 0))

# Create " OUT_Null" node in the geo
out_null = geo_node.createNode("null", "OUT_Null")
out_null.setPosition(hou.Vector2(0, -2))



# Create a prism::FileCache::1.0 
file_cache = geo_node.createNode("prism::Filecache::1.0", "ModH_FileCache_Publish")
file_cache.setColor(hou.Color(0.776, 0.776, 0.157))  # Yellow
file_cache.setPosition(hou.Vector2(0, -4))
# Set the "task" parameter to "ModL_Export"
file_cache.parm("task").set("ModH_Publish")
file_cache.parm("framerange").set(0)
file_cache.parm("format").set(".abc")

file_cache_export = file_cache.createOutputNode("prism::Filecache::1.0", "ModH_FileCache_Export")
file_cache_export.setColor(hou.Color(0.776, 0.776, 0.157))  # Yellow
file_cache_export.setPosition(hou.Vector2(4, -4))
file_cache_export.parm("task").set("ModH_Export")
file_cache_export.parm("framerange").set(0)
file_cache_export.parm("format").set(".abc")



# Connect the nodes together
modl_subnet.setInput(0, import_subnet)
out_null.setInput(0, modl_subnet)
file_cache.setInput(0, out_null)
file_cache_export.setInput(0, out_null)


# Save the Houdini file
hou.hipFile.save(output_hip_path)