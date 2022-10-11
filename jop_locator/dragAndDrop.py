import os

try:
    import maya.mel as mel
    import maya.cmds as mc
    import shutil
    isMaya = True
except ImportError:
    isMaya = False

def isWritable(fileToCheck):
    if os.path.exists(fileToCheck):
        if os.path.isfile(fileToCheck):
            return os.access(fileToCheck, os.W_OK)
    else:
        return True


def defineScriptCommand(scriptName,mayaScriptDir,function):
    command = '''
# -----------------------------------
# {myScriptName}
# Copyright (c) <2021> <JesseOngPho>
# jesseongpho@hotmail.com
# -----------------------------------

import os
import sys
from imp import reload

if not os.path.exists(r'{path}'):
    mc.error( r'The source path "{path}" does not exist!')
if r'{path}' not in sys.path:
    sys.path.insert(0, r'{path}')

import {myScriptName}
reload({myScriptName})
{myScriptName}.{myCommand}()
 
'''.format(myScriptName = scriptName,path=mayaScriptDir, myCommand=function)
    return command
        
def createShelfButton(scriptName,mayaScriptDir,iconsToCopy):
    #Check if the current shelf is non-writable
    shelftoplevel = mel.eval("$gShelfTopLevel = $gShelfTopLevel;")
    active_shelf = mc.tabLayout(shelftoplevel, query=True,selectTab=True)

    if not isWritable(str(mc.internalVar(userPrefDir=True) + 'shelves/shelf_' + active_shelf + '.mel')):
        mc.confirmDialog(title='Can\'t install',icon = 'warning', message='The current shelf is non-writable. Select another shelf and try the installation again')

    else:
        command = defineScriptCommand(scriptName,mayaScriptDir,'main')
        menuCommand1 = defineScriptCommand(scriptName,mayaScriptDir, 'timeSliderKeyframes' )
        menuCommand2 = defineScriptCommand(scriptName,mayaScriptDir, 'timeSliderEveryFrames' )
        menuCommand3 = defineScriptCommand(scriptName,mayaScriptDir, 'timeSliderWorldSpaceDriver' )
        
        menuCommand4 = defineScriptCommand(scriptName,mayaScriptDir, 'allKeysKeyframes' )
        menuCommand5 = defineScriptCommand(scriptName,mayaScriptDir, 'allKeysEveryFrames' )
        menuCommand6 = defineScriptCommand(scriptName,mayaScriptDir, 'allKeysWorldSpaceDriver' )
        
        menuCommand7 = defineScriptCommand(scriptName,mayaScriptDir, 'zeroGrpOnCurrentFrame' )
        menuCommand8 = defineScriptCommand(scriptName,mayaScriptDir, 'zeroGrpConstraint' )
        menuCommand9 = defineScriptCommand(scriptName,mayaScriptDir, 'zeroGrpBake' )
        noAction =  defineScriptCommand(scriptName,mayaScriptDir, 'noAction' )
        shelf = mel.eval('$gShelfTopLevel=$gShelfTopLevel')
        parent = mc.tabLayout(shelf, query=True, selectTab=True)
        
        #Create the button with all the attributes
        mc.shelfButton(
            command=command,
            annotation=scriptName+'\n1) Select controller(s).\n2) Click on the locator icon.\nRight click to see option' ,
            sourceType='Python',
            image=iconsToCopy,
            menuItem = [('----------- Range : Time Slider -----',noAction),('On Every frames', menuCommand2),('On Keyframes', menuCommand1),('World space Driver', menuCommand3),('----------- Range : All Keys ---------',noAction),('On Every frames', menuCommand5),('On Keyframes', menuCommand4),('World space Driver', menuCommand6),('----------- Zero Group  --------------',noAction),('On Current Frame', menuCommand7),('Parent Constraint', menuCommand8),('Time Slider Bake', menuCommand9)],
            menuItemPython = [0,1,2,3,4,5,6,7,8,9,10,11,12],
            parent=parent,
            label=scriptName
         )

        mc.inViewMessage( amg=(scriptName+  " has been added to the current shelf."), pos='midCenter', fade=True)

def getScriptName():
    installPath = (os.path.realpath(__file__)) 
    scriptName = installPath.split(os.sep)[-2]
    return scriptName
    
def fileSetup(scriptName):
#currentLocation
    installPath = (os.path.realpath(__file__)) 
    currentFolder = installPath.split('dragAndDrop.py') [0]
    iconsToCopy = currentFolder+ scriptName+"_icon.png"
    scriptToCopy= currentFolder+ scriptName+".py"
    
    #target directories

    mayaPref = os.path.normpath(mc.internalVar(userPrefDir=True))
    mayaIconTraget = os.sep.join([mayaPref, 'icons',scriptName+"_icon.png"])
    mayaScriptDir = os.sep.join([mayaPref, 'scripts'])
    print(mayaPref, mayaIconTraget, mayaScriptDir)
    
    #check if the files are at the good location
    if not os.path.exists(iconsToCopy):
        mc.error('The icon is missing. Make sure the icon file is in the installation folder' )
    if not os.path.exists(scriptToCopy):
        mc.error('The script is missing. Make sure the script file is in the installation folder' )
    
    return iconsToCopy, mayaIconTraget,scriptToCopy, mayaScriptDir

#When Drag and Drop
def onMayaDropped(*args, **kwargs):
    scriptName = getScriptName()

    iconsToCopy, mayaIconTraget,scriptToCopy, mayaScriptDir = fileSetup(scriptName)
    
    #copy the icon and the python script to maya preferences.
    shutil.copy( iconsToCopy, mayaIconTraget)
    shutil.copy( scriptToCopy, mayaScriptDir)

    createShelfButton (scriptName,mayaScriptDir,mayaIconTraget)
    
if isMaya:
    onMayaDropped()
