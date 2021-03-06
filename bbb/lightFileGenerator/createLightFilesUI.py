from maya import cmds, mel
import re, os
import sys;	sys.path.append('T:/bubblebathbay_APPDIR/ginyih/2013.5-x64/scripts')
import createLightFiles as clf
reload(clf)

def createLightFilesUI():
	if cmds.window('createLightFiles', q = True, exists = True):
		cmds.deleteUI('createLightFiles')
		cmds.windowPref('createLightFiles', remove = True)
	
	cmds.window('createLightFiles')
	cmds.columnLayout('clf_mainLayout', adjustableColumn = True, columnOffset = ('both', 5), height = 268, width = 221)
	
	cmds.text(label = 'Static ENVs')
	cmds.separator(height = 5)
	cmds.text(label = '')
	
	cmds.rowColumnLayout(numberOfColumns = 3, columnAlign = ([3, 'left']))
	cmds.checkBox('checkBox_010', label = '', value = True)
	cmds.text(label = '')
	cmds.text(label = 'ep000_sh010 ', align = 'left')
	cmds.checkBox('checkBox_020', label = '', value = True)
	cmds.text(label = '')
	cmds.text(label = 'ep000_sh020 ', align = 'left')
	cmds.checkBox('checkBox_030', label = '', value = True)
	cmds.text(label = '')
	cmds.text(label = 'ep000_sh030 ', align = 'left')
	cmds.checkBox('checkBox_040', label = '', value = True)
	cmds.text(label = '')
	cmds.text(label = 'ep000_sh040 ', align = 'left')
	cmds.checkBox('checkBox_050', label = '', value = True)
	cmds.text(label = '')
	cmds.text(label = 'ep000_sh050 ', align = 'left')
	cmds.checkBox('checkBox_060', label = '', value = True)
	cmds.text(label = '')
	cmds.text(label = 'ep000_Docks_Addon ', align = 'left')
	cmds.text(label = '')
	cmds.text(label = '')
	cmds.text(label = '')
	cmds.checkBox('optimizeStaticEnv_checkBox', label = '', value = True)
	cmds.text(label = '')
	cmds.text(label = 'Optimize Static ENVs ', align = 'left', backgroundColor = [.33, 1, 0.33])
	
	cmds.columnLayout(adjustableColumn = True, parent = 'clf_mainLayout')
	cmds.text(label = '')
	cmds.separator(height = 5)
	cmds.text(label = 'Render Layer(s) Setup')
	cmds.separator(height = 5)
	cmds.text(label = '')

	cmds.rowColumnLayout(numberOfColumns = 3, columnAlign = ([3, 'left']), parent = 'clf_mainLayout')
	cmds.checkBox('checkBox_rippleLayer', label = '', value = True)
	cmds.text(label = '')
	cmds.text(label = 'Ripple Layer ', align = 'left')

	cmds.checkBox('checkBox_bgHills', label = '', value = True)
	cmds.text(label = '')
	cmds.text(label = 'BG Hills ', align = 'left')

	cmds.columnLayout(adjustableColumn = True, parent = 'clf_mainLayout')

	cmds.text(label = '')
	cmds.separator(height = 5)
	cmds.text(label = 'Settings')
	cmds.separator(height = 5)
	cmds.text(label = '')

	cmds.text(label = ' Directory ', align = 'left')
	cmds.textField('directory_textField', text = 'I:/bubblebathbay/episodes')
	cmds.button('directory_textField', label = 'browse...', command = 'clfUI.dirBrowseDialog()')

	cmds.text(label = '')

	cmds.text(label = ' Episode ', align = 'left')
	cmds.textField('episode_textField', text = '')
	
	cmds.text(label = '')
	
	cmds.text(label = ' Shots ', align = 'left')
	cmds.textField('shots_textField', text = '1-999')
	
	cmds.text(label = '')
	
	cmds.columnLayout(adjustableColumn = True, parent = 'clf_mainLayout')
	cmds.button(label = 'Setup Lighting Files!', command = 'clfUI.ui_getter()')
	cmds.text(label = '')
	
	cmds.showWindow()
	
	cmds.window('createLightFiles', q = True, height = True)

def getDirPath(dirpath, type):
	cmds.textField('directory_textField', e = True, text = dirpath)
	return True

def dirBrowseDialog():
	cmds.fileBrowserDialog(fileCommand = getDirPath, mode = 4, actionName = 'Set')

def hyphen_range(s):
	""" Takes a range in form of "a-b" and generate a list of numbers between a and b inclusive.
	Also accepts comma separated ranges like "a-b,c-d,f" will build a list which will include
	Numbers from a to b, a to d and f
	"""
	
	s = "".join( s.split() )
	r = set()
	for x in s.split(','):
		t = x.split('-')
		if len(t) not in [1, 2]: raise SyntaxError("hash_range is given its arguement as "+s+" which seems not correctly formated.")
		r.add(int(t[0])) if len(t) == 1 else r.update(set(range(int(t[0]),int(t[1])+1)))
	
	l = list(r)
	l.sort()
	
	return l

def queryShots():
	shots = cmds.textField('shots_textField', q = True, text = True)
	
	if shots:
		if re.match(r'^[-,0-9 ]+$', shots):
			return hyphen_range(shots)

def queryEpisode():
	episode = cmds.textField('episode_textField', q = True, text = True)

	if episode:
		if re.match(r'^-?[0-9]+$', episode):
			return "".join( episode.split() )

def ui_getter():
	directory = cmds.textField('directory_textField', q = True, text = True)
	if os.path.exists(directory):

		episode = queryEpisode()
		if episode:

			shots = queryShots()
			if shots:
				shots = ['%03d' % i for i in shots]

				cb010 = cmds.checkBox('checkBox_010', q = True, value = True)
				cb020 = cmds.checkBox('checkBox_020', q = True, value = True)
				cb030 = cmds.checkBox('checkBox_030', q = True, value = True)
				cb040 = cmds.checkBox('checkBox_040', q = True, value = True)
				cb050 = cmds.checkBox('checkBox_050', q = True, value = True)
				cb060 = cmds.checkBox('checkBox_060', q = True, value = True)
				optimizeEnv = cmds.checkBox('optimizeStaticEnv_checkBox', q = True, value = True)
				rippleLyr = cmds.checkBox('checkBox_rippleLayer', q = True, value = True)
				bgHillLyr = cmds.checkBox('checkBox_bgHills', q = True, value = True)

				import bbbLightToolsUI
				reload(bbbLightToolsUI)

				clf.setupLightFiles(cb010 = cb010, cb020 = cb020, cb030 = cb030, cb040 = cb040, cb050 = cb050, cb060 = cb060, optimizeEnv = optimizeEnv, rippleLyr = rippleLyr, bgHillLyr = bgHillLyr, directory = directory, episode = episode, shots = shots)
	else:
		cmds.warning('Directory provided don\'t exist!')
		
createLightFilesUI()