__author__ = 'ginyih'

from maya import cmds

def curveShapeReplacer(selection):
	'''
	Replace curve shape without altering the pivot and transformation. **Mainly for rig use, changing the appearance of rig controller curves for better design and usability.**

	Usage:	Select old curve -> new curve -> curveShapeReplacer( cmds.ls( selection = True ) )

	:param selection: Curve(s) selection
	:type selection: str
	'''

	oldCurve = selection[::2]
	newCurve = selection[1::2]

	if selection:

		c = 0
		for each in oldCurve:

			try:
				if newCurve[c]:

					oldCurveShape = cmds.listRelatives( each, shapes = True, fullPath = True )[0]
					newCurveShape = cmds.listRelatives( newCurve[c], shapes = True, fullPath = True )[0]

					cmds.select( '%s.cv[*]' %(newCurveShape), replace = True )
					curveSpans = len( cmds.ls( selection = True, flatten = True ) )

					preservePos = []
					for each2 in range(curveSpans):
						preservePos.append( cmds.xform( '%s.cv[%s]' %(newCurveShape, each2), query = True, translation = True, worldSpace = True ) )

					newCurveShape = cmds.parent( newCurveShape, each, addObject = True, shape = True )[0]
					cmds.delete( oldCurveShape, newCurve[c] )

					count = 0
					for each3 in preservePos:
						cmds.xform( '%s.cv[%s]' %(newCurveShape, count), translation = [each3[0], each3[1], each3[2]], worldSpace = True )
						count += 1

					cmds.select( clear = True )

					c += 1

			except:
				pass