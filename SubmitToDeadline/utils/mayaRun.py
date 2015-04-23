import sys, subprocess, re, os, itertools
sys.path.append('//192.168.5.253/BBB_main/bbb/i/ginyih/SubmitToDeadline/SubmitToDeadline/utils')
from submit_to_deadline_v2 import Deadline
from maya import cmds, mel

## Primary setup
repository_Dir	= '//192.168.5.202/deadline_repository'
projDir			= '//192.168.5.253/BBB_main/bbb'
prePythonScript	= ''

def queryPriority():
	result = cmds.promptDialog(title = 'Priority', message = 'Priority (1-100):', button = ['OK'], defaultButton = 'OK', text = 99)
	if result == 'OK':
		text = cmds.promptDialog(q = True, text = True)
		try:
			int(text)
			return int(text)
		except:
			cmds.confirmDialog(message = 'Please ensure to insert only digits!', title = 'Priority')

def queryFrameRange(input):
	result = cmds.promptDialog(title = 'Frame Range', message = 'Frame Range:', button = ['OK', 'Cancel'], defaultButton = 'OK', cancelButton = 'Cancel', dismissString = 'Cancel', text = input)
	if result == 'OK':
		text = cmds.promptDialog(q = True, text = True)
		if re.match(r'^[-,0-9 ]+$', text):
			return text
		else:
			cmds.confirmDialog(message = 'Please ensure to insert only digits, commas and hypens!', title = 'Frame Range')
	else:
		return None
		
def _getLatestVersion(path):
	if os.path.exists(path):
		for i in itertools.count():
			outputPath = os.path.join(path, 'R%03d' % i).replace('\\', '/')
			
			if os.path.exists(outputPath):
				if not os.listdir(outputPath):
					return outputPath
					break
			
			else:
				return outputPath
				break

sceneName = cmds.file(q = True, sceneName = True)
if sceneName:
	
	if os.path.dirname(sceneName).endswith('/Light/work/maya'):
		
		## Check whether current file needs to be saved before proceeding
		if not cmds.file(modified = True, q = True):
		
			minFrame = int( str(cmds.playbackOptions(min = True, q = True)).split('.')[0] )
			maxFrame = int( str(cmds.playbackOptions(max = True, q = True)).split('.')[0] )
			
			frameRange = queryFrameRange( '%s-%s' %(minFrame, maxFrame) )
			if frameRange:
				
				## Initialize deadline submission class to access some of the features and functions
				deadline = Deadline()
			
				# # Get slaves
				# get_slaves = subprocess.Popen('Deadlinecommandeadline.exe "GetSlaveNames"', stdout = subprocess.PIPE)
				# slaves = get_slaves.communicate()
				# try:	slaves = ','.join( slaves[0].strip().split('\r\n') )
				# except:	slaves = ''
				
				## Output path
				output_dir = os.path.dirname(sceneName).replace('I:/', 'K:/').replace('/Light/work/maya', '/RenderLayers')
				output_dir = _getLatestVersion(output_dir)
				deadline.make_dirs(output_dir)

				## Priority
				priority = queryPriority()
				priority = priority if priority else 99

				deadline.Renderer 			= 'MentalRay'
				deadline.Priority			= priority
				deadline.MachineLimit		= 1
				deadline.Version 			= 2013.5
				deadline.Build 				= '64bit'
				# deadline.Blacklist 			= ','.join( ['Lkarleong-pc', 'Mandeep-pc', 'Ramos-pc', 'Tehtiongshih-pc'] )
				deadline.UserName			= 'administrator'
				deadline.TaskTimeoutMinutes	= 120
				deadline.Name             	= os.path.splitext( os.path.basename(sceneName) )[0]
				deadline.Frames             = '%s' % frameRange
				deadline.OutputDirectory0   = '%s' % output_dir
				deadline.OutputFilePath		= deadline.OutputDirectory0
				deadline.ProjectPath        = projDir
				deadline.MachineLimit 		= 10
				
				maya_job                	= deadline.build_maya_job_info()
				maya_plugin             	= deadline.build_maya_plugin_info()
				
				if os.path.isfile(sceneName):
					deadline.submit_to_deadline(maya_job, maya_plugin, sceneName)
					os.startfile(output_dir)
				else:
					cmds.warning('%s is not a valid file!' % sceneName)
				
		else:
			cmds.warning('Please save your file!')
			
	else:
		cmds.warning('Not in correct workspace, i.e. I:/bubblebathbay/episodes/ep###/ep###_sh###/Light/work/maya')
		
else:
	cmds.warning('Please save your file!')