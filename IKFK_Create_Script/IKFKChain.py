
import maya.cmds as mc


#CREATE UI
def UI():
    windowID = "IKFK_UI"
    if(mc.window(windowID,q = True, exists = True)):
        mc.deleteUI(windowID)

    window = mc.window(windowID, title = "IK FK Window", rtf = True, s = True)
    windowLayout = mc.columnLayout(co = ("both", 10))

    #create IKFK Chain section UI
    mc.setParent(windowID)
    IKFKLayout = mc.frameLayout(l = "Create IK FK Chain", cll = True, w = 320)
    mc.text(h = 5, l = "")
    mc.text(l = "  Create an IKFK set up based on a given joint chain", al = "left")
    mc.text(h = 5, l = "")

    mc.setParent(IKFKLayout)
    mc.rowColumnLayout(nc = 2)
    mc.text(l = "  Joint name: (name to replace)     ", al = "left")
    JointNameField = mc.textField(vis = True, ed = True, w = 120, tx = "bn")
    mc.text(h = 10, l = "")
    mc.text(h = 10, l = "")
    firstJointBtn = mc.button(l = " First Joint:" , vis = True, c = lambda *x: assignTextField(firstJointField), w = 150)
    firstJointField = mc.textField(vis = True, ed = False, w = 150)
    lastJointBtn = mc.button(l = " Last Joint:", vis = True, c = lambda *x: assignTextField(lastJointField), w = 150)
    lastJointField = mc.textField( vis = True, ed = False, w = 150)

    mc.setParent(windowID)
    mc.setParent(IKFKLayout)
    StretchyLayout = mc.columnLayout()
    mc.text(h = 5, l = "")
    stretchyBtn = mc.checkBox( l = " Stretchy IK", v = True, onc = lambda *x: Show(StretchyScale, StretchyTranslate), ofc = lambda *x: Hide(StretchyScale, StretchyTranslate))

    mc.rowColumnLayout(nc = 2, columnWidth =[(1, 120)])
    StretchyMode = mc.radioCollection()
    StretchyTranslate = mc.radioButton("Translate", sl = True)
    StretchyScale = mc.radioButton("Scale")
    mc.setParent(StretchyLayout)

    mc.columnLayout()
    ScaleBtn = mc.checkBox( l = " Scalable Rig", v = True)
    mc.text(h = 5, l = "")
    OrientBtn = mc.checkBox( l = " Orient Joints (Check if the joint chain is not already oriented)", v = True)
    mc.text(h = 8, l = "")
    mc.button(l = "CREATE", w = 300, h = 50, c = lambda *x: IKFKChain(firstJointField, lastJointField, stretchyBtn, OrientBtn, IKCCSHape, FKCCSHape, Color, JointNameField, CCNameField, LocatorNameField, StretchyMode, ScaleBtn))
    mc.text(h = 12, l = "")

    #Change Controllers section UI
    mc.setParent(windowID)
    CClayout = mc.frameLayout(l = "Change Controllers (Optional)", cll = True, collapse = True, w = 320)
    mc.text(h = 5, l = "")
    mc.text(l = "  Change the shape and collor of IK and FK Controllers", al = "left")
    mc.text(h = 5, l = "")
    mc.text(l = "  Shape:", al = "left")
    mc.rowColumnLayout(nc = 2)
    mc.text(l = "  IK Controller:         ")
    IKCCSHape = mc.optionMenu(w = 150)
    mc.menuItem( label='Cube' )
    mc.menuItem( label='Circle' )
    mc.menuItem( label='Star' )
    mc.text(l = "  FK Controller:         ")
    FKCCSHape = mc.optionMenu(w = 150)
    mc.menuItem( label='Circle' )
    mc.menuItem( label='Cube' )
    mc.menuItem( label='Star' )
    mc.text(h = 20, l = "")
    mc.text(h = 20, l = "")

    mc.text(l = "  Color:", al = "left")
    Color = mc.optionMenu(w = 150)
    mc.menuItem( label='Red' )
    mc.menuItem( label='Blue' )
    mc.menuItem( label='Yellow' )
    mc.text(h = 10, l = "")
    mc.setParent(windowID)

    #Change Controllers section UI
    CClayout = mc.frameLayout(l = "Naming Convention (Optional)", cll = True, collapse = True, w = 320)
    mc.text(h = 5, l = "")
    mc.text(l = "  Determine the name of the resulted Chain elements", al = "left")
    mc.text(h = 5, l = "")
    mc.rowColumnLayout(nc = 2)
    mc.text(l = "  Controller name:    ", al = "left")
    CCNameField = mc.textField(vis = True, ed = True, w = 120, tx = "cc")
    mc.text(l = "  Locator name:    ", al = "left")
    LocatorNameField = mc.textField(vis = True, ed = True, w = 120, tx = "locAlign")
    mc.text(h = 5, l = "")
    mc.setParent(windowID)

    FirstJoint = mc.textField(firstJointField, q = True, tx = True)
    JointName = mc.textField(JointNameField, q = True, tx = True)

    #SHOW WINDOW
    mc.showWindow(windowID)
    return firstJointField, lastJointField, stretchyBtn, OrientBtn, IKCCSHape, FKCCSHape, Color, JointNameField, CCNameField, LocatorNameField, StretchyLayout, StretchyScale, StretchyTranslate, StretchyMode, ScaleBtn

def Show(StretchyScale, StretchyTranslate):
    mc.radioButton(StretchyScale, e = True, vis = True )
    mc.radioButton(StretchyTranslate,  e = True, vis = True)

def Hide(StretchyScale, StretchyTranslate):
    mc.radioButton(StretchyScale, e = True, vis = False)
    mc.radioButton(StretchyTranslate, e = True, vis = False)

def assignTextField(Field):

    selection = mc.ls(sl = True)
    if not mc.objectType(selection) == "joint":
        mc.confirmDialog( icn = "warning", title='ERROR!', message='The selection for the first joint must be of type: Joint', button=['OK'], ma='center')
    else:
        selectionString = ", ".join(selection)
        mc.textField(Field, e = True, tx = selectionString)

def orientJoints(FirstJoint):
    #Orient Joint Chain
    mc.joint(FirstJoint, e = True, oj = "xyz", sao = "yup", ch = True, zso = True)

def RenameChain(Chain, JointName, newName):

    mc.select(Chain[0], hi = True)
    selection = mc.ls(sl = True, dag=True, l=True)
    children = mc.listRelatives(selection, children=True, ad=True, f=True)
    for item in children:
        root,_,  tail =  item.rpartition("|")
        FinalName = tail.replace(JointName, newName)
        mc.rename(item, FinalName)

def createController(IKCCSHape, FKCCSHape, Color):

    #Define Color variables
    if Color == "Red":
        colorCode = 13
    elif Color == "Blue":
        colorCode = 6
    elif Color == "Yellow":
        colorCode = 17
    else:
        colorCode = 17

    #Create Controllers
    if IKCCSHape == "Cube":
        Controller = mc.curve(p=[(-1.0, 1.0, 1.0), (-1.0, 1.0, -1.0), (1.0, 1.0, -1.0),
                         (1.0, 1.0, 1.0), (-1.0, 1.0, 1.0), (-1.0, -1.0, 1.0),
                         (1.0, -1.0, 1.0), (1.0, -1.0, -1.0), (-1.0, -1.0, -1.0),
                         (-1.0, -1.0, 1.0), (-1.0, -1.0, -1.0), (-1.0, 1.0, -1.0),
                         (1.0, 1.0, -1.0), (1.0, -1.0, -1.0), (1.0, -1.0, 1.0), (1.0, 1.0, 1.0)],
                         k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], d=1, n= "temp_IK_name")

    if IKCCSHape == "Circle":
        Controller = mc.circle(d = 3, n= "temp_IK_name")
        mc.select(Controller[0] + ".cv[0:7]")
        mc.rotate(0, 90, 0)

    if IKCCSHape == "Star":
        Controller = mc.circle(d = 3, n= "temp_IK_name")
        mc.select(Controller[0] + ".cv[2]", Controller[0] + ".cv[0]", Controller[0] + ".cv[4]", Controller[0] + ".cv[6]")
        mc.scale(0, 0, 0, r = True)
        mc.select(Controller[0] + ".cv[0:7]")
        mc.rotate(0, 90, 0)
        mc.scale(2, 2, 2, r = True)

    if FKCCSHape == "Cube":
        Controller = mc.curve(p=[(-1.0, 1.0, 1.0), (-1.0, 1.0, -1.0), (1.0, 1.0, -1.0),
                         (1.0, 1.0, 1.0), (-1.0, 1.0, 1.0), (-1.0, -1.0, 1.0),
                         (1.0, -1.0, 1.0), (1.0, -1.0, -1.0), (-1.0, -1.0, -1.0),
                         (-1.0, -1.0, 1.0), (-1.0, -1.0, -1.0), (-1.0, 1.0, -1.0),
                         (1.0, 1.0, -1.0), (1.0, -1.0, -1.0), (1.0, -1.0, 1.0), (1.0, 1.0, 1.0)],
                         k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], d=1, n= "temp_FK_name")
    if FKCCSHape == "Circle":
        Controller = mc.circle(d = 3, n= "temp_FK_name")
        mc.select(Controller[0] + ".cv[0:7]")
        mc.rotate(0, 90, 0)

    if FKCCSHape == "Star":
        Controller = mc.circle(d = 3, n= "temp_FK_name")
        mc.select(Controller[0] + ".cv[2]", Controller[0] + ".cv[0]", Controller[0] + ".cv[4]", Controller[0] + ".cv[6]")
        mc.scale(0, 0, 0, r = True)
        mc.select(Controller[0] + ".cv[0:7]")
        mc.rotate(0, 90, 0)
        mc.scale(2, 2, 2, r = True)

    if FKCCSHape == None and IKCCSHape == None:
        #Diamond shape for Pole Vector
        Controller = mc.curve(d=1, p=[(0, 1, 0),(-1, 0.00278996, 6.18172e-08),(0, 0, 1),(0, 1, 0),(1, 0.00278996, 0),
                (0, 0, 1),(1, 0.00278996, 0),(0, 0, -1),(0, 1, 0),(0, 0, -1),
                (-1, 0.00278996, 6.18172e-08),(0, -1, 0),(0, 0 ,-1),(1, 0.00278996, 0),
                (0, -1, 0),(0, 0, 1)],k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], n = "temp_IKPoleVector_name")

    #Change Controller Color
    ControllerList = mc.ls(Controller)
    shapes = mc.listRelatives(ControllerList, s = True)
    for item in shapes:
        mc.setAttr(item + ".overrideEnabled", 1)
        mc.setAttr(item + ".overrideColor", colorCode)

def getRotationAxis(joint):
    '''Get the rotation axis from the translation in the IK Joints'''
    #Get the translation Values of the child joint
    translate = mc.getAttr(joint + ".t")[0]
    axis = ""

    for i, t in enumerate(translate):
        #CHeck which translation values has non-zero values
        value = abs(t)
        if value > .0001:
            if i ==0:
                axis ="x"
            elif i == 1:
                axis = "y"
            elif i == 2:
                axis = "z"
    if not axis:
        mc.error("Child joint is to close to it's parent")
    return axis

def stretchy(firstJoint, endJoint, IKHandle, StretchyMode, IKCCName, Scalable, scaleCC):

    # Init start and end joint attributes
    firstJoint = firstJoint
    endJoint = endJoint

    # Create the distance dimension
    startLocator = mc.spaceLocator(n="startDist_" + firstJoint)[0]
    mc.pointConstraint(firstJoint, startLocator, mo=False)
    endLocator = mc.spaceLocator(n="endDist_" + endJoint)[0]
    mc.xform(endLocator, ws=True, a = True, translation = mc.xform(IKHandle[0], q = True, ws = True, translation = True))
    mc.pointConstraint(IKHandle[0], endLocator, mo = False)

    #DistanceDimension
    distanceNode = mc.createNode("distanceDimShape", n = endJoint + "_shape_distance01")
    mc.rename("distanceDimension1", endJoint + "_distance01")
    mc.connectAttr(startLocator + "Shape.worldPosition[0]", distanceNode + ".startPoint")
    mc.connectAttr(endLocator + "Shape.worldPosition[0]", distanceNode + ".endPoint")

    if Scalable == True:
        scaledDistance = mc.createNode("multiplyDivide", n = IKHandle[0] + "_scaledDistance")
        mc.setAttr(scaledDistance + ".operation", 2) #Divide
        mc.connectAttr(scaleCC + ".Scale", scaledDistance + ".input2X", )
        mc.connectAttr(distanceNode + ".distance", scaledDistance + ".input1X")

    else:
        pass

    #Group Distance Nodes
    distanceGroup = mc.group(em= True, w = True, n = "grp_" + endJoint + "_distance01")
    mc.matchTransform(distanceGroup, firstJoint)
    mc.makeIdentity(distanceGroup, apply=True, translate=True, rotate=True)
    mc.parent(endJoint + "_distance01", startLocator, endLocator, distanceGroup)
    mc.setAttr(distanceGroup + ".v", 0)

    rotationAxis = getRotationAxis(endJoint)
    #Store original Joint Chain length
    originalLength = 0.0
    SumLength = 0.0
    #store childJoints
    childJoints = []
    currentJoint = firstJoint
    done = False
    while not done:
        #Get the child of the current joint
        children = mc.listRelatives(currentJoint, c = True)
        children = mc.ls(children, type="joint")

        #Reach the end of the chain
        if not children:
            done=True
        else:
            child = children[0]
            childJoints.append(child)
            #Summ up the length of the joints
            currentJoint = child
            #We reached the end of the stretchy IK
            if child == endJoint:
                done = True

    else:
        pass

    for child in childJoints:
        SumLength += mc.getAttr(child + ".t" + rotationAxis)

    if StretchyMode == "Scale":
        childJoints.remove(endJoint)
        childJoints.append(firstJoint)

    #Control constraint with IKCC attribute
    mc.connectAttr(IKCCName + ".Stretchy", "endDist_" + endJoint + "_pointConstraint1." + IKHandle[0] + "W0")

    for i in childJoints:
        originalLength = mc.getAttr(i + ".t" + rotationAxis)

        #divide Node to control Translation Value
        if Scalable == True:
            if StretchyMode == "Translate":
                stretchFactorNode = mc.createNode("multiplyDivide", n = IKHandle[0] + "_stretchFactor")
                mc.setAttr(stretchFactorNode + ".operation", 3) #Divide
                mc.setAttr(stretchFactorNode + ".input2X", SumLength)
                mc.connectAttr(scaledDistance + ".outputX", stretchFactorNode + ".input1X")

                #Multiply translation Value by the stretchFactor
                MultFactor = mc.createNode("multiplyDivide", n = IKHandle[0] + "_mult")
                mc.setAttr(stretchFactorNode + ".operation", 2) #Multiply
                mc.setAttr( MultFactor + ".input1X", originalLength )
                mc.connectAttr(stretchFactorNode + ".outputX", MultFactor + ".input2X")

                #Create a condition node to make stretchy just when distance is bigger than the original length
                conditionNode = mc.createNode("condition", n = firstJoint + "_condition")
                mc.setAttr(conditionNode + ".operation", 3)
                mc.connectAttr(scaledDistance + ".outputX", conditionNode + ".firstTerm")
                mc.setAttr(conditionNode + ".secondTerm", SumLength)
                mc.setAttr(conditionNode + ".colorIfFalseR", originalLength)
                mc.connectAttr(MultFactor + ".outputX", conditionNode + ".colorIfTrueR")

                #Connect to Joints
                mc.connectAttr(conditionNode + ".outColorR", i + ".t" + rotationAxis)

            elif StretchyMode == "Scale":
                stretchFactorNode = mc.createNode("multiplyDivide", n = IKHandle[0] + "_stretchFactor")
                mc.setAttr(stretchFactorNode + ".operation", 2) #Divide
                mc.setAttr(stretchFactorNode + ".input2X", SumLength)
                mc.connectAttr(scaledDistance + ".outputX", stretchFactorNode + ".input1X")

                conditionNode = mc.createNode("condition", n = firstJoint + "_condition")
                mc.setAttr(conditionNode + ".operation", 3)
                mc.connectAttr(scaledDistance + ".outputX", conditionNode + ".firstTerm")
                mc.setAttr(conditionNode + ".secondTerm", SumLength)
                mc.setAttr(conditionNode + ".colorIfFalseR", 1)
                mc.connectAttr(stretchFactorNode + ".outputX", conditionNode + ".colorIfTrueR")

                #Connect to Joints
                mc.connectAttr(conditionNode + ".outColorR", i + ".s" + rotationAxis)

        else:
            if StretchyMode == "Translate":
                stretchFactorNode = mc.createNode("multiplyDivide", n = IKHandle[0] + "_stretchFactor")
                mc.setAttr(stretchFactorNode + ".operation", 3) #Divide
                mc.setAttr(stretchFactorNode + ".input2X", SumLength)
                mc.connectAttr(distanceNode + ".distance", stretchFactorNode + ".input1X")

                #Multiply translation Value by the stretchFactor
                MultFactor = mc.createNode("multiplyDivide", n = IKHandle[0] + "_mult")
                mc.setAttr(stretchFactorNode + ".operation", 2) #Multiply
                mc.setAttr( MultFactor + ".input1X", originalLength )
                mc.connectAttr(stretchFactorNode + ".outputX", MultFactor + ".input2X")

                #Create a condition node to make stretchy just when distance is bigger than the original length
                conditionNode = mc.createNode("condition", n = firstJoint + "_condition")
                mc.setAttr(conditionNode + ".operation", 3)
                mc.connectAttr(distanceNode + ".distance", conditionNode + ".firstTerm")
                mc.setAttr(conditionNode + ".secondTerm", SumLength)
                mc.setAttr(conditionNode + ".colorIfFalseR", originalLength)
                mc.connectAttr(MultFactor + ".outputX", conditionNode + ".colorIfTrueR")

                #Connect to Joints
                mc.connectAttr(conditionNode + ".outColorR", i + ".t" + rotationAxis)

            elif StretchyMode == "Scale":
                stretchFactorNode = mc.createNode("multiplyDivide", n = IKHandle[0] + "_stretchFactor")
                mc.setAttr(stretchFactorNode + ".operation", 2) #Divide
                mc.setAttr(stretchFactorNode + ".input2X", SumLength)
                mc.connectAttr(distanceNode + ".distance", stretchFactorNode + ".input1X")

                conditionNode = mc.createNode("condition", n = firstJoint + "_condition")
                mc.setAttr(conditionNode + ".operation", 3)
                mc.connectAttr(distanceNode + ".distance", conditionNode + ".firstTerm")
                mc.setAttr(conditionNode + ".secondTerm", SumLength)
                mc.setAttr(conditionNode + ".colorIfFalseR", 1)
                mc.connectAttr(stretchFactorNode + ".outputX", conditionNode + ".colorIfTrueR")

                #Connect to Joints
                mc.connectAttr(conditionNode + ".outColorR", i + ".s" + rotationAxis)


def poleVectorPosition(startJnt, midJnt, endJnt):

	import maya.api.OpenMaya as om

	start = mc.xform(startJnt ,q= 1 ,ws = 1,t =1 )
	mid = mc.xform(midJnt ,q= 1 ,ws = 1,t =1 )
	end = mc.xform(endJnt ,q= 1 ,ws = 1,t =1 )
	startV = om.MVector(start[0] ,start[1],start[2])
	midV = om.MVector(mid[0] ,mid[1],mid[2])
	endV = om.MVector(end[0] ,end[1],end[2])

	startEnd = endV - startV
	startMid = midV - startV
	# projection vector is vecA projected onto vecB
	# it is calculated by dot product if one vector normalized

	# proj= vecA * vecB.normalized (dot product result is scalar)
	proj = startMid * startEnd.normal()

	# multiply proj scalar with normalized startEndVector to project it onto vector
	startEndN = startEnd.normal()
	projV = startEndN * proj

	arrowV = startMid - projV
	arrowVN = arrowV.normal()

	# scale up to length and offset to midV
	finalV = arrowVN*12 + midV

	loc = mc.spaceLocator(n='polePos')
	mc.xform(loc , ws =1 , t= (finalV.x , finalV.y ,finalV.z))
	return loc

	return finalV

def clean(cleanList, CCName, LocatorName):
    #Hide Locator Visibility
    for obj in cleanList:
        if not LocatorName == "":
            if LocatorName in obj and mc.objectType(obj) == "transform":
                mc.select(obj + "Shape")
                mc.setAttr(obj + "Shape" + ".lodVisibility", 0)
        if CCName in obj and mc.objectType(obj) == "transform":
            mc.setAttr(obj + ".sx", l = True, k = False, cb = False)
            mc.setAttr(obj + ".sy", l = True, k = False, cb = False)
            mc.setAttr(obj + ".sz", l = True, k = False, cb = False)
            mc.setAttr(obj + ".v", l = True, k = False, cb = False)

def IKFKChain(firstJointField, lastJointField, stretchyBtn, OrientBtn, IKCCSHape, FKCCSHape, Color, JointNameField, CCNameField, LocatorNameField, StretchyMode, ScaleBtn):

    FirstJoint = mc.textField(firstJointField, q = True, tx = True)
    LastJoint = mc.textField(lastJointField, q = True, tx = True)
    StretchyCHeckBox = mc.checkBox(stretchyBtn, q = True, v = True)
    Scalable = mc.checkBox(ScaleBtn, q = True, v = True)
    OrientJoints = mc.checkBox(OrientBtn, q = True, v = True)
    JointName = mc.textField(JointNameField, q = True, tx = True)
    LocatorName = mc.textField(LocatorNameField, q = True, tx = True)
    CCName = mc.textField(CCNameField, q = True, tx = True)
    IKCCSHape = mc.optionMenu(IKCCSHape, q = True, value = True)
    FKCCSHape = mc.optionMenu(FKCCSHape, q = True, value = True)
    Color = mc.optionMenu(Color, q = True, value = True)
    StretchyMode = mc.radioCollection(StretchyMode, q = True, sl = True)
    bindJoints = []
    IKJoints = []
    FKJoints = []
    FKCCList = []
    FKLocatorList = []

    if FirstJoint == "":
        mc.confirmDialog( icn = "warning", title='ERROR!', message='Please select the first Joint', button=['OK'], ma='center')
    elif LastJoint == "":
        mc.confirmDialog( icn = "warning", title='ERROR!', message='Please select the Last Joint', button=['OK'], ma='center')
    #Check if the first Joint exists when getting name
    elif JointName not in FirstJoint:
        mc.confirmDialog( icn = "warning", title='ERROR!', message='Joint name convention is not correct, '
                                                                   'make sure the first and last joint are named with the Joint name variable', button=['OK'], ma='center')
    elif JointName not in LastJoint:
        mc.confirmDialog( icn = "warning", title='ERROR!', message='Joint name convention is not correct, '
                                                                   'make sure the first and last joint are named with the Joint name variable', button=['OK'], ma='center')
    else:
        #Orient Joints just when Checked
        mc.makeIdentity(FirstJoint, apply=True, translate=True, rotate=True)
        if OrientJoints == True:
            orientJoints(FirstJoint)

        #Create IK and FK Joints
        FKJoint = mc.duplicate(FirstJoint, n=FirstJoint.replace(JointName, "FK"))
        RenameChain(Chain= FKJoint, JointName = JointName, newName = "FK")
        IKJoint = mc.duplicate(FirstJoint, n=FirstJoint.replace(JointName, "IK"))
        RenameChain(Chain= IKJoint, JointName = JointName, newName = "IK")

        #Check if there are children under last Joint
        mc.select(LastJoint, hi = True)
        selection = mc.ls(sl = True, dag=True, l=True)
        children = mc.listRelatives(selection, children=True, f=True)

        if children == None:
            pass
        else:
            #If there are children, delete children and duplicate joint chains
            mc.select(cl=True)
            mc.select(LastJoint.replace(JointName, "IK"), hi =True)
            IKselection = mc.ls(sl = True, dag=True, l=True)
            IKChildren = mc.listRelatives(IKselection, children=True, f=True)
            mc.delete(IKChildren)
            mc.select(LastJoint.replace(JointName, "FK"), hi =True)
            FKselection = mc.ls(sl = True, dag=True, l=True)
            FKChildren = mc.listRelatives(FKselection, children=True, f=True)
            mc.delete(FKChildren)

        #Store Joints in a variable
        mc.select(FKJoint[0], hi= True)
        FKSelection = mc.ls(sl = True)
        for item in FKSelection:
            FKJoints.append(item)

        mc.select(IKJoint[0], hi= True)
        IKSelection = mc.ls(sl = True)
        for item in IKSelection:
            IKJoints.append(item)

        mc.select(FirstJoint, hi= True)
        BindSelection = mc.ls(sl = True)
        for item in BindSelection:
            bindJoints.append(item)

        #Remove Joints under Last joint from Variable
        mc.select(LastJoint, hi = True)
        BindSelection = mc.ls(sl = True, dag=True, l=True)
        BindChildren = mc.listRelatives(BindSelection, children=True)
        if BindChildren == None:
            pass
        else:
            for i in BindChildren:
                bindJoints.remove(i)
        if OrientJoints == False:
            orientJoints(FirstJoint = IKJoints[0])
            orientJoints(FirstJoint = FKJoints[0])

        #Create IK Controller
        createController(IKCCSHape = IKCCSHape, FKCCSHape = None, Color = Color)
        IKCCName = mc.rename("temp_IK_name", LastJoint.replace(JointName, CCName + "_IK"))

        #Add Xtra Attributes
        if StretchyCHeckBox == True:
            mc.addAttr(IKCCName, ln="Settings", at = "enum", en = "_________")
            mc.setAttr(IKCCName + ".Settings", e = True, channelBox = True)
            mc.addAttr(IKCCName, ln = "Stretchy", at = "double", min = 0, max= 1, dv= 1, k = True)
        else:
            pass

        IKLocator = mc.spaceLocator(n = LocatorName + "_" + IKCCName)
        mc.parent(IKCCName, IKLocator)
        mc.matchTransform(IKLocator, LastJoint.replace(JointName, "IK"))

        #Create IK Handle
        mc.select(FirstJoint.replace(JointName, "IK"), LastJoint.replace(JointName, "IK"))
        IKHandle = mc.ikHandle(n = IKJoint[-1].replace(JointName, "IKHandle"))
        mc.parent(IKJoint[-1].replace(JointName, "IKHandle"), IKCCName)
        mc.setAttr(IKJoint[-1].replace(JointName, "IKHandle") + ".visibility",0)

        #Constraint and create connections IK Handle
        mc.orientConstraint(IKCCName, IKJoints[-1], mo = True)

        #Create Pole Vector
        #Get Pole Vector Position
        poleVectorPosition(startJnt = IKJoints[0], midJnt = IKJoints[1], endJnt = IKJoints[-1])

        #Create Pole Vector Controller
        createController(IKCCSHape = None, FKCCSHape = None, Color= Color)
        IKPoleVector = mc.rename("temp_IKPoleVector_name", LastJoint.replace(JointName, CCName + "_IK_poleVector"))

        IKPVLocator = mc.spaceLocator(n = LocatorName + "_" + IKPoleVector)
        mc.parent(IKPoleVector, IKPVLocator)
        mc.matchTransform(IKPVLocator, "polePos")
        mc.delete("polePos")

        #Constraint Pole Vector to IKHandle
        mc.poleVectorConstraint(IKPoleVector, IKJoint[-1].replace(JointName, "IKHandle"))

        #Create FK Controllers
        for joint in FKJoints:
            createController(IKCCSHape = None, FKCCSHape = FKCCSHape, Color = Color)
            FKCCName = mc.rename("temp_FK_name", joint.replace("FK", CCName + "_FK"))
            FKCCList.append(FKCCName)
            FKLocator = mc.spaceLocator(n = LocatorName + "_" + FKCCName)
            FKLocatorList.append(FKLocator)
            mc.parent(FKCCName, FKLocator)
            mc.matchTransform(FKLocator, joint)

            #Constraint to Joint
            mc.parentConstraint(FKCCName, joint, mo = True)

        #Parent controller under previous FK Controller
        for i in range(1, len(FKLocatorList)):
            mc.parent(FKLocatorList[i], FKCCList[i-1] )

        #Create IKFK Switch Controller
        IKFKSwitch = mc.curve(p=[(0, 0, -1), (1, 0, 0), (0, 0, 1),
                             (-1, 0, 0), (0, 0, -1)], d = 1, n = IKCCName.replace(CCName + "_IK", "IKFKSwitch"))
        IKFKSwitchLoc = mc.spaceLocator(n = LocatorName + IKFKSwitch)
        mc.parent(IKFKSwitch, IKFKSwitchLoc)
        mc.matchTransform(IKFKSwitchLoc, LastJoint)
        mc.parentConstraint(LastJoint, IKFKSwitchLoc, mo = True)

        #Change IKFKSwitch CC Shape and add custom attribute
        mc.select(IKFKSwitch + ".cv[0:4]")
        mc.rotate(0, 0, 90, r = True)
        mc.move(0, 3.5, 0, r = True, os = True, wd = True)
        mc.setAttr(IKFKSwitch + ".overrideEnabled", 1)
        mc.setAttr(IKFKSwitch + ".overrideColor", 17)
        mc.setAttr(IKFKSwitch + ".tx", k=False, l=True, channelBox=False)
        mc.setAttr(IKFKSwitch + ".ty", k=False, l=True, channelBox=False)
        mc.setAttr(IKFKSwitch + ".tz", k=False, l=True, channelBox=False)
        mc.setAttr(IKFKSwitch + ".rx", k=False, l=True, channelBox=False)
        mc.setAttr(IKFKSwitch + ".ry", k=False, l=True, channelBox=False)
        mc.setAttr(IKFKSwitch + ".rz", k=False, l=True, channelBox=False)
        mc.setAttr(IKFKSwitch + ".sx", k=False, l=True, channelBox=False)
        mc.setAttr(IKFKSwitch + ".sy", k=False, l=True, channelBox=False)
        mc.setAttr(IKFKSwitch + ".sz", k=False, l=True, channelBox=False)
        mc.setAttr(IKFKSwitch + ".v", k=False, l=True, channelBox=False)
        mc.addAttr(IKFKSwitch, ln='IKFKSwitch',at='float',min=0,max=1,dv=1, k=True)

        mc.select(cl = True)

        #Clean Scene Number 1
        CCGroup = mc.group(em = True, w = True, n = "grp_" + LastJoint.replace(JointName, CCName))
        mc.matchTransform(CCGroup, FirstJoint)
        mc.makeIdentity(CCGroup, apply=True, translate=True, rotate=True)
        IKCCGroup = mc.group(em = True, w = True, n = "grp_IK_" + LastJoint.replace(JointName, CCName))
        mc.matchTransform(IKCCGroup, FirstJoint)
        mc.makeIdentity(IKCCGroup, apply=True, translate=True, rotate=True)
        FKCCGroup = mc.group(em = True, w = True, n = "grp_FK_" + LastJoint.replace(JointName, CCName))
        mc.matchTransform(FKCCGroup, FirstJoint)
        mc.makeIdentity(FKCCGroup, apply=True, translate=True, rotate=True)
        DriverBonesGroup = mc.group(em = True, w = True, n = "grp_Driver_" + LastJoint)
        mc.matchTransform(DriverBonesGroup, FirstJoint)
        mc.makeIdentity(DriverBonesGroup, apply=True, translate=True, rotate=True)

        mc.setAttr(DriverBonesGroup + ".v", 0)
        mc.parent(IKCCGroup, FKCCGroup, CCGroup)
        mc.parent(FKJoints[0], DriverBonesGroup)
        mc.parent(IKJoints[0], DriverBonesGroup)
        mc.parent(IKLocator, IKCCGroup)
        mc.parent(IKPVLocator, IKCCGroup)
        mc.parent(FKLocatorList[0], FKCCGroup)
        mc.parent(IKFKSwitchLoc, CCGroup)

        #Create Connections to Bind Joints
        IKRevNode01 = mc.shadingNode('reverse', asUtility=True, n="reverse_" + IKFKSwitch)
        mc.connectAttr(IKFKSwitch + ".IKFKSwitch", IKRevNode01 + ".inputX" )
        for j in range(0, len(bindJoints)):
            PConstraint = mc.parentConstraint(FKJoints[j], IKJoints[j], bindJoints[j], mo = True)
            Sconstraint = mc.scaleConstraint(FKJoints[j], IKJoints[j], bindJoints[j], mo = True)
            #Control Joints
            mc.connectAttr(IKFKSwitch + ".IKFKSwitch", PConstraint[0] + "." + IKJoints[j] + "W1")
            mc.connectAttr(IKRevNode01 + ".output.outputX", PConstraint[0] + "." + FKJoints[j] + "W0")
            mc.connectAttr(IKFKSwitch + ".IKFKSwitch", Sconstraint[0] + "." + IKJoints[j] + "W1")
            mc.connectAttr(IKRevNode01 + ".output.outputX", Sconstraint[0] + "." + FKJoints[j] + "W0")

        #Control CC Visibility
        mc.connectAttr(IKFKSwitch + ".IKFKSwitch", IKCCGroup + ".visibility")
        mc.connectAttr(IKRevNode01 + ".output.outputX", FKCCGroup + ".visibility")

        #Clean Scene
        #Group everything under group
        RigGroup = mc.group(em= True, w = True, n = "grp_" + LastJoint.replace(JointName + "_", "") + "_rig01")
        mc.matchTransform(RigGroup, FirstJoint)
        mc.makeIdentity(RigGroup, apply=True, translate=True, rotate=True)
        mc.parent(CCGroup, DriverBonesGroup, RigGroup)

        if Scalable == True:
            scaleCC = mc.curve(d = 1, p=[(-1.0, 0, -1.0), (1.0, 0, -1.0), (1.0, 0, 1.0),
                         (-1.0, 0, 1.0), (-1, 0, -1)], n = FirstJoint.replace(JointName, CCName) + "_scale")
            #Change Color
            IKShape = mc.listRelatives(IKCCName, s = True)
            IKColor = mc.getAttr(IKShape[0] + ".overrideColor")
            scaleCCShape = mc.listRelatives(scaleCC, s = True)
            mc.setAttr(scaleCCShape[0] + ".overrideEnabled", 1)
            mc.setAttr(scaleCCShape[0] + ".overrideColor", IKColor)

            #Change shape
            mc.select(scaleCC + ".cv[0:4]")
            mc.rotate(0, 0, -90, r = True)

            #Customize attributes
            mc.setAttr(scaleCC + ".sx", k=False, l=True, channelBox=False)
            mc.setAttr(scaleCC + ".sy", k=False, l=True, channelBox=False)
            mc.setAttr(scaleCC + ".sz", k=False, l=True, channelBox=False)
            mc.setAttr(scaleCC + ".v", k=False, l=True, channelBox=False)
            mc.addAttr(scaleCC, ln='Scale',at='float',min=0.01,dv=1, k=True)

            #Connect
            scaleLocator = mc.spaceLocator(n = LocatorName + "_" + scaleCC)
            mc.setAttr(scaleLocator[0] + "Shape" + ".lodVisibility", 0)
            mc.parent(scaleCC, scaleLocator)
            mc.matchTransform(scaleLocator, FirstJoint)
            aimConst = mc.aimConstraint(LastJoint, scaleLocator, offset = (0,0, 0), aimVector = (1, 0, 0), worldUpType = "vector", worldUpVector = (0, 1, 0))
            mc.delete(aimConst)
            mc.parent(RigGroup, scaleCC)
            mc.parentConstraint(scaleCC, RigGroup, mo=True)
            mc.connectAttr(scaleCC + ".Scale", RigGroup + ".sx")
            mc.connectAttr(scaleCC + ".Scale", RigGroup + ".sy")
            mc.connectAttr(scaleCC + ".Scale", RigGroup + ".sz")

        else:
            pass

        if StretchyCHeckBox == True:
            stretchy(firstJoint = IKJoints[0], endJoint = IKJoints[-1], IKHandle = IKHandle, StretchyMode = StretchyMode, IKCCName = IKCCName,Scalable = Scalable, scaleCC = scaleCC)
        else:
            pass

        if mc.objExists("grp_" + IKJoints[-1] + "_distance01"):
            mc.parent("grp_" + IKJoints[-1] + "_distance01", RigGroup)
        else:
            pass

        #Run Clean command
        mc.select(RigGroup, hi=True)
        cleanList=  mc.ls(type= "transform", sl=True)
        clean(cleanList, CCName, LocatorName)
        mc.select(cl = True)
        print "Succesfully created IK FK Chain"



