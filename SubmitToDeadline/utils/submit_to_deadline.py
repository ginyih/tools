import os, tempfile, subprocess, socket
from collections import OrderedDict

class Deadline(object):
		
		MAYA_JOB_INFO_ATTRS    =	(("Plugin"                             , "MayaBatch"),
									 ("Frames"                             , "1-24"), 
									 ("Name"                               , "Untitled"),
									 ("UserName"                           , ""),
									 ("MachineName"                        , ""),
									 ("Department"                         , socket.gethostname()),
									 ("Comment"                            , ""),
									 ("Group"                              , ""),
									 ("Pool"                               , "none"),
									 ("Priority"                           , 50),
									 ("ChunkSize"                          , 1),
									 ("ForceReloadPlugin"                  , "False"),
									 ("SynchronizeAllAuxiliaryFiles"       , "False"),
									 ("InitialStatus"                      , "Active"),
									 ("LimitGroups"                        , ""), 
									 ("MachineLimit"                       , 0),
									 ("MachineLimitProgress"               , -1.0),
									 ("Whitelist"                          , ""),
									 ("Blacklist"                          , ""),
									 ("DeleteOnComplete"                   , "False"),
									 ("ArchiveOnComplete"                  , "False"),
									 ("OnJobComplete"                      , "Nothing"),
									 ("ConcurrentTasks"                    , 1),
									 ("LimitConcurrentTasksToNumberOfCpus" , "True"),
									 ("Sequential"                         , "False"),
									 ("Interruptible"                      , "False"),
									 ("SuppressEvents"                     , "False"),
									 ("OverrideJobFailureDetection"        , "False"),
									 ("FailureDetectionJobErrors"          , 0),
									 ("OverrideTaskFailureDetection"       , "False"),
									 ("FailureDetectionTaskErrors"         , 0),
									 ("IgnoreBadJobDetection"              , "False"),
									 ("SendJobErrorWarning"                , "True"),
									 ("MinRenderTimeSeconds"               , 0),
									 ("MinRenderTimeMinutes"               , 0),
									 ("TaskTimeoutSeconds"                 , 0),
									 ("TaskTimeoutMinutes"                 , 0),
									 ("OnTaskTimeout"                      , "Error"),
									 ("EnableAutoTimeout"                  , "False"),
									 ("EnableTimeoutsForScriptTasks"       , "False"),
									 ("JobDependencies"                    , ""),
									 ("JobDependencyPercentage"            , -1),
									 ("IsFrameDependent"                   , "False"),
									 ("ResumeOnCompleteDependencies"       , "True"),
									 ("ResumeOnDeletedDependencies"        , "False"),
									 ("ResumeOnFailedDependencies"         , "False"),
									 ("OutputFilename0"                    , ""),
									 ("OutputDirectory0"                   , ""),
									 ("OutputFilename1"                    , ""),
									 ("OutputDirectory1"                   , ""),
									 ("OutputFilename2"                    , ""),
									 ("OutputDirectory2"                   , ""),
									 ("OutputFilename3"                    , ""),
									 ("OutputDirectory3"                   , ""),
									 ("OutputFilename4"                    , ""),
									 ("OutputDirectory4"                   , ""),
									 ("OutputFilename5"                    , ""),
									 ("OutputDirectory5"                   , ""),
									 ("OutputFilename6"                    , ""),
									 ("OutputDirectory6"                   , ""),
									 ("NotificationTargets"                , ""),
									 ("ClearNotificationTargets"           , "False"),
									 ("NotificationEmails"                 , ""),
									 ("OverrideNotificationMethod"         , "False"),
									 ("EmailNotification"                  , "False"),
									 ("GrowlNotification"                  , "False"),
									 ("NetsendNotification"                , "False"),
									 ("NotificationNote"                   , ""),
									 ("PreJobScript"                       , ""),
									 ("PostJobScript"                      , ""),
									 ("PreTaskScript"                      , ""),
									 ("PostTaskScript"                     , ""),
									 ("TileJob"                            , "False"),
									 ("TileJobFrame"                       , 0),
									 ("TileJobTilesInX"                    , 0),
									 ("TileJobTilesInY"                    , 0),
									 )
		
		MAYA_PLUGIN_INFO_ATTRS =	(("Version"                            , 2013), 
									 ("Build"                              , "64bit"), 
									 ("ProjectPath"                        , ""), 
									 ("StrictErrorChecking"                , "False"), 
									 ("LocalRendering"                     , "True"),
									 ("MaxProcessors"                      , 0), 
									 ("OutputFilePath"                     , ""),
									 ("Renderer"                           , "MentalRay"), 
									 ("MentalRayVerbose"                   , "Progress Messages"), 
									 ("AutoMemoryLimit"                    , "True"), 
									 ("MemoryLimit"                        , 0), 
									 ("CommandLineOptions"                 , ""), 
									 ("UseOnlyCommandLineOptions"          , 0), 
									 ("IgnoreError211"                     , "True"),
									 )
		
		MAYA_JOB_INFO_ATTRS    = OrderedDict(MAYA_JOB_INFO_ATTRS)
		MAYA_PLUGIN_INFO_ATTRS = OrderedDict(MAYA_PLUGIN_INFO_ATTRS)

		def __init__(self):
			for key, val in self.MAYA_JOB_INFO_ATTRS.iteritems():
				setattr(self, key, val)
					
			for key, val in self.MAYA_PLUGIN_INFO_ATTRS.iteritems():
				setattr(self, key, val)
						
		def _create_job_file(self, path = "", orderedDict = None):
			if orderedDict:
				job_file = open(path, mode = "w")
				for key, val in orderedDict.iteritems():
					job_file.write( "%s=%s\n" %( key, val ) )

				job_file.close()
										
		def _getAttr(self, orderedDict = None):
			if orderedDict:
				myDict = ()
				for key in orderedDict:
					myDict += ( ( key, eval("self.%s" % key) ), )

				return OrderedDict(myDict)

		def build_maya_job_info( self, name = "maya_job_info.job", path = tempfile.gettempdir() ):	
			attrs       = self._getAttr(self.MAYA_JOB_INFO_ATTRS)
			job_path    = os.path.join(path, name).replace("\\", "/")
			self._create_job_file(job_path, attrs)
			
			return job_path
				
		def build_maya_plugin_info( self, name = "maya_plugin_info.job", path = tempfile.gettempdir() ):
			attrs       = self._getAttr(self.MAYA_PLUGIN_INFO_ATTRS)
			job_path    = os.path.join(path, name).replace("\\", "/")
			self._create_job_file(job_path, attrs)

			return job_path

		def build_maya_job_xml(self):
			pass
		
		def build_maya_plugin_xml(self):
			pass
		
		def make_dirs(self, path = ""):
			if path:
				if not os.path.exists(path):
					os.makedirs(path)
						
		def submit_to_deadline(self, *args):
			if self.OutputDirectory0:
				if not os.path.exists(self.OutputDirectory0):
					self.make_dirs(self.OutputDirectory0)
					
			subprocess.call( 'Deadlinecommand.exe "%s" "%s" "%s"' %(args[0], args[1], args[2]) )