import hou
import os

# Template to create houdini low geo

output_hip_path = "C:/Users/Thomas/OneDrive/Bureau/Pipeline 2025/Pipeline_USD_2025-2026_src/prism/Badger_Pipeline/Scripts/src/core/FileTemplates/output.hip"
assetName = "TEST"
assetType = "Chars"
numberOfGroups = "03"

task_name = "Modeling_Houdini"
department_name = "ModL"

# Create a new Houdini scene
hou.hipFile.clear(suppress_save_prompt=True)

# Create the Stage node if it doesn't exist
obj = hou.node("/obj")
if obj is None:
    obj = hou.node("/").createNode("geo", "stage")


# Convert the number of groups to integer
numberOfGroupsInt = int(numberOfGroups)



###############################################
#### Create the nodes in the OBJ   context ####
###############################################



for i in range(numberOfGroupsInt):

    # Create a geo node
    geo_node = None

    if numberOfGroupsInt <= 1:
        geo_node = obj.createNode("geo", "ModL_Main")
    else:
        geo_node = obj.createNode("geo", "ModL_Variant_{}".format(i + 1))
        geo_node.setPosition(hou.Vector2(i * 3, 0))

    # Create a "ModL" subnet node
    modl_subnet = geo_node.createNode("subnet", "ModL")
    modl_subnet.setColor(hou.Color(0.273, 0.627, 0.278)) # Green
    modl_subnet.setUserData("nodeshape", "burst")
    modl_subnet.setPosition(hou.Vector2(0, 0))

    
    # Create a "SceneCleaning" subnet called "Scene_Cleaning"
    sceneCleaning_subnet = geo_node.createNode("subnet", "Scene_Cleaning")
    sceneCleaning_subnet.setColor(hou.Color(0.776, 0.157, 0.157)) # Red
    sceneCleaning_subnet.setPosition(modl_subnet.position() + hou.Vector2(0, -2))
    sceneCleaning_subnet.setComment("Ne pas toucher a ce node !")
    sceneCleaning_subnet.setGenericFlag(hou.nodeFlag.DisplayComment,True)
    def build_sceneCleaning_subnet():    # Get the ouput0 node of the sceneCleaning subnet
        output0 = sceneCleaning_subnet.createNode("output", "Output0")
        # Get the input0 node of the sceneCleaning subnet
        inputs = sceneCleaning_subnet.indirectInputs()
        input_stage = inputs[0] if inputs else None

        # Create a "Null" node called "IN_SCENE_CLEANING"
        in_scene_cleaning = sceneCleaning_subnet.createNode("null", "IN_SCENE_CLEANING")
        in_scene_cleaning.setPosition(hou.Vector2(0, 0))

        # Create a "Transform" node called "Transform_m_to_cm"
        transform_m_to_cm = sceneCleaning_subnet.createNode("xform", "Transform_m_to_cm")
        transform_m_to_cm.setPosition(hou.Vector2(0, -2))
        transform_m_to_cm.parm("sx").set(100)
        transform_m_to_cm.parm("sy").set(100)
        transform_m_to_cm.parm("sz").set(100)

        # Create a "null" node called "OUT_SCENE_CLEANING"
        out_scene_cleaning = sceneCleaning_subnet.createNode("null", "OUT_SCENE_CLEANING")
        out_scene_cleaning.setPosition(hou.Vector2(0, -4))


        # Place the input and output nodes
        input_stage.setPosition(hou.Vector2(0, 2))
        output0.setPosition(hou.Vector2(0, -6))

        # Connect the nodes together
        # Connect the IN_SCENE_CLEANING node to the graftstages node
        transform_m_to_cm.setInput(0, in_scene_cleaning, 0)
        out_scene_cleaning.setInput(0, transform_m_to_cm, 0)
        in_scene_cleaning.setInput(0, input_stage, 0)
        # Connect the output0 node to the out_scene_cleaning node
        output0.setInput(0, out_scene_cleaning, 0)

        return

    build_sceneCleaning_subnet()

    # Create " OUT_Null" node in the geo
    out_null = geo_node.createNode("null", "OUT_Null")
    out_null.setPosition(sceneCleaning_subnet.position() + hou.Vector2(0, -2))



    # Create a prism::FileCache::1.0 
    file_cache = geo_node.createNode("prism::Filecache::1.0", "ModL_FileCache_Publish")
    file_cache.setColor(hou.Color(0.776, 0.776, 0.157))  # Yellow
    file_cache.setPosition(out_null.position() + hou.Vector2(0, -2))
    file_cache.parm("task").set("ModL_Publish")
    if numberOfGroupsInt > 1:
        file_cache.parm("task").set("ModL_Publish_var{}".format(i + 1))
    file_cache.parm("framerange").set(0)
    file_cache.parm("format").set(".usdc")

    # Create a prism::FileCache::1.0 for the exports
    file_cache_export = file_cache.createOutputNode("prism::Filecache::1.0", "ModL_FileCache_Export")
    file_cache_export.setColor(hou.Color(0.776, 0.776, 0.157))  # Yellow
    file_cache_export.setPosition(out_null.position() + hou.Vector2(5, -2))
    file_cache_export.parm("task").set("ModL_Export_" + task_name)
    if numberOfGroupsInt > 1:
        file_cache_export.parm("task").set("ModL_Export_" + task_name +"_var{}".format(i + 1))
    file_cache_export.parm("framerange").set(0)
    file_cache_export.parm("format").set(".usdc")

    # Connect the nodes together
    sceneCleaning_subnet.setInput(0, modl_subnet)
    out_null.setInput(0, sceneCleaning_subnet)
    file_cache.setInput(0, out_null)
    file_cache_export.setInput(0, out_null)





# Add a sticky note 
sticky_note = obj.createStickyNote("title")
sticky_note.setPosition(hou.Vector2(0, 0.5))
sticky_note.resize(hou.Vector2(8, 1))
sticky_note_text = "Departement : " + department_name + "\n"
sticky_note_text += "Asset : " + assetName
sticky_note.setText(sticky_note_text)
sticky_note.setDrawBackground(False)
sticky_note.setTextColor(hou.Color(1, 1, 1)) # White
sticky_note.setTextSize(0.7)


# Save the Houdini file
hou.hipFile.save(output_hip_path)




