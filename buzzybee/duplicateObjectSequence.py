import maya.cmds as cmds

selection = cmds.ls(selection=True)

min = cmds.playbackOptions(query=True, minTime=True)
max = cmds.playbackOptions(query=True, maxTime=True)

int = 0
dupe = []

cmds.currentTime(min)
while cmds.currentTime(query=True) <= max :

	dupe.append(cmds.duplicate(selection)[0])
	
	cmds.setKeyframe(dupe[int], attribute = 'visibility', value = 0, time = [cmds.currentTime(query=True) - 1, cmds.currentTime(query=True) - 1] )
	cmds.setKeyframe(dupe[int], attribute = 'visibility', value = 1, time = [cmds.currentTime(query=True), cmds.currentTime(query=True)] )
	cmds.setKeyframe(dupe[int], attribute = 'visibility', value = 0, time = [cmds.currentTime(query=True) + 1, cmds.currentTime(query=True) + 1] )

	int += 1
	cmds.currentTime(min + int)
	
cmds.group(dupe, name='%s_duplicateSequence_GRP' %(selection))