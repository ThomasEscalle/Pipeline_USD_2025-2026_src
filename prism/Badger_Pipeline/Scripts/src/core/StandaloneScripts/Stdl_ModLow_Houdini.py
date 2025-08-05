import hou
import os

# Template to create houdini low geo

output_hip_path = "$$OUTPUT_PATH$$"
assetName = "$$ASSET_NAME$$"
assetType = "$$TYPE_ASSET$$"

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
geo_node = obj.createNode("geo", "ModL_Main")


# Create a "ModL" subnet node
modl_subnet = geo_node.createNode("subnet", "ModL")
modl_subnet.setColor(hou.Color(0.273, 0.627, 0.278)) # Green
modl_subnet.setUserData("nodeshape", "burst")
modl_subnet.setPosition(hou.Vector2(0, 0))

# Create " OUT_Null" node in the geo
out_null = geo_node.createNode("null", "OUT_Null")
out_null.setPosition(hou.Vector2(0, -2))



# Create a prism::FileCache::1.0 
file_cache = geo_node.createNode("prism::Filecache::1.0", "ModL_FileCache_Publish")
file_cache.setColor(hou.Color(0.776, 0.776, 0.157))  # Yellow
file_cache.setPosition(hou.Vector2(0, -4))
# Set the "task" parameter to "ModL_Export"
file_cache.parm("task").set("ModL_Publish")
file_cache.parm("framerange").set(0)
file_cache.parm("format").set(".abc")


file_cache_export = file_cache.createOutputNode("prism::Filecache::1.0", "ModL_FileCache_Export")
file_cache_export.setColor(hou.Color(0.776, 0.776, 0.157))  # Yellow
file_cache_export.setPosition(hou.Vector2(4, -4))
file_cache_export.parm("task").set("ModL_Export")
file_cache_export.parm("framerange").set(0)
file_cache_export.parm("format").set(".abc")



# Connect the nodes together
out_null.setInput(0, modl_subnet)
file_cache.setInput(0, out_null)
file_cache_export.setInput(0, out_null)


# Save the Houdini file
hou.hipFile.save(output_hip_path)