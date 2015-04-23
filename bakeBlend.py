import maya.cmds as mcoriTime = mc.currentTime(query=True)minTime = mc.playbackOptions(query=True, minTime=True)maxTime = mc.playbackOptions(query=True, maxTime=True)selection = mc.ls(selection=True)mc.currentTime(minTime)finalMesh = []for each in selection:	if mc.objectType(mc.pickWalk(each, direction='down')) == 'mesh':		mc.select(each, replace=True)		finalMesh += mc.duplicate()mc.currentTime(minTime + 1)frameStep = minTime + 1targets = []for each in selection:	if mc.objectType(mc.pickWalk(each, direction='down')) == 'mesh':		targets += [[]]c = 0while frameStep < maxTime + 1:	for each in selection:		if mc.objectType(mc.pickWalk(each, direction='down')) == 'mesh':			mc.select(each, replace=True)			targets[c] += mc.duplicate()			c += 1			c = 0	frameStep += 1	mc.currentTime(frameStep)c = 0blendShape = []for each in selection:	if mc.objectType(mc.pickWalk(each, direction='down')) == 'mesh':		mc.select(targets[c], replace=True)		mc.select(finalMesh[c], add=True)		blendShape += mc.blendShape(frontOfChain=True, inBetween=True)		c += 1c = 0while c < len(targets):	mc.delete(targets[c])	c += 1c = 0for each in selection:	if mc.objectType(mc.pickWalk(each, direction='down')) == 'mesh':		bsAttr = '.' + str(targets[c][len(targets[c]) - 1])						#to call list of list, example myVar[0][4]		mc.setKeyframe(blendShape[c] + bsAttr, value = 0, time = minTime)		mc.setKeyframe(blendShape[c] + bsAttr, value = 1, time = maxTime)		c += 1mc.select(finalMesh, replace=True)mc.currentTime(oriTime)