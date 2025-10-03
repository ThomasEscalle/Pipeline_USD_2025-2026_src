try: 			
    import maya.standalone 			
    maya.standalone.initialize() 		
except: 			
    pass


import maya.cmds as cmds
import os
import maya.api.OpenMaya as om2

# Autorig maya for Props
# It :
# - Create a new scene
# - Import the usd file
# - Create a hierarchy
# - Create the necessary nodes for autorigging

# Hierarchy de groupes :
# - chaise
#     - Asset_root
#       - geo
#         - render
#            - <Les geos viennent ici, sans leurs groupes parent.. A voir comment gerer les references ?? > 
#     - GlobalMove_01
#          - Joints_01
#          - CTRLs_01
#          - IKs_01
#     - RelaySystem_01
#     - ExtraNodes_01
#          - ExtraNodes_To_Show_01
#          - ExtraNodes_To_Hide_01


asset_path = "$$REFERENCE_PATH$$"  # The path to the USD file to import
asset_type = "$$TYPE_ASSET$$"   # The type of the asset (Prop, Vehicle, Creature, etc.)
asset_name = "$$ASSET_NAME$$"   # The name of the asset without type prefix

position = "$$CTRL_PLACEMENTS$$" # centered, bottom, top
save_path = "$$OUTPUT_PATH$$"    # The path to save the Maya file

subdiv_level = "$$SUBDIV_LEVEL$$" # The subdivision level to apply to the geometry (rigl or righ) 

def setColor(obj, color ):

    # If the color is empty, we return
    if color == "":
        print("Invalid color : " + color)
        return


    # If the color is not valid (size != 7), we return
    if len(color) != 7:
        print("Invalid color : " + color)
        return
    
    # If the object is a list, we iterate over it
    # and call the function recursively
    if type(obj) == list:
        for o in obj:
            setColor(o, color)
        return
    
    # Get the color as RGB
    r = int(color[1:3], 16) / 255
    g = int(color[3:5], 16) / 255
    b = int(color[5:7], 16) / 255

    # Round the values
    r = round(r, 3)
    g = round(g, 3)
    b = round(b, 3)

    # Convert the color to display space
    colorV = [r , g , b]
    colorVdp = cmds.colorManagementConvert(toDisplaySpace=[colorV[0], colorV[1], colorV[2]])


    # Set the color in the viewport
    cmds.setAttr(obj + ".overrideEnabled", 1)
    cmds.setAttr(obj + ".overrideRGBColors", 1)
    cmds.setAttr(obj + ".overrideColorRGB", colorV[0], colorV[1], colorV[2])

    # Color in the outliner
    cmds.setAttr(obj + ".useOutlinerColor", 1)
    cmds.setAttr(obj + ".outlinerColor", colorVdp[0], colorVdp[1], colorVdp[2])


    # Get the shapes of the object
    shapes = cmds.listRelatives(obj, shapes=True)

    # If the object has shapes, we color them
    if shapes is not None:
        for shape in shapes:
            cmds.setAttr(shape + ".overrideEnabled", 1)
            cmds.setAttr(shape + ".overrideRGBColors", 1)
            cmds.setAttr(shape + ".overrideColorRGB", colorV[0], colorV[1], colorV[2])



def build():
    cmds.file(new=True, force=True)

    # Make sure the AbcImport plugin is loaded
    if not cmds.pluginInfo("AbcImport", query=True, loaded=True):
        cmds.loadPlugin("AbcImport")
    # Make sure the AbcExport plugin is loaded
    if not cmds.pluginInfo("AbcExport", query=True, loaded=True):
        cmds.loadPlugin("AbcExport")
    # Make sure the mayaUsdPlugin plugin is loaded
    if not cmds.pluginInfo("mayaUsdPlugin", query=True, loaded=True):
        cmds.loadPlugin("mayaUsdPlugin")



    # Import the USD file
    result = cmds.file(asset_path, i=True, returnNewNodes=True)
    imported_nodes = result if result else []

    # Crée les groupes standards
    group_name = asset_name
    grp = cmds.group(empty=True, name=group_name)

    # Crées les groupes standards
    grp_asset_root = cmds.group(empty=True, name="Asset_root")
    grp_geo = cmds.group(empty=True, name="geo")
    if subdiv_level == "righ":
        grp_render = cmds.group(empty=True, name="render")
    else:
        grp_render = cmds.group(empty=True, name="proxy")  # Proxy because we are in Riggin 'LOW'

    grp_globalMove = cmds.group(empty=True, name="GlobalMove_01")
    grp_joints = cmds.group(empty=True, name="Joints_01")
    grp_ctrls = cmds.group(empty=True, name="CTRLs_01")
    grp_IKs = cmds.group(empty=True, name="IKs_01")
    grp_relaySystem = cmds.group(empty=True, name="RelaySystem_01")
    grp_extraNodes = cmds.group(empty=True, name="ExtraNodes_01")
    grp_extraNodesToShow = cmds.group(empty=True, name="ExtraNodes_To_Show_01")
    grp_extraNodesToHide = cmds.group(empty=True, name="ExtraNodes_To_Hide_01")

    # Parent les groupes
    cmds.parent(grp_asset_root, grp)
    cmds.parent(grp_geo, grp_asset_root)
    cmds.parent(grp_render, grp_geo)
    cmds.parent(grp_globalMove, grp)
    cmds.parent(grp_joints, grp_globalMove)
    cmds.parent(grp_ctrls, grp_globalMove)
    cmds.parent(grp_IKs, grp_globalMove)
    cmds.parent(grp_relaySystem, grp)
    cmds.parent(grp_extraNodes, grp)
    cmds.parent(grp_extraNodesToShow, grp_extraNodes)
    cmds.parent(grp_extraNodesToHide, grp_extraNodes)

    # Set the outliner color of the root group to blue
    cmds.setAttr(grp + ".useOutlinerColor", 1)
    cmds.setAttr(grp + ".outlinerColor", 0, 0.847, 0.813, type="double3")




    def is_top_level_transform(node):
        if not cmds.objectType(node, isType='transform'):
            return False
        parents = cmds.listRelatives(node, parent=True)
        return not parents
    
    top_level_transforms = [n for n in imported_nodes if is_top_level_transform(n)]
    for node in top_level_transforms:
        try:
            children = cmds.listRelatives(node, children=True, fullPath=True) or []
            for child in children:
                cmds.parent(child, grp_render)
            # After reparenting children, delete the empty parent node
            cmds.delete(node)
        except Exception:
            print("Error while deleting node:", node)
            pass


    # Autorig :

    # Get the bounding box of the geometry group
    bbox = cmds.exactWorldBoundingBox(grp_geo)

    # Calculate the center of the bounding box
    center_x = (bbox[0] + bbox[3]) / 2.0
    center_y = (bbox[1] + bbox[4]) / 2.0
    center_z = (bbox[2] + bbox[5]) / 2.0

    # Get the biggest dimension between width and depth, to set the radius of the control curve
    width = bbox[3] - bbox[0]
    depth = bbox[5] - bbox[2]
    height = bbox[4] - bbox[1]
    max_dimension = max(width, depth)

    radius = (max_dimension / 2.0 ) # Add a little padding

    # Create 3 Controll curves, one inside the other
    # - Ctrl_Global
    #  - Ctrl_Main_01
    #   - Ctrl_Main_02

    position_x = 0
    position_y = 0
    position_z = 0

    if position == "bottom":
        position_y = bbox[1]
    elif position == "top":
        position_y = bbox[4]

    # Create the control curves at the center of the bounding box
    ctrl_curve_global = cmds.circle(name="Ctrl_Global", center=(0, 0, 0), normal=(0, 1, 0), radius=radius * 1.4)[0]
    ctrl_curve_main_01 = cmds.circle(name="Ctrl_Main_01", center=(0, 0, 0), normal=(0, 1, 0), radius=radius * 1.3)[0]
    ctrl_curve_main_02 = cmds.circle(name="Ctrl_Main_02", center=(0, 0, 0), normal=(0, 1, 0), radius=radius * 1.2)[0]

    # Move the control curves to the center of the bounding box
    cmds.move(position_x, position_y, position_z, ctrl_curve_global)
    cmds.move(position_x, position_y, position_z, ctrl_curve_main_01)
    cmds.move(position_x, position_y, position_z, ctrl_curve_main_02)

    # Freeze transformations on the control curves
    cmds.makeIdentity(ctrl_curve_global, apply=True, translate=1, rotate=1, scale=1, normal=0)
    cmds.makeIdentity(ctrl_curve_main_01, apply=True, translate=1, rotate=1, scale=1, normal=0)
    cmds.makeIdentity(ctrl_curve_main_02, apply=True, translate=1, rotate=1, scale=1, normal=0)


    # Add color to the control curves
    setColor(ctrl_curve_global, "#FFA419") # Orange
    setColor(ctrl_curve_main_01, "#E4BD20") # Yellow
    setColor(ctrl_curve_main_02, "#E4BD20") # Yellow
    # Set the line width of the ctrl_curve_global
    cmds.setAttr(ctrl_curve_global + ".lineWidth", 2)


    # Parent the control curves
    cmds.parent(ctrl_curve_global, grp_ctrls)
    cmds.parent(ctrl_curve_main_01, ctrl_curve_global)
    cmds.parent(ctrl_curve_main_02, ctrl_curve_main_01)

    # Create the joints
    joint = cmds.joint(name="Bin_Jnt_Root", position=(center_x, center_y, center_z))
    cmds.parent(joint, grp_joints)

    # Create a parent constraint from the control curve to the joint
    cmds.parentConstraint(ctrl_curve_main_02, joint, maintainOffset=True)
    # Create a scale constraint from the control curve to the joint
    cmds.scaleConstraint(ctrl_curve_main_02, joint, maintainOffset=True)

    # Get all the geometry shapes under grp_geo
    geo_shapes = cmds.listRelatives(grp_geo, allDescendents=True, type='mesh', fullPath=True) or []

    # Bind the geometry to the joint using skinCluster
    if geo_shapes:
        for shape in geo_shapes:
            cmds.select(shape, replace=True)
            cmds.select(joint, add=True)
            cmds.skinCluster(toSelectedBones=True, bindMethod=0, skinMethod=0, normalizeWeights=1)

    cmds.file(rename=save_path)
    cmds.file(save=True, type='mayaAscii')

build()