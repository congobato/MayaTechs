// IK FK Chain
// version 1.01
// February 03, 2021
// Ignacio Zorrilla
// izbarbera94@gmail.com


NOTES

DESCRIPTION:
	This script lets you create an IK FK joint set up based on a given joint chain. The resulted group will control the whole rig. 
	
	

INSTALLATION:
	a) Copy the file (IKFKChain.py) to your Maya scripts directory. On Windows that is Documents/maya/20xx/scripts/
	
	b) Open Maya. In the Script Editor (Python), past the following code:
	import IKFKChain
	reload(IKFKChain)
	IKFKChain.UI()
	
	c) Hit execute (or Ctrl Enter)
	

USAGE:
	- Select the first joint of the joint chain from which you want to create the IK FK set up and hit "First Joint:"
	- Select the last Joint of the joint chain (does not have to be the last joint of the chain, just the joint that will be parenting the effector)
	and hit "Last Joint:"
	- Customize controllers shape and color
	- Customize naming convenction
	- Hit "CREATE"


LIMITATIONS:

	Future Improvements/Optimzations planned:
	 -   Make an option to mirror the set up based on given search and replace names

