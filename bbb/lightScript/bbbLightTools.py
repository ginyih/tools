import maya.OpenMaya as om
import maya.OpenMayaUI as omu
import maya.cmds as cmds
import maya.mel as mel
try:	from mentalcore import mapi
except:	pass
import xml.etree.ElementTree as ET
from maya import cmds, mel
import os, sys, subprocess, re, itertools
import sys, json
sys.path.append('//192.168.5.253/BBB_main/bbb/t/bubblebathbay_APPDIR/bbb_kialiam/2013.5-x64/scripts')
sys.path.append('//192.168.5.253/BBB_main/bbb/i/ginyih/SubmitToDeadline/SubmitToDeadline/utils')
#from submit_to_deadline_v4 import Deadline
import KillSmooth
reload(KillSmooth)
#Render Settings            
def fileRenderSettings():
	cmds.setAttr("mentalcoreGlobals.en_colour_management", 1)
	cmds.setAttr("mentalcoreGlobals.unified_sampling", 1)
	cmds.setAttr("mentalcoreGlobals.samples_max", 80)
	cmds.setAttr("mentalcoreGlobals.samples_quality", 0.8)
	cmds.setAttr("mentalcoreGlobals.samples_error_cutoff", 0.02)
	cmds.setAttr("mentalcoreGlobals.en_envl", 1)
	cmds.setAttr("mentalcoreGlobals.envl_scale", 0.5)
	cmds.setAttr("mentalcoreGlobals.envl_blur", 0)
	cmds.setAttr("mentalcoreGlobals.envl_blur_res", 0)
	cmds.setAttr("mentalcoreGlobals.envl_en_flood_colour", 1)
	cmds.setAttr("mentalcoreGlobals.envl_flood_colour", 1, 1, 1, type = 'double3')
	cmds.setAttr("mentalcoreGlobals.en_ao", 1)
	cmds.setAttr("mentalcoreGlobals.ao_samples", 24)
	cmds.setAttr("mentalcoreGlobals.ao_spread", 60)
	cmds.setAttr("mentalcoreGlobals.ao_far_clip", 10)
	cmds.setAttr("mentalcoreGlobals.ao_opacity", 1)
	cmds.setAttr("mentalcoreGlobals.ao_vis_indirect", 0)
	cmds.setAttr("mentalcoreGlobals.ao_vis_refl", 1)
	cmds.setAttr("mentalcoreGlobals.ao_vis_refr", 0)
	cmds.setAttr("mentalcoreGlobals.ao_vis_trans", 1)
	cmds.setAttr("mentalcoreGlobals.ao_flag_shadow", 1)
	#cmds.setAttr("mentalcoreGlobals.samples_per_object", 1)

	cmds.setAttr('mia_physicalsun1.shadow_softness', 4) if cmds.objExists('mia_physicalsun1.shadow_softness') else None
	cmds.setAttr('mia_physicalsun1.samples', 24) if cmds.objExists('mia_physicalsun1.samples') else None
	cmds.setAttr('depth_norm.filtering', 1) if cmds.objExists('depth_norm.filtering') else None

#Neutrilize all Core Randomiser nodes
def killRandomiser():
	mel.eval('source "T:/misc/Lighting-DoNotDelete/Scripts/SourceScripts/killRandomiser.mel"')
	try:
		mel.eval('killRandomiser')
	except:
		print("Error : No randomiser found")

def doRivet():
	mel.eval('source "T:/misc/Lighting-DoNotDelete/Scripts/SourceScripts/rivet.mel"')
	try:
		mel.eval('rivet')
	except:
		print("Error : No rivetscript found")

def UvTransferTool():
	mel.eval('source "//192.168.5.253/BBB_main/bbb/t/misc/Lighting-DoNotDelete/Scripts/SourceScripts/srbUVTransfer.mel"')
	mel.eval('srbUVTransfer()')

def oceanSrfToPolyPreview():
	mel.eval('source "//192.168.5.253/BBB_main/bbb/t/misc/Lighting-DoNotDelete/Scripts/SourceScripts/C2i_OceanOven.mel"')
	mel.eval('C2i_OceanOven()')

## Turn off eye shadows    
def turnOffEyeShad():
	eyeNodes = cmds.ls(['*eyeball_clear*', '*eyebrow*','*eyeBrow*', '*eyelash*','*eyeLash*', '*owser_meter_glass*', '*_eye_glass*','*spec_glasses_geoShape','*_speedmetre_glass_*','*_speedmetre_01_glass_*','*_speedmetre_02_glass_*','*_speedmetre_03_glass_*','*glass_geo*','*eyeclear*','*Glass_big_geo*','*Glass_small_geo*'], type = 'mesh', l = True)
	[cmds.setAttr('%s.castsShadows' % mesh, False) for mesh in eyeNodes] if eyeNodes else None

## Turn off cast shadows for unwanted objects    
def turnOffCastShad():
	shadNodes = cmds.ls(sl = True, l = True)
	[cmds.setAttr('%s.castsShadows' % mesh, False) for mesh in shadNodes] if shadNodes else None

## Turn on cast shadows for unwanted objects    
def turnOnCastShad():
	shadNodes = cmds.ls(sl = True, l = True)
	[cmds.setAttr('%s.castsShadows' % mesh, True) for mesh in shadNodes] if shadNodes else None

## Turn off receive shadows for unwanted objects    
def turnOffRecShad():
	shadNodes = cmds.ls(sl = True, l = True)
	[cmds.setAttr('%s.receiveShadows' % mesh, False) for mesh in shadNodes] if shadNodes else None

## Turn on receive shadows for unwanted objects    
def turnOnRecShad():
	shadNodes = cmds.ls(sl = True, l = True)
	[cmds.setAttr('%s.receiveShadows' % mesh, True) for mesh in shadNodes] if shadNodes else None

## Turn off visible in reflection for unwanted objects    
def turnOffVisRefl():
	shadNodes = cmds.ls(sl = True, l = True)
	[cmds.setAttr('%s.visibleInReflections' % mesh, False) for mesh in shadNodes] if shadNodes else None

## Turn on visible in reflection for unwanted objects    
def turnOnVisRefl():
	shadNodes = cmds.ls(sl = True, l = True)
	[cmds.setAttr('%s.visibleInReflections' % mesh, True) for mesh in shadNodes] if shadNodes else None

## Turn off visible in refraction for unwanted objects    
def turnOffVisRefr():
	shadNodes = cmds.ls(sl = True, l = True)
	[cmds.setAttr('%s.visibleInRefractions' % mesh, False) for mesh in shadNodes] if shadNodes else None

## Turn on visible in refraction for unwanted objects    
def turnOnVisRefr():
	shadNodes = cmds.ls(sl = True, l = True)
	[cmds.setAttr('%s.visibleInRefractions' % mesh, True) for mesh in shadNodes] if shadNodes else None

## Turn BBXon on selected
def bbxSelectedOn():
	selection = cmds.ls(sl = True, l = True)
	meshes = [cmds.listRelatives(each, shapes = True, fullPath = True)[0] for each in selection] if selection else None
	[(cmds.setAttr('%s.overrideEnabled' % mesh, 1), cmds.setAttr('%s.overrideLevelOfDetail' % mesh, 1)) for mesh in meshes] if meshes else None

## Turn BBXoff on selected
def bbxSelectedOff():         
	selection = cmds.ls(sl = True, l = True)
	meshes = [cmds.listRelatives(each, shapes = True, fullPath = True)[0] for each in selection] if selection else None
	[(cmds.setAttr('%s.overrideEnabled' % mesh, 0), cmds.setAttr('%s.overrideLevelOfDetail' % mesh, 0)) for mesh in meshes] if meshes else None

## Turn BBXon on all
def bbxAllOn():         
	meshes = cmds.ls(type = 'mesh', l = True)
	[(cmds.setAttr('%s.overrideEnabled' % mesh, 1), cmds.setAttr('%s.overrideLevelOfDetail' % mesh, 1)) for mesh in meshes] if meshes else None

## Turn BBXoff on all
def bbxAllOff():         
	meshes = cmds.ls(type = 'mesh', l = True)
	[(cmds.setAttr('%s.overrideEnabled' % mesh, 0), cmds.setAttr('%s.overrideLevelOfDetail' % mesh, 0)) for mesh in meshes] if meshes else None

## function for creating foam shader

def ImportStormyFoamShader():
	i=0
	if cmds.objExists('StormyFoam_fractal')==True:
		i=1
	if cmds.objExists('StormyFoam_cloud')==True:
		i=i+1
	if cmds.objExists('StormyFoam_Caustics')==True:
		i=i+1
	if cmds.objExists('StormyFoam_gammaCorrect')==True:
		i=i+1
	if cmds.objExists('StormyFoam_Merge')==True:
		i=i+1
	if cmds.objExists('fractal_place2dTexture')==True:
		i=i+1
	if cmds.objExists('cloud_place3dTexture')==True:
		i=i+1
	if cmds.objExists('Caustics_place2dTexture')==True:
		i=i+1
	if cmds.objExists('StormyFoam_expression')==True:
		i=i+1
	if cmds.objExists('StormyFoamN_uiConfigurationScriptNode')==True:
		i=i+1
	if cmds.objExists('StormyFoamN_sceneConfigurationScriptNode')==True:
		i=i+1
	if i<11 and i>0:
		if cmds.objExists('StormyFoam_fractal')==True:
			cmds.delete('StormyFoam_fractal')
		if cmds.objExists('StormyFoam_cloud')==True:
			cmds.delete('StormyFoam_cloud')
		if cmds.objExists('StormyFoam_Caustics')==True:
			cmds.delete('StormyFoam_Caustics')
		if cmds.objExists('StormyFoam_gammaCorrect')==True:
			cmds.delete('StormyFoam_gammaCorrect')
		if cmds.objExists('StormyFoam_Merge')==True:
			cmds.delete('StormyFoam_Merge')
		if cmds.objExists('fractal_place2dTexture')==True:
			cmds.delete('fractal_place2dTexture')
		if cmds.objExists('cloud_place3dTexture')==True:
			cmds.delete('cloud_place3dTexture')
		if cmds.objExists('Caustics_place2dTexture')==True:
			cmds.delete('Caustics_place2dTexture')
		if cmds.objExists('StormyFoam_expression')==True:
			cmds.delete('StormyFoam_expression')
		if cmds.objExists('StormyFoamN_uiConfigurationScriptNode')==True:
			cmds.delete('StormyFoamN_uiConfigurationScriptNode')
		if cmds.objExists('StormyFoamN_sceneConfigurationScriptNode')==True:
			cmds.delete('StormyFoamN_sceneConfigurationScriptNode')
		i=0
	if i==0:       
		cmds.file('T:/misc/Lighting-DoNotDelete/StormyShaderPreset/StormyFoam.ma',i=True) #file path for foam shader file

#function for connectng foam shader
			
def connectStormyFoam():
	if cmds.objExists('StormyFoam_gammaCorrect')==True:
		cmds.duplicate('ocean_dispShader',n='oceanStormSeaFoam',ic=True)
		try:	cmds.connectAttr('time1.outTime','oceanStormSeaFoam.time')
		except:	pass
		try:	cmds.connectAttr('StormyFoam_gammaCorrect.outValue','oceanStormSeaFoam.foamColor')
		except:	pass
		try:	cmds.connectAttr('oceanWakeTextureShape.outAlpha','oceanStormSeaFoam.waveHeightOffset')
		except:	pass
		try:	cmds.connectAttr('oceanWakeFoamTextureShape.outAlpha','oceanStormSeaFoam.foamOffset')
		except:	pass
		stormFoamCreate=mel.eval('mrCreateCustomNode -asShader "" core_surface_shader;')
		cmds.rename(stormFoamCreate,'stormSeaFoam')
		cmds.rename(cmds.listConnections('stormSeaFoam',type='shadingEngine')[0],'stormSeaFoamSG')
		try:	cmds.connectAttr('oceanStormSeaFoam.outColor','stormSeaFoam.colour')
		except:	pass
		try:	cmds.connectAttr('oceanStormSeaFoam.outColor','stormSeaFoamSG.displacementShader')
		except:	pass
	else:
		print("# Error: Foam Shader Missing! #")

def connectCharFoam():
	try:
		charFoamCreate=mel.eval('mrCreateCustomNode -asShader "" core_surface_shader;')
		cmds.rename(charFoamCreate,'charSeaFoam')
		cmds.rename(cmds.listConnections('charSeaFoam',type='shadingEngine')[0],'charSeaFoamSG')
		cmds.connectAttr('oceanWater_incd_cTxBld.outColor','charSeaFoam.colour')
		cmds.connectAttr('ocean_dispShader.outColor','charSeaFoamSG.displacementShader')
	except:
		pass

def setRippleLYR():
	if cmds.objExists('LIB_WORLD_Shoreline_hrc') or cmds.objExists('LIB_WORLD_RoseInlet_Shoreline_hrc'):
		cmds.delete( cmds.ls('*shorlineLight') ) if cmds.ls('*shorlineLight') else None
		cmds.delete( cmds.ls('*RSHD*') ) if cmds.ls('*RSHD*') else None
		cmds.delete('ripple_LYR') if cmds.objExists('ripple_LYR') else None

		cmds.shadingNode('useBackground', asShader = True, n = 'RSHD_rippleBase')
		cmds.setAttr("RSHD_rippleBase.specularColor", 0, 0, 0, type = 'double3')
		cmds.setAttr("RSHD_rippleBase.reflectivity", 0)
		cmds.setAttr("RSHD_rippleBase.reflectionLimit", 0)
			
		cmds.shadingNode('core_surface_shader', asShader = True, n = 'RSHD_foamBase')
		cmds.connectAttr('RSHD_rippleBase.outMatteOpacity', 'RSHD_foamBase.colour')
		cmds.sets(n = 'RSHD_RippleShaderSG', renderable = True, noSurfaceShader = True, empty = True)
		cmds.connectAttr('RSHD_foamBase.outValue', 'RSHD_RippleShaderSG.miMaterialShader')
		cmds.connectAttr('RSHD_foamBase.outValue', 'RSHD_RippleShaderSG.miShadowShader')
		cmds.connectAttr('ocean_dispShader.outColor', 'RSHD_RippleShaderSG.displacementShader')
		[cmds.connectAttr('ocean_dispShader.outColor', '%s.displacementShader' % sg) for sg in cmds.ls('World_Shoreline_House_ripple_SHDSG*') if not cmds.isConnected('ocean_dispShader.outColor', '%s.displacementShader' % sg)]
			
		cmds.editRenderLayerGlobals(currentRenderLayer = 'defaultRenderLayer')

		## cmds.displaySmoothness('LIB_WORLD_Shoreline_hrc', polygonObject = 1)
		cmds.setAttr('LIB_WORLD_Shoreline_hrc.translateY', 0.1) if cmds.objExists('LIB_WORLD_Shoreline_hrc') else None
		[(cmds.setAttr('%s.receiveShadows' % each, 0), cmds.setAttr('%s.motionBlur' % each, 0), cmds.setAttr('%s.primaryVisibility' % each, 0), cmds.setAttr('%s.visibleInReflections' % each, 0), cmds.setAttr('%s.visibleInRefractions' % each, 0)) for each in cmds.listRelatives('LIB_WORLD_Shoreline_hrc', allDescendents = True, fullPath = True, type = 'mesh')] if cmds.objExists('LIB_WORLD_Shoreline_hrc') else None
		[(cmds.setAttr('%s.receiveShadows' % each, 0), cmds.setAttr('%s.motionBlur' % each, 0), cmds.setAttr('%s.primaryVisibility' % each, 0), cmds.setAttr('%s.visibleInReflections' % each, 0), cmds.setAttr('%s.visibleInRefractions' % each, 0)) for each in cmds.listRelatives('LIB_WORLD_RoseInlet_Shoreline_hrc', allDescendents = True, fullPath = True, type = 'mesh')] if cmds.objExists('LIB_WORLD_RoseInlet_Shoreline_hrc') else None
		cmds.directionalLight(rotation = (-90, 0, 0), n = 'shorlineLight')
		cmds.setAttr("shorlineLightShape.useRayTraceShadows", 1)
		cmds.setAttr('LIB_WORLD_Shoreline_hrc.visibility', False)  if cmds.objExists('LIB_WORLD_Shoreline_hrc') else None
		cmds.setAttr('shorlineLight.visibility', False)

		CORALRipple = [x for x in cmds.ls("*shoreline*",type = "mesh", l =True) if "RoseInlet" in x or "CORALCAVE" in x] #
		CORALripple = [x for x in cmds.listRelatives(CORALRipple, p=True, fullPath =True)] if CORALRipple else None	
		[cmds.setAttr( "%s.visibility" %(x) , False ) for x in CORALripple] if CORALripple else None #

		cmds.createRenderLayer('LIB_WORLD_Shoreline_hrc', 'shorlineLight', 'ocean_srf', n = "ripple_LYR", noRecurse = True) if cmds.objExists('LIB_WORLD_Shoreline_hrc') else None
		cmds.createRenderLayer( CORALripple , 'shorlineLight', 'ocean_srf', n = "ripple_LYR", noRecurse = True) if CORALripple else None	
			
		cmds.editRenderLayerGlobals(currentRenderLayer = 'ripple_LYR')
		[cmds.setAttr( "%s.visibility" %(x) , True ) for x in ( CORALripple )] if CORALripple else None

		cmds.setAttr('LIB_WORLD_Shoreline_hrc.visibility', True) if cmds.objExists('LIB_WORLD_Shoreline_hrc') else None
		cmds.setAttr('shorlineLight.visibility', True)

		cmds.editRenderLayerAdjustment("mentalcoreGlobals.en_envl")
		cmds.setAttr("mentalcoreGlobals.en_envl", 0)
		cmds.editRenderLayerAdjustment("miDefaultOptions.finalGather")
		cmds.setAttr("miDefaultOptions.finalGather", 0)
		cmds.editRenderLayerAdjustment("mentalcoreGlobals.en_ao")
		cmds.setAttr("mentalcoreGlobals.en_ao", 0)

		cmds.sets('ocean_srf', edit = True, forceElement = 'RSHD_RippleShaderSG')
	
# def setRippleLYR():
# 	#FuncStart
# 	#Setting render layer
# 	#creating ripple shader
	
# 	try:
# 		cmds.delete(cmds.delete('*RSHD*'))
# 	except:
# 		pass
	
# 	if cmds.objExists('RSHD_rippleBase')==False:
# 		cmds.shadingNode('useBackground',asShader=True,n='RSHD_rippleBase')
# 		cmds.setAttr("RSHD_rippleBase.specularColor",0,0,0,type='double3')
# 		cmds.setAttr("RSHD_rippleBase.reflectivity",0)
# 		cmds.setAttr("RSHD_rippleBase.reflectionLimit",0)
# 		cmds.setAttr("RSHD_rippleBase.matteOpacity",5)

# 	if cmds.objExists('RSHD_foamBase')==False:
# 		cmds.shadingNode('surfaceShader',asShader=True,n='RSHD_foamBase')
# 		cmds.setAttr("RSHD_foamBase.outMatteOpacity",0,0,0,type='double3')
# 		cmds.connectAttr('RSHD_rippleBase.outMatteOpacity','RSHD_foamBase.outColor')

# 	if cmds.objExists('RSHD_shaderMerge')==False:
# 		cmds.shadingNode('layeredTexture',asShader=True,n='RSHD_shaderMerge')
# 		cmds.connectAttr('RSHD_foamBase.outColor','RSHD_shaderMerge.inputs[0].color')
# 		cmds.setAttr("RSHD_shaderMerge.inputs[1].color",0,0,0,type='double3')
# 		cmds.setAttr("RSHD_shaderMerge.inputs[1].blendMode",0)

# 	if cmds.objExists('RSHD_foamMerge')==False:
# 		cmds.shadingNode('surfaceShader',asShader=True,n='RSHD_foamMerge')
# 		cmds.connectAttr('RSHD_shaderMerge.outColor','RSHD_foamMerge.outColor')

# 	if cmds.objExists('RSHD_shaderReverse')==False:
# 		cmds.shadingNode('reverse',asShader=True,n='RSHD_shaderReverse')
# 		cmds.connectAttr('RSHD_foamMerge.outColor','RSHD_shaderReverse.input')

# 	if cmds.objExists('RSHD_RippleShader')==False:
# 		RippleShader=mel.eval('createRenderNodeCB -asShader "surfaceShader" lambert "";')
# 		cmds.rename(RippleShader,'RSHD_RippleShader')
# 		cmds.rename(cmds.listConnections('RSHD_RippleShader',type='shadingEngine'),'RSHD_RippleShaderSG')
# 		cmds.connectAttr('RSHD_shaderReverse.output','RSHD_RippleShader.transparency')
# 		cmds.setAttr("RSHD_RippleShader.color",1,1,1,type='double3')
# 		cmds.setAttr("RSHD_RippleShader.ambientColor",0.12,0.12,0.12,type='double3')
# 		cmds.connectAttr('ocean_dispShader.outColor','RSHD_RippleShaderSG.displacementShader')

# 	# #creating ripple layer
# 	if cmds.objExists('ripple_LYR')==False:
# 		cmds.createRenderLayer(n="ripple_LYR")
		
# 	#=====================
# 	#Master layer settings
# 	#=====================

# 	cmds.editRenderLayerGlobals(currentRenderLayer='defaultRenderLayer')

# 	#creating ripple layer specific light and doing linking

# 	if cmds.objExists('shorlineLight')==False:
# 		cmds.directionalLight(rotation=(-90,0,0),n='shorlineLight')
# 		cmds.setAttr('shorlineLight.scale',200,200,200,type='double3')
# 		try:
# 			cmds.disconnectAttr('shorlineLight.instObjGroups[0]','defaultLightSet.dagSetMembers[0]')
# 		except:
# 			pass
# 		cmds.setAttr('shorlineLight.visibility',False)
# 		cmds.setAttr("shorlineLightShape.useRayTraceShadows",1)

# 	slObj=cmds.ls(['*shoreline*','*ShoreLine*','*ocean_srf*','*Shoreline*'],type='transform',l=True)
# 	for eachObj in slObj:
# 		if not 'shorlineLight' in eachObj:
# 			cmds.lightlink(object=eachObj, light='shorlineLight')

# 	#creating a unique list of objects other than not required (this function has bugs, need to change as per new naming conventions)
# 	# comment for test
# 	#####everything=cmds.ls('*',type='transform',l=True)
# 	#####newList=[]
# 	#####for each in everything:
# 	#####	if "_geo" in each and not "CArch" in each and not "ShoreLine" in each and not "shoreline" in each and not "Shoreline" in each:
# 	#####		newList.append(each)

	

# 	#doing layer specific changes to shoreline geo   

# 	shorlineObj=cmds.ls(["*ShoreLine*","*shoreline*","*Shoreline*"],type="transform")
# 	for each in shorlineObj:
# 		if not "hrc" in each:
# 			cmds.setAttr(each+'.receiveShadows',0)  
# 			cmds.setAttr(each+'.primaryVisibility',0)
# 			cmds.setAttr(each+'.visibleInReflections',0)
# 			cmds.setAttr(each+'.visibleInRefractions',0)
# 			#cmds.setAttr(each+'.translateY',0.1)
# 			cmds.setAttr(each+'.visibility',0)

# 	cmds.editRenderLayerMembers('ripple_LYR',['*ocean_srf*','*ShoreLine*','*shoreline*','*Shoreline*'],noRecurse=True)

# 	#===================
# 	#ripple_LYR settings
# 	#===================

# 	cmds.editRenderLayerGlobals(currentRenderLayer='ripple_LYR')
# 	#Commenting for test
# 	#####everything=cmds.ls('*',type='shape')
# 	#####for each in everything:
# 	#####	if "_geo" in each and not "CArch" in each and not "ShoreLine" in each and not "shoreline" in each and not "Shoreline" in each:
# 	#####		cmds.setAttr(each+'.castsShadows',0)
			

# 	#setting attrs for objects
# 	#Commenting for test
# 	#####try:
# 	#####	cmds.hide(cmds.ls('*CArch*', type='transform'))
# 	#####except:
# 	#####	pass

# 	#####cmds.setAttr('ocean_srf.castsShadows',0)
	
# 	for eachObj in shorlineObj:
# 		if not "hrc" in eachObj:
# 			cmds.setAttr(eachObj+'.visibility',1)

# 	cmds.setAttr('shorlineLight.visibility',True)
# 	cmds.editRenderLayerMembers('ripple_LYR',['shorlineLight'],noRecurse=True)
# 	#####cmds.editRenderLayerMembers('ripple_LYR',newList,noRecurse=True)

# 	#doing layer based feature disable

# 	cmds.editRenderLayerAdjustment("mentalcoreGlobals.en_envl")
# 	cmds.setAttr("mentalcoreGlobals.en_envl",0)
# 	cmds.editRenderLayerAdjustment("miDefaultOptions.finalGather")
# 	cmds.setAttr("miDefaultOptions.finalGather",0)
# 	cmds.editRenderLayerAdjustment("mentalcoreGlobals.en_ao")
# 	cmds.setAttr("mentalcoreGlobals.en_ao",0)

# 	#assigning created shaders

# 	mel.eval('assignSG "RSHD_RippleShader" "ocean_srf"')
# 	#Commenting for test
# 	#####if cmds.objExists('RSHD_matte_ripple')==False:
# 	#####	matteRippleShader=mel.eval('mrCreateCustomNode -asShader "" core_material;')
# 	#####	cmds.rename(matteRippleShader,'RSHD_matte_ripple')
# 	#####	cmds.rename(cmds.listConnections('RSHD_matte_ripple',type='shadingEngine')[0],'RSHD_matte_rippleSG')
# 	#####	cmds.setAttr('RSHD_matte_ripple.output_override',3)

# 	#####cmds.sets(newList, e=True, forceElement='RSHD_matte_rippleSG')

# 	#FuncEnd

def setStormFoamLYR():

	
	ImportStormyFoamShader()
	connectStormyFoam()

	#creating stormFoam layer
	
	if cmds.objExists('stormyFoam_LYR')==False:
		cmds.createRenderLayer(n="stormyFoam_LYR")
			
	cmds.editRenderLayerGlobals(currentRenderLayer='defaultRenderLayer')
	everything=cmds.ls('*',type='transform',l=True)
	newList=[]
	for each in everything:
		if "_geo" in each and not "CArch" in each and not "ShoreLine" in each and not "shoreline" in each and not "Shoreline" in each:
			newList.append(each)

	cmds.editRenderLayerMembers('stormyFoam_LYR','*ocean_srf*',noRecurse=True)

	#Layer Specific settings

	cmds.editRenderLayerGlobals(currentRenderLayer='stormyFoam_LYR')

	#setting attrs for objects
	try:
		cmds.hide(cmds.ls('*CArch*', type='transform'))
	except:
		pass
		
	cmds.setAttr('ocean_srf.castsShadows',0)
	cmds.setAttr('oceanStormSeaFoam.foamEmission', 0.59)
	cmds.setAttr('oceanStormSeaFoam.foamThreshold', 0.6)
	cmds.editRenderLayerMembers('stormyFoam_LYR',newList,noRecurse=True)
	cmds.editRenderLayerMembers('stormyFoam_LYR',['sunDirection'],noRecurse=True)

	#doing layer based feature disable

	cmds.editRenderLayerAdjustment("mentalcoreGlobals.en_envl")
	cmds.setAttr("mentalcoreGlobals.en_envl",0)
	cmds.editRenderLayerAdjustment("miDefaultOptions.finalGather")
	cmds.setAttr("miDefaultOptions.finalGather",0)
	cmds.editRenderLayerAdjustment("mentalcoreGlobals.en_ao")
	cmds.setAttr("mentalcoreGlobals.en_ao",0)

	#assigning created shaders

	mel.eval('assignSG "stormSeaFoam" "ocean_srf"')
	if cmds.objExists('RSHD_matte_StormFoam')==False:
		matteRippleShader=mel.eval('mrCreateCustomNode -asShader "" core_material;')
		cmds.rename(matteRippleShader,'RSHD_matte_StormFoam')
		cmds.rename(cmds.listConnections('RSHD_matte_StormFoam',type='shadingEngine')[0],'RSHD_matte_StormFoamSG')
		cmds.setAttr('RSHD_matte_StormFoam.output_override',3)

	cmds.sets(newList, e=True, forceElement='RSHD_matte_StormFoamSG')

def setOceanFoamSepLYR():

	connectCharFoam()
	
	#creating stormFoam layer
	
	if cmds.objExists('OceanFoamSep_LYR')==False:
		cmds.createRenderLayer(n="OceanFoamSep_LYR")
			
	cmds.editRenderLayerGlobals(currentRenderLayer='defaultRenderLayer')
	everything=cmds.ls('*',type='transform',l=True)
	newList=[]
	for each in everything:
		if "_geo" in each and not "CArch" in each and not "ShoreLine" in each and not "shoreline" in each and not "Shoreline" in each:
			newList.append(each)

	cmds.editRenderLayerMembers('OceanFoamSep_LYR','*ocean_srf*',noRecurse=True)

	#Layer Specific settings

	cmds.editRenderLayerGlobals(currentRenderLayer='OceanFoamSep_LYR')

	#setting attrs for objects
	try:
		cmds.hide(cmds.ls('*CArch*', type='transform'))
	except:
		pass
		
	cmds.setAttr('ocean_srf.castsShadows',0)
	cmds.editRenderLayerMembers('OceanFoamSep_LYR',newList,noRecurse=True)
	cmds.editRenderLayerMembers('OceanFoamSep_LYR',['sunDirection'],noRecurse=True)

	#doing layer based feature disable

	cmds.editRenderLayerAdjustment("mentalcoreGlobals.en_envl")
	cmds.setAttr("mentalcoreGlobals.en_envl",0)
	cmds.editRenderLayerAdjustment("miDefaultOptions.finalGather")
	cmds.setAttr("miDefaultOptions.finalGather",0)
	cmds.editRenderLayerAdjustment("mentalcoreGlobals.en_ao")
	cmds.setAttr("mentalcoreGlobals.en_ao",0)

	#assigning created shaders

	mel.eval('assignSG "charSeaFoam" "ocean_srf"')
	if cmds.objExists('RSHD_matte_StormFoam')==False:
		matteRippleShader=mel.eval('mrCreateCustomNode -asShader "" core_material;')
		cmds.rename(matteRippleShader,'RSHD_matte_StormFoam')
		cmds.rename(cmds.listConnections('RSHD_matte_StormFoam',type='shadingEngine')[0],'RSHD_matte_StormFoamSG')
		cmds.setAttr('RSHD_matte_StormFoam.output_override',3)

	cmds.sets(newList, e=True, forceElement='RSHD_matte_StormFoamSG')

def setBGHills():
	FilePath = 'I:/bubblebathbay/assets/LibraryAsset/LIB_WORLD_BGhill/SRF/publish/maya/'
	File = os.listdir(FilePath)
	Latest = 0
	Num = 0
	BasicPasses=["ao","beauty","colour","depth_norm","diffuse","environment","facing_ratio","incandescence","indirect","reflection","refraction","specular"]
	Members = ["LIB_WORLD_BGhills_hrc","LIGHTS_hrc"] if cmds.objExists("LIGHTS_hrc") else ["LIB_WORLD_BGhills_hrc"]

	for v in File:
		if "LIBWORLDBGhill" in v:
			Num = v.split('.')[-2].lstrip("v") if int(v.split('.')[-2].lstrip("v")) > Latest else Num
			Latest = int(Num)

	Version = "%.3d" %Latest
	if cmds.objExists("LIB_WORLD_BGhills_hrc")==False:     
		cmds.file('I:/bubblebathbay/assets/LibraryAsset/LIB_WORLD_BGhill/SRF/publish/maya/LIBWORLDBGhill.v%s.mb' %Version,i=True )  
	try:
		cmds.editRenderLayerGlobals(currentRenderLayer='defaultRenderLayer')
	except:
		pass

	if cmds.objExists("LIB_WORLD_BGhills_hrc"):    
		cmds.setAttr("LIB_WORLD_BGhills_hrc.visibility",0)
		if cmds.objExists("BGHills_LYR")==False:         
			cmds.createRenderLayer(n="BGHills_LYR")
		cmds.editRenderLayerMembers("BGHills_LYR",Members,noRecurse=True)
		cmds.editRenderLayerGlobals(currentRenderLayer="BGHills_LYR")
		
		cmds.setAttr("LIB_WORLD_BGhills_hrc.visibility",1)
		
	if cmds.objExists("BGHills_LYR"):
		for x in BasicPasses:
			mapi.associate_pass(x,"BGHills_LYR")

	for mesh in cmds.listRelatives("LIB_WORLD_BGhills_hrc",ad=True,type='mesh',fullPath=True):
		if not cmds.objExists('%s.miSubdivApprox' %mesh):
			cmds.addAttr(mesh,longName="miSubdivApprox",dataType="string")
		try:
			cmds.connectAttr('auto_mrSubdAppx.message','%s.miSubdivApprox' %mesh)
		except:
			pass	     

def ExtendOceanMatte():
	if cmds.objExists("fakeOceanPlane_geo"):
		if not cmds.listConnections("matte_water.linked_objs[1]"):
			cmds.connectAttr("fakeOceanPlane_geo.message","matte_water.linked_objs[1]",force = True)
		if cmds.objExists("matte_ExtendOcean")==False:
			matte_node = mapi.create_pass( 'Matte', n = "matte_ExtendOcean" )
			cmds.setAttr('matte_ExtendOcean.en_obj_linking', 1)
		if not cmds.listConnections("matte_ExtendOcean.linked_objs[0]"):
			cmds.connectAttr("fakeOceanPlane_geo.message","matte_ExtendOcean.linked_objs[0]",force = True)
		mapi.associate_pass("matte_ExtendOcean", 'defaultRenderLayer')    
		
## Set SubD Levels
def setSubD():
	mrSubDNodes = cmds.ls(type = 'mentalraySubdivApprox')
	[cmds.setAttr('%s.maxSubdivisions' % each, 2) for each in mrSubDNodes] if mrSubDNodes else None

## Preview Render Settings
def previewSettings():
	cmds.setAttr("mentalcoreGlobals.unified_sampling", 1)
	cmds.setAttr("mentalcoreGlobals.samples_max", 50)
	cmds.setAttr("mentalcoreGlobals.samples_quality", 0.1)
	cmds.setAttr("mentalcoreGlobals.samples_error_cutoff", 0.05)

## Render final Settings
def finalSettings():
	cmds.setAttr("mentalcoreGlobals.unified_sampling", 1)
	cmds.setAttr("mentalcoreGlobals.samples_max", 80)
	cmds.setAttr("mentalcoreGlobals.samples_quality", 0.8)
	cmds.setAttr("mentalcoreGlobals.samples_error_cutoff", 0.02)

## Feature Displacement OFF
def turnOffFD():
	meshes = cmds.ls(type = 'mesh', l = True)
	[cmds.setAttr('%s.featureDisplacement' % mesh, 0) for mesh in meshes] if meshes else None

def killEyeWhites():
	eyeShapeNodes = cmds.ls('*eyeball_white*', type = 'mesh', long = True)
	eyeNodeSG = [sg for mesh in eyeShapeNodes for sg in cmds.listSets(type = 1, object = mesh)] if eyeShapeNodes else None
	core_materials = [cmds.listConnections('%s.miMaterialShader' % cm, source = True, destination = True)[0] if cmds.listConnections('%s.miMaterialShader' % cm, source = True, destination = True) else None for cm in eyeNodeSG] if eyeNodeSG else None
	core_materials = list( set( core_materials ) ) if core_materials else None
	core_materials = [each for each in core_materials if each is not None] if core_materials else None
	[cmds.setAttr('%s.diffuse_weight' % mat, 0.5) for mat in core_materials] if core_materials else None

def importWorldClouds():
	cmds.file('I:/bubblebathbay/assets/LibraryAsset/LIB_WORLD_Sunnycloud/SRF/work/maya/LIBWORLDSunnycloud.v005.ma',i=True)

def importWorldHills():
	cmds.file('I:/bubblebathbay/assets/LibraryAsset/LIB_WORLD_BGhill/SRF/publish/maya/LIBWORLDBGhill.v003.mb',i=True)

def importTWD():
	cmds.file('T:/misc/Lighting-DoNotDelete/ENV/twr.ma', i = True)

def importSLG():
	cmds.file('T:/misc/Lighting-DoNotDelete/ENV/ground_terrain.mb', i = True)

def importMGH():
	cmds.file('T:/misc/Lighting-DoNotDelete/ENV/MangoHill.ma', i = True)

def importFloatingDocks():
	cmds.file('T:/misc/Lighting-DoNotDelete/ENV/BakedDocks.ma', i = True)

def removeEmptyGroups():
	## First, get all groups
	transforms = cmds.ls(type = 'transform', dag = True, long = True)
	
	## Then, filter those that are end child only
	end_child = [each for each in transforms if not cmds.listRelatives(each, children = True) and not cmds.listConnections(each)]
	
	## Delete empty groups
	[cmds.delete(each) for each in end_child] if end_child else None
	
	return end_child

## RenderSetUp button
def RenderSetup():
	fileRenderSettings()
	killRandomiser()
	turnOffEyeShad()
	setSubD()
	turnOffFD()
	killEyeWhites()

	## Mattes
	createPropMattes() if cmds.checkBox('createPropMattesCB', value = True, query = True) else None
	createCharMattes() if cmds.checkBox('createCharMattesCB', value = True, query = True) else None
	createCharTongueMattes() if cmds.checkBox('createCharTongueMattesCB', value = True, query = True) else None
	createEyeMattes() if cmds.checkBox('createEyeMattesCB', value = True, query = True) else None
	createEyelashMattes() if cmds.checkBox('createEyelashMattesCB', value = True, query = True) else None
	createBuildingMattes() if cmds.checkBox('createBuildingMattesCB', value = True, query = True) else None
	createOceanMattes() if cmds.checkBox('createOceanMattesCB', value = True, query = True) else None
	createLandMattes() if cmds.checkBox('createLandMattesCB', value = True, query = True) else None
	createCoreArchiveMattes() if cmds.checkBox('createCoreArchiveMattesCB', value = True, query = True) else None
	createCPropMattes() if cmds.checkBox('createPropMattesCB', value = True, query = True) else None
	createSydneySailMattes() if cmds.checkBox('createSydneySailMattesCB', value = True, query = True) else None
	#createLightsMattes() if cmds.checkBox('createLightsMattesCB', value = True, query = True) else None

	## Subdiv approximation
	subdivSmoothedAttr()

	## Ambient Occlusion overrides
	fixBgOcc() if cmds.checkBox('fixBgOccCB', value = True, query = True) else None#fixBgOccOff()

	## Clean-ups
	cleanupNonManifoldGeometry() if cmds.checkBox('cleanupNonManifoldGeometryCB', value = True, query = True) else None
	KillSmooth.UnsmoothSetUp()
	removeCoreArchiveOfOrigin() if cmds.checkBox('removeCoreArchiveOfOriginCB', value = True, query = True) else None

	## Fix bad long passes name
	bad_passes_name = [crp for crp in mapi.get_associated_passes('defaultRenderLayer') if len(crp) > 29]
	[mapi.unassociate_pass(crp, 'defaultRenderLayer') for crp in bad_passes_name]
	ExtendOceanMatte()

	## Remove Empty MentalCore Render Pass's mattes
	removeEmptyRenderPassMattes()

	## Cornea reflection fix
	characterCorneaFix()
	#animCacheVersion
	animCacheVersionToLog()
	FXVersionToLog()
	HardSurface()
	TurnOffEyeLashBlinn()
	ResetSubdiv()

	## More stuffs
	while removeEmptyGroups():
		removeEmptyGroups()

def removeEmptyRenderPassMattes():
	for x in mapi.get_associated_passes('defaultRenderLayer'):
		
		linked_objs = cmds.listConnections('%s.linked_objs' % x)
		if linked_objs:
			
			# objs_visibility = True
			objs_visibility = []
			for each in linked_objs:
				if nodeIsVisible(each) == False:
					objs_visibility.append(False)
				else:
					objs_visibility.append(True)
					break
					
			if True not in objs_visibility:
				mapi.unassociate_pass(x, 'defaultRenderLayer')

def nodeIsVisible(node):
	## If user is asking about a bogus node, return FALSE.
	if not cmds.objExists(node):
		return False

	## Object must be a DAG node, or it's not visible.
	## There's no MEL query to identify a DAG node, but the kDagNode class adds
	## the '.visibility' attribute, so we'll use its existence as a cue.
	if not cmds.attributeQuery('visibility', node = node, exists = True):
		return False

	## The obvious: Start with the '.visibility' attribute on the node.
	visible = cmds.getAttr("%s.visibility" % node)

	## If this is an intermediate mesh, it's not visible.
	if cmds.attributeQuery('intermediateObject', node = node, exists = True):
		visible = visible and not cmds.getAttr("%s.intermediateObject" % node)

	## If the object is in a displayLayer, and the displayLayer is hidden,
	## then the object is hidden.
	if cmds.attributeQuery('overrideEnabled', node = node, exists = True) and cmds.getAttr("%s.overrideEnabled" % node):
		visible = visible and cmds.getAttr("%s.overrideVisibility" % node)

	## Ascend the hierarchy and check all of the parent nodes.
	if visible:
		parents = cmds.listRelatives(node, parent = True, fullPath = True)
		if parents:
			visible = visible and nodeIsVisible(parents[0])
	
	return visible
	
def fixBgOcc():
	alembic_nodes = cmds.ls(type = 'AlembicNode')
	if alembic_nodes:
		all_geo = cmds.ls(type = 'mesh', long = True)
		#alembic_nodes = cmds.ls(type = 'AlembicNode')
		animated_geo = cmds.filterExpand(cmds.listHistory(alembic_nodes, future = True), sm = 12, fullPath = True) if alembic_nodes else None
		non_animated_geo = [geo for geo in all_geo if geo not in animated_geo] if animated_geo else None
	else:
		non_animated_geo = cmds.ls(type = 'mesh', long = True)
		
	shadingEngines = [cmds.listConnections(geo, type = 'shadingEngine')[0] for geo in non_animated_geo if cmds.listConnections(geo, type = 'shadingEngine')] if non_animated_geo else None
	shadingEngines = list( set( shadingEngines ) ) if shadingEngines else None
	core_materials = [cmds.listConnections(se, type = 'core_material')[0] for se in shadingEngines if cmds.listConnections(se, type = 'core_material')] if shadingEngines else None
	[(cmds.setAttr('%s.ao_enable_overrides' % mat, 1), cmds.setAttr('%s.ao_override_spread' % mat, 90), cmds.setAttr('%s.ao_override_samples' % mat, 24), cmds.setAttr('%s.ao_override_distance' % mat, 1000)) for mat in core_materials] if core_materials else None

def fixBgOccOff():
	all_geo = cmds.ls(type = 'mesh', long = True)
	alembic_nodes = cmds.ls(type = 'AlembicNode')
	animated_geo = cmds.filterExpand(cmds.listHistory(alembic_nodes, future = True), sm = 12, fullPath = True) if alembic_nodes else None
	non_animated_geo = [geo for geo in all_geo if geo not in animated_geo] if animated_geo else None
	shadingEngines = [cmds.listConnections(geo, type = 'shadingEngine')[0] for geo in non_animated_geo if cmds.listConnections(geo, type = 'shadingEngine')] if non_animated_geo else None
	shadingEngines = list( set( shadingEngines ) ) if shadingEngines else None
	core_materials = [cmds.listConnections(se, type = 'core_material')[0] for se in shadingEngines if cmds.listConnections(se, type = 'core_material')] if shadingEngines else None
	[(cmds.setAttr('%s.ao_enable_overrides' % mat, 1), cmds.setAttr('%s.ao_override_spread' % mat, 60), cmds.setAttr('%s.ao_override_samples' % mat, 24), cmds.setAttr('%s.ao_override_distance' % mat, 10)) for mat in core_materials] if core_materials else None

def searchExtension(directory = '', imageName = ''):
	if os.path.exists(directory):
		imageExtensions = ['.iff', '.tif', '.tiff', '.bmp', '.tga', '.psd', '.jpg', '.jpeg', '.png', '.exr']
		image = [ os.path.join(directory, x).replace('\\', '/') for x in os.listdir(directory) if os.path.splitext(x)[-1].lower() in imageExtensions and os.path.splitext(x)[0].lower() in imageName.lower() ]
		if image:
			return image[0]

def swapToLowRes(fileIn = '', fullResPath = ''):
	if cmds.objExists(fileIn) and os.path.exists(fullResPath):
		lowResPath = '%s.png' % os.path.splitext( os.path.abspath( os.path.join( os.path.dirname(fullResPath), '256', os.path.basename(fullResPath) ) ).replace('\\', '/') )[0]
		if os.path.exists(lowResPath):
			cmds.setAttr('%s.fileTextureName' % fileIn, lowResPath, type = 'string')
		else:
			if 'work/maya' in lowResPath:
				lowResPath = lowResPath.replace('work/maya', 'publish')
			elif 'publish' in lowResPath:
				lowResPath = lowResPath.replace('publish', 'work/maya')

			if os.path.exists(lowResPath):
				cmds.setAttr('%s.fileTextureName' % fileIn, lowResPath, type = 'string')
			else:
				cmds.warning('%s doesn\'t exist, skipping...' % lowResPath)

def swapToFullRes(fileIn = '', lowResPath = ''):
	if cmds.objExists(fileIn) and os.path.exists(lowResPath):
		fullResPath = os.path.splitext( os.path.abspath( os.path.join( os.path.dirname( os.path.dirname(lowResPath) ), os.path.basename(lowResPath) ) ).replace('\\', '/') )[0]
		fullResPath = searchExtension( directory = os.path.dirname(fullResPath), imageName = os.path.basename(fullResPath) )
		if fullResPath:
			if os.path.exists(fullResPath):
				cmds.setAttr('%s.fileTextureName' % fileIn, fullResPath, type = 'string')
			else:
				if 'work/maya' in fullResPath:
					fullResPath = fullResPath.replace('work/maya', 'publish')
				elif 'publish' in fullResPath:
					fullResPath = fullResPath.replace('publish', 'work/maya')

				if os.path.exists(fullResPath):
					cmds.setAttr('%s.fileTextureName' % fileIn, fullResPath, type = 'string')
				else:
					cmds.warning('%s doesn\'t exist, skipping...' % fullResPath)

def fullToLowRes():
	#skipAsset = ['CharacterA', 'CharacterB', 'CharacterC', 'Prop', 'Interactive-Prop']
	skipAsset = ['']

	selection = [x for x in cmds.ls(selection = True, l = True)]
	if selection:
		selection = cmds.filterExpand(selection, selectionMask = 12, fullPath = True)
		if selection:
			for each in selection:
				se = cmds.listConnections(each, type = 'shadingEngine')
				if se:
					fileIns = [x for x in cmds.listHistory(se[0], allConnections = True) if cmds.nodeType(x) == 'file' or cmds.nodeType(x) == 'mentalrayTexture']
					if fileIns:
						for x in fileIns:
							fullResPath = cmds.getAttr('%s.fileTextureName' % x)
							if '256' not in fullResPath.split('/')[-2]:
								swapToLowRes(fileIn = x, fullResPath = fullResPath) if fullResPath.split('/')[3] not in skipAsset else None

def lowToFullRes():
	#skipAsset = ['CharacterA', 'CharacterB', 'CharacterC', 'Prop', 'Interactive-Prop']
	skipAsset = ['']

	selection = [x for x in cmds.ls(selection = True, l = True)]
	if selection:
		selection = cmds.filterExpand(selection, selectionMask = 12, fullPath = True)
		if selection:
			for each in selection:
				se = cmds.listConnections(each, type = 'shadingEngine')
				if se:
					fileIns = [x for x in cmds.listHistory(se[0], allConnections = True) if cmds.nodeType(x) == 'file' or cmds.nodeType(x) == 'mentalrayTexture']
					if fileIns:
						for x in fileIns:
							lowResPath = cmds.getAttr('%s.fileTextureName' % x)
							if '256' in lowResPath.split('/')[-2]:
								swapToFullRes(fileIn = x, lowResPath = lowResPath) if lowResPath.split('/')[3] not in skipAsset else None

###########################
## Create mentalcore mattes
###########################

def createPropMattes():
	alembic_nodes = cmds.ls(type = 'AlembicNode')
	animated_geo = cmds.filterExpand(cmds.listHistory(alembic_nodes, future = True), sm = 12, fullPath = True) if alembic_nodes else None
	filter_anim_geo_root = {}
	[filter_anim_geo_root.setdefault(each, []) for mesh in animated_geo for each in mesh.split('|') if each.startswith('PROP_') and each.endswith('_hrc')] if animated_geo else None
	jajaja = [cmds.ls(root, long = True)[0] if cmds.listRelatives(cmds.ls(root, long = True)[0], allDescendents = True, type = 'mesh') else None for root in filter_anim_geo_root] if filter_anim_geo_root else None
	[filter_anim_geo_root[root.split('|')[-1]].append( cmds.listRelatives(mesh, parent = True, fullPath = True)[0] ) for root in jajaja if cmds.listRelatives(root, allDescendents = True, fullPath = True, type = 'mesh') for mesh in cmds.listRelatives(root, allDescendents = True, fullPath = True, type = 'mesh')] if jajaja else None

	if filter_anim_geo_root:
		for mat, geo in filter_anim_geo_root.iteritems():
			matte_name = 'matte_%s' % mat.strip('_hrc')
			cmds.delete(matte_name) if cmds.objExists(matte_name) else None
			matte_node = mapi.create_pass( 'Matte', n = matte_name )
			cmds.setAttr('%s.en_obj_linking' % matte_node, 1)
			# mapi.link_to_pass(geo, matte_node, mapi.OBJECTS)
			mentalCoreLink(geo, matte_node)
			mapi.associate_pass(matte_node, 'defaultRenderLayer')

	BuoyTop = filter(lambda x: ('lightcover_geo' in x or 'lightbulb_geo' in x ) and 'buoy' in x.lower() ,cmds.ls(['*lightcover_geo*','lightbulb_geo*'],type="transform",l=True))
	if BuoyTop:
		cmds.delete('matte_BuoyTop') if cmds.objExists('matte_BuoyTop') else None
		mapi.create_pass('Matte', n = 'matte_BuoyTop')
		cmds.setAttr('%s.en_obj_linking' % 'matte_BuoyTop', 1)
		# mapi.link_to_pass(filtered_geo, 'matte_TerryStorageShed', mapi.OBJECTS)
		mentalCoreLink(BuoyTop, 'matte_BuoyTop')
		mapi.associate_pass('matte_BuoyTop', 'defaultRenderLayer')	

def createLightsMattes():

	SignalLight = [x for x in cmds.ls('*RedLightGlass*','*l_light_geo*','*r_light_geo*','*_sidelight_*','*_sideLight_*','*redlight*','*greenlight*','*red_light_geo*','*green_light*','*light_green*','*light_red*',long=True) if (cmds.nodeType(x)=='mesh' or cmds.nodeType(x)=='nurbsSurface' ) and not 'BLD' in x]
	Spotlight = [x for x in cmds.ls('*lightcover_geo*','*spotlight_glass_geo*','*spotlightglass_geo*','light_cover_geo*','*mainlight_geo*','*CHAR_Zip_hrc|geo_hrc|main_glass_geo|main_glass_geoShape','frontlight_geo*','backlight_geo*',long=True) if (cmds.nodeType(x)=='mesh' or cmds.nodeType(x)=='nurbsSurface' ) and not 'BLD' in x]
	FlagLight = [x for x in cmds.ls('*antennaball_geo*','*flag_ball_geo*','*yellowlight*','*yellow_light*','*mast_sphere*','*flag_light_geo*','MainlPillarTop_geo*','topLight_geo*',long=True) if (cmds.nodeType(x)=='mesh' or cmds.nodeType(x)=='nurbsSurface' ) and not 'BLD' in x]
	BulbLight = [x for x in cmds.ls('*BigPort_LND_3*','*lamp_glass*','*AI_Jetty_cluttrt_565_geo*','*lampost_glass*','*Bulb*','*bulb*','*Lamp_glass*',long=True) if (cmds.nodeType(x)=='mesh' or cmds.nodeType(x)=='nurbsSurface') and not 'standlightbulb_geo' in x and not 'BLD' in x]
	RedLight = [x for x in SignalLight if (('l_light_green_geo' in x.lower() and 'terry' in x.lower()) or 'RedLightGlass01_geo' in x or 'l_light_geo' in x.lower() or 'l_sidelight' in x.lower() or 'red' in x.lower()) and not 'r_redlightbase_geo' in x and not 'l_redlightbase_geo' in x and not 'r_baseredlight_geo' in x and not 'l_baseredlight_geo' in x and not 'r_red_sideLight_geo' in x and not 'RedLightGlass02_geo' in x and not ('GEN009_MarinaBoat' in x and 'r_redlight_geo' in x) and not ('CHAR_GEN002_MarinaBoat_hrc' in x and 'r_redlight_geo' in x)] if SignalLight else None
	GreenLight = [x for x in SignalLight if (('CHAR_GEN002_MarinaBoat_hrc' in x and 'r_redlight_geo' in x) or ('GEN009_MarinaBoat' in x and 'r_redlight_geo' in x) or ('RedLightGlass02_geo' in x and 'Jett' in x) or 'r_light_geo' in x.lower() or 'r_sidelight' in x.lower() or 'green' in x.lower() or 'r_red_sideLight_geo' in x) and not 'r_baseredlight_geoShape' in x and not ('CHAR_Jett_hrc' in x and 'greenlight_geo' in x)] if SignalLight else None
	WindowLight = [x for x in cmds.ls('*r_portHole_window_geo*','*l_portHole_window_geo*','*windowGlass_geo*','*frontGlass*','*window*','*glass_M_geo*','*doorGlass_*','glass_geo*','r_glass_geo*','l_glass_geo*','*glass01_geo*','*glass02_geo*',long=True) if (cmds.nodeType(x)=='mesh' or cmds.nodeType(x)=='nurbsSurface') and not 'standlightbulb_geo' in x and not 'BLD' in x]
	LightShader = ['AdmiralBridge_lambert30SG','BigTown_01_LND_9_SG','BigPort_LND_3_SG1','DingleIsland_LND_lamp_glass_SG'#,'MulliganTown_East_LND'
	]
	WindowLight = filter(lambda x: not ('CHAR_Samira_hrc' in x and 'Broder' in x ) and not ('CHAR_Minder_hrc' in x and 'holder' in x ) and not ('CHAR_Jett_hrc' in x and 'glass_geo' in x) and not ('CHAR_Lulu_hrc' in x and ('l_windowpot_geo' in x or 'r_windowpot_geo' in x)) and not ('CHAR_Cleo_hrc' in x and 'windowFrame_geo' in x) and not ('CHAR_Rodney_hrc' in x and ('r_mini_window_frame_geo' in x or 'l_mini_window_frame_geo' in x)) and not ('CHAR_GEN002_MarinaBoat_hrc' in x and ('l_sidewindow_geo' in x or 'r_sidewindow_geo' in x)) , WindowLight) if WindowLight else None 
	FlagLight = filter(lambda x: not ( 'CHAR_Minder_hrc' in x and 'flag_ball_geo' in x ) , FlagLight) if FlagLight else None 

	SignalLights = [cmds.listRelatives(x, parent = True, fullPath = True,type='transform')[0] for x in SignalLight] if SignalLight else None
	RedLights = [cmds.listRelatives(x, parent = True, fullPath = True,type='transform')[0] for x in RedLight] if RedLight else None
	GreenLights = [cmds.listRelatives(x, parent = True, fullPath = True,type='transform')[0] for x in GreenLight] if GreenLight else None
	Spotlights = [cmds.listRelatives(x, parent = True, fullPath = True,type='transform')[0] for x in Spotlight] if Spotlight else None
	FlagLights = [cmds.listRelatives(x, parent = True, fullPath = True,type='transform')[0] for x in FlagLight] if FlagLight else None
	BulbLights = [cmds.listRelatives(x, parent = True, fullPath = True,type='transform')[0] for x in BulbLight] if BulbLight else None
	WindowLights = [cmds.listRelatives(x, parent = True, fullPath = True,type='transform')[0] for x in WindowLight] if WindowLight else None

	lightMattes = [BulbLights,FlagLights,Spotlights,SignalLights,GreenLights,RedLights,WindowLights]
	nameMatt = ('BulbLights','FlagLights','Spotlights','NavLights','GreenLights','RedLights','WindowLights')
	num=0
	for matt in lightMattes:
		if matt: 
			matte_name = 'matte_%s' % nameMatt[num]
			cmds.delete(matte_name) if cmds.objExists(matte_name) else None
			matte_node = mapi.create_pass( 'Matte', n = matte_name )
			cmds.setAttr('%s.en_obj_linking' % matte_node, 1)
			try:
				mapi.link_to_pass(LightShader, matte_node, mapi.MATERIALS) if num==0 else None
			except:
				pass
			## mapi.link_to_pass(geo, matte_node, mapi.OBJECTS)
			mentalCoreLink(matt, matte_node)
			#mapi.associate_pass(matte_node, 'defaultRenderLayer')
			num+=1
		else:
			num+=1
	#Temporary fix for signal red light		
	mapi.link_to_pass(["CHARMinder_CHARMuddles_greenlight_SG1"], 'matte_GreenLights', mapi.MATERIALS) if cmds.objExists("CHARMinder_CHARMuddles_greenlight_SG1") and "matte_GreenLights" else None

	#############################################################
	#############################################################
	##ColorLighBultVariable
	YellowBulb = cmds.ls(["*yellowBulb*","*Yellow_LightBulb*","*LightBulb_Yellow*"],type="transform",l=True)
	RedBulb = cmds.ls(["*redBulb*","*Red_LightBulb*","*LightBulb_Red*"],type="transform",l=True)
	PurpleBulb = cmds.ls(["*prupleBulb*","*purpleBulb*","*Purple_LightBulb*","*LightBulb_Purple*"],type="transform",l=True)
	AllGreen = cmds.ls(["*green2*","*green1*","*greenBulb*","*Green_LightBulb*","*LightBulb_Green*","*green30_geo*"],type="transform",l=True)
	GreenBulb=filter(lambda x: not("green1_geo" in x or "green2_geo" in x or "green10_geo" in x or "green11_geo" in x), AllGreen)
	OrangeBulb = cmds.ls(["*orangeBulb*","*Orange_LightBulb*","*LightBulb_Orange*"],type="transform",l=True)
	BlueBulb = cmds.ls(["*blueBulb*","*Blue_LightBulb*","*LightBulb_Blue*"],type="transform",l=True)
	#############################################################

	##Create SurfaceShader
	[cmds.delete(x) for x in cmds.ls("*RedSurface*",l=True) if len(cmds.ls("*RedSurface*",l=True))!=0 ]
	SurfaceSHD = mel.eval('mrCreateCustomNode -asShader "" core_surface_shader;')
	cmds.rename(SurfaceSHD,'RedSurface');cmds.rename(cmds.listConnections('RedSurface',type='shadingEngine')[0],'RedSurfaceSG')
	[cmds.delete(x) for x in cmds.ls("*GreenSurface*",l=True) if len(cmds.ls("*GreenSurface*",l=True))!=0 ]
	SurfaceSHD = mel.eval('mrCreateCustomNode -asShader "" core_surface_shader;')
	cmds.rename(SurfaceSHD,'GreenSurface');cmds.rename(cmds.listConnections('GreenSurface',type='shadingEngine')[0],'GreenSurfaceSG')
	[cmds.delete(x) for x in cmds.ls("*BlueSurface*",l=True) if len(cmds.ls("*BlueSurface*",l=True))!=0 ]
	SurfaceSHD = mel.eval('mrCreateCustomNode -asShader "" core_surface_shader;')
	cmds.rename(SurfaceSHD,'BlueSurface');cmds.rename(cmds.listConnections('BlueSurface',type='shadingEngine')[0],'BlueSurfaceSG')

	cmds.setAttr("RedSurface.colour", 1 , 0 , 0 ,type='double3')
	cmds.setAttr("BlueSurface.colour", 0 , 0 , 1 ,type='double3')
	cmds.setAttr("GreenSurface.colour", 0 , 1 , 0 ,type='double3')
	##############################################################
	Material = cmds.ls(type = "core_material")
	if not cmds.objExists('ExtraShader'):
		LShader = mel.eval('mrCreateCustomNode -asShader "" core_material;')
		cmds.rename(LShader,'ExtraShader')
		cmds.rename(cmds.listConnections('ExtraShader',type='shadingEngine')[0],'ExtraShaderSG')
		cmds.setAttr("ExtraShader.diffuse",1,1,1,type='double3')
		cmds.setAttr("ExtraShader.en_blinn", 0)
	
	AllMesh = cmds.ls(type = 'mesh')
	cmds.sets( AllMesh , e=True, forceElement='ExtraShaderSG') if AllMesh else None
	cmds.setAttr("ExtraShader.output_override",1)

	##LightBultMatte1	
	if len(RedBulb+GreenBulb+BlueBulb)!=0:
		cmds.createRenderLayer(n="LightBultMatte1") if cmds.objExists("LightBultMatte1")==False or RedBulb or GreenBulb or BlueBulb else None
		cmds.editRenderLayerGlobals(currentRenderLayer="LightBultMatte1")
		cmds.editRenderLayerMembers("LightBultMatte1",cmds.ls(type='transform'),noRecurse=True)
		cmds.sets(RedBulb, e=True, forceElement='RedSurfaceSG') if RedBulb else None
		cmds.sets(GreenBulb, e=True, forceElement='GreenSurfaceSG') if GreenBulb else None
		cmds.sets(BlueBulb, e=True, forceElement='BlueSurfaceSG') if BlueBulb else None
		# for x in Material:
		# 	if not "BlueSurface" in x or not "GreenSurface" in x or not "RedSurface" in x:
		# 		cmds.setAttr(x+".output_override",1)
		[cmds.setAttr('%s.visibility' %cmds.listRelatives(x,p=True,type="transform")[0] ,0 ) for x in cmds.ls() if "light" in cmds.nodeType(x).lower() and ("direct" in cmds.nodeType(x).lower()  or "spot" in cmds.nodeType(x).lower())]
		cmds.setAttr("oceanWater_cMia_shd.output_override",1) if cmds.objExists("oceanWater_cMia_shd") else None

	##LightBultMatte2
	if len(YellowBulb+OrangeBulb+PurpleBulb)!=0:
		cmds.createRenderLayer(n="LightBultMatte2") if cmds.objExists("LightBultMatte2")== False or YellowBulb or OrangeBulb or PurpleBulb else None
		cmds.editRenderLayerMembers("LightBultMatte2",cmds.ls(),noRecurse=True)
		cmds.editRenderLayerGlobals(currentRenderLayer="LightBultMatte2")
		cmds.sets(YellowBulb, e=True, forceElement='RedSurfaceSG') if YellowBulb else None
		cmds.sets(OrangeBulb, e=True, forceElement='GreenSurfaceSG') if OrangeBulb else None
		cmds.sets(PurpleBulb, e=True, forceElement='BlueSurfaceSG') if PurpleBulb else None
		# for x in Material:
		# 	if not "BlueSurface" in x or not "GreenSurface" in x or not "RedSurface" in x:
		# 		cmds.setAttr(x+".output_override",1)
		[cmds.setAttr('%s.visibility' %cmds.listRelatives(x,p=True,type="transform")[0] ,0 ) for x in cmds.ls() if "light" in cmds.nodeType(x).lower() and ("direct" in cmds.nodeType(x).lower()  or "spot" in cmds.nodeType(x).lower())]
		cmds.setAttr("oceanWater_cMia_shd.output_override",1) if cmds.objExists("oceanWater_cMia_shd") else None

	##NaviSpotLightMatte
	if len(RedLight+GreenLight+Spotlight)!=0:
		cmds.createRenderLayer(n="NaviSpotLightMatte") if cmds.objExists("NaviSpotLightMatte")==False or RedLight or GreenLight or Spotlight else None
		cmds.editRenderLayerMembers("NaviSpotLightMatte",cmds.ls(),noRecurse=True)
		cmds.editRenderLayerGlobals(currentRenderLayer="NaviSpotLightMatte")
		cmds.sets(RedLight, e=True, forceElement='RedSurfaceSG') if RedLight else None
		cmds.sets(GreenLight, e=True, forceElement='GreenSurfaceSG') if GreenLight else None
		cmds.sets(Spotlight, e=True, forceElement='BlueSurfaceSG') if Spotlight else None
		# for x in Material:
		# 	if not "BlueSurface" in x or not "GreenSurface" in x or not "RedSurface" in x:
		# 		cmds.setAttr(x+".output_override",1)
		[cmds.setAttr('%s.visibility' %cmds.listRelatives(x,p=True,type="transform")[0] ,0 ) for x in cmds.ls() if "light" in cmds.nodeType(x).lower() and ("direct" in cmds.nodeType(x).lower()  or "spot" in cmds.nodeType(x).lower())]
		cmds.setAttr("oceanWater_cMia_shd.output_override",1) if cmds.objExists("oceanWater_cMia_shd") else None
		[mapi.associate_pass('matte_%s' %x, 'NaviSpotLightMatte') for x in ['Spotlights','GreenLights','RedLights'] ]

	##BultFlagWindowLightMatte
	if len(BulbLight+FlagLight+WindowLight)!=0:
		cmds.createRenderLayer(n="BultFlagWindowLightMatte") if cmds.objExists("BultFlagWindowLightMatte")==False or BulbLight or FlagLight or WindowLight else None
		cmds.editRenderLayerMembers("BultFlagWindowLightMatte",cmds.ls(),noRecurse=True)
		cmds.editRenderLayerGlobals(currentRenderLayer="BultFlagWindowLightMatte")
		cmds.sets(BulbLight, e=True, forceElement='RedSurfaceSG') if BulbLight else None
		cmds.sets(FlagLight, e=True, forceElement='GreenSurfaceSG') if FlagLight else None
		cmds.sets(WindowLight, e=True, forceElement='BlueSurfaceSG') if WindowLight else None
		# for x in Material:
		# 	if not "BlueSurface" in x or not "GreenSurface" in x or not "RedSurface" in x:
		# 		cmds.setAttr(x+".output_override",1)
		[cmds.setAttr('%s.visibility' %cmds.listRelatives(x,p=True,type="transform")[0] ,0 ) for x in cmds.ls() if "light" in cmds.nodeType(x).lower() and ("direct" in cmds.nodeType(x).lower()  or "spot" in cmds.nodeType(x).lower())]
		cmds.setAttr("oceanWater_cMia_shd.output_override",1) if cmds.objExists("oceanWater_cMia_shd") else None
		[mapi.associate_pass('matte_%s' %x, 'BultFlagWindowLightMatte') for x in ['BulbLights','FlagLights','WindowLights'] ]

def createCPropMattes():
	alembic_nodes = cmds.ls(type = 'AlembicNode')
	animated_geo = cmds.filterExpand(cmds.listHistory(alembic_nodes, future = True), sm = 12, fullPath = True) if alembic_nodes else None
	filter_anim_geo_root = {}
	[filter_anim_geo_root.setdefault(each, []) for mesh in animated_geo for each in mesh.split('|') if each.startswith('CPROP_') and each.endswith('_hrc')] if animated_geo else None
	jajaja = [cmds.ls(root, long = True)[0] if cmds.listRelatives(cmds.ls(root, long = True)[0], allDescendents = True, type = 'mesh') else None for root in filter_anim_geo_root] if filter_anim_geo_root else None
	[filter_anim_geo_root[root.split('|')[-1]].append( cmds.listRelatives(mesh, parent = True, fullPath = True)[0] ) for root in jajaja for mesh in cmds.listRelatives(root, allDescendents = True, fullPath = True, type = 'mesh')] if jajaja else None

	if filter_anim_geo_root:
		for mat, geo in filter_anim_geo_root.iteritems():
			matte_name = 'matte_%s' % mat.strip('_hrc')
			cmds.delete(matte_name) if cmds.objExists(matte_name) else None
			matte_node = mapi.create_pass( 'Matte', n = matte_name )
			cmds.setAttr('%s.en_obj_linking' % matte_node, 1)
			# mapi.link_to_pass(geo, matte_node, mapi.OBJECTS)
			mentalCoreLink(geo, matte_node)
			mapi.associate_pass(matte_node, 'defaultRenderLayer')			

def createCharMattes():
	alembic_nodes = cmds.ls(type = 'AlembicNode')
	animated_geo = cmds.filterExpand(cmds.listHistory(alembic_nodes, future = True), sm = 12, fullPath = True) if alembic_nodes else None
	filter_anim_geo_root = {}
	[filter_anim_geo_root.setdefault(each, []) for mesh in animated_geo for each in mesh.split('|') if each.startswith('CHAR_') and each.endswith('_hrc')] if animated_geo else None
	jajaja = [cmds.ls(root, long = True)[0] if cmds.listRelatives(cmds.ls(root, long = True)[0], allDescendents = True, type = 'mesh') else None for root in filter_anim_geo_root] if filter_anim_geo_root else None
	[filter_anim_geo_root[root.split('|')[-1]].append( cmds.listRelatives(mesh, parent = True, fullPath = True)[0] ) for root in jajaja for mesh in cmds.listRelatives(root, allDescendents = True, fullPath = True, type = 'mesh')] if jajaja else None
	#EyeBrow
	EyeBrow = filter(lambda x: "eyebrow" in x.lower(), [cmds.listRelatives(x, parent = True, fullPath = True)[0] for x in animated_geo]) if animated_geo else None
	filter_anim_geo_root.setdefault('EyeBrow', EyeBrow) if EyeBrow else None
	#TaxiText
	TaxiText = filter(lambda x: "taxi_letter_" in x.lower(), [cmds.listRelatives(x, parent = True, fullPath = True)[0] for x in animated_geo]) if animated_geo else None
	filter_anim_geo_root.setdefault('TaxiText', TaxiText) if TaxiText else None
	ZipSpotLightMatte = filter(lambda x: "main_glass_geo" in x.lower(), [cmds.listRelatives(x, parent = True, fullPath = True)[0] for x in animated_geo]) if animated_geo else None
	filter_anim_geo_root.setdefault('ZipSpotLightMatte', ZipSpotLightMatte) if ZipSpotLightMatte else None

	if filter_anim_geo_root:
		for mat, geo in filter_anim_geo_root.iteritems():
			matte_name = 'matte_%s' % mat.strip('_hrc')
			cmds.delete(matte_name) if cmds.objExists(matte_name) else None
			matte_node = mapi.create_pass( 'Matte', n = matte_name )
			cmds.setAttr('%s.en_obj_linking' % matte_node, 1)
			# mapi.link_to_pass(geo, matte_node, mapi.OBJECTS)
			mentalCoreLink(geo, matte_node)
			mapi.associate_pass(matte_node, 'defaultRenderLayer')

def createCharTongueMattes():
	alembic_nodes = cmds.ls(type = 'AlembicNode')
	animated_geo = cmds.filterExpand(cmds.listHistory(alembic_nodes, future = True), sm = 12, fullPath = True) if alembic_nodes else None
	tongue_geo = [cmds.listRelatives(mesh, parent = True, fullPath = True)[0] for mesh in animated_geo if 'to' in mesh and 'ngue' in mesh] if animated_geo else None
	if tongue_geo:
		cmds.delete('matte_tongue') if cmds.objExists('matte_tongue') else None
		mapi.create_pass('Matte', n = 'matte_tongue')
		cmds.setAttr('%s.en_obj_linking' % 'matte_tongue', 1)
		# mapi.link_to_pass(tongue_geo, 'matte_tongue', mapi.OBJECTS)
		mentalCoreLink(tongue_geo, 'matte_tongue')
		mapi.associate_pass('matte_tongue', 'defaultRenderLayer')

def createEyeMattes():
	geo = cmds.ls(['*eyeball_white*', '*eyeball_clear*'], type = 'transform')
	if geo:
		cmds.delete('matte_eye') if cmds.objExists('matte_eye') else None
		mapi.create_pass( 'Matte', n = 'matte_eye' )
		cmds.setAttr('%s.en_obj_linking' % 'matte_eye', 1)
		# mapi.link_to_pass(geo, 'matte_eye', mapi.OBJECTS)
		mentalCoreLink(geo, 'matte_eye')
		mapi.associate_pass('matte_eye', 'defaultRenderLayer')

def createEyelashMattes():
	geo = cmds.ls('*eyelash*','*lashes_*','*eyeLash*',  type = 'transform')
	if geo:
		cmds.delete('matte_eyelash') if cmds.objExists('matte_eyelash') else None
		mapi.create_pass( 'Matte', n = 'matte_eyelash' )
		cmds.setAttr('%s.en_obj_linking' % 'matte_eyelash', 1)
		# mapi.link_to_pass(geo, 'matte_eyelash', mapi.OBJECTS)
		mentalCoreLink(geo, 'matte_eyelash')
		mapi.associate_pass('matte_eyelash', 'defaultRenderLayer')

def createBuildingMattes():
	meshes = cmds.ls(type = 'mesh', long = True)
	## filtered_geo = [cmds.listRelatives(mesh, parent = True, fullPath = True)[0] for mesh in meshes if 'BLD' in mesh or 'jetty' in mesh.lower() or 'fence' in mesh.lower() or 'road' in mesh.lower() or 'port' in mesh.lower() or 'carpark' in mesh.lower() or 'stair' in mesh.lower() or 'house' in mesh.lower()] if meshes else None
	#filtered_geo = [cmds.listRelatives(mesh, parent = True, fullPath = True)[0] for mesh in meshes if 'BLD' in mesh] if meshes else None
	filtered_geo = []	
	filtered_geo = [cmds.listRelatives(mesh, parent = True, fullPath = True)[0] for mesh in meshes if 'BLD' in mesh or 'Admiral' in mesh or 'platform' in mesh.lower() or 'house' in mesh.lower() or 'stair' in mesh.lower() or 'jetty' in mesh.lower()] if meshes else None 
	THouse=cmds.ls('*wall*','*fence*','*roadmain*','*LND_Dinghy*','*_lampost_*','*WestPoint_right_brick_geo','*EastPoint_left_brick_geo','*_Lightpole_*','*_boathanger*','MulliganTown_West_LND_wood_pier_geo','HC_Pylon001_geo')
	for x in THouse:
		if cmds.nodeType(x)=='transform' and not '_hrc' in x:
			filtered_geo.append(x) 
	GHouses = []	            
	GHouse=[
	'BBB_WestPoint_anchor_hrc','BBB_WestPoint_surfboards_hrc','DingleIsland_LND_hrc',
	'BigTown_01_LND_hrc','BigTown_02_LND_hrc','BigTown_LND_hrc','BBB_WestPoint_roadmain_left_wall_brick_hrc',
	'BBB_EastPoint_roadmain_right_wall_brick_hrc','FWB_wall_hrc','MulliganTown_East_LND_boat_A_hrc',
	'MulliganTown_East_LND_boat_B_hrc','pp_brick_hrc','pp_Dinghy001_hrc','pp_Dinghy002_hrc',
	'pp_Dinghy003_hrc','LittleTown_West_Ground_hrc','LittleTown_East_concrete_ground_hrc','LittleTown_Mid_LND_hrc'
	]
	for each in GHouse:
		GHouses.extend(cmds.ls("*%s" %each,l=True,type="transform"))
		for each in GHouses:
			if cmds.objExists(each):
				allDescendents = cmds.listRelatives(each, ad = True, fullPath = True, type = 'transform')
				if allDescendents:
					for child in allDescendents:
						if '_geo' in child and cmds.nodeType(child) == 'transform':
							filtered_geo.append(child)
	Extra=cmds.ls('LittleTown_East_14_geo','LittleTown_East_15_geo','LittleTown_East_16_geo','LittleTown_East_rock_17_geo',long=True)            
	for extra in Extra:
		if cmds.objExists(extra):
			filtered_geo.append(x)	 

	# NotHouse=['LittleTown_Mid_LND_4_geo','LittleTown_Mid_sand_1_geo','bigtown_02_hill_02_geo','bigtown_01_hill_01_geo','BigNorthPort_muligan_geo','DingleIsland_LND_Island01_geo','DingleIsland_LND_Island02_geo']
	filtered_geo = filter(lambda x: not('static_barnacles_geo' in x or'LittleTown_Mid_LND_4_geo' in x or 'LittleTown_Mid_sand_1_geo' in x or 'bigtown_02_hill_02_geo' in x or 'bigtown_01_hill_01_geo' in x or 'BigNorthPort_muligan_geo' in x or 'DingleIsland_LND_Island01_geo' in x or 'DingleIsland_LND_Island02_geo' in x or ('BBB_Jetty_BLD_hrc' in x and 'shore_geo' in x)), filtered_geo ) if filtered_geo else [] 
	# for each in NotHouse:
	# 	if cmds.objExists(each):
	# 		each=cmds.ls(each,l=True)[0]
	# 		try:           
	# 			filtered_geo.remove(each)
	# 		except:
	# 			pass   
	TerryStorage = filter(lambda x: "TerrysStorage" in x, filtered_geo)
	ZipBoatHouseRoof = []
	if cmds.objExists("sunDirection"):
		if cmds.getAttr("sunDirection.rotateZ") == 114.5999062:
			ZipBoatHouseRoof = filter(lambda x: "RF_cover_rim_geo" in x or "RF_cover_geo" in x or "flag_mount_geo" in x or ("RF_mount_0" in x and "pylon" in x), filtered_geo)


	if filtered_geo:
		cmds.delete('matte_houses') if cmds.objExists('matte_houses') else None
		mapi.create_pass('Matte', n = 'matte_houses')
		cmds.setAttr('%s.en_obj_linking' % 'matte_houses', 1)
		# mapi.link_to_pass(filtered_geo, 'matte_houses', mapi.OBJECTS)
		mentalCoreLink(filtered_geo, 'matte_houses')
		mapi.associate_pass('matte_houses', 'defaultRenderLayer')

	if TerryStorage:
		cmds.delete('matte_TerryStorageShed') if cmds.objExists('matte_TerryStorageShed') else None
		mapi.create_pass('Matte', n = 'matte_TerryStorageShed')
		cmds.setAttr('%s.en_obj_linking' % 'matte_TerryStorageShed', 1)
		# mapi.link_to_pass(filtered_geo, 'matte_TerryStorageShed', mapi.OBJECTS)
		mentalCoreLink(TerryStorage, 'matte_TerryStorageShed')
		mapi.associate_pass('matte_TerryStorageShed', 'defaultRenderLayer')

	if ZipBoatHouseRoof:
		cmds.delete('matte_ZipBoatHouseRoof') if cmds.objExists('matte_ZipBoatHouseRoof') else None
		mapi.create_pass('Matte', n = 'matte_ZipBoatHouseRoof')
		cmds.setAttr('%s.en_obj_linking' % 'matte_ZipBoatHouseRoof', 1)
		# mapi.link_to_pass(filtered_geo, 'matte_TerryStorageShed', mapi.OBJECTS)
		mentalCoreLink(ZipBoatHouseRoof, 'matte_ZipBoatHouseRoof')
		mapi.associate_pass('matte_ZipBoatHouseRoof', 'defaultRenderLayer')	

def createOceanMattes():
	geo = cmds.ls('*ocean_srf*', type = 'transform')
	if geo:
		cmds.delete('matte_water') if cmds.objExists('matte_water') else None
		mapi.create_pass( 'Matte', n = 'matte_water' )
		cmds.setAttr('%s.en_obj_linking' % 'matte_water', 1)
		mentalCoreLink(geo, 'matte_water')
		mapi.associate_pass('matte_water', 'defaultRenderLayer')

def createLandMattes():
	CORALCAVE_LND = [cmds.listRelatives(x, p=True, fullPath=True, type = "transform")[0] for x in cmds.ls(["*stone*","*rock*","*Rock*","*terrain*","*waterfall_01_geo*","*Cave001*","*cave*"],type="mesh",l=True) if ("coralcave" in x.lower() or "roseinlet" in x.lower())]  	
	LandObj=[
	"BigNorthPort_muligan_geo","pp_banjobay_terrain_geo","BBB_EastPoint_terrain_geo","BBB_Midpoint_Terrain_LND_terrain_geo",
	"BB_OysterFarm_LND_terrain_01_geo","LittleTown_West_9_geo","TWR_LND_Land_geo","TWR_LND_land_01_geo","TWR_LND_Land_2_geo","LittleTown_Mid_LND_4_geo",
	"MulliganTown_East_LND_terrain_geo","MulliganTown_West_LND_terrain_geo","BBB_WestPoint_terrain_geo","DingleIsland_LND_Island02_geo","DingleIsland_LND_Island01_geo",
	"LittleTown_East_1_geo","bigtown_01_hill_01_geo","bigtown_02_hill_02_geo","TH_IrisIsle_terrain_geo","TH_MangoShore01_Terrain001_geo",
	"TH_MangoShore02_terrain001_geo","TH_RainbowCliffs_LND_island_geo","TH_RainbowShore01_LND_island_geo","TH_RainbowShore02_LND_island_01_geo",
	"AI_LND_geo","FWB_finger1_geo","FWB_finger2_geo","FWB_finger3_geo","FWB_finger4_geo","FWB_finger5_geo","FWB_finger6_geo","HC_terrain001_East_geo","pasted__FWB_sandbar004_geoShape","FWB_terrain001_geo",
	"HC_mountain001_East_geo","HC_terrain001_south_geo","HC_terrain001_west_geo","FWB_land_geo","FWB_sandbar004_geo","shore_geo",
	"TH_MangoShore02_Terrain_geo","TH_MangoShore01_Terrain_geo","TH_RainbowCliffs_Island_geo","TH_RainbowShore02_Island_geo","TH_RainbowShore01_Island_geo","TH_IrisIsle_Terrain_geo"
	]
	geo = CORALCAVE_LND
	for each in LandObj:
		if cmds.objExists(each) and ( not 'BBB_Jetty_BLD_hrc' in each and not 'shore_geo' in each) :
			geo.append(each)

	#geo = cmds.ls(['*terrain_geo*', '*beach_geo*'], type = 'transform')
	if geo:
		cmds.delete('matte_ground') if cmds.objExists('matte_ground') else None
		mapi.create_pass( 'Matte', n = 'matte_ground' )
		cmds.setAttr('%s.en_obj_linking' % 'matte_ground', 1)
		# mapi.link_to_pass(geo, 'matte_ground', mapi.OBJECTS)
		mentalCoreLink(geo, 'matte_ground')
		mapi.associate_pass('matte_ground', 'defaultRenderLayer')
	createSandMattes()
	createclutterMatte()
	createRockCompileMatte()
	createStonesMatte()

def createclutterMatte():
	clutter = [i for i in cmds.ls('clutter_hrc', long = True) if 'AI_LND' in i]
	if clutter:
		if cmds.listRelatives(clutter, ad = True , fullPath = True , type = 'mesh'):
			matte_clutter = [cmds.listRelatives(i, p = True, fullPath = True, type = 'transform')[0] for i in cmds.listRelatives(clutter, ad = True , fullPath = True , type = 'mesh') if not 'brick' in i.lower()]
		
			if matte_clutter:      
				cmds.delete('matte_clutter') if cmds.objExists('matte_clutter') else None
				mapi.create_pass('Matte', n = 'matte_clutter')
				cmds.setAttr('matte_clutter.en_obj_linking', 1)
				mentalCoreLink(matte_clutter, 'matte_clutter')
				mapi.associate_pass('matte_clutter', 'defaultRenderLayer')

def createRockCompileMatte():
	matte_RockCompile = []

	RockCompileAll = cmds.listRelatives( cmds.ls('HC_RockCompile_LND_hrc', l = True)[0], ad = True, fullPath = True, type = 'mesh') if cmds.objExists('HC_RockCompile_LND_hrc') else None
	if RockCompileAll:
		for x in RockCompileAll:
			RockCompileGeo = cmds.listRelatives(x, p = True, fullPath = True, type = 'transform')
			matte_RockCompile.extend(RockCompileGeo)

	if matte_RockCompile:      
		cmds.delete('matte_RockCompile') if cmds.objExists('matte_RockCompile') else None
		mapi.create_pass( 'Matte', n = 'matte_RockCompile')
		cmds.setAttr('%s.en_obj_linking' %'matte_RockCompile', 1)
		mentalCoreLink(matte_RockCompile,'matte_RockCompile')
		mapi.associate_pass('matte_RockCompile', 'defaultRenderLayer')		
	   
def createStonesMatte():
	matte_stones = []

	stonesAll = cmds.listRelatives(cmds.ls('*AI_LND_hrc|geo_hrc|stones_hrc', l = True)[0], ad = True , fullPath = True , type = 'mesh') if cmds.objExists('stones_hrc') else None
	if stonesAll:
		for x in stonesAll:
			stonesGeo = cmds.listRelatives(x, p = True, fullPath = True, type = 'transform')
			matte_stones.extend(stonesGeo)

	if matte_stones:      
		cmds.delete('matte_stones') if cmds.objExists('matte_stones') else None
		mapi.create_pass( 'Matte', n = 'matte_stones')
		cmds.setAttr('%s.en_obj_linking' %'matte_stones', 1)
		# mapi.link_to_pass(geo, 'matte_ground', mapi.OBJECTS)
		mentalCoreLink(matte_stones,'matte_stones')
		mapi.associate_pass('matte_stones', 'defaultRenderLayer')
			
def createSandMattes():
	Extra_SND = [cmds.listRelatives(x, p=True, fullPath=True, type = "transform")[0] for x in cmds.ls(["*sandbar*","*Sandbar*"],type="mesh",l=True) if not "shoreline" in x and ("coralcave" in x.lower() or "roseinlet" in x.lower()) or "LIB_WORLD_Sandbar" in x] 
	SandObj=[
	"BB_OysterFarm_LND_sand_01_geo","BB_OysterFarm_LND_sand_02_geo","pp_sand_geo","BBB_EastPoint_beach_geo",
	"BBB_WestPoint_sand_geo","TWR_LND_sand_geo","LittleTown_Mid_sand_1_geo","LittleTown_West_Sand_1_geo",
	"TH_IrisIsle_sandbar_geo","TH_MangoShore01_sandbar001_geo","TH_MangoShore02_sandbar001_geo",
	"FWB_sand_1_geo","FWB_sand_2_geo","FWB_sand_3_geo","FWB_sand_4_geo","FWB_sand_5_geo",
	"FWB_sand_6_geo","FWB_sand_7_geo","FWB_sand_8_geo","FWB_sand_9_geo","FWB_sand_10_geo","FWB_sand_11_geo",
	"FWB_sand_12_geo","FWB_sand_13_geo","FWB_sand_14_geo","FWB_sand_15_geo","FWB_sandbar005_geo",
	"FWB_sandbar006_geo","TH_RainbowShore01_LND_sandbar_geo","TH_RainbowShore02_LND_sandbar_geo",
	"HC_island001_East_geo","HC_island002_East_geo","HC_island003_East_geo","HC_North_island005_geo",
	"HC_North_island001_geo","HC_North_island002_geo","HC_North_island004_geo","HC_sandbar001_south_geo",
	"HC_island002_west_geo","HC_sandbar001_west_geo","HC_lowtide_sandbar006_geo","HC_lowtide_sandbar001_geo",
	"HC_lowtide_sandbar002_geo","HC_lowtide_sandbar003_geo","HC_lowtide_sandbar004_geo","HC_island001_west_geo",
	"HC_lowtide_sandbar005_geo","shore_geo","RoseInlet_sand_geo","TH_MangoShore01_Sandbar_geo","TH_MangoShore02_Sandbar_geo","TH_IrisIsle_Sandbar_geo",
	"TH_RainbowShore02_Sandbar_geo","TH_RainbowShore01_Sandbar_geo","World_Sandbar_01_geo"
	]
	geo = Extra_SND
	for each in SandObj:
		if cmds.objExists(each):
			geo.append(each)
	#geo = cmds.ls(['*terrain_geo*', '*beach_geo*'], type = 'transform')
	if geo:
		cmds.delete('matte_sand') if cmds.objExists('matte_sand') else None
		mapi.create_pass( 'Matte', n = 'matte_sand' )
		cmds.setAttr('%s.en_obj_linking' % 'matte_sand', 1)
		# mapi.link_to_pass(geo, 'matte_ground', mapi.OBJECTS)
		mentalCoreLink(geo, 'matte_sand')
		mapi.associate_pass('matte_sand', 'defaultRenderLayer')

def createSydneySailMattes():
	sails = cmds.ls(['*sails_hrc*','*main_sail*','small_sail_edge_geo','small_geo'], long = True, type = 'transform') 
	Spinaker = cmds.ls(['small_sail_edge_geo','small_geo','*spinnaker_sail_geo*','big_sail_edge_geo*','big_sail_geo*','Broken_spinnaker_sail_geo*','jib_geo','jibRim_geo'], long = True, type = 'transform')
	#sails = [root for root in sails if 'CHAR_Sydney' and cmds.listRelatives(sails, allDescendents = True, fullPath = True, type = 'mesh')] if sails else None
	#sails_geo = [cmds.listRelatives(mesh, parent = True, fullPath = True)[0] for mesh in sails] if sails else None
	SailDict={}
	
	for root in sails:
		if 'CHAR_Sydney' in root and 'sails_hrc' in root and not 'ctrl' in root:
			Descendents_sail = []
			Descendents_sail.append(cmds.listRelatives(root,allDescendents = True, fullPath = True, type = 'mesh'))
			if Descendents_sail:
				for x in Descendents_sail:
					geo=cmds.listRelatives(x,parent =True,fullPath = True)
					if geo:
						for x in geo:
							SailDict.setdefault('sail',[])
							SailDict['sail'].append(x)

		if 'CHAR_Cleo' in root and ('small_sail_edge_geo' in root or 'small_geo' in root or 'main_sail' in root) and not 'ctrl' in root:
			Descendents_sail = []
			Descendents_sail.append(cmds.listRelatives(root,allDescendents = True, fullPath = True, type = 'mesh'))
			if Descendents_sail:
				for x in Descendents_sail:
					geo=cmds.listRelatives(x,parent =True,fullPath = True)
					if geo:
						for x in geo:
							SailDict.setdefault('Cleo_sail',[])
							SailDict['Cleo_sail'].append(x)

	for root in Spinaker:
		if 'CHAR_Sydney' in root and ('spinnaker_sail_geo' in root or 'jibRim_geo' in root or 'jib_geo' in root) and not 'ctrl' in root:
			Descendents_sail = []
			Descendents_sail.append(cmds.listRelatives(root,allDescendents = True, fullPath = True, type = 'mesh'))
			if Descendents_sail:
				for x in Descendents_sail:             
					geo=cmds.listRelatives(x,parent =True,fullPath = True)
					if geo:
						for x in geo:
							SailDict.setdefault('Sydney_Spinaker',[])
							SailDict['Sydney_Spinaker'].append(x)

		if 'CHAR_Cleo' in root and ('big_sail_edge_geo' in root or 'big_sail_geo' in root or 'small_sail_edge_geo' in root or 'small_geo' in root) and not 'ctrl' in root:
			Descendents_sail = []
			Descendents_sail.append(cmds.listRelatives(root,allDescendents = True, fullPath = True, type = 'mesh'))
			if Descendents_sail:
				for x in Descendents_sail:
					geo=cmds.listRelatives(x,parent =True,fullPath = True)
					if geo:
						for x in geo:
							SailDict.setdefault('Cleo_Spinaker',[])
							SailDict['Cleo_Spinaker'].append(x)

	if SailDict:
		for mat , geo in SailDict.iteritems():
			matte_name = 'matte_%s' % mat
			cmds.delete(matte_name) if cmds.objExists(matte_name) else None
			matte_node = mapi.create_pass( 'Matte', n = matte_name )
			cmds.setAttr('%s.en_obj_linking' % matte_node, 1)
			# mapi.link_to_pass(geo, matte_node, mapi.OBJECTS)
			mentalCoreLink(geo, matte_node)
			mapi.associate_pass(matte_node, 'defaultRenderLayer')

def createCoreArchiveMattes():
	shading_engines = cmds.ls(type = 'shadingEngine')
	shading_engines = [sg for sg in shading_engines if cmds.sets(sg, q = True) for mesh in cmds.sets(sg, q = True) if ':ref:' in mesh] if shading_engines else None
	shading_engines = list( set( shading_engines ) ) if shading_engines else None

	filters = ['bush', 'grass', 'vine', 'leaf'] ## whatever that is green according to Deepesh...
	sg_dict = {}
	if shading_engines:
		sg_dict = {}
		for sg in shading_engines:
			core_archive_meshes = cmds.sets(sg, q = True)
			matte = core_archive_meshes[0].split('|')[0].split('_')[0] if core_archive_meshes else None
			
			sg_dict.setdefault( matte, [] )
			sg_dict[matte].append(sg) if sg not in sg_dict[matte] else sg_dict[matte]

	if sg_dict:
		for matte, sg in sg_dict.iteritems():
			for each in sg:
				core_archive_meshes = cmds.sets(each, q = True)
				processed = [cmds.listRelatives(mesh, fullPath = True, parent = True)[0] for mesh in core_archive_meshes for fil in filters if fil in mesh.lower()] if core_archive_meshes else None
				
				if not processed:
					## checked all core archive geos for the shading engine but non fits the filter so we check the material assigned instead...
					core_material = cmds.listConnections('%s.miMaterialShader' % each)
					processed = [mat for mat in core_material for fil in filters if fil in mat.lower()] if core_material else None
				
				if processed:
					cmds.delete(matte) if cmds.objExists(matte) else None
					matte_node = mapi.create_pass('Matte', n = matte)
					mapi.associate_pass(matte_node, 'defaultRenderLayer')
					mapi.link_to_pass([each], matte_node, mapi.MATERIALS)

###########################
## Clean-up
###########################

def removeCoreArchiveOfOrigin(distance = 17):
	core_archive = cmds.ls(type = 'core_archive')
	core_archive_geo = [(cmds.xform(geo, centerPivots = True), geo)[1] for ca in core_archive if cmds.listConnections('%s.message' % ca) for geo in cmds.listConnections('%s.message' % ca)] if core_archive else None
	[cmds.setAttr('%s.translateY' % mesh, -50000) for mesh in core_archive_geo if abs(cmds.xform(mesh, query = True, absolute = True, worldSpace = True, rotatePivot = True)[0]) < distance and abs(cmds.xform(mesh, query = True, absolute = True, worldSpace = True, rotatePivot = True)[2]) < distance] if core_archive_geo else None

def arraysMatch(a, b):
	'''
	Utility to compare two string list
	'''
	return True if a == b else False

def cleanupNonManifoldGeometry(normals = True, promptDialog = False):
	## Get all the mesh that has mentalraySubdivApprox connected and has non-manifold problem
	# subdiv_mesh = [cmds.listRelatives(mesh, parent = True, fullPath = True)[0] for mesh in cmds.ls(type = 'mesh') if cmds.listConnections(mesh, type = 'mentalraySubdivApprox') if cmds.polyInfo(mesh, nme = True) or cmds.polyInfo(nmv = True)]
	subdiv_mesh = [cmds.listRelatives(mesh, parent = True, fullPath = True)[0] for mesh in cmds.ls(type = 'mesh') if cmds.polyInfo(mesh, nme = True) or cmds.polyInfo(nmv = True)]
	subdiv_mesh = list( set( subdiv_mesh ) )

	if subdiv_mesh:
		for each in subdiv_mesh:
			## Make sure we do indeed have nonmanifold geometry
			##
			nonManifold = cmds.polyInfo(each, nmv = True, nme = True)
			if nonManifold:

				proceed = cmds.confirmDialog(title = 'Non-Manifold Geometry!', message = 'Geo Name:\n%s' % each, button = ['Cleanup!', 'Skip...'], defaultButton = 'Skip...', cancelButton = 'Skip...', dismissString = 'Skip...') if promptDialog else 'Cleanup!'
				if proceed == 'Cleanup!':

					## Conform the geo and see if that gets rid of all the nonmanifold bits
					##
					if normals:
						cmds.polyNormal('%s.f[*]' % each, normalMode = 2, constructionHistory = True)

					edges			= cmds.polyInfo(each, nme = True) if cmds.polyInfo(each, nme = True) else []
					vertices 		= [] if edges else cmds.polyInfo(each, nmv = True)
					lastEdges		= []
					lastVertices	= []

					while ( not arraysMatch(lastEdges, edges) or not arraysMatch(lastVertices, vertices) ) and ( edges or vertices ):
						## Remember what was nonmanifold last time
						##
						lastEdges		= edges
						lastVertices	= vertices
						## Split any nonmanifold edges
						##
						if edges:
							cmds.polySplitEdge(edges, constructionHistory = True)
							vertices = cmds.polyInfo(each, nmv = True)
							edges = []

						## Split any remaining nonmanifold vertices
						##
						if vertices:
							cmds.polySplitVertex(vertices, constructionHistory = True)
							vertices = []

						## Now check to see if the object is still nonmanifold
						##
						nonManifold = cmds.polyInfo(each, nmv = True, nme = True)
						if nonManifold:
							## Chip off the faces
							##
							nonManifoldFaces = cmds.polyListComponentConversion(nonManifold, toFace = True)
							cmds.polyChipOff(nonManifoldFaces, kft = 0, dup = 0, constructionHistory = True)
							## And then check for nonmanifold bits again
							##
							edges = cmds.polyInfo(each, nme = True)
							if not edges:
								vertices = cmds.polyInfo(each, nmv = True)

					## Check to see if we failed to cleanup
					if edges or vertices:
						cmds.warning('Failed to cleanup non-manifold geometry of %s...' % each)

###########################
## Custom functions
###########################

def mentalCoreLink(meshes, corePass):
	[cmds.connectAttr('%s.message' % mesh, '%s.linked_objs[%s]' % (corePass, i), force = True) for i, mesh in enumerate(meshes, start = 0)]

def selectionToMeshes():
	selection = cmds.ls(selection = True)
	meshDescendents = [cmds.listRelatives(mesh, parent = True, fullPath = True)[0] for mesh in cmds.listRelatives(allDescendents = True, fullPath = True, type = 'mesh')]
	cmds.select(meshDescendents, replace = True)

def fixDarkEye():
	turnOffEyeShad()
	killEyeWhites()
	createEyeMattes()
	createCharTongueMattes()
	createEyelashMattes()

def attachMentalRaySubDiv(subdName = 'auto_mrSubdAppx'):
	## Build the auto-mrSubDAppx now...
	subdNode = cmds.createNode('mentalraySubdivApprox', name = subdName) if not cmds.objExists(subdName) else subdName
	
	## Now set the attrs for the approx node..
	cmds.setAttr('%s.approxMethod' % subdNode, 2)
	cmds.setAttr('%s.minSubdivisions' % subdNode, 0)
	cmds.setAttr('%s.maxSubdivisions' % subdNode, 2)
	cmds.setAttr('%s.length' % subdNode, 0.6)
	cmds.setAttr('%s.viewDependent' % subdNode, 1)
	cmds.setAttr('%s.fine' % subdNode, 1)
	
	objWithSmoothedTag = cmds.ls('*.smoothed')
	objWithSmoothedTag.extend( cmds.ls('*:*.smoothed') )
	if objWithSmoothedTag:
		objWithSmoothedTag = [each for each in objWithSmoothedTag if cmds.getAttr(each) == 1]
		meshToSubdiv = [cmds.listRelatives(each.split('.')[0], fullPath = True, shapes = True)[0] for each in objWithSmoothedTag if cmds.listRelatives(each.split('.')[0], fullPath = True, shapes = True)] if objWithSmoothedTag else None
		[cmds.addAttr(each, longName = 'miSubdivApprox', dataType = 'string') for each in meshToSubdiv if not cmds.objExists('%s.miSubdivApprox' % each)] if meshToSubdiv else None
		[cmds.connectAttr('%s.message' % subdNode, '%s.miSubdivApprox' % each, force = True) for each in meshToSubdiv if not cmds.isConnected('%s.message' % subdNode, '%s.miSubdivApprox' % each)]
		
def subdivSmoothedAttr():
	## Lips treatment
	charLips = [cmds.listRelatives(lip, parent = True, fullPath = True)[0] for lip in cmds.ls('*lips_geoShape*', l = True)]
	[cmds.setAttr('%s.smoothed' % lip, 1) for lip in charLips if cmds.objExists('%s.smoothed' % lip)] if charLips else None

	attachMentalRaySubDiv()

def optimizedRenderSettings():
	cmds.setAttr('mentalcoreGlobals.en_envl', 0)
	cmds.setAttr('mentalcoreGlobals.en_ao', 0)
	cmds.setAttr('miDefaultOptions.finalGather', 0)
	cmds.setAttr('miDefaultOptions.rayTracing', 0)
	cmds.setAttr('miDefaultOptions.shadowMethod', 0)
	[mapi.unassociate_pass(each, 'defaultRenderLayer') for each in mapi.get_associated_passes('defaultRenderLayer')]

def attachColorMattes(color = [0, 0, 0]):
	selection = cmds.ls(selection = True)
	meshDescendents = [cmds.listRelatives(mesh, parent = True, fullPath = True)[0] for mesh in cmds.listRelatives(allDescendents = True, fullPath = True, type = 'mesh')] if cmds.listRelatives(allDescendents = True, fullPath = True, type = 'mesh') else None
	nurbsDescendents = [cmds.listRelatives(nurb, parent = True, fullPath = True)[0] for nurb in cmds.listRelatives(allDescendents = True, fullPath = True, type = 'nurbsSurface')] if cmds.listRelatives(allDescendents = True, fullPath = True, type = 'nurbsSurface') else None

	if meshDescendents or nurbsDescendents:
		core_mat = cmds.createNode('core_surface_shader')
		core_mat_sg = cmds.sets(renderable = True, noSurfaceShader = True, empty = True)
		cmds.connectAttr('%s.outValue' % core_mat, '%s.miMaterialShader' % core_mat_sg)
		cmds.connectAttr('%s.outValue' % core_mat, '%s.miShadowShader' % core_mat_sg)
		
		cmds.setAttr('%s.colour' % core_mat, color[0], color[1], color[2], type = 'double3')

		cmds.sets(meshDescendents, edit = True, forceElement = core_mat_sg) if meshDescendents else None
		if nurbsDescendents:
			cmds.sets(nurbsDescendents, edit = True, forceElement = core_mat_sg)
			try:
				cmds.connectAttr('ocean_dispShader.outColor', '%s.displacementShader' % core_mat_sg)
			except:
				pass

		try:	cmds.setAttr('LIGHTS_hrc.visibility', 0 )
		except:	pass

def attachShadingMatte(ocean = False):
	selection = cmds.ls(selection = True)
	meshDescendents = [cmds.listRelatives(mesh, parent = True, fullPath = True)[0] for mesh in cmds.listRelatives(allDescendents = True, fullPath = True, type = 'mesh')]

	core_mat = cmds.createNode('core_material')
	core_mat_sg = cmds.sets(renderable = True, noSurfaceShader = True, empty = True)
	cmds.connectAttr('%s.outValue' % core_mat, '%s.miMaterialShader' % core_mat_sg)
	cmds.connectAttr('%s.outValue' % core_mat, '%s.miShadowShader' % core_mat_sg)

	cmds.setAttr('%s.diffuse' % core_mat, 1, 1, 1, type = 'double3')
	cmds.setAttr('%s.en_blinn' % core_mat, 0)

	cmds.sets(meshDescendents, edit = True, forceElement = core_mat_sg)

	if ocean and cmds.objExists('ocean_dispShader'):
		cmds.connectAttr("ocean_dispShader.outColor", "%s.displacementShader" % core_mat_sg, force = True)

	try:	cmds.setAttr('FX_CACHES_hrc.visibility', 0 )
	except:	pass
	try:	cmds.setAttr('LIGHTS_hrc.visibility', 0 )
	except:	pass

def attachShadingMatte2(ocean = False, mesh = []):
	if mesh:
		core_mat = cmds.createNode('core_material')
		core_mat_sg = cmds.sets(renderable = True, noSurfaceShader = True, empty = True)
		cmds.connectAttr('%s.outValue' % core_mat, '%s.miMaterialShader' % core_mat_sg)
		cmds.connectAttr('%s.outValue' % core_mat, '%s.miShadowShader' % core_mat_sg)
	
		cmds.setAttr('%s.diffuse' % core_mat, 1, 1, 1, type = 'double3')
		cmds.setAttr('%s.en_blinn' % core_mat, 0)
	
		cmds.sets(mesh, edit = True, forceElement = core_mat_sg)
	
		if ocean and cmds.objExists('ocean_dispShader'):
			cmds.connectAttr("ocean_dispShader.outColor", "%s.displacementShader" % core_mat_sg, force = True)

def setupFoamOnlyShader():
	if cmds.objExists('oceanWater_incd_cTxBld') and cmds.objExists('ocean_srfShape'):
		core_mat = cmds.createNode('core_surface_shader')
		core_mat_sg = cmds.sets(renderable = True, noSurfaceShader = True, empty = True)
		cmds.connectAttr('%s.outValue' % core_mat, '%s.miMaterialShader' % core_mat_sg)
		cmds.connectAttr('%s.outValue' % core_mat, '%s.miShadowShader' % core_mat_sg)
		
		cmds.connectAttr('oceanWater_incd_cTxBld.outColor', '%s.colour' % core_mat)
		cmds.connectAttr('oceanWater_incd_cTxBld.outColorA', '%s.colourA' % core_mat)
		cmds.connectAttr('ocean_dispShader.outColor', '%s.displacementShader' % core_mat_sg)
		
		cmds.sets('ocean_srfShape', edit = True, forceElement = core_mat_sg)

def deleteUnusedJunks():
	for each in cmds.ls(type = 'core_renderpass'):
		cmds.lockNode(each, lock = True)

	mel.eval("MLdeleteUnused();")

	for each in cmds.ls(type = 'core_renderpass'):
		cmds.lockNode(each, lock = False)

def _doSTATIC_import(path, namespace):
	"""       
	:param path: Path to file.
	"""

	if os.path.exists(path):
		workingFile = os.listdir(path)
		latestWorkingFile = '%s/%s' % ( path, max(workingFile) )
		
		# perform a more or less standard maya import, putting all nodes brought in into a specific namespace
		cmds.file(latestWorkingFile, i = True)

		if '_Addon' not in path:
			## Clean any bad build grps just incase the person in cahrge of the static env rebuilt the cores but didn't clean the geo_hrc core groups out..
			## This helps stop a full scene rebuild from failing if the lighter needs to do this..
			_removeCoreGrps()

			## Clean general namespaces from the import ignoring the core archive names...
			getAllNameSpaces = cmds.namespaceInfo(listOnlyNamespaces = True)
			for eachNS in getAllNameSpaces:
				if namespace in eachNS and 'CORE' not in eachNS:
					try:
						cmds.namespace(removeNamespace = eachNS, mergeNamespaceWithRoot = True)
					except RuntimeError:
						pass

			## Now try to clean the duplicate cores that may exist
			_cleanFnCores()
			_removeCoreGrps()

def _removeCoreGrps():
	"""
	Exposing function for operator to cleanup after a rebuild
	"""
	## Step one after import
	## Clean the fucking left over grps first if they exist
	ENVLIST = ['ENV_MIDDLEHARBOUR_STATIC_ABC_STATIC_CACHES_hrc', 'ENV_MIDDLEHARBOUR_EAST_STATIC_ABC_STATIC_CACHES_hrc', 'ENV_WESTHARBOUR_STATIC_ABC_STATIC_CACHES_hrc', 
				'ENV_THEHEADS_STATIC_ABC_STATIC_CACHES_hrc', 'ENV_BIGTOWN_STATIC_ABC_STATIC_CACHES_hrc','ENV_ROSE_INLET_STATIC_ABC_STATIC_CACHES_hrc', 
				'ENV_CORALCAVE_ABC_STATIC_CACHES_hrc', 'ENV_CORALCAVE_ENTRANCE_ABC_STATIC_CACHES_hrc']    
	getHRCS = [[eachGrp for eachGrp in cmds.listRelatives(eachENV, children = True, f= True) if 'LND' in eachGrp] for eachENV in ENVLIST if cmds.objExists(eachENV)]
	for eachList in getHRCS:
		[[cmds.delete(eachChild) for eachChild in cmds.listRelatives(eachHrc, ad = True, f = True) if '_CORE_' in eachChild] for eachHrc in eachList]

def _makeFinalShotBaseCoreGroups():
	grps = ['MASTER_COREARCHIVES_hrc', 'MASTER_ROOTCOREARCHIVES_hrc', 'MASTER_COREPLACEMENTS_hrc']
	for each in grps:
		if not cmds.objExists(each):
			cmds.group(n = each, em = True)

def _reconnectDuplicates(eachGeo = '', core_archive = ''):
	"""
	used to renumber the transforms in a duplicate group
	@param baseGrp: Name of the duplicate group to renumber the children of
	@type baseGrp: String
	"""
	## Fetch the Geo Shaders
	## Now reconnect
	try:
		getCoreConnections = cmds.listConnections('%s.message' % core_archive, plugs = True)
	except:
		pass
		
	if not cmds.objExists(core_archive):
		cmds.warning('_reconnectDuplicates needs a valid core_archive to work!!\n\t%s is invalid!' % core_archive)
	else:
		if '%s.miGeoShader' % eachGeo not in getCoreConnections:
			cmds.connectAttr('%s.message' % core_archive, '%s.miGeoShader' % eachGeo, force = True)

def _cleanFnCores():    
	removedNameSpaces = []
	## Remove duplicate root core namespaces
	getAllNameSpaces = cmds.namespaceInfo(listOnlyNamespaces = True)

	for eachNS in getAllNameSpaces:
		if eachNS.endswith('1'):
			cmds.namespace(removeNamespace = eachNS, mergeNamespaceWithRoot = True)
			removedNameSpaces.append(eachNS.replace('1', '').replace('_CORE', ''))
	
	## Make the final core groups
	_makeFinalShotBaseCoreGroups()
	getAllPlacementGrps = cmds.ls('*placements_hrc*', l = True)
	getAllUniqueGrps = cmds.ls('*unique_geo_hrc*', l = True)
	coreHRCS = {}
	rootCores = []
	duplicateCores = []
	for eachCoreGrp in getAllUniqueGrps:
		getChildren = cmds.listRelatives(eachCoreGrp, children = True, f = True)
		
		for eachChild in getChildren:
			## Process the cores
			if 'CORE_ARCHIVES_hrc' in eachChild:
				getHRCS = cmds.listRelatives(eachChild, children = True, f = True)
				for eachHRC in getHRCS:
					if eachHRC.split("|")[-1] not in coreHRCS.keys():
						coreHRCS[eachHRC.split("|")[-1]] = cmds.listRelatives(eachHRC, children = True, f = True)
					else:
						coreHRCS[eachHRC.split("|")[-1]].append(cmds.listRelatives(eachHRC, children = True, f = True))
	
			## Process the root cores
			elif 'ROOT_ARCHIVES_DNT_hrc' in eachChild:
				getCores = cmds.listRelatives(eachChild, children = True)
				for eachCore in getCores:
					if eachCore not in rootCores:
						rootCores.append(eachCore)
					else:
						duplicateCores.append(eachCore)
			else:
				pass
		
	## Make new base grps and clean up the old ones
	for key, var in coreHRCS.items():
		## first check to see if the group is in the MASTERCORES if so use that
		if not cmds.objExists('|MASTER_COREARCHIVES_hrc|%s' % key):
			## now check if the root hrc exists
			if not cmds.objExists('|%s' % key):
				cmds.group(n = '|%s' % key, em = True)
				grpPath = '|%s' % key
			else:
				grpPath = '|%s' % key
		else:
			grpPath = '|MASTER_COREARCHIVES_hrc|%s' % key
		
		## Figure out the core_archive name from the hrc group
		coreName = '%s_CORE_Geoshader' % grpPath.replace('_Archives_hrc', '')
		if cmds.objExists(coreName):
			getCoreGeo = [eachGeo for eachGeo in cmds.listConnections(coreName) if cmds.nodeType(eachGeo) != 'expression']
		else:
			getCoreGeo = []
		## Now parent each of the archives to the right hrc group
		for eachCore in var:
			try:
				cmds.parent(eachCore, grpPath)
			except RuntimeError:
				pass
			##Now check if the core archive already exists in the scene.
			if cmds.objExists(coreName):
				if eachCore not in getCoreGeo:
					## Now try to reconnect them to the working core_root
					_reconnectDuplicates(eachCore, coreName)

	## Now try to parent these groups under the final MASTER_COREARCHIVES_hrc group  
	for key in coreHRCS.keys():
		try:
			cmds.parent('|%s' % key, 'MASTER_COREARCHIVES_hrc')
		except:
			pass
			
	## Now clean the placements
	for eachPlc in getAllPlacementGrps:
		try:
			for eachChild in cmds.listRelatives(eachPlc, children = True, f = True):
				try:
					cmds.parent(eachChild, 'MASTER_COREPLACEMENTS_hrc')
				except RuntimeError:
					pass
		except:
			pass
	
	## Now parent valid cores to the root core group
	getAllNameSpaces = cmds.namespaceInfo(listOnlyNamespaces = True)
	for eachNS in getAllNameSpaces:
		if '_CORE' in eachNS:
			try:
				cmds.parent(cmds.listRelatives(cmds.namespaceInfo(eachNS, r = True, dp = True, listNamespace = True)[1], parent = True, f = True), 'MASTER_ROOTCOREARCHIVES_hrc')
			except RuntimeError:
				pass

	## Now try to delete any existing core groups from import
	grps = ['ENV_THEHEADS_STATIC_Core_Archives_hrc', 'ENV_MIDDLEHARBOUR_STATIC_Core_Archives_hrc', 'ENV_MIDDLEHARBOUR_EAST_STATIC_Core_Archives_hrc',
			'ENV_WESTHARBOUR_STATIC_Core_Archives_hrc',  'ENV_BIGTOWN_STATIC_Core_Archives_hrc', 'ENV_ROSE_INLET_STATIC_Core_Archives_hrc', 
			'ENV_CORALCAVE_STATIC_Core_Archives_hrc', 'ENV_CORALCAVE_ENTRANCE_STATIC_Core_Archives_hrc']
	for each in grps:
		try:	cmds.delete(each)
		except:	pass
	
	## now check for a stupid name from import
	for each in cmds.ls(type = 'core_archive'):
		if 'ep000' in each:
			coreName = '_'.join(each.split('_')[2:])
			for eachGeo in cmds.listConnections(each):
				if cmds.nodeType(eachGeo) != 'expression':
					cmds.connectAttr('%s.message' % coreName, '%s.miGeoShader' % eachGeo, force = True)
			
	## Just in case lets make sure we get rid of any dead cores now
	cleanupDeadCoreArchives()

def cleanupDeadCoreArchives():
	"""
	Quick method for searching for core_archives that only have an expression attached and nothing else = dead archive.
	This removes the expression and the archive from the scene and then preforms a cleanup on the shaders to get rid of any dead shading networks in the scene
	"""
	for each in cmds.ls(type = 'core_archive'):
		if len(cmds.listConnections(each)) == 1:
			if cmds.nodeType(cmds.listConnections(each)[0]) == 'expression':
				cmds.delete(cmds.listConnections(each)[0])
				cmds.delete(each)

				## Now remove all the nameSpaces!! This is to remove any clashes with the core_assemblies later on...
				safeNS = ['UI', 'shared']
				getAllNameSpaces = cmds.namespaceInfo(listOnlyNamespaces = True)
				for eachNS in getAllNameSpaces:
					if eachNS not in safeNS:
						try:
							for eachNS in cmds.namespaceInfo(eachNS, listNamespace = True):
								if each in eachNS:
									try:
										cmds.namespace(removeNamespace = eachNS, mergeNamespaceWithRoot = True)
									except RuntimeError:
										pass
						except TypeError:
							pass

	[cmds.lockNode(x, lock = True) for x in cmds.ls(type = 'core_renderpass')]
	mel.eval("MLdeleteUnused();")
	[cmds.lockNode(x, lock = False) for x in cmds.ls(type = 'core_renderpass')]

## RenderSetUp button
def importStaticEnv():
	## ENVS
	_doSTATIC_import(path = '//192.168.5.253/BBB_main/bbb/i/bubblebathbay/episodes/ep000/ep000_sh010/Light/publish/maya', namespace = 'ep000_sh010_ep000sh010_LIGHTENV') if cmds.checkBox('bubbleBathBayStaticCB', value = True, query = True) else None
	_doSTATIC_import(path = '//192.168.5.253/BBB_main/bbb/i/bubblebathbay/episodes/ep000/ep000_sh020/Light/publish/maya', namespace = 'ep000_sh020_ep000sh020_LIGHTENV') if cmds.checkBox('westHarbourStaticCB', value = True, query = True) else None
	_doSTATIC_import(path = '//192.168.5.253/BBB_main/bbb/i/bubblebathbay/episodes/ep000/ep000_sh030/Light/publish/maya', namespace = 'ep000_sh030_ep000sh030_LIGHTENV') if cmds.checkBox('bigTownStaticCB', value = True, query = True) else None
	_doSTATIC_import(path = '//192.168.5.253/BBB_main/bbb/i/bubblebathbay/episodes/ep000/ep000_sh040/Light/publish/maya', namespace = 'ep000_sh040_ep000sh040_LIGHTENV') if cmds.checkBox('theHeadsStaticCB', value = True, query = True) else None
	_doSTATIC_import(path = '//192.168.5.253/BBB_main/bbb/i/bubblebathbay/episodes/ep000/ep000_sh050/Light/publish/maya', namespace = 'ep000_sh050_ep000sh050_LIGHTENV') if cmds.checkBox('hiddenCoveStaticCB', value = True, query = True) else None
	_doSTATIC_import(path = '//192.168.5.253/BBB_main/bbb/i/bubblebathbay/episodes/ep000/ep000_Docks_Addon/Light/publish/maya', namespace = 'ep000_sh050_ep000sh060_LIGHTENV') if cmds.checkBox('DockAddonCB', value = True, query = True) else None

## RenderSetUp button
def importRippleLayer(path = '//192.168.5.253/BBB_main/bbb/i/bubblebathbay/assets/LibraryAsset/LIB_WORLD_Shoreline/SRF/publish/maya'):
	if os.path.exists(path):
		workingFile = os.listdir(path)
		latestWorkingFile = '%s/%s' % ( path, max(workingFile) )
		
		# perform a more or less standard maya import, putting all nodes brought in into a specific namespace
		## cmds.file(latestWorkingFile, i = True)
		cmds.file(latestWorkingFile, i = True)

def cleanupStatics():
	'''
	Do a complete clean-up of Core Archives setup...
	'''
	[cmds.delete(x) for x in cmds.ls('*CORE_ARCHIVES_hrc')]
	[cmds.delete(x) for x in cmds.ls('*placements_hrc')]
	[cmds.delete(x) for x in cmds.ls('*ROOT_ARCHIVES_DNT_hrc')]
	[cmds.delete(x) for x in cmds.ls('*unique_geo_hrc')]
	[cmds.delete(x) for x in cmds.ls('*_STATIC_ABC_STATIC_CACHES_hrc')]
	try:    cmds.delete('MASTER_COREARCHIVES_hrc')
	except:    pass
	try:    cmds.delete('MASTER_ROOTCOREARCHIVES_hrc')
	except:    pass
	try:	cmds.delete('MASTER_COREPLACEMENTS_hrc')
	except:    pass

	cleanupDeadCoreArchives()
	removeAllNS()

def removeAllNS(deleteContent = False):
	## Now remove all the nameSpaces!! This is to remove any clashes with the core_assemblies later on...
	safeNS = ['UI', 'shared']
	getAllNameSpaces = cmds.namespaceInfo(listOnlyNamespaces = True)
	for eachNS in getAllNameSpaces:
		if eachNS not in safeNS:
			try:
				if deleteContent:
					cmds.namespace(removeNamespace = eachNS, deleteNamespaceContent = True)
				else:
					cmds.namespace(removeNamespace = eachNS, mergeNamespaceWithRoot = True)
			except RuntimeError:
				pass

	if cmds.namespaceInfo(listOnlyNamespaces = True) != ['UI', 'shared']:
		removeAllNS()

def setupOceanIntegrationMatteLayer(layerName = 'featherEdge_LYR'):
	if cmds.objExists(layerName):
		cmds.editRenderLayerGlobals(currentRenderLayer = 'defaultRenderLayer')
		cmds.delete(layerName)

	geos = ['ABC_ANIM_CACHES_hrc']
	geos = [each for each in cmds.listRelatives(geos, fullPath = True, allDescendents = True, type = 'mesh')]
	nurbs = ['FX_CACHES_hrc']
	nurbs = [each for each in cmds.listRelatives(nurbs, fullPath = True, allDescendents = True, type = 'nurbsSurface')]

	cmds.editRenderLayerGlobals(currentRenderLayer = 'defaultRenderLayer')
	cmds.createRenderLayer(geos, nurbs, name = layerName, noRecurse = True)
	cmds.editRenderLayerGlobals(currentRenderLayer = layerName)
	
	cmds.editRenderLayerAdjustment('miDefaultOptions.finalGather', layer = layerName)
	cmds.setAttr('miDefaultOptions.finalGather', 0)
	
	cmds.editRenderLayerAdjustment('miDefaultOptions.rayTracing', layer = layerName)
	cmds.setAttr('miDefaultOptions.rayTracing', 0)
	
	cmds.editRenderLayerAdjustment('miDefaultOptions.shadowMethod', layer = layerName)
	cmds.setAttr('miDefaultOptions.shadowMethod', 0)
	
	cmds.editRenderLayerAdjustment('mentalcoreGlobals.en_ao', layer = layerName)
	cmds.setAttr('mentalcoreGlobals.en_ao', 1)
	
	cmds.editRenderLayerAdjustment('mentalcoreGlobals.en_envl', layer = layerName)
	cmds.setAttr('mentalcoreGlobals.en_envl', 0)

	[mapi.unassociate_pass(each, layerName) for each in mapi.get_associated_passes(layerName)]
	mapi.associate_pass('ao', layerName) if cmds.objExists('ao') else None

	attachColorMattes2(color = [0, 0, 0], mesh = geos)
	attachColorMattes3(color = [0, 0, 0], mesh = nurbs)

def setWaterfallLYR():
	if cmds.objExists('LIB_WORLD_Waterfall_hrc'):
		if not cmds.objExists('waterfall_mist_LYR'):
			geos = ['ABC_ANIM_CACHES_hrc', 'MASTER_COREARCHIVES_hrc']
			geos.extend( cmds.ls('*STATIC_ABC_STATIC_CACHES_hrc') )
			geos = [each for each in cmds.listRelatives(geos, fullPath = True, allDescendents = True, type = 'mesh')]
					
			filteredTypes = ['nParticle', 'mesh', 'directionalLight']
			mistObjects = [each for each in cmds.listRelatives('LIB_WORLD_Waterfall_hrc', allDescendents = True, fullPath = True) if 'mist' in each or 'geo' in each if cmds.objectType(each) in filteredTypes]
			mistObjects.extend(geos)
			
			cmds.createRenderLayer(mistObjects, name = 'waterfall_mist_LYR', noRecurse = True)
			cmds.editRenderLayerGlobals(currentRenderLayer = 'waterfall_mist_LYR')
			
			cmds.editRenderLayerAdjustment('miDefaultOptions.finalGather', layer = 'waterfall_mist_LYR')
			cmds.setAttr('miDefaultOptions.finalGather', 0)
			
			cmds.editRenderLayerAdjustment('miDefaultOptions.rayTracing', layer = 'waterfall_mist_LYR')
			cmds.setAttr('miDefaultOptions.rayTracing', 0)
			
			cmds.editRenderLayerAdjustment('miDefaultOptions.shadowMethod', layer = 'waterfall_mist_LYR')
			cmds.setAttr('miDefaultOptions.shadowMethod', 0)
			
			cmds.editRenderLayerAdjustment('mentalcoreGlobals.en_ao', layer = 'waterfall_mist_LYR')
			cmds.setAttr('mentalcoreGlobals.en_ao', 0)
			
			cmds.editRenderLayerAdjustment('mentalcoreGlobals.en_envl', layer = 'waterfall_mist_LYR')
			cmds.setAttr('mentalcoreGlobals.en_envl', 0)

			[mapi.unassociate_pass(each, 'waterfall_mist_LYR') for each in mapi.get_associated_passes('waterfall_mist_LYR')]

			meshes = [each for each in cmds.editRenderLayerMembers('waterfall_mist_LYR', fullNames = True, q = True) if cmds.objectType(each) == 'mesh']
			attachColorMattes2(color = [0, 0, 0], mesh = meshes)

		if not cmds.objExists('waterfall_ocean_LYR'):
			geos = ['ABC_ANIM_CACHES_hrc', 'MASTER_COREARCHIVES_hrc']
			geos.extend( cmds.ls('*STATIC_ABC_STATIC_CACHES_hrc') )
			geos = [each for each in cmds.listRelatives(geos, fullPath = True, allDescendents = True, type = 'mesh')]

			filteredTypes = ['mesh']
			mistObjects = [each for each in cmds.listRelatives('LIB_WORLD_Waterfall_hrc', allDescendents = True, fullPath = True) if 'geo' in each if cmds.objectType(each) in filteredTypes]
			mistObjects.append('LIGHTS_hrc')
			mistObjects.extend(geos)

			cmds.createRenderLayer(mistObjects, name = 'waterfall_ocean_LYR', noRecurse = True)
			cmds.editRenderLayerGlobals(currentRenderLayer = 'waterfall_ocean_LYR')
			
			cmds.editRenderLayerAdjustment('miDefaultOptions.finalGather', layer = 'waterfall_ocean_LYR')
			cmds.setAttr('miDefaultOptions.finalGather', 0)
			
			cmds.editRenderLayerAdjustment('miDefaultOptions.rayTracing', layer = 'waterfall_ocean_LYR')
			cmds.setAttr('miDefaultOptions.rayTracing', 0)
			
			cmds.editRenderLayerAdjustment('miDefaultOptions.shadowMethod', layer = 'waterfall_ocean_LYR')
			cmds.setAttr('miDefaultOptions.shadowMethod', 0)
			
			cmds.editRenderLayerAdjustment('mentalcoreGlobals.en_ao', layer = 'waterfall_ocean_LYR')
			cmds.setAttr('mentalcoreGlobals.en_ao', 0)
			
			cmds.editRenderLayerAdjustment('mentalcoreGlobals.en_envl', layer = 'waterfall_ocean_LYR')
			cmds.setAttr('mentalcoreGlobals.en_envl', 0)

			[mapi.unassociate_pass(each, 'waterfall_ocean_LYR') for each in mapi.get_associated_passes('waterfall_ocean_LYR')]
			[ mapi.associate_pass(each, 'waterfall_ocean_LYR') for each in ['beauty', 'incandescence', 'colour'] ]

			meshes = [each for each in cmds.editRenderLayerMembers('waterfall_ocean_LYR', fullNames = True, q = True) if cmds.objectType(each) == 'mesh' and 'waterfall_geo' not in each]
			attachColorMattes2(color = [0, 0, 0], mesh = meshes)

		if not cmds.objExists('waterfall_splash_LYR'):
			geos = ['ABC_ANIM_CACHES_hrc']
			geos.extend( cmds.ls('*STATIC_ABC_STATIC_CACHES_hrc') )
			geos = [each for each in cmds.listRelatives(geos, fullPath = True, allDescendents = True, type = 'mesh')]

			filteredTypes = ['mesh', 'nParticle']
			mistObjects = [each for each in cmds.listRelatives('LIB_WORLD_Waterfall_hrc', allDescendents = True, fullPath = True) if 'splash' in each or 'geo' in each if cmds.objectType(each) in filteredTypes]
			mistObjects.extend(geos)

			cmds.createRenderLayer(mistObjects, name = 'waterfall_splash_LYR', noRecurse = True)
			cmds.editRenderLayerGlobals(currentRenderLayer = 'waterfall_splash_LYR')

			cmds.editRenderLayerAdjustment('defaultRenderGlobals.imageFormat', layer = 'waterfall_splash_LYR')
			cmds.setAttr('defaultRenderGlobals.imageFormat', 7)
			
			cmds.editRenderLayerAdjustment('defaultRenderGlobals.currentRenderer', layer = 'waterfall_splash_LYR')
			cmds.setAttr('defaultRenderGlobals.currentRenderer', 'mayaHardware', type = 'string')
			
			cmds.editRenderLayerAdjustment('defaultRenderGlobals.currentRenderer', layer = 'waterfall_splash_LYR')
			cmds.setAttr('defaultRenderGlobals.currentRenderer', 'mayaHardware', type = 'string')
			
			cmds.editRenderLayerAdjustment('hardwareRenderGlobals.enableHighQualityLighting', layer = 'waterfall_splash_LYR')
			cmds.setAttr('hardwareRenderGlobals.enableHighQualityLighting', 1)
			
			cmds.editRenderLayerAdjustment('hardwareRenderGlobals.enableAcceleratedMultiSampling', layer = 'waterfall_splash_LYR')
			cmds.setAttr('hardwareRenderGlobals.enableAcceleratedMultiSampling', 1)
						
			cmds.editRenderLayerAdjustment('hardwareRenderGlobals.numberOfSamples', layer = 'waterfall_splash_LYR')
			cmds.setAttr('hardwareRenderGlobals.numberOfSamples', 9)
						
			cmds.editRenderLayerAdjustment('hardwareRenderGlobals.frameBufferFormat', layer = 'waterfall_splash_LYR')
			cmds.setAttr('hardwareRenderGlobals.frameBufferFormat', 0)
			
			cmds.editRenderLayerAdjustment('hardwareRenderGlobals.transparentShadowCasting', layer = 'waterfall_splash_LYR')
			cmds.setAttr('hardwareRenderGlobals.transparentShadowCasting', 1)
			
			cmds.editRenderLayerAdjustment('hardwareRenderGlobals.transparencySorting', layer = 'waterfall_splash_LYR')
			cmds.setAttr('hardwareRenderGlobals.transparencySorting', 0)
			
			cmds.editRenderLayerAdjustment('hardwareRenderGlobals.transparencySorting', layer = 'waterfall_splash_LYR')
			cmds.setAttr('hardwareRenderGlobals.transparencySorting', 0)
			
			cmds.editRenderLayerAdjustment('hardwareRenderGlobals.colorTextureResolution', layer = 'waterfall_splash_LYR')
			cmds.setAttr('hardwareRenderGlobals.colorTextureResolution', 512)
						
			cmds.editRenderLayerAdjustment('hardwareRenderGlobals.bumpTextureResolution', layer = 'waterfall_splash_LYR')
			cmds.setAttr('hardwareRenderGlobals.bumpTextureResolution', 1024)
			
			cmds.editRenderLayerAdjustment('hardwareRenderGlobals.textureCompression', layer = 'waterfall_splash_LYR')
			cmds.setAttr('hardwareRenderGlobals.textureCompression', 0)
			
			cmds.editRenderLayerAdjustment('hardwareRenderGlobals.enableNonPowerOfTwoTexture', layer = 'waterfall_splash_LYR')
			cmds.setAttr('hardwareRenderGlobals.enableNonPowerOfTwoTexture', 1)
			
			cmds.editRenderLayerAdjustment('hardwareRenderGlobals.culling', layer = 'waterfall_splash_LYR')
			cmds.setAttr('hardwareRenderGlobals.culling', 0)
			
			cmds.editRenderLayerAdjustment('hardwareRenderGlobals.smallObjectCulling', layer = 'waterfall_splash_LYR')
			cmds.setAttr('hardwareRenderGlobals.smallObjectCulling', 1)
			
			cmds.editRenderLayerAdjustment('hardwareRenderGlobals.cullingThreshold', layer = 'waterfall_splash_LYR')
			cmds.setAttr('hardwareRenderGlobals.cullingThreshold', 0)
			
			cmds.editRenderLayerAdjustment('hardwareRenderGlobals.graphicsHardwareGeometryCachingData', layer = 'waterfall_splash_LYR')
			cmds.setAttr('hardwareRenderGlobals.graphicsHardwareGeometryCachingData', 1)
			
			cmds.editRenderLayerAdjustment('hardwareRenderGlobals.maximumGeometryCacheSize', layer = 'waterfall_splash_LYR')
			cmds.setAttr('hardwareRenderGlobals.maximumGeometryCacheSize', 64)
			
			cmds.editRenderLayerAdjustment('hardwareRenderGlobals.hardwareEnvironmentLookup', layer = 'waterfall_splash_LYR')
			cmds.setAttr('hardwareRenderGlobals.hardwareEnvironmentLookup', 0)
			
			cmds.editRenderLayerAdjustment('hardwareRenderGlobals.enableMotionBlur', layer = 'waterfall_splash_LYR')
			cmds.setAttr('hardwareRenderGlobals.enableMotionBlur', 0)
			
			cmds.editRenderLayerAdjustment('hardwareRenderGlobals.enableGeometryMask', layer = 'waterfall_splash_LYR')
			cmds.setAttr('hardwareRenderGlobals.enableGeometryMask', 1)
			
			cmds.editRenderLayerAdjustment('hardwareRenderGlobals.blendSpecularWithAlpha', layer = 'waterfall_splash_LYR')
			cmds.setAttr('hardwareRenderGlobals.blendSpecularWithAlpha', 0)

def attachColorMattes3(color = [0, 0, 0], mesh = ['']):
	core_mat = cmds.createNode('core_material')
	core_mat_sg = cmds.sets(renderable = True, noSurfaceShader = True, empty = True)
	cmds.connectAttr('%s.outValue' % core_mat, '%s.miPhotonShader' % core_mat_sg)
	cmds.connectAttr('%s.outValue' % core_mat, '%s.miShadowShader' % core_mat_sg)
	cmds.connectAttr('%s.outValue' % core_mat, '%s.miMaterialShader' % core_mat_sg)
	cmds.connectAttr('ocean_dispShader.outColor', '%s.displacementShader' % core_mat_sg) if cmds.objExists('ocean_dispShader') else None
	
	cmds.setAttr('%s.en_blinn' % core_mat, 0)
	cmds.setAttr('%s.en_indirect' % core_mat, 0)
	cmds.setAttr('%s.ao_enable_overrides' % core_mat, 1)
	cmds.setAttr('%s.ao_override_spread' % core_mat, 125)
	cmds.setAttr('%s.ao_override_distance' % core_mat, 0.5)
	cmds.setAttr('%s.diffuse' % core_mat, color[0], color[1], color[2], type = 'double3')

	cmds.sets(mesh, edit = True, forceElement = core_mat_sg)

def attachColorMattes2(color = [0, 0, 0], mesh = ['']):
	core_mat = cmds.createNode('core_surface_shader')
	core_mat_sg = cmds.sets(renderable = True, noSurfaceShader = True, empty = True)
	cmds.connectAttr('%s.outValue' % core_mat, '%s.miMaterialShader' % core_mat_sg)
	cmds.connectAttr('%s.outValue' % core_mat, '%s.miShadowShader' % core_mat_sg)
	
	cmds.setAttr('%s.colour' % core_mat, color[0], color[1], color[2], type = 'double3')

	cmds.sets(mesh, edit = True, forceElement = core_mat_sg)

def NukeCameraWriter():
	import Maya2Nuke
	reload(Maya2Nuke)
	try:
		Maya2Nuke.maya2nuke()
	except:
		pass
	#########################

	Cam=filter(lambda x: "ep" in x,cmds.ls(ca=True))
	for x in Cam:
		camName = x.rstrip("_bakeShape")
		version=cmds.getAttr("%s.version" %(cmds.listRelatives(x,ap=True,f=True)[0].split("|")[1]))
		Episode = camName.split("_")[0]
		if not "ep" in Episode:
			next
		path = 'K:/bubblebathbay/episodes/%s/NukeCams/' % Episode
		if os.path.exists(path):
			print('This is not the 1st Update cam')
		else:
			cmds.sysFile(path,makeDir=True)
			print('NewDir created!!')
		cmds.select(x)
		Maya2Nuke.getAllCamera(cmds.ls(sl=True))
		Maya2Nuke.generator()
		text = cmds.cmdScrollFieldExecuter('copytext' ,q=1,t=1)
		if not text :
			cmds.warning("%s import error" %cmds.ls(sl=True))
			#return
		else:
			#if fileName.split(".")[0] in dirPath:
			cmds.sysFile( path+'/%s.' %(filter(lambda x: camName in x , path)), delete=True)# Windows
			f = open(path+'%s.nk' %(camName+"_"+version),'w')
			f.write(text)
			f.close

	if not text :
		cmds.warning("%s import error" %cmds.ls(sl=True))
		#return
	else:
		#if fileName.split(".")[0] in dirPath:
		cmds.sysFile( path+'/%s.' %(filter(lambda x: camName in x , os.listdir(path)))[0], delete=True)# Windows
		f = open(path+'%s.nk' %(camName+"_"+version),'w')
		f.write(text)
		f.close

def extraLightFog(renderLayer = 'ExtraLightFog'):
	if renderLayer:
		if not cmds.objExists(renderLayer):
			cmds.editRenderLayerGlobals(currentRenderLayer = 'defaultRenderLayer')
			geos = []
			geos.append('ABC_ANIM_CACHES_hrc') if cmds.objExists('ABC_ANIM_CACHES_hrc') else geos
			geos = [each for each in cmds.listRelatives(geos, fullPath = True, allDescendents = True, type = 'mesh') if 'eyelash' not in each] if geos else geos
			
			if geos:
				cmds.createRenderLayer(geos, name = renderLayer, noRecurse = True)
				cmds.editRenderLayerGlobals(currentRenderLayer = renderLayer)
				
				cmds.editRenderLayerAdjustment('miDefaultOptions.finalGather', layer = renderLayer)
				cmds.setAttr('miDefaultOptions.finalGather', 0)
				
				cmds.editRenderLayerAdjustment('miDefaultOptions.rayTracing', layer = renderLayer)
				cmds.setAttr('miDefaultOptions.rayTracing', 0)
				
				cmds.editRenderLayerAdjustment('miDefaultOptions.shadowMethod', layer = renderLayer)
				cmds.setAttr('miDefaultOptions.shadowMethod', 0)
				
				cmds.editRenderLayerAdjustment('mentalcoreGlobals.en_ao', layer = renderLayer)
				cmds.setAttr('mentalcoreGlobals.en_ao', 0)
				
				cmds.editRenderLayerAdjustment('mentalcoreGlobals.en_envl', layer = renderLayer)
				cmds.setAttr('mentalcoreGlobals.en_envl', 0)

				[mapi.unassociate_pass(each, renderLayer) for each in mapi.get_associated_passes(renderLayer)]

				meshes = [each for each in cmds.editRenderLayerMembers(renderLayer, fullNames = True, q = True) if cmds.objectType(each) == 'mesh']
				
				attachColorMattes2(color = [0, 0, 0], mesh = meshes)

def extraLightGlow(renderLayer = 'ExtraLightGlow'):
	if renderLayer:
		if not cmds.objExists(renderLayer):
			cmds.editRenderLayerGlobals(currentRenderLayer = 'defaultRenderLayer')
			geos = []
			geos.append('ABC_ANIM_CACHES_hrc') if cmds.objExists('ABC_ANIM_CACHES_hrc') else geos
			geos = [each for each in cmds.listRelatives(geos, fullPath = True, allDescendents = True, type = 'mesh') if 'eyelash' not in each] if geos else geos
			
			if geos:
				cmds.createRenderLayer(geos, name = renderLayer, noRecurse = True)
				cmds.editRenderLayerGlobals(currentRenderLayer = renderLayer)
				
				cmds.editRenderLayerAdjustment('miDefaultOptions.finalGather', layer = renderLayer)
				cmds.setAttr('miDefaultOptions.finalGather', 0)
				
				cmds.editRenderLayerAdjustment('miDefaultOptions.rayTracing', layer = renderLayer)
				cmds.setAttr('miDefaultOptions.rayTracing', 0)
				
				cmds.editRenderLayerAdjustment('miDefaultOptions.shadowMethod', layer = renderLayer)
				cmds.setAttr('miDefaultOptions.shadowMethod', 0)
				
				cmds.editRenderLayerAdjustment('mentalcoreGlobals.en_ao', layer = renderLayer)
				cmds.setAttr('mentalcoreGlobals.en_ao', 0)
				
				cmds.editRenderLayerAdjustment('mentalcoreGlobals.en_envl', layer = renderLayer)
				cmds.setAttr('mentalcoreGlobals.en_envl', 0)

				[mapi.unassociate_pass(each, renderLayer) for each in mapi.get_associated_passes(renderLayer)]

				meshes = [each for each in cmds.editRenderLayerMembers(renderLayer, fullNames = True, q = True) if cmds.objectType(each) == 'mesh']
				
				attachColorMattes2(color = [0, 0, 0], mesh = meshes)

def customRenderLayerSetup(renderLayer = 'ExtraLightLit'):
	if renderLayer:
		if not cmds.objExists(renderLayer):
			geos = []
			geos.append('ABC_ANIM_CACHES_hrc') if cmds.objExists('ABC_ANIM_CACHES_hrc') else geos
			geos.append('MASTER_COREARCHIVES_hrc') if cmds.objExists('MASTER_COREARCHIVES_hrc') else geos
			geos.extend( cmds.ls('*STATIC_ABC_STATIC_CACHES_hrc') )
			geos = [each for each in cmds.listRelatives(geos, fullPath = True, allDescendents = True, type = 'mesh') if 'eyelash' not in each]
			geos.append('ocean_srf')

			geos = [x for x in geos if cmds.objExists(x)]
			cmds.createRenderLayer(geos, name = renderLayer, noRecurse = True)
			cmds.editRenderLayerGlobals(currentRenderLayer = renderLayer)
			
			cmds.editRenderLayerAdjustment('miDefaultOptions.finalGather', layer = renderLayer)
			cmds.setAttr('miDefaultOptions.finalGather', 0)
			
			cmds.editRenderLayerAdjustment('miDefaultOptions.rayTracing', layer = renderLayer)
			cmds.setAttr('miDefaultOptions.rayTracing', 1)
			
			cmds.editRenderLayerAdjustment('miDefaultOptions.shadowMethod', layer = renderLayer)
			cmds.setAttr('miDefaultOptions.shadowMethod', 1)
			
			cmds.editRenderLayerAdjustment('mentalcoreGlobals.en_ao', layer = renderLayer)
			cmds.setAttr('mentalcoreGlobals.en_ao', 0)
			
			cmds.editRenderLayerAdjustment('mentalcoreGlobals.en_envl', layer = renderLayer)
			cmds.setAttr('mentalcoreGlobals.en_envl', 0)

			[mapi.unassociate_pass(each, renderLayer) for each in mapi.get_associated_passes(renderLayer)]

			meshes = [each for each in cmds.editRenderLayerMembers(renderLayer, fullNames = True, q = True) if cmds.objectType(each) == 'mesh']
			
			attachShadingMatte2(ocean = False, mesh = meshes)
			attachShadingMatte2(ocean = True, mesh = ['ocean_srf']) if cmds.objExists('ocean_srf') else None

def setupExtraLight(**kwargs):
	pLight = cmds.pointLight(**kwargs)
	
	cmds.setAttr('%s.lightRadius' % pLight, 1)
	cmds.setAttr('%s.shadowRays' % pLight, 16)

	return pLight

def setupExtraSpotLight(**kwargs):
	pLight = cmds.spotLight(**kwargs)
	
	cmds.setAttr('%s.lightRadius' % pLight, 2)
	cmds.setAttr('%s.shadowRays' % pLight, 16)

	cmds.setAttr('%s.scaleX' % cmds.listRelatives(pLight, parent = True, fullPath = True)[0], 0.126)
	cmds.setAttr('%s.scaleY' % cmds.listRelatives(pLight, parent = True, fullPath = True)[0], 0.126)
	cmds.setAttr('%s.scaleZ' % cmds.listRelatives(pLight, parent = True, fullPath = True)[0], -0.3)

	return pLight

def auroraFogRenderLayerSetup(renderLayer = 'auroraFog', renderLayer2 = 'auroraFogLit'):
	lightFogBulb = cmds.ls('*AI_LightHouse_BLD_Lighthouse_stand_023_geo')
	if lightFogBulb:

			cmds.file('//192.168.5.253/BBB_main/bbb/i/ginyih/towerLightFog.ma', i = True)
			
			geos = ['AI_LightHouse_BLD_hrc']
			geos = [each for each in cmds.listRelatives(geos, fullPath = True, allDescendents = True, type = 'mesh')]
			geos.append('|towerFogLightGrp')
			
			cmds.createRenderLayer(geos, name = renderLayer, noRecurse = True)
			cmds.editRenderLayerGlobals(currentRenderLayer = renderLayer)
			
			cmds.editRenderLayerAdjustment('miDefaultOptions.finalGather', layer = renderLayer)
			cmds.setAttr('miDefaultOptions.finalGather', 0)
			
			cmds.editRenderLayerAdjustment('miDefaultOptions.rayTracing', layer = renderLayer)
			cmds.setAttr('miDefaultOptions.rayTracing', 1)
			
			cmds.editRenderLayerAdjustment('miDefaultOptions.shadowMethod', layer = renderLayer)
			cmds.setAttr('miDefaultOptions.shadowMethod', 1)
			
			cmds.editRenderLayerAdjustment('mentalcoreGlobals.en_ao', layer = renderLayer)
			cmds.setAttr('mentalcoreGlobals.en_ao', 0)
			
			cmds.editRenderLayerAdjustment('mentalcoreGlobals.en_envl', layer = renderLayer)
			cmds.setAttr('mentalcoreGlobals.en_envl', 0)

			[mapi.unassociate_pass(each, renderLayer) for each in mapi.get_associated_passes(renderLayer)]

			meshes = [each for each in cmds.editRenderLayerMembers(renderLayer, fullNames = True, q = True) if cmds.objectType(each) == 'mesh']
			
			attachColorMattes2(color = [0, 0, 0], mesh = meshes)
			
			cmds.xform(lightFogBulb[0], centerPivots = True)
			cmds.delete( cmds.pointConstraint(lightFogBulb[0], '|towerFogLightGrp', mo = False, offset = [0, 0.5, 0]) )

			hideObjects = ['*AI_LightHouse_BLD_House01_Bulb_1_geoShape', '*AI_LightHouse_BLD_bulbGlass_geoShape', '*AI_LightHouse_BLD_WhiteWireStand_geoShape', '*AI_LightHouse_BLD_GoldWireStand_geoShape', '*AI_LightHouse_BLD_BulbInnerWire_geoShape']
			if hideObjects:
				[cmds.setAttr('%s.visibility' % cmds.listRelatives(each, parent = True, fullPath = True)[0], 0) for each in hideObjects]

			######################################################################
			cmds.editRenderLayerGlobals(currentRenderLayer = 'defaultRenderLayer')

			cmds.file('//192.168.5.253/BBB_main/bbb/i/ginyih/towerLight.ma', i = True)
			
			geos = ['MASTER_COREARCHIVES_hrc']
			geos.extend( cmds.ls('*STATIC_ABC_STATIC_CACHES_hrc') )
			geos = [each for each in cmds.listRelatives(geos, fullPath = True, allDescendents = True, type = 'mesh')]
			geos.append('FX_CACHES_hrc')
			geos.append('|towerLightCtrl')
			
			cmds.createRenderLayer(geos, name = renderLayer2, noRecurse = True)
			cmds.editRenderLayerGlobals(currentRenderLayer = renderLayer2)
			
			cmds.editRenderLayerAdjustment('miDefaultOptions.finalGather', layer = renderLayer2)
			cmds.setAttr('miDefaultOptions.finalGather', 0)
			
			cmds.editRenderLayerAdjustment('miDefaultOptions.rayTracing', layer = renderLayer2)
			cmds.setAttr('miDefaultOptions.rayTracing', 1)
			
			cmds.editRenderLayerAdjustment('miDefaultOptions.shadowMethod', layer = renderLayer2)
			cmds.setAttr('miDefaultOptions.shadowMethod', 1)
			
			cmds.editRenderLayerAdjustment('mentalcoreGlobals.en_ao', layer = renderLayer2)
			cmds.setAttr('mentalcoreGlobals.en_ao', 0)
			
			cmds.editRenderLayerAdjustment('mentalcoreGlobals.en_envl', layer = renderLayer2)
			cmds.setAttr('mentalcoreGlobals.en_envl', 0)

			[mapi.unassociate_pass(each, renderLayer2) for each in mapi.get_associated_passes(renderLayer2)]

			meshes = [each for each in cmds.editRenderLayerMembers(renderLayer2, fullNames = True, q = True) if cmds.objectType(each) == 'mesh']

			noShadowObjects = cmds.ls('*AI_LightHouse_BLD_House01_Bulb_1_geoShape')
			if noShadowObjects:
				[(cmds.setAttr('%s.castsShadows' % each, 0), cmds.setAttr('%s.receiveShadows' % each, 0)) for each in noShadowObjects]

			attachShadingMatte2(ocean = False, mesh = meshes)
			attachShadingMatte2(ocean = True, mesh = ['ocean_srf'])


def LookThruCamera(*args):
	for x in cmds.listRelatives('*BAKE_CAM_hrc*', children = True, fullPath = True):

		cmds.lookThru(x)

		cmds.camera(x, e=True, displayResolution = True, displayGateMask = True, displayFilmGate = False, overscan=1.3 )


############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################

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

def submitToDeadline():
	## Primary setup
	repository_Dir	= '//192.168.5.202/deadline_repository'
	projDir			= '//192.168.5.253/BBB_main/bbb'
	prePythonScript	= ''

	sceneName = cmds.file(q = True, sceneName = True)
	if sceneName:
		
		if os.path.dirname(sceneName).endswith('/Light/work/maya'):
			
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

				## Blacklist slaves
				blacklistSlaves = [	'Bbbrender11',
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
									'Noel-pc']

				deadline.Renderer 			= 'MentalRay'
				deadline.Priority			= priority
				deadline.Pool 				= 'maya'
				deadline.MachineLimit		= 1
				deadline.Version 			= 2013.5
				deadline.Build 				= '64bit'
				deadline.Blacklist 			= ','.join(blacklistSlaves)
				deadline.UserName			= 'administrator'
				deadline.TaskTimeoutMinutes	= 120
				deadline.Name             	= os.path.splitext( os.path.basename(sceneName) )[0]
				deadline.Frames             = '%s' % frameRange
				deadline.OutputDirectory0   = '%s' % output_dir
				deadline.OutputFilePath		= deadline.OutputDirectory0
				deadline.ProjectPath        = projDir
				deadline.MachineLimit 		= 0

				## Tile Rendering
				deadline.TileJob			= True
				deadline.TileJobFrame		= 394
				deadline.TileJobTilesInX	= 5
				deadline.TileJobTilesInY	= 5
				
				maya_job                	= deadline.build_maya_job_info()
				maya_plugin             	= deadline.build_maya_plugin_info()
				
				if os.path.isfile(sceneName):
					deadline.submit_to_deadline(maya_job, maya_plugin, sceneName)
					os.startfile(output_dir)
				else:
					cmds.warning('%s is not a valid file!' % sceneName)
				
		else:
			cmds.warning('Not in correct workspace, i.e. I:/bubblebathbay/episodes/ep###/ep###_sh###/Light/work/maya')
			
	else:
		cmds.warning('Please save your file!')

def miCreateSunSky():
	cmds.editRenderLayerGlobals(currentRenderLayer = 'defaultRenderLayer')
	cmds.loadPlugin('Mayatomr.mll') if not cmds.pluginInfo('Mayatomr.mll', query = 1, loaded = 1) else None
	cmds.loadPlugin('OpenEXRLoader.mll') if not cmds.pluginInfo('OpenEXRLoader.mll', query = 1, loaded = 1) else None
	mel.eval("miCreateDefaultNodes") if not cmds.objExists("miDefaultOptions") else None
	cmds.setAttr('defaultRenderGlobals.currentRenderer', 'mentalRay', type = 'string')
	cmds.setAttr('miDefaultOptions.finalGather', 1)

	exposureControl = cmds.shadingNode('mia_exposure_simple', asUtility = True)
	cmds.setAttr("%s.pedestal" % exposureControl, 0.0)
	cmds.setAttr("%s.gain" % exposureControl, 0.2)
	cmds.setAttr("%s.knee" % exposureControl, 0.75)
	cmds.setAttr("%s.compression" % exposureControl, 3.0)
	cmds.setAttr("%s.gamma" % exposureControl, 2.2)

	lightInst = cmds.createNode('transform', name = 'sunDirection')
	lightShape = cmds.shadingNode('directionalLight', name = 'sunShape', p = lightInst, asLight = True)
	cmds.setAttr("%s.rotateX" % lightInst, -75.0)
	light = cmds.listRelatives(lightInst)

	cmds.setAttr("%s.miExportMrLight" % light[0], 1)
	sunShader = cmds.shadingNode('mia_physicalsun', asUtility = True)
	cmds.connectAttr("%s.message" % sunShader, "%s.miLightShader" % light[0])
	cmds.connectAttr("%s.message" % sunShader, "%s.miPhotonEmitter" % light[0])

	skyShader = cmds.shadingNode('mia_physicalsky', asUtility = True)
	cmds.connectAttr("%s.message" % lightInst, "%s.sun" % skyShader)
	cmds.setAttr("%s.y_is_up" % skyShader, 1)
	cmds.addAttr(skyShader, shortName = "miSkyExposure", longName = "miSkyExposure", hidden = True, at = "message")
	cmds.connectAttr("%s.message" % exposureControl, "%s.miSkyExposure" % skyShader)

	cmds.connectAttr("%s.on" % skyShader, "%s.on" % sunShader)
	cmds.connectAttr("%s.multiplier" % skyShader, "%s.multiplier" % sunShader)
	cmds.connectAttr("%s.rgb_unit_conversion" % skyShader, "%s.rgb_unit_conversion" % sunShader)
	cmds.connectAttr("%s.haze" % skyShader, "%s.haze" % sunShader)
	cmds.connectAttr("%s.redblueshift" % skyShader, "%s.redblueshift" % sunShader)
	cmds.connectAttr("%s.saturation" % skyShader, "%s.saturation" % sunShader)
	cmds.connectAttr("%s.horizon_height" % skyShader, "%s.horizon_height" % sunShader)
	cmds.connectAttr("%s.y_is_up" % skyShader, "%s.y_is_up" % sunShader)

	cameras = cmds.ls(type = 'camera')
	for cam in cameras:
		if not cmds.getAttr('%s.orthographic' % cam):
			cmds.connectAttr("%s.message" % exposureControl, "%s.miLensShader" % cam, force = True)
			cmds.connectAttr("%s.message" % skyShader, "%s.miEnvironmentShader" % cam, force = True)
			
	try:	cmds.addAttr('mentalrayGlobals', shortName = "sunAndSkyShader", longName = "sunAndSkyShader", hidden = True, at = "message")
	except:	pass
	cmds.connectAttr("%s.message" % skyShader, "mentalrayGlobals.sunAndSkyShader", force = True)

def setTOD(TODay = 'midday'):
	"""
	Main time of day load and setup
	"""
	sunPresetPath           = 'I:/bubblebathbay/fx/presets/Lighting/transform/%s.mel' % TODay
	physicalSkyPresetPath   = 'I:/bubblebathbay/fx/presets/Lighting/mia_physicalsky/%s.mel' % TODay
	physicalSunPresetPath   = 'I:/bubblebathbay/fx/presets/Lighting/mia_physicalsun/%s.mel' % TODay

	cmds.delete('sunDirection') if cmds.objExists('sunDirection') else None

	cmds.setAttr('defaultRenderGlobals.currentRenderer','mentalRay', type = 'string')
	mel.eval("unifiedRenderGlobalsWindow;")
	mel.eval("int $index = 6;")
	mel.eval("string $renderer = `currentRenderer`;")
	mel.eval("print $renderer")
	mel.eval("string $tabLayout = `getRendererTabLayout $renderer`;")
	mel.eval("print $tabLayout")
	mel.eval("tabLayout -e -sti $index $tabLayout;")
	mel.eval("fillSelectedTabForCurrentRenderer;")
	cmds.window('unifiedRenderGlobalsWindow', e = True, vis = False)

	## NOW DO THE MAYA BUILD FOR PHYSICAL SKY Note this builds a new directional light every time which is why we delete the old one!!
	## remove the olds
	cmds.delete('sunDirection') if cmds.objExists('sunDirection') else None
	
	try:	[cmds.delete(each) for each in cmds.ls(type = 'mia_physicalsky')]
	except:	pass
	try:	[cmds.delete(each) for each in cmds.ls(type = 'mia_physicalsun')]
	except:	pass
	try:	[cmds.delete(each) for each in cmds.ls(type = 'mia_exposure_simple')]
	except:	pass

	## Now do the sun and sky setup
	mel.eval("miCreateSunSky;")
	# miCreateSunSky()
	##
	try:	cmds.disconnectAttr('mia_physicalsky1.redblueshift','mia_physicalsun1.redblueshift')
	except:	pass
	try:	cmds.disconnectAttr('mia_physicalsky1.saturation','mia_physicalsun1.saturation')
	except:	pass
	try:	cmds.disconnectAttr('mia_physicalsky1.multiplier','mia_physicalsun1.multiplier')
	except:	pass

	## Apply preset
	cmds.evalDeferred( 'mel.eval("""applyPresetToNode \"sunDirection\" "" "" \"%s\" 1;""")' % sunPresetPath )
	cmds.evalDeferred( 'mel.eval("""applyPresetToNode \"mia_physicalsky1\" "" "" \"%s\" 1;""")' % physicalSkyPresetPath )
	cmds.evalDeferred( 'mel.eval("""applyPresetToNode \"mia_physicalsun1\" "" "" \"%s\" 1;""")' % physicalSunPresetPath )
	cmds.setAttr("mia_physicalsun1.shadow_softness", 4)
	cmds.setAttr("mia_physicalsun1.samples", 24)

	cmds.group(n = 'LIGHTS_hrc', em = True) if not cmds.objExists('LIGHTS_hrc') else None
	try:	cmds.parent('sunDirection', 'LIGHTS_hrc')
	except:	pass

	## Setup exposure
	buildExposure()
	setup_MC_renderPasses()
	buildCustomMCRenderPasses()
	subdivSmoothedAttr()
	
	cmds.setAttr('LIGHTS_hrc.rotateY', -90) if cmds.objExists('LIGHTS_hrc') else None

def setTOD_automatic(TODay = 'midday'):
	cmds.delete('sunDirection') if cmds.objExists('sunDirection') else None

	# cmds.setAttr('defaultRenderGlobals.currentRenderer','mentalRay', type = 'string')
	# mel.eval("unifiedRenderGlobalsWindow;")
	# mel.eval("int $index = 6;")
	# mel.eval("string $renderer = `currentRenderer`;")
	# mel.eval("print $renderer")
	# mel.eval("string $tabLayout = `getRendererTabLayout $renderer`;")
	# mel.eval("print $tabLayout")
	# mel.eval("tabLayout -e -sti $index $tabLayout;")
	# mel.eval("fillSelectedTabForCurrentRenderer;")
	# cmds.window('unifiedRenderGlobalsWindow', e = True, vis = False)
	
	try:	[cmds.delete(each) for each in cmds.ls(type = 'mia_physicalsky')]
	except:	pass
	try:	[cmds.delete(each) for each in cmds.ls(type = 'mia_physicalsun')]
	except:	pass
	try:	[cmds.delete(each) for each in cmds.ls(type = 'mia_exposure_simple')]
	except:	pass

	miCreateSunSky()
	try:	cmds.disconnectAttr('mia_physicalsky1.redblueshift','mia_physicalsun1.redblueshift')
	except:	pass
	try:	cmds.disconnectAttr('mia_physicalsky1.saturation','mia_physicalsun1.saturation')
	except:	pass
	try:	cmds.disconnectAttr('mia_physicalsky1.multiplier','mia_physicalsun1.multiplier')
	except:	pass

	cmds.setAttr("mia_physicalsun1.shadow_softness", 4)
	cmds.setAttr("mia_physicalsun1.samples", 24)

	cmds.group(n = 'LIGHTS_hrc', em = True) if not cmds.objExists('LIGHTS_hrc') else None
	try:	cmds.parent('sunDirection', 'LIGHTS_hrc')
	except:	pass

	## Setup exposure
	buildExposure()
	setup_MC_renderPasses()
	buildCustomMCRenderPasses()
	subdivSmoothedAttr()
	
	cmds.setAttr('LIGHTS_hrc.rotateY', -90) if cmds.objExists('LIGHTS_hrc') else None
			
def buildCustomMCRenderPasses():
	getAllPasses = mapi.get_all_passes()

	passes = {
			  'matte_water' : ['*ocean_srf*'],
			  'matte_ground' : ['*bbb_terrain_geo*','*beach_geo*']
			  }

	for key , var in passes.items():
		if 'matte' in key:
			if not key in getAllPasses:
				mapi.create_pass('Matte', n= key)
			for eachGeo in var:
				getAllGeo = cmds.ls(eachGeo, type='transform')
				for each in getAllGeo:
					try:
						mapi.link_to_pass([each], key, mapi.OBJECTS)
					except:
						cmds.warning('Failed to set {0} to renderpass {1}'.format(each, key))
						pass

def buildExposure():
	if cmds.objExists('mia_exposure_simple1'):
		cmds.delete('mia_exposure_simple1')

	shotCamera = ''
	for eachCam in cmds.ls(type = 'camera'):
		if cmds.objExists('%s.type' % cmds.listRelatives(eachCam, parent = True)[0]):
			if cmds.getAttr('%s.type' % cmds.listRelatives(eachCam, parent = True)[0]) == 'shotCam':
				shotCamera = eachCam

	if shotCamera:
		if cmds.objExists('mentalcoreLens'):
			if not cmds.isConnected('mentalcoreLens.message', '%s.miLensShader' % shotCamera):
				cmds.connectAttr('mentalcoreLens.message', '%s.miLensShader' % shotCamera, f = True)
		else:
			cmds.warning('mentalcoreLens doesn\'t exist!')
	else:
		cmds.warning('NO SHOT CAMERA FOUND!!!')

def setup_MC_renderPasses():
	"""
	Sets the base default render passes for mental core
	"""
	try:
		getAllPasses = mapi.get_all_passes()
		## ELEMENTS + VISIBLE IN REFRACTIONS
		if not 'ao' in getAllPasses:
			aoPass = mapi.create_pass('Ambient Occlusion')
			cmds.setAttr(aoPass + '.vis_in_refr', 1)
			mapi.associate_pass(aoPass, 'defaultRenderLayer')
		
		if not 'beauty' in getAllPasses:
			beautyPass = mapi.create_pass('Beauty')
			mapi.associate_pass(beautyPass, 'defaultRenderLayer')
			mapi.associate_pass(beautyPass, 'cloud_LYR')
		
		if not 'colour' in getAllPasses:
			colourPass = mapi.create_pass('Colour')
			cmds.setAttr(colourPass + '.vis_in_refr', 1)
			mapi.associate_pass(colourPass, 'defaultRenderLayer')
			mapi.associate_pass(colourPass, 'cloud_LYR')

		if not 'depth_norm' in getAllPasses:
			depthPass = mapi.create_pass('Depth (Normalized)')
			mapi.associate_pass(depthPass, 'defaultRenderLayer')
			cmds.setAttr(depthPass + '.vis_in_refr', 1)
			cmds.setAttr("depth_norm.filtering",1)
			
		if not 'diffuse' in getAllPasses:
			diffusePass = mapi.create_pass('Diffuse')
			cmds.setAttr(diffusePass + '.vis_in_refr', 1)
			mapi.associate_pass(diffusePass, 'defaultRenderLayer')
			
		if not 'facing_ratio' in getAllPasses:
			facingPass = mapi.create_pass('Facing Ratio')
			cmds.setAttr(facingPass + '.vis_in_refr', 1)
			mapi.associate_pass(facingPass, 'defaultRenderLayer')
			mapi.associate_pass(facingPass, 'cloud_LYR')
		
		if not 'incandescence' in getAllPasses:
			incandescencePass = mapi.create_pass('Incandescence')
			mapi.associate_pass(incandescencePass, 'defaultRenderLayer')
		
		if not 'indirect' in getAllPasses:
			indirectPass = mapi.create_pass('Indirect')
			cmds.setAttr(indirectPass + '.vis_in_refr', 1)
			mapi.associate_pass(indirectPass, 'defaultRenderLayer')
	
		if not 'matte_ground' in getAllPasses:
			matteGround = mapi.create_pass('Matte', n = 'matte_ground')
			mapi.associate_pass(matteGround, 'defaultRenderLayer')
		
		if not 'matte_houses' in getAllPasses:
			matteHouses = mapi.create_pass('Matte', n = 'matte_houses')
			mapi.associate_pass(matteHouses, 'defaultRenderLayer')
		
		if not 'matte_water' in getAllPasses:
			matteWater = mapi.create_pass('Matte', n = 'matte_water')
			mapi.associate_pass(matteWater, 'defaultRenderLayer')
		
		if not 'reflection' in getAllPasses:
			reflectionPass = mapi.create_pass('Reflection')
			cmds.setAttr(reflectionPass + '.vis_in_refr', 1)
			mapi.associate_pass(reflectionPass, 'defaultRenderLayer')
		
		if not 'refraction' in getAllPasses:
			refractionPass = mapi.create_pass('Refraction')
			mapi.associate_pass(refractionPass, 'defaultRenderLayer')
		
		if not 'specular' in getAllPasses:
			specularPass = mapi.create_pass('Specular')
			cmds.setAttr(specularPass + '.vis_in_refr', 1)
			mapi.associate_pass(specularPass, 'defaultRenderLayer')

		if cmds.objExists('normal_camera_norm') == False:
			normalWorldPass = mapi.create_pass('Normal Camera (Normalized)')
			cmds.setAttr(normalWorldPass + '.vis_in_refr', 1)
			cmds.setAttr(normalWorldPass + '.filtering' , 1)
			mapi.associate_pass(normalWorldPass, 'defaultRenderLayer')
	except:
		pass

def characterCorneaFix():
	refFile = cmds.ls('*forest_jpg_FileIn*')
	refFileList = []
	for refFileName in refFile:
		if not "place2dTexture" in refFileName:
			print refFileName
			refFileList.append(refFileName)

	for refFileImage in refFileList:
		refFileNameList = cmds.listConnections(refFileImage)
		for refFileShader in refFileNameList:
			if cmds.nodeType(refFileShader) != 'place2dTexture':
				1
				try:	cmds.disconnectAttr(refFileImage + '.outColor', refFileShader + '.diffuse')
				except:	pass
				try:	cmds.disconnectAttr(refFileImage + '.outAlpha', refFileShader + '.diffuseA')
				except:	pass
				try:	cmds.setAttr(refFileShader + ".en_refl", 1)
				except:	pass
				try:	cmds.connectAttr('%s.outColor' % refFileImage, refFileShader + '.refl_col')
				except:	pass
				try:	cmds.connectAttr('%s.outAlpha' % refFileImage, refFileShader + '.refl_colA')
				except:	pass

def rebuild_cache_from_xml(xmlPath, fluidShape = ''):
	"""
	Based off Autodesk cache's xml file structure to get and set
	*.tag / *.attrib / *.text / *.tail

	NOTE: Interactive cache attachments;
	IF the interactive master boat is found in the scene
	These caches need to be attached to the interactive wake and foam 3D fluid textures for the purposes of previewing the caches.
	Later on during publish we cache the base wake and foam, then attach these caches back to the ocean_dispShader and then perform a merge caches and output that to the publish folder.
	"""
	import xml.etree.cElementTree as ET

	if os.path.exists(xmlPath):
		# Create a new cache node
		cache = cmds.cacheFile(createCacheNode = True, fileName = xmlPath)

		# Parse xml file
		xml  = ET.parse(xmlPath)
		root = xml.getroot()

		# By default, Autodesk's xml structure has all the attributes and value set in the <extra> tag.
		# Therefore, we have to go through all of them and set them in maya because cache only works
		# properly with all the same settings or it'll show some warning stating some values aren't the same.
		for tag in root.findall("extra"):
			try:	attr, tag = tag.text.split("=")
			except:	attr = None

			if attr is not None:
				if cmds.objExists(attr):
					try:	cmds.setAttr( attr, eval(tag) )
					except:	mel.eval( r'warning "Failed to set \"%s\"...";' %attr )

		# Get exactly the same slot number of the cache and fluid's connection hook-ups or cache won't work properly.
		fluids = []
		for x in root.findall("Channels"):
			for y in x.getchildren():
				channelName = y.get("ChannelName")

				if 'interactive' in y.get("ChannelName"): ## Note the split here was separating the interactive_oceanFoam naming badly so this gets handled differently here for interactive
					fluid = '_'.join(y.get("ChannelName").split("_")[0:-1])
					attr = y.get("ChannelName").split("_")[-1]
				else:
					fluid, attr = y.get("ChannelName").split("_")

				if cmds.objExists(fluidShape):
					fluid = fluidShape

				index = y.tag.strip("channel")
				src = "%s.outCacheData[%s]" %(cache, index)
				dst = "%s.in%s" %( fluid, attr.title() )

				cmds.setAttr("%s.ch[%s]" %(cache, index), channelName, type = "string")
				_connectAttr(src, dst, force = 1)

				if fluid not in fluids:
					fluids.append(fluid)

		# More connections to hook up...
		for fluid in fluids:
			src = "time1.outTime"
			dst = "%s.currentTime" %fluid
			_connectAttr(src, dst, force = 1)

			src = "%s.inRange" %cache
			dst = "%s.playFromCache" %fluid
			_connectAttr(src, dst, force = 1)

		return cache
	else:
		return None

def _connectAttr(src, dst, **kwargs):
	"""
	Helper function used in the rebuild_cache_from_xml function
	"""
	src = str(src)
	dst = str(dst)

	if cmds.objExists(src) and cmds.objExists(dst):
		if not cmds.isConnected(src, dst):
			try:
				cmds.connectAttr(src, dst, **kwargs)
			except:
				mel.eval( r'warning "Failed to connect \"%s\" to \"%s\"...";' %(src, dst) )

def removeOceanSetup():
	"""
	Function to blow away anything related to an ocean setup.
	USE WITH CARE
	"""
	[cmds.delete(each) for each in cmds.ls('*_NurbsIntersect_geo')]
	[cmds.delete(eachExp) for eachExp in cmds.ls(type = 'expression') if 'oceanLock' in eachExp or 'IntersectionPlane' in eachExp]
	[cmds.delete(each) for each in cmds.ls(type = 'shadingEngine') if 'ocean' in each]
	[cmds.delete(each) for each in cmds.ls(type = 'fluidEmitter')]
	[cmds.delete(each) for each in cmds.ls(type = 'fluidTexture3D')]

	toDel = ['OCEAN_hrc', 'BOAT_OceanLocators_hrc', 'ocean_dispShader', 'ocean_animShader', 'ocean_srf', 'oceanPreviewPlane_prv',
			 'wakesOnOfMultiDiv', 'wakesOnOffMultiDiv', 'FLUID_EMITTERS_hrc', 'nPARTICLE_EMITTERS_hrc', 'Shot_FX_hrc', 'FX_CACHES_hrc']
	[cmds.delete(each) for each in toDel if cmds.objExists(each)]

	[cmds.lockNode(each, lock = True) for each in cmds.ls(type = 'core_renderpass')]
	mel.eval("MLdeleteUnused();")
	[cmds.lockNode(each, lock = False) for each in cmds.ls(type = 'core_renderpass')]

def _fetchAnimPublish(filteredPublish = '', sceneName = ''):
	"""
	Used to fetch most recent cache files
	"""
	import os

	if sceneName == '':
		sceneName = cmds.workspace(rootDirectory = True, q = True)
		sceneName = cmds.workspace(directory = True, q = True) if 'bubblebathbay' not in sceneName else sceneName

	if sceneName:
		if filteredPublish == 'Fetch Anim Publish':
			publishType = 'alembic_anim'
		elif filteredPublish == 'Fetch Camera Publish':
			publishType = 'cam'
		elif filteredPublish == 'Fetch Crease XML Publish':
			publishType = 'crease_xml'
		elif filteredPublish == 'Fetch FX Publish':
			publishType = 'fx'

		publish_dir = '%s/Anm/publish/%s' % (sceneName.split('/Light/work/maya/')[0], publishType) if publishType != 'fx' else '%s/FX/publish/%s' % (sceneName.split('/Light/work/maya/')[0], publishType)

		if os.path.exists(publish_dir):
			getAnimVersionFolders = ['%s/%s' % (publish_dir, each) for each in os.listdir(publish_dir) if os.path.isdir( '%s/%s' % (publish_dir, each) )]

			if getAnimVersionFolders:
				## now find the highest version folder number
				highestVersionFolder = max(getAnimVersionFolders)
				versionNumber = highestVersionFolder.split('/')[-1]
				getCacheFiles = os.listdir(highestVersionFolder)

				##################################################################################################################
				## ANIMATED CACHE LOADER
				if 'publish/alembic_anim' in highestVersionFolder:
					if filteredPublish == 'Fetch Anim Publish':
						hrc = 'ABC_ANIM_CACHES_hrc'

						## Build the group if it doesn't already exist
						proceedFetch = True
						if cmds.objExists(hrc):
							proceedFetch = cmds.confirmDialog(title = 'Fetch Anim Publish', message = '"%s" already exist! Press OK to re-fetch a latest publish.' % hrc, button = ['OK', 'Cancel'], defaultButton = 'OK', cancelButton = 'Cancel', dismissString = 'Cancel')
							proceedFetch = True if proceedFetch == 'OK' else False

						## Now process the caches
						if proceedFetch:
							if cmds.objExists(hrc):
								try:
									cmds.delete(hrc)
								except:
									cmds.warning('Failed to delete "%s"...' % hrc)
									proceedFetch = False

							if not cmds.objExists(hrc):
								try:
									_buildGroup(hrc, versionNumber)
								except:
									cmds.warning('Failed to create "%s"...' % hrc)
									proceedFetch = False

							if proceedFetch:
								for each in getCacheFiles:
									abcNode = '%s/%s' % (highestVersionFolder, each)
									cmds.AbcImport(abcNode, reparent  = "|%s" % hrc, setToStartFrame = True)
							else:
								cmds.warning('FAILED TO SETUP "%s", PLEASE CHECK WITH YOUR SUPERVISOR!!!' % hrc)
						else:
							cmds.warning('"%s" ALREADY SETUP SKIPPING...' % hrc)

				##################################################################################################################
				## OCEAN PUBLISH

				if 'publish/fx' in highestVersionFolder:
					if filteredPublish == 'Fetch FX Publish':
						hrc = 'FX_CACHES_hrc'

						## First clean up any existing caches and fluids
						removeOceanSetup()

						## Build the group if it doesn't already exist
						_buildGroup(hrc, versionNumber)

						if not cmds.objExists('fluids_hrc'):
							for each in getCacheFiles:
								if each.endswith('.mb'):
									fluidsNode = '%s/%s' % (highestVersionFolder, each)

									## Import the fluids_hrc group mb file now...
									try:
										cmds.file(fluidsNode, i = True)

										## Now assign the fluid presets again! Or the caches DO NOT WORK!!!
										## Apply foam preset
										pathToFoamPreset = 'I:/bubblebathbay/fx/presets/ocean/%s' % 'newOceanWakeFoamTexture.mel'
										mel.eval( 'applyPresetToNode "%s" "" "" "%s" 1;' %('oceanWakeFoamTextureShape', pathToFoamPreset) )

										## Apply wake preset
										pathToWakePreset = 'I:/bubblebathbay/fx/presets/ocean/%s' % 'newOceanWakeTexture.mel'
										mel.eval( 'applyPresetToNode "%s" "" "" "%s" 1;' %('oceanWakeTextureShape', pathToWakePreset) )
									except:
										cmds.warning('Failed to load FX file, file is corrupt.')

							## NOW ATTACH THE CACHE TO THE FLUID TEXTURES!
							## Changed export to single file altered this to accommodate the single file exported.
							for each in getCacheFiles:
								if each.endswith('.xml'):
									cachePath = '%s/%s' % (highestVersionFolder, each)
									rebuild_cache_from_xml(xmlPath = cachePath)
									# try:	rebuild_cache_from_xml(xmlPath = cachePath)
									# except:	cmds.warning('Failed to connect cache %s' % cachePath)
						else:
							cmds.warning('THERE ARE NO FLUID CONTAINERS PUBLISHED FROM FX FOR THIS SHOT! Please see your cg supervisor now...')

						################################################################################

						getFxVersionFolders = [x.replace('/FX/publish/', '/Anm/publish/') for x in getAnimVersionFolders]
						getFxVersionFolders = '%s/publish/fx' % getFxVersionFolders[0].split('/publish/fx/')[0]
						getFxVersionFolders = ['%s/%s' % (getFxVersionFolders, each) for each in os.listdir(getFxVersionFolders) if os.path.isdir('%s/%s' % (getFxVersionFolders, each))]
						highestVersionFolder_fx = max(getFxVersionFolders)
						versionNumber_fx = highestVersionFolder_fx.split('/')[-1]
						getCacheFiles_fx = os.listdir(highestVersionFolder_fx)

						## No maya ocean in scene? Build a new one...
						if not cmds.objExists('oceanShader1'):
							mel.eval("CreateOcean;")

							## Clean up the names
							## NOTE we are not renaming the actual OCEAN SHADER here because in Marks scripts we are reconnecting like so
							## cmds.disconnectAttr('oceanShader1.outColor', 'oceanShader1SG.surfaceShader')
							heightField = cmds.listRelatives(cmds.ls(selection = True)[0], parent = True, fullPath = True)[0]
							cmds.rename(heightField, 'oceanPreviewPlane_prv')
							cmds.rename('oceanPlane1', 'ocean_srf')
							cmds.rename('oceanPreviewPlane1', 'oceanPreviewPlane_heightF')
							cmds.parent('ocean_srf', hrc)
							cmds.parent('oceanPreviewPlane_prv', hrc)
							cmds.rename('oceanShader1', 'ocean_dispShader')
							cmds.rename('oceanShader1SG', '%sSG' % 'ocean_dispShader')

							## Lock translateY and rotation so that monkeys don't mess up with the ocean level
							toLock = ['translateY', 'rotateX', 'rotateY', 'rotateZ']
							for attr in toLock:
								cmds.setAttr('ocean_srf.%s' % attr, lock = True)

							## Hard set the render tesselation
							cmds.setAttr("ocean_srfShape.numberU", 200)
							cmds.setAttr("ocean_srfShape.numberV", 200)

							allOceans = cmds.ls(type= 'oceanShader')

							## now put the ocean in the right position
							if cmds.objExists('fluids_hrc'):
								_setOceanLocation()
							else:
								if cmds.objExists('ocean_srf') and cmds.objExists('oceanPreviewPlane_prv'):
									if not cmds.isConnected('oceanPreviewPlane_prv.translateX', 'ocean_srf.translateX'):
										cmds.connectAttr('oceanPreviewPlane_prv.translateX', 'ocean_srf.translateX', f = True)
									if not cmds.isConnected('oceanPreviewPlane_prv.translateZ', 'ocean_srf.translateZ'):
										cmds.connectAttr('oceanPreviewPlane_prv.translateZ', 'ocean_srf.translateZ', f = True)
								else:
									cmds.warning('MISSING ocean_srf or oceanPreviewPlane_prv node from scene...')

						for each in getCacheFiles_fx:
							## Now attach the preset to the maya ocean build a new one if it doesn't already exist
							if each.endswith('.mel'): ## the ocean shader preset saved out
								pathToPreset = '%s/%s' % (highestVersionFolder_fx, each)

								## Now apply the exported preset to each ocean in the scene. There really should only be ONE
								for eachOcean in allOceans:

									if cmds.objExists(hrc):
										if not cmds.objExists('%s.presetVersion' % hrc):
											cmds.addAttr(hrc, ln = 'presetVersion', dt = 'string')
											cmds.setAttr('%s.presetVersion' % hrc, versionNumber_fx, type = 'string')

									mel.eval( 'applyPresetToNode "%s" "" "" "%s" 1;' %(eachOcean, pathToPreset) )

						################################################################################

						_cleanupShit()

						## Straight up connection if no interactive is found.
						if cmds.objExists('ocean_dispShader') and cmds.objExists('oceanWakeTextureShape') and cmds.objExists('oceanWakeFoamTextureShape'):
							try:	cmds.connectAttr("oceanWakeTextureShape.outAlpha", "ocean_dispShader.waveHeightOffset", force = True)
							except:	pass
							try:	cmds.connectAttr("oceanWakeFoamTextureShape.outAlpha", "ocean_dispShader.foamOffset", force = True)
							except:	pass

						delAllImagePlanes()
						_setRenderGlobals()
						oceanAttach()
						createOceanMattes()

				##################################################################################################################
				## CREASE XML LOADER
				if 'publish/crease_xml' in highestVersionFolder:
					if filteredPublish == 'Fetch Crease XML Publish':
						hrc = 'ABC_ANIM_CACHES_hrc'

						if cmds.objExists('ABC_ANIM_CACHES_hrc'):
							for each in getCacheFiles:
								xmlPath = '%s/%s' % (highestVersionFolder, each)

							if os.path.isfile(xmlPath):

								import xml.etree.cElementTree as ET

								tree = ET.parse(xmlPath)
								root = tree.getroot()
								if root.tag == 'CreaseXML':

									for mesh in root.getchildren():
										mesh_name = mesh.attrib.get('name')
										mesh_name = '|'.join( [x.split(':')[-1] for x in mesh_name.split('|')] )
										mesh_name = '%s%s' % (hrc, mesh_name) if hrc else mesh_name

										if cmds.objExists(mesh_name):
											for edge in mesh.getchildren():
												vertexA     = int( edge.attrib.get('vertexA') )
												vertexB     = int( edge.attrib.get('vertexB') )
												creaseValue = edge.attrib.get('creaseValue')
												edgeID      = cmds.polyListComponentConversion('%s.vtx[%d]' % (mesh_name, vertexA), '%s.vtx[%d]' % (mesh_name, vertexB), fromVertex = 1, toEdge = 1, internal = 1)[0].split('.')[-1]

												if '-inf' not in creaseValue:
													cmds.polyCrease( '%s.%s' % (mesh_name, edgeID), value = float(creaseValue) )
										else:
											cmds.warning('%s doesn\'t exist, skipping...' % mesh_name)
								else:
									cmds.warning('Not a valid xml...')
							else:
								cmds.warning('Not a valid crease xml path...')

				##################################################################################################################
				## CAMERA LOADER
				if 'publish/cam' in highestVersionFolder:
					if filteredPublish == 'Fetch Camera Publish':
						hrc = 'BAKE_CAM_hrc'

						## Build the group if it doesn't already exist
						proceedFetch = True
						if cmds.objExists(hrc):
							proceedFetch = cmds.confirmDialog(title = 'Fetch Camera Publish', message = '"%s" already exist! Press OK to re-fetch a latest publish.' % hrc, button = ['OK', 'Cancel'], defaultButton = 'OK', cancelButton = 'Cancel', dismissString = 'Cancel')
							proceedFetch = True if proceedFetch == 'OK' else False

						## Now process the caches
						if proceedFetch:
							if cmds.objExists(hrc):
								try:
									cmds.delete(hrc)
								except:
									cmds.warning('Failed to delete "%s"...' % hrc)
									proceedFetch = False

							if proceedFetch:
								for each in getCacheFiles:
									camNode = '%s/%s' % (highestVersionFolder, each)
									cmds.file(camNode, i = True)

									for each in cmds.listRelatives(hrc, children = True):
										camShape = cmds.listRelatives(each, shapes = True, fullPath = True)[0]
										cmds.connectAttr('mia_physicalsky1.message', '%s.miEnvironmentShader' % camShape, force = True) if cmds.objExists('mia_physicalsky1') else None
										cmds.connectAttr('mentalcoreLens.message', '%s.miLensShader' % camShape, force = True) if cmds.objExists('mentalcoreLens') else None

										channels = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']
										for eachChan in channels:
											cmds.setAttr('%s.%s' %(each, eachChan), lock = True)
											
											if not cmds.objExists('%s.version' % hrc):
												cmds.addAttr(('%s' % hrc), ln = 'version', dt = 'string')
												cmds.setAttr('%s.version' % hrc, versionNumber, type = 'string')
							else:
								cmds.warning('FAILED TO SETUP "%s", PLEASE CHECK WITH YOUR SUPERVISOR!!!' % hrc)
						else:
							cmds.warning('"%s" ALREADY SETUP SKIPPING...' % hrc)
			else:
				if publish_dir.endswith('/FX/publish/fx'):
					setupNonFxOcean(hrc = 'FX_CACHES_hrc', oceanStateCachePath = publish_dir)

def setupNonFxOcean(hrc = 'FX_CACHES_hrc', oceanStateCachePath = ''):
	## First clean up any existing caches and fluids
	removeOceanSetup()

	## Build the group if it doesn't already exist
	_buildGroup(hrc, versionNumber = 'static')

	if not cmds.objExists('ocean_dispShader'):
		mel.eval("CreateOcean;")

		heightField = cmds.listRelatives(cmds.ls(selection = True)[0], parent = True, fullPath = True)[0]
		cmds.rename(heightField, 'oceanPreviewPlane_prv')
		cmds.rename('oceanPlane1', 'ocean_srf')
		cmds.rename('oceanPreviewPlane1', 'oceanPreviewPlane_heightF')
		cmds.parent('ocean_srf', hrc)
		cmds.parent('oceanPreviewPlane_prv', hrc)
		cmds.rename('oceanShader1', 'ocean_dispShader')
		cmds.rename('oceanShader1SG', '%sSG' % 'ocean_dispShader')

		## Lock translateY and rotation so that monkeys don't mess up with the ocean level
		toLock = ['translateY', 'rotateX', 'rotateY', 'rotateZ']
		for attr in toLock:
			cmds.setAttr('ocean_srf.%s' % attr, lock = True)

		## Hard set the render tesselation
		cmds.setAttr("ocean_srfShape.numberU", 100)
		cmds.setAttr("ocean_srfShape.numberV", 100)

		allOceans = cmds.ls(type= 'oceanShader')

		if cmds.objExists('ocean_srf') and cmds.objExists('oceanPreviewPlane_prv'):
			if not cmds.isConnected('oceanPreviewPlane_prv.translateX', 'ocean_srf.translateX'):
				cmds.connectAttr('oceanPreviewPlane_prv.translateX', 'ocean_srf.translateX', f = True)
			if not cmds.isConnected('oceanPreviewPlane_prv.translateZ', 'ocean_srf.translateZ'):
				cmds.connectAttr('oceanPreviewPlane_prv.translateZ', 'ocean_srf.translateZ', f = True)

	################################################################################

	oceanStateCachePath = oceanStateCachePath.replace('/FX/', '/Anm/')
	if os.path.exists(oceanStateCachePath):
		oceanStateCachePath = ['%s/%s' % (oceanStateCachePath, x) for x in os.listdir(oceanStateCachePath) if os.path.isdir('%s/%s' % (oceanStateCachePath, x))]
		highestVersionFolder_fx = max(oceanStateCachePath)
		versionNumber_fx = highestVersionFolder_fx.split('/')[-1]
		getCacheFiles_fx = os.listdir(highestVersionFolder_fx)

	for each in getCacheFiles_fx:
		## Now attach the preset to the maya ocean build a new one if it doesn't already exist
		if each.endswith('.mel'): ## the ocean shader preset saved out
			pathToPreset = '%s/%s' % (highestVersionFolder_fx, each)

			## Now apply the exported preset to each ocean in the scene. There really should only be ONE
			for eachOcean in allOceans:

				if cmds.objExists(hrc):
					if not cmds.objExists('%s.presetVersion' % hrc):
						cmds.addAttr(hrc, ln = 'presetVersion', dt = 'string')
						cmds.setAttr('%s.presetVersion' % hrc, versionNumber_fx, type = 'string')

				mel.eval( 'applyPresetToNode "%s" "" "" "%s" 1;' %(eachOcean, pathToPreset) )

	################################################################################

	_cleanupShit()

	## Straight up connection if no interactive is found.
	if cmds.objExists('ocean_dispShader') and cmds.objExists('oceanWakeTextureShape') and cmds.objExists('oceanWakeFoamTextureShape'):
		try:	cmds.connectAttr("oceanWakeTextureShape.outAlpha", "ocean_dispShader.waveHeightOffset", force = True)
		except:	pass
		try:	cmds.connectAttr("oceanWakeFoamTextureShape.outAlpha", "ocean_dispShader.foamOffset", force = True)
		except:	pass

	delAllImagePlanes()
	_setRenderGlobals()
	oceanAttach()
	createOceanMattes()

	################################################################################
	## Place ocean to center of shotCam's position

	shotCam = [cam for cam in cmds.listCameras(perspective = True) if cam != 'persp' if cmds.objExists('%s.type' % cam) if cmds.getAttr('%s.type' % cam) == 'shotCam']
	shotCam = shotCam[0] if shotCam else None
	if shotCam:
		cmds.modelPanel('modelPanel4', e = True, camera = shotCam)
		mel.eval('setFocus("modelPanel4")')
		
		position = cmds.camera(shotCam, q = True, worldCenterOfInterest = True)
		
		## From maya.api get camera's center vector position
		import maya.OpenMaya as om
		vec = om.MVector(position[0], 0, position[2])
		
		if cmds.objExists('oceanPreviewPlane_prv'):
			cmds.setAttr('oceanPreviewPlane_prv.translateX', vec.x)
			cmds.setAttr('oceanPreviewPlane_prv.translateZ', vec.z)

def _setRenderGlobals(width = 1280, height = 720, animation = False):
	from mentalcore import mapi

	cmds.editRenderLayerGlobals(currentRenderLayer = 'defaultRenderLayer')

	cmds.currentUnit(time='pal')
	cmds.currentUnit(linear='cm')

	mel.eval('setAttr defaultResolution.width %s' % width)
	mel.eval('setAttr defaultResolution.height %s' % height)
	mel.eval('setAttr defaultResolution.deviceAspectRatio 1.777')
	mel.eval('setAttr defaultResolution.pixelAspect 1')

	## load mentalray
	if not cmds.pluginInfo( 'Mayatomr', query=True, loaded = True ):
		cmds.loadPlugin('Mayatomr')

	mel.eval("miCreateDefaultNodes") if not cmds.objExists("miDefaultOptions") else None
	cmds.setAttr('defaultRenderGlobals.currentRenderer','mentalRay', type = 'string')
	cmds.setAttr('miDefaultOptions.finalGather', 1)

	# Default Render Globals
	# /////////////////////
	cmds.setAttr('defaultRenderGlobals.imageFormat', 51)
	cmds.setAttr('defaultRenderGlobals.imfkey','exr', type = 'string')
	cmds.setAttr('defaultRenderGlobals.animation', 1)
	cmds.setAttr('defaultRenderGlobals.extensionPadding', 3)
	cmds.getAttr('defaultRenderGlobals.extensionPadding')
	cmds.setAttr('defaultRenderGlobals.periodInExt', 1)
	cmds.setAttr('defaultRenderGlobals.outFormatControl', 0)
	cmds.setAttr('defaultRenderGlobals.putFrameBeforeExt', 1)
	cmds.setAttr('defaultRenderGlobals.enableDefaultLight', 0)
	cmds.setAttr('defaultResolution.aspectLock', 0)

	# MentalRay Globals
	# /////////////////////
	cmds.setAttr('mentalrayGlobals.imageCompression', 4)
	cmds.setAttr('mentalrayGlobals.exportPostEffects', 0)
	cmds.setAttr('mentalrayGlobals.accelerationMethod', 4)
	cmds.setAttr('mentalrayGlobals.exportVerbosity', 5)
	# miDefault Frame Buffer
	cmds.setAttr('miDefaultFramebuffer.datatype', 16)
	# miDefault sampling defaults
	cmds.setAttr('miDefaultOptions.filterWidth', 0.6666666667)
	cmds.setAttr('miDefaultOptions.filterHeight', 0.6666666667)
	cmds.setAttr('miDefaultOptions.filter', 2)
	cmds.setAttr('miDefaultOptions.sampleLock', 0)
	# enable raytracing, disable scanline
	cmds.setAttr('miDefaultOptions.scanline', 0)
	try:
		cmds.optionMenuGrp('miSampleModeCtrl', edit = True,  select = 2)
	except:
		pass
	cmds.setAttr('miDefaultOptions.minSamples', -2)
	cmds.setAttr('miDefaultOptions.maxSamples', 0)

	# set sampling quality for RGB channel to eliminate noise
	# costs a bit extra time because it will sample more in the
	# red / green channel but will be faster for blue.
	# using unified sampling
	cmds.setAttr('miDefaultOptions.contrastR', 0.04)
	cmds.setAttr('miDefaultOptions.contrastG', 0.03)
	cmds.setAttr('miDefaultOptions.contrastB', 0.06)
	cmds.setAttr('miDefaultOptions.contrastA', 0.03)

	cmds.setAttr('miDefaultOptions.maxReflectionRays', 3)
	cmds.setAttr('miDefaultOptions.maxRefractionRays', 3)
	cmds.setAttr('miDefaultOptions.maxRayDepth', 5)
	cmds.setAttr('miDefaultOptions.maxShadowRayDepth', 5)

	cmds.setAttr('miDefaultOptions.finalGatherRays', 20)
	cmds.setAttr('miDefaultOptions.finalGatherPresampleDensity', 0.2)
	cmds.setAttr('miDefaultOptions.finalGatherTraceDiffuse', 0)
	cmds.setAttr('miDefaultOptions.finalGatherPoints', 50)

	cmds.setAttr('miDefaultOptions.displacePresample', 0)

	playStart  = cmds.playbackOptions(query = True, minTime= True)
	playFinish = cmds.playbackOptions(query = True, maxTime= True)
	cmds.setAttr('defaultRenderGlobals.startFrame', playStart)
	cmds.setAttr('defaultRenderGlobals.endFrame', playFinish)

	# MentalCore
	# /////////////////////
	if not animation:
		try:
			mapi.enable(True)
			cmds.setAttr('mentalcoreGlobals.en_colour_management',1)
			cmds.setAttr('mentalcoreGlobals.contrast_all_buffers', 1)
			cmds.setAttr('mentalcoreGlobals.output_mode', 0)
			cmds.setAttr('mentalcoreGlobals.unified_sampling', 1)
			cmds.setAttr('mentalcoreGlobals.samples_min', 1)
			cmds.setAttr('mentalcoreGlobals.samples_max', 80)
			cmds.setAttr('mentalcoreGlobals.samples_quality', 0.8)
			cmds.setAttr('mentalcoreGlobals.samples_error_cutoff', 0.02)

			cmds.setAttr('mentalcoreGlobals.en_envl', 1)
			cmds.setAttr('mentalcoreGlobals.envl_scale', 0.5)
			cmds.setAttr('mentalcoreGlobals.envl_blur_res', 0)
			cmds.setAttr('mentalcoreGlobals.envl_blur', 0)
			cmds.setAttr('mentalcoreGlobals.envl_en_flood_colour', 1)
			cmds.setAttr('mentalcoreGlobals.envl_flood_colour', 1, 1, 1, 1, type = 'double3')
			cmds.setAttr('mentalcoreGlobals.en_ao', 1)
			cmds.setAttr('mentalcoreGlobals.ao_samples', 24)
			cmds.setAttr('mentalcoreGlobals.ao_spread', 60)
			cmds.setAttr('mentalcoreGlobals.ao_near_clip', 1)
			cmds.setAttr('mentalcoreGlobals.ao_far_clip', 10)
			cmds.setAttr('mentalcoreGlobals.ao_opacity', 0)
			cmds.setAttr('mentalcoreGlobals.ao_vis_indirect', 0)
			cmds.setAttr('mentalcoreGlobals.ao_vis_refl', 0)
			cmds.setAttr('mentalcoreGlobals.ao_vis_refr', 1)
			cmds.setAttr('mentalcoreGlobals.ao_vis_trans', 1)
		except:
			cmds.warning('NO MENTAL CORE LOADED!!!')
			pass

		# Default Resolution
		cmds.setAttr('defaultResolution.width', 1280)
		cmds.setAttr('defaultResolution.height', 720)
		cmds.setAttr('defaultResolution.pixelAspect', 1)
		cmds.setAttr('defaultResolution.deviceAspectRatio', 1.7778)

def delAllImagePlanes():
	"""
	Func to just delete all image planes for lighting
	"""
	getAllPlanes = cmds.ls(type = 'imagePlane')
	for each in getAllPlanes:
		try:	cmds.delete( cmds.listRelatives(each, parent =True) )
		except:	pass

def _cleanupShit():
	try:
		cmds.delete(cmds.ls('rig_hrc'))
	except:
		pass
	try:
		cmds.delete(cmds.ls('parts_hrc'))
	except:
		pass
	try:
		cmds.delete(cmds.ls('collisionNurbsHulls'))
	except:
		pass

	for each in cmds.ls(type = 'transform'):
		if 'Constraint' in each:
			cmds.delete(each)

	### CLEAN UP THE OCEAN SETUP
	if cmds.objExists('OCEAN_hrc') and cmds.objExists('fluids_hrc'):
		try:
			cmds.parent('fluids_hrc', 'FX_CACHES_hrc')
		except RuntimeError:
			pass
		try:
			cmds.delete('OCEAN_hrc')
		except:
			pass
	elif cmds.objExists('fluids_hrc'):
		try:
			cmds.parent('fluids_hrc', 'FX_CACHES_hrc')
		except RuntimeError:
			pass
	else:
		pass

	### CLEAN UP THE FX IMPORT ETC
	if cmds.objExists('OCEAN_hrc') and cmds.objExists('fluids_hrc'):
		try:
			cmds.parent('fluids_hrc', 'FX_CACHES_hrc')
		except:
			pass
		try:
			cmds.delete('OCEAN_hrc')
		except:
			pass

	elif cmds.objExists('fluids_hrc'):
		try:
			cmds.parent('fluids_hrc', 'FX_CACHES_hrc')
		except:
			pass

	else:
		pass

	## Cleanup old camera grp
	if cmds.objExists('SHOTCAM_hrc'):
		cmds.delete('SHOTCAM_hrc')

def _setOceanLocation():
	"""
	Exposing a tool to help push the ocean into the right location based off the FX published fluid containers fluids_hrc
	"""
	## If the fluids_hrc exists
	if cmds.objExists('fluids_hrc'):
		if cmds.objExists('ocean_srf'):
			cmds.connectAttr('fluids_hrc.translateX', 'ocean_srf.translateX', f = True)
			cmds.connectAttr('fluids_hrc.translateZ', 'ocean_srf.translateZ', f = True)
		else:
			cmds.warning('MISSING ocean_srf node from scene....')

		if cmds.objExists('oceanPreviewPlane_prv'):
			cmds.connectAttr('fluids_hrc.translateX', 'oceanPreviewPlane_prv.translateX', f = True)
			cmds.connectAttr('fluids_hrc.translateZ', 'oceanPreviewPlane_prv.translateZ', f = True)
		else:
			cmds.warning('MISSING oceanPreviewPlane_prv node from scene....')
	else:
		cmds.warning('NO fluids_hrc FOUND! Can not move the ocean into final position. PLEASE CHECK FX PUBLISH NOW!')

def _buildGroup(groupName, versionNumber):
	## Build the group if it doesn't already exist
	if not cmds.objExists(groupName):
		cmds.group(n = groupName, em = True)

		## Add the version attr if it doesn't already exits
		if not cmds.objExists('%s.version' % groupName):
			cmds.addAttr(groupName, ln = 'version', dt = 'string')
			cmds.setAttr('%s.version' % groupName, versionNumber, type = 'string')

		return False
	else:
		return True

def oceanAttach():
	mayaOceanPresetPath = 'I:/bubblebathbay/fx/presets/Lighting/oceanWaterRenderSHD.ma'
	MC_WATERSHD_NAME = 'oceanWater_cMia_shd'
	OCEANDISPSHADER = 'ocean_dispShader'
	FOAM_FLUID_SHAPENODE = 'oceanWakeFoamTextureShape'
	
	try:
		## Now try to import marks/deepeshes final shader from the ma file.
		if not cmds.objExists(MC_WATERSHD_NAME):
			cmds.file(mayaOceanPresetPath, i = True, type = 'mayaAscii', applyTo = ':', options = 'v=0')          

		## Now fix the connections
		## Out Color
		src = '%s.outColor' % OCEANDISPSHADER
		dst = '%sSG.surfaceShader' % OCEANDISPSHADER
		if cmds.objExists(src) and cmds.objExists(dst):
			if cmds.isConnected(src, dst):
				cmds.disconnectAttr(src, dst)

		## Displacement
		src = '%s.displacement' % OCEANDISPSHADER
		dst = '%sSG.displacementShader' % OCEANDISPSHADER
		if cmds.objExists(src) and cmds.objExists(dst):
			if not cmds.isConnected(src, dst):
				cmds.connectAttr(src, dst)

		## Out Value
		src = '%s.outValue' % MC_WATERSHD_NAME
		dst = '%sSG.miMaterialShader' % OCEANDISPSHADER
		if cmds.objExists(src) and cmds.objExists(dst):
			if not cmds.isConnected(src, dst):
				cmds.connectAttr(src, dst)

		## Out Color
		src = '%s.outColor' % OCEANDISPSHADER
		dst = 'OceanFoam.outColor'
		if cmds.objExists(src) and cmds.objExists(dst):
			if not cmds.isConnected(src, dst):
				cmds.connectAttr(src, dst, f = True)

		## Out Alpha
		src = '%s.outAlpha' % FOAM_FLUID_SHAPENODE
		dst = 'oceanWater_incd_cTxBld.layer[1].opacity'
		if cmds.objExists(src) and cmds.objExists(dst):
			if not cmds.isConnected(src, dst):
				cmds.connectAttr(src, dst, f = True)

		## Out Alpha 2
		src = '%s.outAlpha' % FOAM_FLUID_SHAPENODE
		dst = 'oceanWater_incd_cTxBld.layer[2].opacity'
		if cmds.objExists(src) and cmds.objExists(dst):
			if not cmds.isConnected(src, dst):
				cmds.connectAttr(src, dst, f = True)

		## Now force the final shader to the oceanNURBS plane
		if cmds.objExists('ocean_srf'):
			if cmds.objExists('ocean_dispShaderSG'):
				cmds.sets('ocean_srf', edit = True, forceElement = 'ocean_dispShaderSG')
			else:
				cmds.warning('%s doesn\'t exist...' % 'ocean_dispShaderSG')
		else:
			cmds.warning('%s doesn\'t exist, please rebuild ocean first?' % 'ocean_srf')

		## More from deepesh
		cmds.setAttr("%s.waterColor" % OCEANDISPSHADER, 0,0,0, type = 'double3')
		cmds.setAttr("%s.environment[2].environment_Color" % OCEANDISPSHADER, 0,0,0, type = 'double3')
		cmds.setAttr("%s.specularColor" % OCEANDISPSHADER, 0,0,0, type = 'double3')
		cmds.setAttr("%s.specularity" % OCEANDISPSHADER, 0)
		cmds.setAttr("%s.eccentricity" % OCEANDISPSHADER, 0)
		cmds.setAttr("%s.reflectivity" % OCEANDISPSHADER, 0)

		mel.eval("removeMultiInstance -break true %s.environment[1];" % OCEANDISPSHADER)
		mel.eval("removeMultiInstance -break true %s.environment[0];" % OCEANDISPSHADER)
	except RuntimeError:
		cmds.warning('Ocean Attach FAILED!')

def importPublishes():
	_fetchAnimPublish(filteredPublish = 'Fetch Anim Publish') if cmds.checkBox('bbbAnimPublishCB', value = True, query = True) else None
	_fetchAnimPublish(filteredPublish = 'Fetch Camera Publish') if cmds.checkBox('bbbCamPublishCB', value = True, query = True) else None
	_fetchAnimPublish(filteredPublish = 'Fetch Crease XML Publish') if cmds.checkBox('bbbCreaseXMLPublishCB', value = True, query = True) else None
	_fetchAnimPublish(filteredPublish = 'Fetch FX Publish') if cmds.checkBox('bbbFXPublishCB', value = True, query = True) else None

def createAll(XMLPath = '', parentGrp = '', Namespace = '', Root = 'MaterialNodes', selected = False, selectedOrigHrcName = ''):
	import xml.etree.ElementTree as ET

	# If the namespace doesn't exist, the objects wont get named correctly
	# create the namespace
	if Namespace != "" and Namespace != ":":
		if not cmds.namespace( exists= Namespace[:-1] ):
			cmds.namespace( add = Namespace[:-1])
	if selected:
		prefix = '%s_' % selectedOrigHrcName
	else:
		prefix = ''
	
	typeShader      = cmds.listNodeTypes( 'shader' ) or []
	typeTexture     = cmds.listNodeTypes( 'texture' )  or []
	typeUtility     = cmds.listNodeTypes( 'utility' )  or []
	typeMRTexture   = cmds.listNodeTypes( 'rendernode/mentalray/texture' )  or []
	typeMRDisp      = cmds.listNodeTypes( 'rendernode/mentalray/displace' )  or []
	typeMREnv       = cmds.listNodeTypes( 'rendernode/mentalray/environment' )  or []
	typeMRLightMaps = cmds.listNodeTypes( 'rendernode/mentalray/lightmap' )  or []
	typeMRMisc      = cmds.listNodeTypes( 'rendernode/mentalray/misc' )  or []
	typeMRConv      = cmds.listNodeTypes( 'rendernode/mentalray/conversion') or []
	typeMRInternal  = cmds.listNodeTypes( 'rendernode/mentalray/internal')  or []

	# get the root of the XMLPath argument
	root = ET.parse(XMLPath).getroot()

	# Create an iterator based on the the root argument
	shaderIterator = root.getiterator(Root)

	# Progress bar
	progress_33 = len( [levelOne for levelOne in shaderIterator if levelOne.getchildren() for levelTwo in levelOne if levelTwo.tag == 'Nodes' for levelThree in levelTwo.getchildren()] )
	progress_66 = len( [levelOne for levelOne in shaderIterator if levelOne.getchildren() for levelTwo in levelOne if levelTwo.tag == 'ShadingEngine' for levelThree in levelTwo.getchildren()] )
	progress_100 = len( [levelOne for levelOne in shaderIterator if levelOne.getchildren() for levelTwo in levelOne if levelTwo.tag == 'Attributes' for levelThree in levelTwo.getchildren()] )
	gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
	cmds.progressBar(gMainProgressBar, e = True, beginProgress = True, isInterruptable = True, status = 'Processing %s ...' % XMLPath, maxValue = (progress_33 + progress_66 + progress_100) * 2)
					
	# Iterate on shader level
	for levelOne in shaderIterator:
		# Iterate on parent tag level
		if levelOne.getchildren():
			for levelTwo in levelOne:
				if levelTwo.tag == 'Nodes':
					for levelThree in levelTwo.getchildren():

						if cmds.progressBar(gMainProgressBar, q = True, isCancelled = True,):
							break
						else:
							cmds.progressBar(gMainProgressBar, e = True, status = 'Processing %s ...' % XMLPath, step = 1)

						node_name = levelThree.tag
						if '_cCc_' in node_name:
							node_name = node_name.replace('_cCc_', ':')
						node_name = '%s%s%s' % (Namespace, prefix, node_name)
						node_type = levelThree.attrib['value']
						# Create all node types and sort them into correct hypershade tabs
						if node_type in typeShader or node_type in typeMRInternal:
							if not doesAssetAlreadyExistInScene(node_name):
								cmds.shadingNode(node_type, asShader = True , name = node_name)
						if node_type in typeTexture or node_type in typeMRInternal:
							if not doesAssetAlreadyExistInScene(node_name):
								cmds.shadingNode(node_type, asTexture = True , name = node_name)
						if node_type in typeUtility or node_type in typeMRTexture or node_type in typeMREnv or node_type in typeMRLightMaps or node_type in typeMRMisc or node_type in typeMRConv or node_type in typeMRDisp or node_type in typeMRInternal:
							if not doesAssetAlreadyExistInScene(node_name):
								cmds.shadingNode(node_type, asUtility = True , name = node_name)

				if levelTwo.tag == 'ShadingEngine':
					for levelThree in levelTwo.getchildren():

						if cmds.progressBar(gMainProgressBar, q = True, isCancelled = True):
							break
						else:
							cmds.progressBar(gMainProgressBar, e = True, status = 'Processing %s ...' % XMLPath, step = 1)

						node_name  = '%s%s' % (prefix, levelThree.tag)
						if '_cCc_' in node_name:
							node_name = node_name.replace('_cCc_', ':')
						node_type  = levelThree.attrib['value']
						node_split = node_type.split(', ')
						node_name  = node_split[0]
						node_name = '%s%s%s' % (Namespace, prefix, node_name)
						node_type  = node_split[1]

						if node_type == 'shadingEngine':
							if not doesAssetAlreadyExistInScene(node_name):
								cmds.sets(renderable = True, noSurfaceShader = True, empty = True, name = node_name)
	
				if levelTwo.tag == 'Attributes':
					for attributes in levelTwo.getchildren():

						if cmds.progressBar(gMainProgressBar, q = True, isCancelled = True):
							break
						else:
							cmds.progressBar(gMainProgressBar, e = True, step = 1)

						attrNode = attributes.tag
						attrNode = '%s%s%s' % (Namespace, prefix, attrNode)
						if '_aAa_' in attrNode:
							attrNode = attrNode.replace('_aAa_', '[')
							attrNode = attrNode.replace('_zZz_', ']')
						if '_cCc_' in attrNode:
							attrNode = attrNode.replace('_cCc_', ':')

						attrValue =  attributes.attrib['value']
						if not attrValue.startswith('[('):
							try:	cmds.setAttr(attrNode, float(attrValue), lock = False)
							except:	pass
							try:	cmds.setAttr(attrNode, str(attrValue), type = 'string', lock = False)
							except:	pass
							try:	cmds.setAttr(attrNode, str(attrValue), type = 'double3', lock = False)
							except:	pass
						else:
							evalList = eval(attrValue)
							evalList = evalList[0]
							if len(evalList) == 2:
								try:	cmds.setAttr(attrNode, evalList[0], evalList[1], type = 'double2', lock = False)
								except:	pass

							if len(evalList) == 3:
								try:	cmds.setAttr(attrNode, evalList[0], evalList[1], evalList[2], type = 'double3', lock = False)
								except:	pass
	
	## Progress bar end!
	return gMainProgressBar

def processSHDTemplate(assetDict = {}, selected = False):
	myFinalAssetDict = {}
	
	## Now fetch all the SRF template paths from shotgun
	rootDir = 'I:/bubblebathbay/assets'
	assetDir = ['%s/%s' % (rootDir, dir) for dir in os.listdir(rootDir) if os.path.isdir( '%s/%s' % (rootDir, dir) )]
	assetDir = ['%s/%s' % (x, y) for x in assetDir for y in os.listdir(x) if os.path.isdir( '%s/%s' % (x, y) )]
	assetDir = ['%s/SRF/publish/xml' % each for each in assetDir if os.path.exists('%s/SRF/publish/xml' % each)]
	getTemplatePaths = ['%s/%s' % (dir, max(os.listdir(dir))) for dir in assetDir if os.listdir(dir)]
	
	## Now look for each assets template path:        
	for key, var in assetDict.items():
		versions = []
		
		for eachPath in getTemplatePaths:
			splitPathToAssetName = eachPath.split('/')[4]

			if key.lower() == splitPathToAssetName.lower():
				versions.append(eachPath)

		## Now if versions has stuff in it..
		if versions:
			if selected:
				myFinalAssetDict[key] = [max(versions), var[0], var[1]]
			else:
				myFinalAssetDict[key] = [max(versions), var]

	allNodes = {}
	for key, var in myFinalAssetDict.items():
		XMLPath = var[0].replace(os.path.sep, "/")
		root = ET.parse(XMLPath).getroot()

		nodes = [each for each in root.getchildren()[0] if each.tag == 'Nodes'][0]
		shadingEngines = [each for each in root.getchildren()[0] if each.tag == 'ShadingEngine'][0]

		for each in nodes.getchildren():
			allNodes.setdefault(each.tag, [])
			allNodes[each.tag].append(key)

		for each in shadingEngines.getchildren():
			sgName = each.attrib['value'].split(',')[0]
			allNodes.setdefault(sgName, [])
			allNodes[sgName].append(key)

	for key, var in myFinalAssetDict.items():
		if os.path.isfile(var[0].replace(os.path.sep, "/")):

			if selected:
				gMainProgressBar = createAll(XMLPath = var[0].replace(os.path.sep, "/"), parentGrp = var[1], Namespace = '', Root = 'MaterialNodes', selected = True, selectedOrigHrcName = var[2])
				versionNumber = var[0].replace(os.path.sep, "/").split('.')[-2].split('v')[-1]
				connectAll(XMLPath = var[0].replace(os.path.sep, "/"), parentGrp= var[1], Namespace = '', Root = 'MaterialNodes', selected = True, selectedOrigHrcName = var[2], xmlVersionNumber = versionNumber, gMainProgressBar = gMainProgressBar)
			else:
				gMainProgressBar = createAll(XMLPath = var[0].replace(os.path.sep, "/"), parentGrp = var[1], Namespace = '', Root = 'MaterialNodes')
				versionNumber = var[0].replace(os.path.sep, "/").split('.')[-2].split('v')[-1]
				connectAll(XMLPath = var[0].replace(os.path.sep, "/"), parentGrp= var[1], Namespace = '', Root = 'MaterialNodes', xmlVersionNumber = versionNumber, gMainProgressBar = gMainProgressBar)

def fetchAllShaders():        
	"""
	Function to handle fetching the shaders
	"""
	from mentalcore import mapi

	## Now get a list of assets in the scene
	assetDict = {}
	dupAssets = {}
	for parentGrp in cmds.ls(assemblies = True, long = True):
		if cmds.ls(parentGrp, dag = True, type = "mesh"):
			for each in cmds.listRelatives(parentGrp, children = True):
				## Check for duplicate or base assets
				if not cmds.objExists('%s.dupAsset' % each):
					assetDict[each.split('_hrc')[0]] = parentGrp
				else: # handle the duplicate naming
					origAssetName = each.split('_hrc')[0]
					dupAssets[each] = [origAssetName, parentGrp]
							  
	## Now process SHD XML
	processSHDTemplate(assetDict = assetDict, selected = False)
	finalBuildStuff()

def fetchShadersForSelected():
	"""
	Function to handle fetching the shaders for selected _hrc groups only.
	"""  
	from mentalcore import mapi

	## ASSSIGN DEFAULT LAMBERT AND CLEAN THE HYERPSHADE!
	for each in cmds.ls(sl = True):
		try:	cmds.sets(each, e = True , forceElement = 'initialShadingGroup')
		except:	cmds.warning('FAILED to set initial Shading group for %s' % each)

	[cmds.lockNode(cp, lock = True) for cp in cmds.ls(type = 'core_renderpass')] ## Lock all the core_renderpasses before deleting unused to preserve...
	mel.eval("MLdeleteUnused();")

	## Now get a list of assets in the scene
	assetDict = {}
	for grp in cmds.ls(sl = True):
		if cmds.ls(grp, dag = True, type = "mesh"):
			getParent = cmds.listRelatives(grp, parent = True)
			if getParent:
				assetDict[grp.split('_hrc')[0]] = [cmds.listRelatives(grp, parent = True)[0], grp]
			else:
				assetDict[grp.split('_hrc')[0]] = ['', grp]

	## Now process XML
	processSHDTemplate(assetDict = assetDict, selected = True)
	finalBuildStuff()

def finalBuildStuff():
	"""
	Generic build stuff both selected and all rebuilds should do
	"""
	replaceBump2WithCoreNormalmap()
	mel.eval("MLdeleteUnused();")
	[cmds.lockNode(cp, lock = False) for cp in cmds.ls(type = 'core_renderpass')] ## Unlock all the core_renderpasses like original after deleting unused to avoid future messed up...

def replaceBump2WithCoreNormalmap():
	for eachBump in cmds.ls(type = 'bump2d'):
		tangentSpaceNormals = cmds.getAttr('%s.bumpInterp' % eachBump)
		if tangentSpaceNormals == 1:
			fileIn = cmds.listConnections(eachBump, source = True, type = 'file') or cmds.listConnections(eachBump, source = True, type = 'mentalrayTexture')
			core_material = cmds.listConnections(eachBump, destination = True, type = 'core_material')
			if fileIn and core_material:
				cmds.delete(eachBump)
				core_normalMap = cmds.createNode('core_normalmap', name = eachBump)
				cmds.connectAttr('%s.outColor' % fileIn[0], '%s.normal_map' % core_normalMap, f = True)
				cmds.connectAttr('%s.outAlpha' % fileIn[0], '%s.normal_mapA' % core_normalMap, f = True)
				for eachShader in core_material:
					cmds.connectAttr('%s.message' % core_normalMap, '%s.normal_map' % eachShader, f = True)

def doesAssetAlreadyExistInScene(assetName):
	assetExists = False
	if cmds.ls(assetName) != []:
		assetExists = True
	
	return assetExists

def connectAll(XMLPath = '', parentGrp = '', Namespace = '', Root = 'MaterialNodes', selected = False, selectedOrigHrcName = '', xmlVersionNumber = '', gMainProgressBar = ''):
	# If the namespace doesn't exist, the objects wont get named correctly
	# create the namespace
	if Namespace != "" and Namespace != ":":
		if not cmds.namespace( exists= Namespace[:-1] ):
			cmds.namespace( add = Namespace[:-1])
	if selected:
		prefix = '%s_' % selectedOrigHrcName
	else:
		prefix = ''

	# get the root of the XMLPath argument
	root = ET.parse(XMLPath).getroot()

	# Create an iterator based on the the root argument
	shaderIterator = root.getiterator(Root)

	# Progress bar
	progress_50 = len( [levelOne for levelOne in shaderIterator if levelOne.getchildren() for levelTwo in levelOne if levelTwo.tag == 'Connections' for connections in levelTwo.getchildren()] )
	progress_100 = len( [levelOne for levelOne in shaderIterator if levelOne.getchildren() for levelTwo in levelOne if levelTwo.tag == 'ShadingEngine' for sg in levelTwo.getchildren()] )
	cmds.progressBar(gMainProgressBar, e = True, status = 'Processing %s ...' % XMLPath, maxValue = (progress_50 + progress_100), progress = (progress_50 + progress_100) / 2)
	
	# Iterate on shader level
	for levelOne in shaderIterator:
		# Iterate on parent tag level
		if levelOne.getchildren():
			for levelTwo in levelOne:
				# For every node, set each attribute
				if levelTwo.tag == 'Connections':

					for connections in levelTwo.getchildren():

						if cmds.progressBar(gMainProgressBar, q = True, isCancelled = True):
							break
						else:
							cmds.progressBar(gMainProgressBar, e = True, status = 'Processing %s ...' % XMLPath, step = 1)

						direction = connections.tag
						connData = connections.attrib['value'].split(', ')
						conn_srce = '%s%s%s' % (Namespace, prefix, connData[0])
						conn_dest = '%s%s%s' % (Namespace, prefix, connData[1])

						if not cmds.objExists(conn_srce):
							conn_srce = '%s%s' % (Namespace, connData[0])
							if cmds.objExists(conn_srce):
								try:
									if not cmds.objectType(conn_srce) == 'mesh':
										conn_srce = '%s%s%s' % (Namespace, prefix, connData[0])
								except RuntimeError:
									pass

						if not cmds.objExists(conn_dest):
							conn_dest = '%s%s' % (Namespace, connData[1])
							if cmds.objExists(conn_dest):
								if not cmds.objectType(conn_dest) == 'mesh':
									conn_dest = '%s%s%s' % (Namespace, prefix, connData[1])

						if direction == 'DownStream':
							try:
								if not cmds.isConnected(conn_srce, conn_dest):
									cmds.connectAttr(conn_srce, conn_dest, force = True)
							except:
								cmds.warning('Failed to connect %s to %s, skipping...' % (conn_srce, conn_dest))
						else:
							try:
								if not cmds.isConnected(conn_dest, conn_srce):
									cmds.connectAttr(conn_dest, conn_srce, force = True)
							except:
								cmds.warning('Failed to connect %s to %s, skipping...' % (conn_dest, conn_srce))
				
				## NOW CONNECT THE SHADING ENGINES TO THE GEO
				if levelTwo.tag == 'ShadingEngine':

					for sg in levelTwo.getchildren():

						if cmds.progressBar(gMainProgressBar, q = True, isCancelled = True):
							break
						else:
							cmds.progressBar(gMainProgressBar, e = True, status = 'Processing %s ...' % XMLPath, step = 1)

						nodeData  = sg.attrib['value'].split(', ')
						node_name = '%s%s%s' % (Namespace, prefix, nodeData[0])
						node_type = nodeData[1]
						
						if sg.getchildren():

							for geo in sg.getchildren():
								if geo.tag == 'Geo':
									origName = '|%s%s' % (parentGrp, geo.attrib['value'])

									if origName.endswith(']'):
										origNameInScene = origName.split('|')[-1]
									else:
										origNameInScene = origName.split('|')[-2]

									## Now get the actual freaking hrc group that was originally publish this is for the rebuild from a lighting publish as opposed to a surfVar assignment.
									if parentGrp:
										baseHRCGrp = origName.split('|')[3]
									else:
										if 'CACHES' not in origName:
											baseHRCGrp = origName.split('|')[2] 
										else:
											baseHRCGrp = origName.split('|')[3] 
									
									## if it exists in the scene, assign the shader, else we have to look for all the LIB objects in the scene via their metaTags and process these accordingly.
									## Processing multiple instances of the same geo!
									if cmds.objExists(origNameInScene):
										## Okay so we have geo in the scene, but what about duplicates for reuse assets.... such as multiple bouys from the same base assets....
										## First we have to list all the assets found in the scene..
										getPathToGeoInScene = cmds.ls(origNameInScene, l = True) ## list the objects in the scene with the transform name from the SRF publish, and make sure these return their full path
 
										if getPathToGeoInScene: ## Check there are any objects in the scene with the original name!
											for eachGeo in getPathToGeoInScene:## go through each of the transforms
												if selected: ## only do it if
													matchFound = [each for each in eachGeo.split('|') if each == selectedOrigHrcName] or False
													if matchFound: ## checks to see if the actual selected top level _hrc group is in the long name
														try:
															cmds.sets(eachGeo, edit=True, forceElement = node_name)
															
															if xmlVersionNumber:
																_addVersionTag(matchFound[0], xmlVersionNumber)
														except ValueError:
															pass                                                   
												else:
													matchFound = [each for each in eachGeo.split('|') if each == baseHRCGrp] or False
													if matchFound:
														try:
															if cmds.nodeType(node_name) == 'shadingEngine':
																cmds.sets(eachGeo, edit=True, forceElement = node_name)

																if xmlVersionNumber:
																	_addVersionTag(matchFound[0], xmlVersionNumber)
															else:
																cmds.confirmDialog(title = 'REBUILD SHADER', message = '"%s" is not a shadingEngine type, skip assigning\n"%s" to "%s"...' % (node_name, eachGeo, node_name), button = 'OK')
														except ValueError:
															pass
									
									## It doesn't exist, so lets lLook for the shading reconnect via the LIB object metaTags
									else:
										foundImportedGeo = {} ## format  fullDAGPath ; geoName
										getAllLibGeo = [eachGeo for eachGeo in cmds.ls(type = 'transform')  if cmds.objExists('%s.LIBORIGNAME'  % eachGeo)]
										if getAllLibGeo:
											for eachGeo in getAllLibGeo:                                               
												## if the attr value is the same as the original geo name continue...
												if cmds.getAttr('%s.LIBORIGNAME' % eachGeo) == origNameInScene:## we have found matching geo to assign to
													## Get the name to assign to (for readability)
													getOrigName = cmds.getAttr('%s.LIBORIGNAME' % eachGeo)
													
													## Get the full path to this new obj as the artist will have re parented this elsewhere..
													fullPathToImportGeo = cmds.ls(eachGeo, l = True)
													
													if fullPathToImportGeo:
														## Now add this to the list pathToGeoInScene :
														if fullPathToImportGeo[0] not in foundImportedGeo:
															foundImportedGeo[fullPathToImportGeo[0]] =  eachGeo
										
										## Now process the list of geo that exist in the scene that match the geo in the xml and assign the shader
										if foundImportedGeo:
											for fullPath, geoName in foundImportedGeo.items():
												try:
													cmds.sets('%s|%sShape' % (fullPath, geoName), edit=True, forceElement = node_name)
												except:
													pass

	## Progress bar end!
	cmds.progressBar(gMainProgressBar, e = True, endProgress = True)

def _addVersionTag(assetName, versionNumber):
	assetName = cmds.ls(assetName, long = True)[0]

	if cmds.objExists('%s.SRFversion' % assetName):
		cmds.deleteAttr('%s.SRFversion' % assetName)
		
	try:	cmds.addAttr(assetName, ln = 'SRFversion', at = 'long', min = 0, max  = 50000, dv = 0)
	except:	pass

	cmds.setAttr('%s.SRFversion' % assetName, int(versionNumber))

def applyOceanState(path):
	if os.path.isfile(path) and path.endswith('.mel'):
		if cmds.objExists('ocean_dispShader'):
			try:
				cmds.evalDeferred( 'mel.eval("""applyPresetToNode \"ocean_dispShader\" "" "" \"%s\" 1;""")' % path )
				cmds.headsUpMessage('%s applied to ocean!' % os.path.basename(path).split('.')[0], time = 1)
			except:
				pass
#temparory
def EyeBallFix():
	
	characterCorneaFix()
	##EyeBallFix
	EyeBAll = cmds.ls("*eyeball_white_geo",type='transform',l=True)

	cmds.createRenderLayer(n="EyeColorFix") if cmds.objExists("EyeColorFix")==False else None
	cmds.editRenderLayerGlobals(currentRenderLayer="EyeColorFix")
	cmds.editRenderLayerMembers("EyeColorFix",EyeBAll,noRecurse=True)

	mapi.associate_pass('ao','EyeColorFix')
	mapi.associate_pass('beauty','EyeColorFix')
	mapi.associate_pass('colour','EyeColorFix')
	mapi.associate_pass('diffuse','EyeColorFix')
	mapi.associate_pass('facing_ratio','EyeColorFix')
	mapi.associate_pass('incandescence','EyeColorFix')
	mapi.associate_pass('indirect','EyeColorFix')
	mapi.associate_pass('reflection','EyeColorFix')
	mapi.associate_pass('refraction','EyeColorFix')
	mapi.associate_pass('specular','EyeColorFix')

def BuoyTopFix():
##BuoyTopFix
	Buoy=[]
	BuoyGroup = cmds.ls(['lightcover_geo*', 'lightbulb_geo*', 'standlightbulb_geo*','base_geo*'],type='mesh',l=True)
	BuoyMesh = [x for x in BuoyGroup]
	Buoy = [x for i in BuoyMesh for x in cmds.listRelatives(i,p=True,fullPath=True,type='transform')]
	if Buoy:
		BuoyTop = filter(lambda x: 'buoy' in x.lower() , Buoy)
		StandLight = filter(lambda x: 'standlightbulb' in x.lower() or 'base_geo' in x.lower() and ('buoy' in x.lower() and 'prop' in x.lower() and not 'lightcover_geo' in x and not 'lightbulb_geo' in x), BuoyTop)
		cmds.createRenderLayer(n="BuoyTopFix") if cmds.objExists("BuoyTopFix")==False else None
		cmds.editRenderLayerGlobals(currentRenderLayer="BuoyTopFix")
		cmds.editRenderLayerMembers("BuoyTopFix",BuoyTop,noRecurse=True)
		[cmds.editRenderLayerAdjustment("%s.primaryVisibility" %x) for x in StandLight]# if StandLight: 
		[cmds.setAttr('%s.primaryVisibility' %x , 0) for x in StandLight]
		mapi.associate_pass('ao','BuoyTopFix')
		mapi.associate_pass('beauty','BuoyTopFix')
		mapi.associate_pass('colour','BuoyTopFix')
		mapi.associate_pass('diffuse','BuoyTopFix')
		mapi.associate_pass('facing_ratio','BuoyTopFix')
		mapi.associate_pass('incandescence','BuoyTopFix')
		mapi.associate_pass('indirect','BuoyTopFix')
		mapi.associate_pass('reflection','BuoyTopFix')
		mapi.associate_pass('refraction','BuoyTopFix')
		mapi.associate_pass('specular','BuoyTopFix')

def animCacheVersionToLog():
	try:
		listAnimCacheHrc = cmds.ls('ABC_ANIM_CACHES_hrc*')
		versions = []
		for each in listAnimCacheHrc:
			try:
				v= cmds.getAttr('%s.version' % each)
				versions.append(v)
			except:
				cmds.warning("%s doesn't have any attribute called version" % each)
		latestVersion = sorted(versions)[-1]

		file_path = cmds.file(query=True, sceneName=1)
		#abc_cache_path = os.path.join(file_path.split("Light")[0], "Anm/publish/alembic_anim")

		#episode_name = file_path.split('/')[-6]
		#shot_name = file_path.split('/')[-5]
		#epPath = file_path.split(shot_name)[0]
		##Temp##################################
		EP = "I:/bubblebathbay/episodes/"
		Path = "/Anm/publish/alembic_anim"
		CameraName = [x for x in cmds.ls(type='camera') if 'Cam' in x and cmds.getAttr('%s.renderable' %x) == True][0]
		Episode = CameraName.split('_')[0]
		#Output var
		shot_name = Episode +'_'+ CameraName.split('_')[1]
		abc_cache_path = EP+Episode+'/'+shot_name+Path
		epPath = EP + Episode
		##Temp#########################
		log_info_dict = {shot_name: os.path.join(abc_cache_path, latestVersion)}
		if os.path.exists(abc_cache_path):
			log_path = os.path.join(epPath, "anim_caches_version.log")
			if not os.path.exists(log_path):
				log = open(log_path, 'wb')
				json.dump(log_info_dict, log)
				log.close()
			else:
				log = open(log_path, 'rb')
				log_info = json.load(log)
				log.close()
				

				if log_info.has_key(shot_name):
					if log_info[shot_name] > os.path.join(abc_cache_path, latestVersion):
						print "Less then"
					elif log_info[shot_name] < os.path.join(abc_cache_path, latestVersion):
						new_log = open(log_path, 'wb')
						log_info[shot_name] = os.path.join(abc_cache_path, latestVersion)
						json.dump(log_info, new_log)
						new_log.close()
						
					else:
						print "Using latest version of caches in Lighting"
						
				else:
					log_info.update(log_info_dict)
					new_log = open(log_path, 'wb')
					json.dump(log_info, new_log)
					new_log.close()
	except:
		cmds.warning("No Anim cache in the scene")

def FXVersionToLog():
	try:
		listAnimCacheHrc = cmds.ls('FX_CACHES_hrc*')
		versions = []
		for each in listAnimCacheHrc:
			try:
				v= cmds.getAttr('%s.version' % each)
				versions.append(v)
			except:
				cmds.warning("%s doesn't have any attribute called version" % each)
		latestVersion = sorted(versions)[-1]
		file_path = cmds.file(query=True, sceneName=1)
		#FX_Version_path = os.path.join(file_path.split("Light")[0], "Anm/publish/alembic_anim")
		#episode_name = file_path.split('/')[-6]
		#shot_name = file_path.split('/')[-5]
		#epPath = file_path.split(shot_name)[0]
		##Temp##################################
		EP = "I:/bubblebathbay/episodes/"
		Path = "/FX/publish/fx"
		CameraName = [x for x in cmds.ls(type='camera') if 'Cam' in x and cmds.getAttr('%s.renderable' %x) == True][0]
		Episode = CameraName.split('_')[0]
		#Output var
		shot_name = Episode +'_'+ CameraName.split('_')[1]
		FX_Version_path = EP+Episode+'/'+shot_name+Path
		epPath = EP + Episode
		##Temp#########################
		log_info_dict = {shot_name: os.path.join(FX_Version_path, latestVersion)}
		if os.path.exists(FX_Version_path):
			log_path = os.path.join(epPath, "FX_version.log")
			if not os.path.exists(log_path):
				log = open(log_path, 'wb')
				json.dump(log_info_dict, log)
				log.close()
			else:
				log = open(log_path, 'rb')
				print "Hahah"
				log_info = json.load(log)
				print "Lol"
				log.close()
				if log_info.has_key(shot_name):
					if log_info[shot_name] > os.path.join(FX_Version_path, latestVersion):
						print "Less then"
					elif log_info[shot_name] < os.path.join(FX_Version_path, latestVersion):
						new_log = open(log_path, 'wb')
						log_info[shot_name] = os.path.join(FX_Version_path, latestVersion)
						json.dump(log_info, new_log)
						new_log.close()
					else:
						print "Using latest version of FX in Lighting"
				else:
					log_info.update(log_info_dict)
					new_log = open(log_path, 'wb')
					json.dump(log_info, new_log)
					new_log.close()
	except:
		cmds.warning("No FX in the scene")

def deleteSetup():
	'''
	Do a complete clean-up of various nodes that setup lighting creates...
	'''
	try:    cmds.delete( _ls(nodeType = 'transform', topTransform = True, stringFilter = 'LIGHTS_hrc', unlockNode = True) )
	except: pass
	try:    cmds.delete( _ls(nodeType = 'mia_exposure_simple', topTransform = True, stringFilter = '', unlockNode = True) )
	except: pass
	try:    cmds.delete( _ls(nodeType = 'mia_physicalsky', topTransform = True, stringFilter = '', unlockNode = True) )
	except: pass
	try:    cmds.delete( _ls(nodeType = 'mia_physicalsun', topTransform = True, stringFilter = '', unlockNode = True) )
	except: pass
	try:    cmds.delete( _ls(nodeType = 'core_renderpass', topTransform = True, stringFilter = '', unlockNode = True) )
	except: pass
	try:    cmds.delete( _ls(nodeType = 'mentalraySubdivApprox', topTransform = True, stringFilter = '', unlockNode = True) )
	except: pass
	try:    cmds.delete( _ls(nodeType = 'renderLayer', topTransform = True, stringFilter = 'cloud_LYR', unlockNode = True) )
	except: pass

def _ls(nodeType = '', topTransform = True, stringFilter = '', unlockNode = False):
	if nodeType:
		nodes = cmds.ls(type = nodeType)
		if nodes:
			final_nodes = []
			for each in nodes:
				each = cmds.ls(each, long = True)[0]
				top_transform = cmds.listRelatives(each, parent = True, fullPath = True) if topTransform else None
				final_node = top_transform[0] if top_transform else each

				if unlockNode:
					try:	cmds.lockNode(final_node, lock = False)
					except:	mel.eval('warning "Failed to unlock %s, skipping...";' % final_node)

				if stringFilter:
					if stringFilter in final_node:
						if final_node not in final_nodes:
							final_nodes.append(final_node)
				else:
					if final_node not in final_nodes:
						final_nodes.append(final_node)

			return final_nodes

		return []


#Quick Fix

def HardSurface():
	HardMesh = cmds.ls('AI_Land_houseplank_002_geo',l=True)
	cmds.select(HardMesh) if HardMesh else None
	cmds.polySoftEdge( a=0 ,ch=1) if HardMesh else None

def extraLightSetup():
	import sys
	sys.path.append('//192.168.5.253/BBB_main/bbb/t/bubblebathbay_APPDIR/bbb_leonloong/scripts')
	import EZ_Light_Tools_Command
	reload(EZ_Light_Tools_Command)
	
	EZ_Light_Tools_Command.EZ_Light_Tools_Extra_Light()



def TurnOffEyeLashBlinn():
	Eyelash = cmds.ls('*eyelash*','*lashes_*','*eyeLash*', type = 'transform')
	EyeLashGeo = []
	for x in Eyelash:
		AllMesh = cmds.listRelatives(x, ad=True, fullPath=True, type='mesh')
		for x in AllMesh:
			ShdEng=cmds.listConnections(x,type='shadingEngine')
			for x in ShdEng:
				if cmds.nodeType(x)=='shadingEngine':
					CoreM = cmds.listConnections(ShdEng)
					for i in CoreM:
						if cmds.nodeType(i)=='core_material':
							print i
							try:
								cmds.setAttr('%s.en_blinn' %i,0)
							except:
								pass

def optimizeScene(still = True, step = 5, offset = 1.1, startFrame = None, endFrame = None):
	## First, go to defaultRenderLayer!
	cmds.editRenderLayerGlobals(currentRenderLayer = 'defaultRenderLayer')

	## Get entire scene's meshes (polygon)
	meshes = [cmds.listRelatives(x, parent = True, fullPath = True)[0] for x in cmds.ls(geometry = True, long = True) if '|MASTER_ROOTCOREARCHIVES_hrc' not in x and '|ABC_ANIM_CACHES_hrc' not in x]

	if meshes:
		## If proper shotCam exist!
		shotCam = [(cam, cmds.listRelatives(cam, shapes = True)[0]) for cam in cmds.listCameras(perspective = True) if cmds.objExists('%s.type' % cam) if cmds.getAttr('%s.type' % cam) == 'shotCam']
		if shotCam:

			## First, turn off bounding box...
			bbxAllOff()
			
			for each in shotCam:
				cam = each[0]
				camShape = each[1]
				
				defaultOverscan = cmds.getAttr('%s.overscan' % camShape)
				None if defaultOverscan == offset else cmds.setAttr('%s.overscan' % camShape, offset)
				
				## Build custom modelPanel
				cmds.deleteUI('temp_bbb_window') if cmds.window('temp_bbb_window', exists = True, q = True) else None

				cmds.window('temp_bbb_window', width = 300, height = 300)
				cmds.paneLayout()
				cmds.modelPanel('temp_bbb_modelPanel', camera = camShape) if not cmds.modelPanel('temp_bbb_modelPanel', exists = True, q = True) else cmds.modelPanel('temp_bbb_modelPanel', edit = True, parent = 'temp_bbb_window')
				cmds.showWindow('temp_bbb_window')
				mel.eval('setFocus("temp_bbb_modelPanel")')
				
				## Suspend modelPanel refresh for speed optimization
				cmds.refresh(suspend = True)
				
				if still:
					view = omu.M3dView.active3dView()
					om.MGlobal.selectFromScreen(0, 0, view.portWidth(), view.portHeight(), om.MGlobal.kReplaceList)
				else:
					fmin = int( cmds.playbackOptions(minTime = True, q = True) ) if not startFrame else startFrame
					fmax = int( cmds.playbackOptions(maxTime = True, q = True) ) if not endFrame else endFrame

					selection = []
					for i in range(fmin, fmax + 1)[::step]:
						cmds.currentTime(i)
						
						view = omu.M3dView.active3dView()
						om.MGlobal.selectFromScreen(0, 0, view.portWidth(), view.portHeight(), om.MGlobal.kReplaceList)
						
						selection.extend( cmds.ls(selection = True, long = True) ) if cmds.ls(selection = True) else None
						
					cmds.select(selection, replace = True) if selection else None
						
				selection = cmds.ls(selection = True, long = True) if cmds.ls(selection = True) else None
				if selection:
					selection = [x for x in selection if '|ABC_ANIM_CACHES_hrc' not in x] ## Filter out Char and Prop
					
					cmds.select(meshes, replace = True)
					cmds.select(selection, deselect = True)
					cmds.delete() if cmds.ls(selection = True) else None
					
				## Delete temp UI
				cmds.deleteUI('temp_bbb_window') if cmds.window('temp_bbb_window', exists = True, q = True) else None
					
				## Set back to default overscan
				cmds.setAttr('%s.overscan' % camShape, defaultOverscan)
				
				## Remove selection
				cmds.select(clear = True)
				
				## Finally, don't forget to turn back modelPanel refresh on
				cmds.refresh(suspend = False)


def ResetSubdiv():
	if not cmds.objExists('auto_mrSubdAppx1'):
		if  cmds.objExists('auto_mrSubdAppx'):
			cmds.duplicate('auto_mrSubdAppx')

	Stormy = cmds.ls(#"CHAR_Stormy02_hrc")[
	##Stormy
	'body_geo',
	'R_wingfeather_hrc',
	'L_wingfeather_hrc',
	'WetFeathers_hrc',
	'eyepatch_hrc',
	'R_eye_hrc',
	'L_eye_hrc',
	'upperBeak_geo',
	'lowerBeak_geo',
	'L_eyeBrow_geo',
	'R_eyeBrow_geo',
	'L_eyeLash_geo',
	'R_eyeLash_geo',
	'body_hrc',
	'feathers_1_hrc',
	'feathers_2_hrc',
	'tongue_geo',
	'Red_eyes_hrc',
	##Stormy
	l=True,
	type='transform'
	)

	Father = []
	Son = []
	for x in Stormy:
		if 'Stormy' in x:
			StomrySon = cmds.listRelatives(x,ad=True,fullPath=True,type="mesh")
			Son.extend(StomrySon) if StomrySon else None
	for x in Son:
		Father.append(cmds.listRelatives(x,p=True,fullPath = True)[0])
		try:
			cmds.disconnectAttr('auto_mrSubdAppx.message','%s.miSubdivApprox' %x)
		except:
			pass
			
	for x in Son:
		Father.append(cmds.listRelatives(x,p=True,fullPath = True)[0])
		try:
			cmds.connectAttr('auto_mrSubdAppx1.message','%s.miSubdivApprox' %x)	
		except:
			pass
	if cmds.objExists('auto_mrSubdAppx1'):			
		cmds.setAttr ("auto_mrSubdAppx1.maxSubdivisions", 1)

def setupExtraSpotLightFog(**kwargs):
	pLight = cmds.spotLight(**kwargs)
	
	## Create anim_curve
	anim_curve = cmds.createNode('animCurveUU')
	cmds.setKeyframe(anim_curve, value = 3, float = 0, itt = 'linear', ott = 'linear')
	cmds.setKeyframe(anim_curve, value = 0, float = 30, itt = 'linear', ott = 'linear')
	
	## Create Light_info
	light_info = cmds.createNode('lightInfo')
	
	## Setup curve intensity
	cmds.connectAttr('%s.sampleDistance' % light_info, '%s.input' % anim_curve)
	cmds.connectAttr('%s.output' % anim_curve, '%s.intensity' % pLight)
	cmds.connectAttr('%s.worldMatrix[0]' % pLight, '%s.worldMatrix' % light_info)

	cmds.setAttr('%s.useDepthMapShadows' % pLight, 1)
	cmds.setAttr('%s.dmapResolution' % pLight, 256)
	cmds.setAttr('%s.dmapFilterSize' % pLight, 5)

	cmds.setAttr('%s.translateZ' % cmds.listRelatives(pLight, parent = True, fullPath = True)[0], -0.23)
	cmds.setAttr('%s.scaleX' % cmds.listRelatives(pLight, parent = True, fullPath = True)[0], 0.126)
	cmds.setAttr('%s.scaleY' % cmds.listRelatives(pLight, parent = True, fullPath = True)[0], 0.126)
	cmds.setAttr('%s.scaleZ' % cmds.listRelatives(pLight, parent = True, fullPath = True)[0], -0.3)
	
	## Create lightfog
	cmds.defaultNavigation(createNew = True, destination = "%s.fogGeometry" % pLight)
	lightFog = cmds.ls(selection = True)[0]
	cmds.setAttr('%s.fastDropOff' % lightFog, 1)

	return pLight