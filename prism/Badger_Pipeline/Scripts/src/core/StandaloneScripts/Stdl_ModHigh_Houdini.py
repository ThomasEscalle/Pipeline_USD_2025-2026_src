import hou
import os

# Template to create houdini high geo

output_hip_path = "$$OUTPUT_PATH$$"    # <-- Path where to save the scene
assetName = "$$ASSET_NAME$$"           # <-- Name of the asset, string to be set by the user
assetType = "$$TYPE_ASSET$$"           # <-- Type of the asset, string to be set by the user, e.g. "character", "prop", etc.
task_name = "$$TASK_NAME$$"               # <-- Name of the task, string to be set by the user, e.g. "Modeling", "Rigging_v012", etc.
department_name = "$$DEPARTMENT_NAME$$"   # <-- Name of the department, string to be set by the user, e.g. "ModL", "ModH", etc.

creationMethod = "$$CREATION_METHOD$$"  # <-- Method to use for creating, can be "Modeling Low first" or "Number of variant first"

importReference = "$$IMPORT_REFERENCE$$"    # <-- If we want to import the reference, string set to "True", otherwise "False"               
importReferencePaths = "$$REFERENCE_PATH$$" # <-- Path to the reference file if importReference is "True". It is a an array of paths contained into a string. Use eval() before to use it.

numberOfGroups = "$$NUMBER_OF_GROUPS$$"   # <-- Number of output groups. Only used if creationMethod is "Number of variant first"



# Create a new Houdini scene
hou.hipFile.clear(suppress_save_prompt=True)

# Create the Obj node if it doesn't exist
obj = hou.node("/obj")
if obj is None:
    obj = hou.node("/").createNode("geo", "stage")


# Convert the importReferencePaths string to a list
importReferencePathsArray = eval(importReferencePaths) if importReference == "True" else []

# Convert the number of groups to integer
numberOfGroupsInt = int(numberOfGroups)

# If the creation method is "Modeling Low first", set the number of groups to the number of import reference paths
if creationMethod == "Modeling Low first":
    numberOfGroupsInt = len(importReferencePathsArray)
    if numberOfGroupsInt == 0:
        creationMethod = "Number of variant first"
        numberOfGroupsInt = int(numberOfGroups)





###############################################
#### Create the nodes in the OBJ   context ####
###############################################



for i in range(numberOfGroupsInt):

    # Create a geo node
    geo_node = None

    if numberOfGroupsInt <= 1:
        geo_node = obj.createNode("geo", "ModH_Main")
    else:
        geo_node = obj.createNode("geo", "ModH_Variant_{}".format(i + 1))
        geo_node.setPosition(hou.Vector2(i * 3, 0))


    # Create a "Import" subnet node
    import_subnet = geo_node.createNode("subnet", "Import")
    import_subnet.setColor(hou.Color(0.776, 0.776, 0.157)) # Yellow
    import_subnet.setPosition(hou.Vector2(0, 2))
    
    def build_import_subnet():
        # Get the ouput0 node of the import subnet
        output0 = import_subnet.createNode("output", "Output0")

        # Create a "file" node called "Import_File"
        import_file = import_subnet.createNode("file", "Import_File")
        import_file.setPosition(hou.Vector2(0, 0))
        if creationMethod == "Modeling Low first":
            import_file.parm("file").set(importReferencePathsArray[i])

        # Create a "transform" node called "Transform_cm_to_m"
        transform_cm_to_m = import_subnet.createNode("xform", "Transform_cm_to_m")
        transform_cm_to_m.setPosition(import_file.position() + hou.Vector2(0, -2))
        transform_cm_to_m.parm("sx").set(0.01)
        transform_cm_to_m.parm("sy").set(0.01)
        transform_cm_to_m.parm("sz").set(0.01)

        # Create a "null" node called "OUT_IMPORT"
        out_import = import_subnet.createNode("null", "OUT_IMPORT")
        out_import.setPosition(transform_cm_to_m.position() + hou.Vector2(0, -2))

        # Move the output0 node
        output0.setPosition(out_import.position() + hou.Vector2(0, -2))

        # Connect the nodes together
        transform_cm_to_m.setInput(0, import_file, 0)
        out_import.setInput(0, transform_cm_to_m, 0)
        output0.setInput(0, out_import, 0)


        pass
    build_import_subnet()


    # Create a "ModH" subnet node
    modl_subnet = geo_node.createNode("subnet", "ModH")
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


    indexWithLeadingZeros = str(i + 1).zfill(3)

    # Create a prism::FileCache::1.0 
    file_cache = geo_node.createNode("prism::Filecache::1.0", "ModH_FileCache_Publish")
    file_cache.setColor(hou.Color(0.776, 0.776, 0.157))  # Yellow
    file_cache.setPosition(out_null.position() + hou.Vector2(0, -2))
    file_cache.parm("task").set("ModH_Publish")
    if numberOfGroupsInt > 1:
        file_cache.parm("task").set("ModH_Publish_var{}".format(indexWithLeadingZeros))
    file_cache.parm("framerange").set(0)
    file_cache.parm("format").set(".usdc")

    # Create a prism::FileCache::1.0 for the exports
    file_cache_export = file_cache.createOutputNode("prism::Filecache::1.0", "ModH_FileCache_Export")
    file_cache_export.setColor(hou.Color(0.776, 0.776, 0.157))  # Yellow
    file_cache_export.setPosition(out_null.position() + hou.Vector2(5, -2))
    file_cache_export.parm("task").set("ModH_Export_" + task_name)
    if numberOfGroupsInt > 1:
        file_cache_export.parm("task").set("ModH_Export_" + task_name +"_var{}".format(indexWithLeadingZeros))
    file_cache_export.parm("framerange").set(0)
    file_cache_export.parm("format").set(".usdc")

    # Connect the nodes together
    modl_subnet.setInput(0, import_subnet)
    sceneCleaning_subnet.setInput(0, modl_subnet)
    out_null.setInput(0, sceneCleaning_subnet)
    file_cache.setInput(0, out_null)
    file_cache_export.setInput(0, out_null)





# Add a sticky note 
sticky_note = obj.createStickyNote("title")
sticky_note.setPosition(hou.Vector2(0, 0.5))
sticky_note.resize(hou.Vector2(8, 0.1))
sticky_note_text = "Departement : " + department_name + "\n"
sticky_note_text += "Asset : " + assetName
sticky_note.setText(sticky_note_text)
sticky_note.setDrawBackground(False)
sticky_note.setTextColor(hou.Color(1, 1, 1)) # White
sticky_note.setTextSize(0.5)

# Save the Houdini file
hou.hipFile.save(output_hip_path)




