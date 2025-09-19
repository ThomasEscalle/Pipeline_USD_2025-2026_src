# Maya script to create a motion path rig with control curves
# It consist in a curve, with several controlls.
# Than there is a rebuild curve to adjust the resolution
# And finally a controll will be attached to the curve using a U coordinate
import maya.cmds as cmds



def createCurveRig( numberOfControls ):
    # Create smooth curve, with the same number of points as controls
    points = []
    for i in range(numberOfControls):
        points.append( (i*2, 0, 0) )
    curve = cmds.curve( d=3, p=points )

    # Add one control for each point
    controls = []
    for i in range(numberOfControls):
        ctrl = cmds.circle( name="ctrl_{}".format(i), radius=0.5 , normal=(0,1,0) )[0]
        cmds.move(i*2, 0, 0, ctrl)
        # Freeze transformations
        # cmds.makeIdentity(ctrl, apply=True, t=1, r=1, s=1, n=0)

        # Connect the translation of the control to the curve point
        cmds.connectAttr( ctrl + ".translate", curve + ".controlPoints[{}]".format(i) )

        controls.append(ctrl)


    # Rebuild the curve to have a smoother result
    rebuiltCurve = cmds.createNode( "rebuildCurve", name="rebuiltCurve" )
    cmds.connectAttr( curve + ".worldSpace[0]", rebuiltCurve + ".inputCurve" )
    cmds.setAttr( rebuiltCurve + ".rebuildType", 0 ) # 0 = uniform
    cmds.setAttr( rebuiltCurve + ".degree", 3 )
    cmds.setAttr( rebuiltCurve + ".spans", 40 )

    # Create a shape curve to visualize the rebuilt curve
    shapeCurve = cmds.curve( d=3, p=[(0,0,0), (1,0,0)] )
    shapeNode = cmds.listRelatives( shapeCurve, shapes=True )[0]
    cmds.connectAttr( rebuiltCurve + ".outputCurve", shapeNode + ".create" )


    # Create a pointoncurveInfo node to get the position on the curve
    pointOnCurve = cmds.createNode( "pointOnCurveInfo", name="pointOnCurve" )
    cmds.connectAttr( rebuiltCurve + ".outputCurve", pointOnCurve + ".inputCurve" )
    cmds.setAttr( pointOnCurve + ".turnOnPercentage", 1 ) # Use percentage for U parameter

    # Create a locator to follow the curve
    locator = cmds.spaceLocator( name="curveLocator" )[0]
    cmds.connectAttr( pointOnCurve + ".position", locator + ".translate" )

    # Add an attribute on the locator to control the U parameter
    cmds.addAttr( locator, longName="uParam", attributeType="float", min=0, max=1, defaultValue=0 )
    cmds.connectAttr( locator + ".uParam", pointOnCurve + ".parameter" )

    # Return the created curve
    return curve, controls

createCurveRig(12)