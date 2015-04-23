import subprocess, sys, os
sys.path.append("//192.168.5.253/BBB_main/bbb/i/ginyih/SubmitToDeadline/SubmitToDeadline")
from utils import submit_to_deadline

## 
mayapy_Path = 'C:/Program Files/Autodesk/Maya2013.5/bin/mayapy.exe'

# string setup
repository_Dir	= "//192.168.5.202/deadline_repository"
projDir			= "//192.168.5.253/BBB_main/bbb"
output_dir		= "//192.168.5.253/BBB_main/bbb/i/ginyih/SubmitToDeadline/output"
prePythonScript	= "//192.168.5.253/BBB_main/bbb/i/ginyih/SubmitToDeadline/SubmitToDeadline/utils/copy_plugins.py"

# Get all maya files recursively
maya_files = []
for x in sys.argv[1:]:
	# if directory
	if os.path.isdir(x):
		for root, dir, files in os.walk(x):
			for fil in files:
				maya_files.append( os.path.join(root, fil).replace("\\", "/") )
	# maya format
	elif os.path.splitext(x)[-1] in [".ma", ".mb"]:
		maya_files.append( x.replace("\\", "/") )

for mFile in maya_files:
	## Initialize deadline submission class to access some of the features and functions
	d = submit_to_deadline.Deadline()

	# ## Setup pre/post python script just incase we need any extra flexibilities...
	# if os.path.exists(prePythonScript):
	# 	d.PreTaskScript = prePythonScript

	# get slaves
	get_slaves = subprocess.Popen('Deadlinecommand.exe "GetSlaveNames"', stdout = subprocess.PIPE)
	slaves = get_slaves.communicate()
	try:	slaves = ",".join( slaves[0].strip().split("\r\n") )
	except:	slaves = ""

	# extract .ma info
	with open(mFile) as data:
		for line in data:
			if "playbackOptions" in line:
				frames = line.split()

	min_frame = eval( frames[6] )
	max_frame = eval( frames[8] )

	blacklist_slaves = 	[	'Anirban-pc',
							'Bbbrender47',
							'Anthonyp-pc',
							'Bbbrender11',
							'Bbbrender12-fixed',
							'Bbbrender13',
							'Bbbrender18',
							'Bbbrender19',
							'Bbbrender20-fixed',
							'Bbbrender23',
							'Bbbrender25',
							'Bbbrender27',
							'Bbbrender30',
							'Bbbrender31',
							'Bbbrender35',
							'Bbbrender37',
							'Bbbrender40',
							'Bbbrender43',
							'Han-pc2',
							'Han-pc2-fixed',
							'Jasmine-pc',
							'Jasonpua-pc',
							'Lkarleong-pc',
							'Ngjiayi-pc',
							'Patrickdeaneuse',
							'Render45',
							'Render46',
							'Render48-fixed',
							'Darrencheong-pc',
							'Noel-pc',
							'Ngjiahao-pc',
							'Davidt-pc',
							'Elias-pc',
							'Seewei-pc',
							'Boonyan-pc',
							'Michelechia-pc2',
							'Yoga-pc2'
						]

	shot 	= os.path.basename(mFile)[5:10]
	episode = os.path.basename(mFile)[:5]

	d.Department			= "ginyih"
	d.Pool					= "maya"
	d.Priority				= 20
	d.MachineLimit			= 0
	d.Version 				= 2013.5
	d.Build 				= "64bit"
	d.Blacklist 			= ",".join(blacklist_slaves)
	d.UserName				= "administrator"
	d.TaskTimeoutMinutes	= 0
	d.Name             		= os.path.splitext( os.path.basename(mFile) )[0]
	d.Frames                = "1,%s,%s" % ((max_frame / 2), max_frame)
	d.OutputDirectory0      = "K:/bubblebathbay/episodes/%s/%s_%s/RenderLayers/ExtraLight" % (episode, episode, shot)
	d.OutputFilePath		= d.OutputDirectory0
	d.ProjectPath           = projDir

	maya_job                = d.build_maya_job_info()
	maya_plugin             = d.build_maya_plugin_info()

	if os.path.isfile(mFile):
		d.submit_to_deadline(maya_job, maya_plugin, mFile)

raw_input("\nPress any key to exit...")