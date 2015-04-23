# import os, ctypes, distutils.dir_util

# plugin_dir		= "//192.168.1.58/tranform_server/Transformer/ovm_workspace/scripts/for_rendering/required_plugins"
# maya_2013_path	= os.path.join(os.environ["USERPROFILE"], "Documents", "maya").replace("\\", "/")

# def drive_free_space(drive = "C:", compareByte = 10737418240):
# 	free_bytes	= ctypes.c_ulonglong(0)
# 	total_bytes = ctypes.c_ulonglong(0)
# 	ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(drive), None, ctypes.pointer(total_bytes), ctypes.pointer(free_bytes))

# 	drive_free_space = int( float(free_bytes.value) )
# 	if drive_free_space < compareByte:
# 		return True

def __main__():

	pass

	# # make sure to copy necessary rendering plugins
	# if os.path.exists(plugin_dir):
	# 	for x in os.listdir(plugin_dir):
	# 		if os.path.exists(maya_2013_path):
	# 			try:
	# 				distutils.dir_util.copy_tree(plugin_dir, maya_2013_path)
	# 			except:
	# 				print "Failed to copy plugins..."

	# # don't copy to local if drive space not more than expected...
	# # drive_free_space(drive = "C:", compareByte = 10737418240)

	# # Delete temp files
	# temp_dir	= os.environ["TEMP"].replace("\\", "/")
	# file_type	= [".mb", ".ma"]

	# for f in os.listdir(temp_dir):
	# 	for typ in file_type:
	# 		if f.endswith(typ):
	# 			try:
	# 				os.remove( os.path.join(temp_dir, f).replace("\\", "/") )
	# 				print "Deleting %s..." %f
	# 			except:
	# 				pass