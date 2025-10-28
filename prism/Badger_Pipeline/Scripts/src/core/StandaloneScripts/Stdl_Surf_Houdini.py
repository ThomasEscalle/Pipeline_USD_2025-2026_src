import hou
import os

# Lookdev scene script

output_hip_path = "$$OUTPUT_PATH$$"      # <-- Path where to save the scene

assetName = "$$ASSET_NAME$$"             # <-- Name of the asset, string to be set by the user
assetType = "$$TYPE_ASSET$$"             # <-- Type of the asset, string to be set by the user, e.g. "character", "prop", etc.
taskName = "$$TASK_NAME$$"               # <-- Name of the task, string to be set by the user, e.g. "Modeling", "Rigging_v012", etc.
departmentName = "$$DEPARTMENT_NAME$$"   # <-- Name of the department, string to be set by the user, e.g. "ModL", "ModH", etc.

variantsShareSameMaterials = "$$VARIANTS_SHARE_SAME_MATERIALS$$"  # <-- If the variants share the same materials, string set to "True", otherwise "False"
creationMethod = "$$CREATION_METHOD$$"   # <-- Method to use for creating, can be "Modeling high first" or "Number of variant first"
numberOfGroups = "$$NUMBER_OF_GROUPS$$"  # <-- Number of output groups. Only used if creationMethod is "Number of variant first"

referencePath = "$$REFERENCE_PATH$$"       # <-- Path to the reference file if importReference is "True". It is a string.
importReference = "$$IMPORT_REFERENCE$$"   # <-- If we want to import the reference, string set to "True", otherwise "False"


# Function to convert a file path to a URI using the Badger_Pipeline plugin
def convertPathToUri(path):
    try:
        import PrismInit
        core = PrismInit.pcore
        plugin = core.getPlugin("Badger_Pipeline")
        uri = plugin.convertPathToUri(path)
        return uri
    except Exception as e:
        return path



# Create a new Houdini scene
hou.hipFile.clear(suppress_save_prompt=True)

# Create the Stage node if it doesn't exist
stage = hou.node("/stage")
if stage is None:
    stage = hou.node("/").createNode("lopnet", "stage")


# Convert the importReferencePaths string to a list
importReferencePathsArray = eval(referencePath) if importReference == "True" else []

# Convert the number of groups to integer
numberOfGroupsInt = int(numberOfGroups)

# If the creation method is "Modeling high first", set the number of groups to the number of import reference paths
if creationMethod == "Modeling high first":
    numberOfGroupsInt = len(importReferencePathsArray)
    if numberOfGroupsInt == 0:
        creationMethod = "Number of variant first"
        numberOfGroupsInt = int(numberOfGroups)

numberOfGroupsIntSaved = numberOfGroupsInt
if variantsShareSameMaterials == "True":
    numberOfGroupsInt = 1


# Create a node for each group
for i in range(numberOfGroupsInt):

    reference_index = i

    # Create a pagging for the created nodes. 
    # _<index> with 3 digits if numberOfGroupsInt > 1, otherwise no suffix
    nodes_suffix = f"_var{i+1:03d}" if numberOfGroupsInt > 1 else ""

    # If there is more than one group, create a subnet for each group
    # Set the parent node to the subnet if there is more than one group, otherwise set it to the stage
    parent_node = stage
    if numberOfGroupsInt > 1:
        group_subnet = stage.createNode("subnet", f"Surf{nodes_suffix}")
        group_subnet.setColor(hou.Color(0.157, 0.627, 0.776))
        group_subnet.setPosition(hou.Vector2(i * 3, 0))
        parent_node = group_subnet

        output_node_of_group = group_subnet.node("output0")
        if output_node_of_group:
            output_node_of_group.destroy()
    



    ###############################################
    #### Create the nodes in the Stage context ####
    ###############################################


    # If we share the same materials, we create one subnet import for each group
    import_subnet_position = hou.Vector2(0, 0)
    import_subnet_suffix = ""
    number_of_import_subnets = numberOfGroupsIntSaved if variantsShareSameMaterials == "True" else 1

    if variantsShareSameMaterials == "True":
        # Create a "switch" node to switch between the import subnets
        switch_import_node = parent_node.createNode("switch", "Switch_Import")
        switch_import_node.setColor(hou.Color(0.157, 0.627, 0.776)) # Cyan
        switch_import_node.setPosition(hou.Vector2(0, 0))


    # Iterate over the number of import subnets to create
    # If variants share same materials, we create one import subnet per group
    # Otherwise, we create only one import subnet
    for j in range(number_of_import_subnets):


        if variantsShareSameMaterials == "True":
            import_subnet_suffix = f"_var{j+1:03d}"
            import_subnet_position = hou.Vector2(j * 3, 3)
            reference_index = j

        # Create an "Import Subnet"
        import_subnet = parent_node.createNode("subnet", "Import" + import_subnet_suffix)
        import_subnet.setColor(hou.Color(0.776, 0.776, 0.157)) # Yellow
        import_subnet.setPosition(import_subnet_position)

        

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
            if importReference == "True" and creationMethod == "Modeling high first" :
                reference_uri = convertPathToUri(importReferencePathsArray[reference_index])
                reference.setParms(
                    {
                        "filepath1": reference_uri.replace("\\", "/"),
                        "primpath1": f"/{assetName}/Asset_root/geo/render"
                    }
                )
                import_subnet.setComment(f"Importing reference: {importReferencePathsArray[reference_index]}")
                import_subnet.setGenericFlag(hou.nodeFlag.DisplayComment,True)
            else:
                reference.setParms(
                    {
                        "filepath1": "", 
                        "primpath1": f"/{assetName}/Asset_root/geo/render"
                    }
                )

            # Create a Transform node called Transform_cm_to_m
            transform_cm_to_m = import_subnet.createNode("xform", "Transform_cm_to_m")
            transform_cm_to_m.setPosition(reference.position() + hou.Vector2(0, -1))
            transform_cm_to_m.parm("sx").set(0.01)  # Scale X to convert from cm to m
            transform_cm_to_m.parm("sy").set(0.01)  # Scale Y to convert from cm to m
            transform_cm_to_m.parm("sz").set(0.01)  # Scale Z to convert from cm to m
            transform_cm_to_m.parm("primpattern").set(f"/{assetName}")  # Apply to all children of the reference

            # Create a "layerbreak" node called "LayerBreak"
            layerbreak = import_subnet.createNode("layerbreak", "LayerBreak")
            layerbreak.setPosition(transform_cm_to_m.position() + hou.Vector2(0, -1))

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
            # Connect the Transform node to the LayerBreak node
            layerbreak.setInput(0, transform_cm_to_m, 0)
            # Connect the LayerBreak node to the OUT_IMPORT node
            out_import.setInput(0, layerbreak, 0)
            # Connect the OUT_IMPORT node to the output0 node
            output0.setInput(0, out_import, 0)

        build_import_subnet()

        if variantsShareSameMaterials == "True":
            # Connect the import subnet to the switch node
            switch_import_node.setInput(j, import_subnet, 0)



    # Create a "mesh" node called "Mesh_edit"
    mesh_edit = parent_node.createNode("mesh", "Mesh_edit")
    mesh_edit.setPosition( hou.Vector2(0, -2))
    mesh_edit.parm("createprims").set(0)
    mesh_edit.parm("primpattern").set("%type:Boundable %type:Mesh")  # Apply to all the geometries
    mesh_edit.parm("subdivisionScheme_control").set("set")
    mesh_edit.parm("subdivisionScheme").set("catmullClark")  # Set subdivision scheme to Catmull-Clark
    mesh_edit.parm("triangleSubdivisionRule_control").set("set")
    mesh_edit.parm("triangleSubdivisionRule").set("catmullClark")  # Set triangle subdivision rule to Catmull-Clark

    # Create a "rendergeometrysettings" node called "Render_Geometry_Settings"
    render_geometry_settings = parent_node.createNode("rendergeometrysettings", "Render_Geometry_Settings")
    render_geometry_settings.setPosition(mesh_edit.position() + hou.Vector2(0, -2))
    render_geometry_settings.parm("primpattern").set("%type:Boundable %type:Mesh")  # Apply to all the geometries



    # Create a "MaterialLibrary" node called "Materials"
    material_library = parent_node.createNode("materiallibrary", "Materials")
    material_library.setColor(hou.Color(0.273, 0.627, 0.278)) # Green
    material_library.setPosition(render_geometry_settings.position() + hou.Vector2(0, -2))
    material_library.setParms({
        "matpathprefix": f"/{assetName}/mtl/"
    })

    # Create a "Assign Material" node called "Assign_Material"
    assign_material = parent_node.createNode("assignmaterial", "Assign_Material")
    assign_material.setColor(hou.Color(0.273, 0.627, 0.278)) # Green
    assign_material.setPosition(material_library.position() + hou.Vector2(0, -2))

    # Create a "SceneCleaning" subnet called "Scene_Cleaning"
    sceneCleaning_subnet = parent_node.createNode("subnet", "Scene_Cleaning")
    sceneCleaning_subnet.setColor(hou.Color(0.776, 0.157, 0.157)) # Red
    sceneCleaning_subnet.setPosition(assign_material.position() + hou.Vector2(0, -2))
    sceneCleaning_subnet.setComment("Ne pas toucher a ce node !")
    sceneCleaning_subnet.setGenericFlag(hou.nodeFlag.DisplayComment,True)

    # Create a null "OUT_SCENE_LOOKDEV" node
    out_scene_lookdev = parent_node.createNode("null", "OUT_SCENE_LOOKDEV")
    out_scene_lookdev.setPosition(sceneCleaning_subnet.position() + hou.Vector2(0, -2))

    def build_lookdev_scene():

        pass
    build_lookdev_scene()


    # Create a "Export" node
    export_node = parent_node.createNode("Thomas::BP_Export::1.0", "Publish")
    export_node.setColor(hou.Color(0.776, 0.776, 0.157))  # Yellow
    export_node.setPosition(out_scene_lookdev.position() + hou.Vector2(0, -2))
    export_node.parm("productName").set("Surf_Publish")
    if numberOfGroupsInt > 1:
        export_node.parm("productName").set(f"Surf_Publish{nodes_suffix}")
    export_node.parm("nextVersion").set(True)
    export_node.parm("updateMaster").set(True)
    export_node.parm("defaultprim").set(f"/{assetName}")
    export_node.setComment("Publier le surf lookdev")
    export_node.setGenericFlag(hou.nodeFlag.DisplayComment,True)


    # Create a "LOOKDEV_SCENE" subnet
    lookdev_scene = parent_node.createNode("Michel::LOOKDEV::1.5", "LOOKDEV_SCENE")
    lookdev_scene.setParms({
        "lookdevPath" : "//Minerva/3d5_2526/100_RESOURCES/Pipe/LookdevScene/",
        "asset_prim" : "/" + assetName,
        "lights_off" : False
    })
    lookdev_scene.setColor(hou.Color(0.776, 0.776, 0.157))  # Yellow
    lookdev_scene.setPosition(out_scene_lookdev.position() + hou.Vector2(-4, -2))



    #####################################
    #### Connect the nodes together #####
    #####################################
    
    # Materials -> Import
    if variantsShareSameMaterials == "True":
        import_subnet = switch_import_node
    
    # Mesh_edit -> Import
    mesh_edit.setInput(0, import_subnet, 0)
    # Render_Geometry_Settings -> Mesh_edit
    render_geometry_settings.setInput(0, mesh_edit, 0)
    # Materials -> Render_Geometry_Settings
    material_library.setInput(0, render_geometry_settings, 0)
    # Assign_Material -> Materials
    assign_material.setInput(0, material_library, 0)
    # SceneCleaning -> Assign_Material
    sceneCleaning_subnet.setInput(0, assign_material, 0)
    # OUT_SCENE_LOOKDEV -> SceneCleaning
    out_scene_lookdev.setInput(0, sceneCleaning_subnet, 0)
    # USD_OUTPUT -> OUT_SCENE_LOOKDEV
    export_node.setInput(0, out_scene_lookdev, 0)
    # LOOKDEV_SCENE -> OUT_SCENE_LOOKDEV
    lookdev_scene.setInput(0, out_scene_lookdev, 0)


    # Set the display flag on the "OUT_SCENE_LOOKDEV" node
    out_scene_lookdev.setDisplayFlag(True)


# Save the Houdini file
hou.hipFile.save(output_hip_path)