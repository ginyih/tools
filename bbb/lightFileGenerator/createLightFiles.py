import sys, os, re
from maya import cmds, mel
sys.path.append('T:/bubblebathbay_APPDIR/deepesh/2013.5-x64/scripts')
sys.path.append('T:/software/python-api')
sys.path.append('C:/Program Files/Autodesk/Maya2013.5/modules/MentalCore/scripts')
import bbbLightTools
reload(bbbLightTools)
from shotgun_api3 import Shotgun
from mentalcore import mapi
import xml.etree.ElementTree as ET

def tod_setter(timeOfDay):
	## mia_physicalsky
	mia_physicalsky = 'mia_physicalsky1'

	if cmds.objExists(mia_physicalsky):
		multiplier = None
		multiplier = 0.5 if timeOfDay == 'Dawn' else multiplier
		multiplier = 0.200000003 if timeOfDay == 'Sunrise' else multiplier
		multiplier = 0.200000003 if timeOfDay == 'Morning' else multiplier
		multiplier = 0.200000003 if timeOfDay == 'Day' else multiplier
		multiplier = 0.200000003 if timeOfDay == 'Afternoon' else multiplier
		multiplier = 0.200000003 if timeOfDay == 'AfternoonLate' else multiplier
		multiplier = 0.5 if timeOfDay == 'Sunset' else multiplier
		multiplier = 0.5 if timeOfDay == 'Dusk' else multiplier
		multiplier = 0.200000003 if timeOfDay == 'Night' else multiplier

		if multiplier:
			cmds.setAttr("%s.on" % mia_physicalsky, 1)
			cmds.setAttr("%s.multiplier" % mia_physicalsky, multiplier)
			cmds.setAttr("%s.rgb_unit_conversionR" % mia_physicalsky, 9.999999747e-005)
			cmds.setAttr("%s.rgb_unit_conversionG" % mia_physicalsky, 9.999999747e-005)
			cmds.setAttr("%s.rgb_unit_conversionB" % mia_physicalsky, 9.999999747e-005)
			cmds.setAttr("%s.haze" % mia_physicalsky, 0)
			cmds.setAttr("%s.redblueshift" % mia_physicalsky, 0)
			cmds.setAttr("%s.saturation" % mia_physicalsky, 1.299999952)
			cmds.setAttr("%s.horizon_height" % mia_physicalsky, 0.6499999762)
			cmds.setAttr("%s.horizon_blur" % mia_physicalsky, 1)
			cmds.setAttr("%s.ground_colorR" % mia_physicalsky, 0.2424900085)
			cmds.setAttr("%s.ground_colorG" % mia_physicalsky, 0.3276892304)
			cmds.setAttr("%s.ground_colorB" % mia_physicalsky, 0.3540000021)
			cmds.setAttr("%s.night_colorR" % mia_physicalsky, 0)
			cmds.setAttr("%s.night_colorG" % mia_physicalsky, 0)
			cmds.setAttr("%s.night_colorB" % mia_physicalsky, 0)
			cmds.setAttr("%s.sun_directionX" % mia_physicalsky, 0)
			cmds.setAttr("%s.sun_directionY" % mia_physicalsky, 0)
			cmds.setAttr("%s.sun_directionZ" % mia_physicalsky, 0)
			cmds.setAttr("%s.sun_disk_intensity" % mia_physicalsky, 1)
			cmds.setAttr("%s.sun_disk_scale" % mia_physicalsky, 4)
			cmds.setAttr("%s.sun_glow_intensity" % mia_physicalsky, 1)
			cmds.setAttr("%s.use_background" % mia_physicalsky, 1)
			cmds.setAttr("%s.visibility_distance" % mia_physicalsky, 0)
			cmds.setAttr("%s.y_is_up" % mia_physicalsky, 1)
			cmds.setAttr("%s.flags" % mia_physicalsky, 0)
			cmds.setAttr("%s.sky_luminance_mode" % mia_physicalsky, 0)
			cmds.setAttr("%s.zenith_luminance" % mia_physicalsky, 0)
			cmds.setAttr("%s.diffuse_horizontal_illuminance" % mia_physicalsky, 0)
			cmds.setAttr("%s.a" % mia_physicalsky, 0)
			cmds.setAttr("%s.b" % mia_physicalsky, 0)
			cmds.setAttr("%s.c" % mia_physicalsky, 0)
			cmds.setAttr("%s.d" % mia_physicalsky, 0)
			cmds.setAttr("%s.e" % mia_physicalsky, 0)
			cmds.setAttr("%s.physically_scaled_sun" % mia_physicalsky, 0)
			
	## mia_physicalsun
	mia_physicalsun = 'mia_physicalsun1'

	if cmds.objExists(mia_physicalsun):
		value = None
		value = (0.5, 4) if timeOfDay == 'Dawn' else value
		value = (0.3000000119, 3) if timeOfDay == 'Sunrise' else value
		value = (0.200000003, 1.299999952) if timeOfDay == 'Morning' else value
		value = (0.200000003, 1.299999952) if timeOfDay == 'Day' else value
		value = (0.200000003, 2) if timeOfDay == 'Afternoon' else value
		value = (0.200000003, 2) if timeOfDay == 'AfternoonLate' else value
		value = (0.5, 4) if timeOfDay == 'Sunset' else value
		value = (0.5, 4) if timeOfDay == 'Dusk' else value
		value = (0.200000003, 1.299999952) if timeOfDay == 'Night' else value

		if value:
			try:	cmds.setAttr("%s.on" % mia_physicalsun, 1)
			except:	pass
			cmds.setAttr("%s.multiplier" % mia_physicalsun, value[0])
			try:	cmds.setAttr("%s.rgb_unit_conversionR" % mia_physicalsun, 9.999999747e-005)
			except:	pass
			try:	cmds.setAttr("%s.rgb_unit_conversionG" % mia_physicalsun, 9.999999747e-005)
			except:	pass
			try:	cmds.setAttr("%s.rgb_unit_conversionB" % mia_physicalsun, 9.999999747e-005)
			except:	pass
			try:	cmds.setAttr("%s.haze" % mia_physicalsun, 0)
			except:	pass
			cmds.setAttr("%s.redblueshift" % mia_physicalsun, 0)
			cmds.setAttr("%s.saturation" % mia_physicalsun, value[1])
			try:	cmds.setAttr("%s.horizon_height" % mia_physicalsun, 0.6499999762)
			except:	pass
			cmds.setAttr("%s.shadow_softness" % mia_physicalsun, 2)
			cmds.setAttr("%s.samples" % mia_physicalsun, 8)
			cmds.setAttr("%s.photon_bbox_minX" % mia_physicalsun, 0)
			cmds.setAttr("%s.photon_bbox_minY" % mia_physicalsun, 0)
			cmds.setAttr("%s.photon_bbox_minZ" % mia_physicalsun, 0)
			cmds.setAttr("%s.photon_bbox_maxX" % mia_physicalsun, 0)
			cmds.setAttr("%s.photon_bbox_maxY" % mia_physicalsun, 0)
			cmds.setAttr("%s.photon_bbox_maxZ" % mia_physicalsun, 0)
			cmds.setAttr("%s.automatic_photon_energy" % mia_physicalsun, 0)
			try:	cmds.setAttr("%s.y_is_up" % mia_physicalsun, 1)
			except:	pass
			cmds.setAttr("%s.illuminance_mode" % mia_physicalsun, 0)
			cmds.setAttr("%s.direct_normal_illuminance" % mia_physicalsun, 0)
			
	## transform
	transform = 'sunDirection'
	
	if cmds.objExists(transform):
		trans = None
		trans = [-126.810445, 6.400256926, 297.0114397, 99.5508123, 13.17107847, 99.31932804] if timeOfDay == 'Dawn' else trans
		trans = [-126.810445, 6.400256926, 297.0114397, 94.17836619, 8.510308082, 111.0515094] if timeOfDay == 'Sunrise' else trans
		trans = [-126.810445, 6.400256926, 297.0114397, 79.03123185, 18.38634569, 114.5999062] if timeOfDay == 'Morning' else trans
		trans = [-126.810445, 6.400256926, 297.0114397, 66.5701432, 3.028482663, 133.749432] if timeOfDay == 'Day' else trans
		trans = [-126.810445, 6.400256926, 297.0114397, 65.61623961, 4.282617622, -159.6751399] if timeOfDay == 'Afternoon' else trans
		trans = [-126.810445, 6.400256926, 297.0114397, 65.61623961, 4.282617622, -159.6751399] if timeOfDay == 'AfternoonLate' else trans
		trans = [-126.810445, 6.400256926, 297.0114397, 46.03332381, 9.522088621, -110.2576592] if timeOfDay == 'Sunset' else trans
		trans = [-126.810445, 6.400256926, 297.0114397, 60.53159771, 11.77218192, -103.4315584] if timeOfDay == 'Dusk' else trans
		trans = [-126.810445, 6.400256926, 297.0114397, 66.95272947, -7.072915646, 156.220059] if timeOfDay == 'Night' else trans

		if trans:
			cmds.setAttr("%s.translateX" % transform, trans[0])
			cmds.setAttr("%s.translateY" % transform, trans[1])
			cmds.setAttr("%s.translateZ" % transform, trans[2])
			cmds.setAttr("%s.rotateX" % transform, trans[3])
			cmds.setAttr("%s.rotateY" % transform, trans[4])
			cmds.setAttr("%s.rotateZ" % transform, trans[5])

def camMovementDetector():
	shotCam = [cam for cam in cmds.listCameras(perspective = True) if cam != 'persp' if cmds.objExists('%s.type' % cam) if cmds.getAttr('%s.type' % cam) == 'shotCam']
	shotCam = shotCam[0] if shotCam else None
	
	animated_curves = []
	anim_curves = cmds.findKeyframe(shotCam, curve = True)
	
	if anim_curves:
		keyframes_min_max = []
		
		for crv in anim_curves:
			keys = cmds.keyframe(crv, valueChange = True, q = True)
			frames = cmds.keyframe(crv, timeChange = True, q = True)
			keyframes = dict( zip(keys, frames) )
	
			if keyframes:
				if len(keyframes) > 1:
					start_anim = max( keyframes.values() )
					stop_anim = min( keyframes.values() )
					
					keyframes_min_max.append(start_anim) if start_anim not in keyframes_min_max else None
					keyframes_min_max.append(stop_anim) if stop_anim not in keyframes_min_max else None
					
		if keyframes_min_max:
			return min(keyframes_min_max), max(keyframes_min_max)

def get_data_from_shotgun(cb010 = True, cb020 = True, cb030 = True, cb040 = True, cb050 = True, cb060 = True, optimizeEnv = True, rippleLyr = True, bgHillLyr = True, directory = 'I:/bubblebathbay/episodes', **kwargs):
	episode = kwargs['code'].split('_')[0] if kwargs['code'] else None
	shotName = kwargs['code'] if kwargs['code'] else None
	minTime = kwargs['sg_cut_in'] if kwargs['sg_cut_in'] else None
	maxTime = kwargs['sg_cut_out'] if kwargs['sg_cut_out'] else None
	timeOfDay = kwargs['sg_tod'] if kwargs['sg_tod'] else None
	oceanType = kwargs['sg_ocean_type'] if kwargs['sg_ocean_type'] else None
	
	if shotName:
		## New File!
		cmds.file(new = True, force = True)

		## Load plugins
		plugins_to_load = ['AbcImport', 'Mayatomr'];	[cmds.loadPlugin(plug) for plug in plugins_to_load if not cmds.pluginInfo(plug, q = True, name = True, loaded = True)]

		## Enable Mentalcore
		cmds.deleteUI('unifiedRenderGlobalsWindow') if cmds.window('unifiedRenderGlobalsWindow', exists = True, q = True) else None
		bbbLightTools._setRenderGlobals()

		if minTime and maxTime:
			## Sync frame range from shotgun (min)
			cmds.playbackOptions(minTime = minTime, maxTime = maxTime, animationStartTime = minTime, animationEndTime = maxTime)

		sceneName = 'I:/bubblebathbay/episodes/%s/%s/Light/work/maya/' % (episode, shotName)
		############################################################################################################
		## Fetch latest anim publish
		bbbLightTools._fetchAnimPublish(filteredPublish = 'Fetch Anim Publish', sceneName = sceneName)
		cmds.select(cmds.listRelatives('ABC_ANIM_CACHES_hrc', children = True, fullPath = True), replace = True) if cmds.objExists('ABC_ANIM_CACHES_hrc') and cmds.listRelatives('ABC_ANIM_CACHES_hrc', children = True) else None
		bbbLightTools.fetchShadersForSelected()
		
		###########################################################################################################
		## Fetch latest crease xml publish
		bbbLightTools._fetchAnimPublish(filteredPublish = 'Fetch Crease XML Publish', sceneName = sceneName)

		###########################################################################################################
		## Fetch latest camera publish
		bbbLightTools._fetchAnimPublish(filteredPublish = 'Fetch Camera Publish', sceneName = sceneName)
		shotCam = [cmds.listRelatives(cam, fullPath = True)[0] for cam in cmds.listCameras(perspective = True) if cam != 'persp' if cmds.objExists('%s.type' % cam) if cmds.getAttr('%s.type' % cam) == 'shotCam']
		shotCam = shotCam[0] if shotCam else None
		cmds.setAttr("%s.displayResolution" % shotCam, 1)
		cmds.setAttr("%s.overscan" % shotCam, 1.3)
		
		###########################################################################################################
		## Fetch latest fx ocean publish
		bbbLightTools._fetchAnimPublish(filteredPublish = 'Fetch FX Publish', sceneName = sceneName)

		## Fetch Static ENVs
		bbbLightTools._doSTATIC_import(path = '//192.168.5.253/BBB_main/bbb/i/bubblebathbay/episodes/ep000/ep000_sh010/Light/publish/maya', namespace = 'ep000_sh010_ep000sh010_LIGHTENV') if cb010 else None
		bbbLightTools._doSTATIC_import(path = '//192.168.5.253/BBB_main/bbb/i/bubblebathbay/episodes/ep000/ep000_sh020/Light/publish/maya', namespace = 'ep000_sh020_ep000sh020_LIGHTENV') if cb020 else None
		bbbLightTools._doSTATIC_import(path = '//192.168.5.253/BBB_main/bbb/i/bubblebathbay/episodes/ep000/ep000_sh030/Light/publish/maya', namespace = 'ep000_sh030_ep000sh030_LIGHTENV') if cb030 else None
		bbbLightTools._doSTATIC_import(path = '//192.168.5.253/BBB_main/bbb/i/bubblebathbay/episodes/ep000/ep000_sh040/Light/publish/maya', namespace = 'ep000_sh040_ep000sh040_LIGHTENV') if cb040 else None
		bbbLightTools._doSTATIC_import(path = '//192.168.5.253/BBB_main/bbb/i/bubblebathbay/episodes/ep000/ep000_sh050/Light/publish/maya', namespace = 'ep000_sh050_ep000sh050_LIGHTENV') if cb050 else None
		bbbLightTools._doSTATIC_import(path = '//192.168.5.253/BBB_main/bbb/i/bubblebathbay/episodes/ep000/ep000_Docks_Addon/Light/publish/maya', namespace = 'ep000_sh050_ep000sh060_LIGHTENV') if cb060 else None

		# Do static env quick optimize
		if optimizeEnv:
			if camMovementDetector():
				bbbLightTools.optimizeScene( still = False, step = 5, offset = 1.1, startFrame = int( camMovementDetector()[0] ), endFrame = int( camMovementDetector()[1] ) )
			else:
				bbbLightTools.optimizeScene(still = True, step = 5, offset = 1.1)

		## Setup Lighting
		if timeOfDay:
			bbbLightTools.setTOD_automatic(TODay = "dawn") if timeOfDay == 'Dawn' else None
			bbbLightTools.setTOD_automatic(TODay = "sunrise") if timeOfDay == 'Sunrise' else None
			bbbLightTools.setTOD_automatic(TODay = "morning") if timeOfDay == 'Morning' else None
			bbbLightTools.setTOD_automatic(TODay = "midday") if timeOfDay == 'Day' else None
			bbbLightTools.setTOD_automatic(TODay = "afternoon") if timeOfDay == 'Afternoon' else None
			bbbLightTools.setTOD_automatic(TODay = "afternoon") if timeOfDay == 'AfternoonLate' else None
			bbbLightTools.setTOD_automatic(TODay = "sunset") if timeOfDay == 'Sunset' else None
			bbbLightTools.setTOD_automatic(TODay = "dusk") if timeOfDay == 'Dusk' else None
			bbbLightTools.setTOD_automatic(TODay = "night") if timeOfDay == 'Night' else None

			tod_setter(timeOfDay = timeOfDay)

		## Finally, render setup!
		bbbLightTools.RenderSetup()

		if rippleLyr:
			## Go to defaultRenderLayer before setting up ripple or bg hills separated render layers
			cmds.editRenderLayerGlobals(currentRenderLayer = 'defaultRenderLayer')
			## Import ripple layer
			bbbLightTools.importRippleLayer()
			## Ripple_Lyr
			bbbLightTools.setRippleLYR()

		if bgHillLyr:
			## Go to defaultRenderLayer before setting up ripple or bg hills separated render layers
			cmds.editRenderLayerGlobals(currentRenderLayer = 'defaultRenderLayer')
			## BGHills_Lyr
			bbbLightTools.setBGHills()

		## Save scene!
		shotPath = '%s.generated__.ma' % shotName.replace('_', '')
		shotPath = '%s/%s/%s/Light/work/maya/%s' % (directory, episode, shotName, shotPath)

		if not os.path.exists( os.path.dirname(shotPath) ):
			os.makedirs( os.path.dirname(shotPath) )

		cmds.file(rename = shotPath)
		cmds.file(save = True, type = "mayaAscii")

def setupLightFiles(cb010 = True, cb020 = True, cb030 = True, cb040 = True, cb050 = True, cb060 = True, optimizeEnv = True, rippleLyr = True, bgHillLyr = True, directory = 'I:/bubblebathbay/episodes', episode = 152, shots = 1):
	## Initialize Shotgun API
	base_url	= "http://bubblebathbay.shotgunstudio.com"
	script_name	= 'audioUploader'
	api_key		= 'bbfc5a7f42364edd915656d7a48d436dc864ae7b48caeb69423a912b930bc76a'
	sgsrv		= Shotgun(base_url = base_url , script_name = script_name, api_key = api_key, ensure_ascii = True, connect = True)

	## Query data from Shotgun
	data = sgsrv.find('Shot', filters = [["code", "contains", 'ep%s_sh' % episode]], fields = ['code', 'sg_cut_in', 'sg_cut_out', 'sg_tod', 'sg_ocean_type'])
	if data:
		if episode:
			if shots:

				for each in data:
					if each['code'].split('_')[-1].strip('sh') in shots:
						try:
							cmds.refresh(suspend = True)
							get_data_from_shotgun(cb010 = cb010, cb020 = cb020, cb030 = cb030, cb040 = cb040, cb050 = cb050, cb060 = cb060, optimizeEnv = optimizeEnv, rippleLyr = rippleLyr, bgHillLyr = bgHillLyr, directory = directory, **each)
						except:
							pass
						finally:
							cmds.refresh(suspend = False)