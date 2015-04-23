from maya import cmds, mel
from mentalcore import mapi
import sys, os, ast
sys.path.append('//192.168.5.253/BBB_main/bbb/t/bubblebathbay_APPDIR/deepesh/2013.5-x64/scripts')
import bbbLightTools
reload(bbbLightTools)
import manageCoreArchives
reload(manageCoreArchives)
sys.path.append('//192.168.5.253/BBB_main/bbb/t/bubblebathbay_APPDIR/bbb_leonloong/scripts')
import EZ_Light_Tools_Command
reload(EZ_Light_Tools_Command)

if cmds.window('bbb_light_tools', exists = True):
	cmds.deleteUI('bbb_light_tools')
	
cmds.window('bbb_light_tools', title = 'BBB_Render_Tools', rtf = True, s = False, width = 250)
cmds.columnLayout('bbb_main_columnLayout', rowSpacing = 1.5, columnWidth = 250, adjustableColumn = True)
# cmds.tabLayout('bbb_tab_layout', parent = 'bbb_main_columnLayout', childResizable = True, selectCommand = 'bbbLightToolsUI.lockTab()')
cmds.tabLayout('bbb_tab_layout', parent = 'bbb_main_columnLayout', childResizable = True)
cmds.columnLayout('bbb_genUtils_columnLayout', rowSpacing = 1.5, columnWidth = 250, parent = 'bbb_tab_layout', adjustableColumn = True)
cmds.columnLayout('bbb_retakes_columnLayout', rowSpacing = 1.5, columnWidth = 250, parent = 'bbb_tab_layout', adjustableColumn = True)

################
## MAJOR SETUPS
################

###################
## Import Publishes
###################

cmds.frameLayout('bbb_publishes_frameLayout', label = '1. Publishes', borderStyle = 'in', collapsable = True, collapse = True, parent = 'bbb_genUtils_columnLayout', width = 250)
cmds.rowColumnLayout(numberOfColumns = 3, width = 250)

cmds.button(label = "Anim Publish", align = "center", command = "bbbLightTools._fetchAnimPublish(filteredPublish = 'Fetch Anim Publish')", width = 230)
cmds.text(label = '', width = 5)
cmds.checkBox('bbbAnimPublishCB', label = '', width = 15, value = True)
cmds.button(label = "Camera Publish", align = "center", command = "bbbLightTools._fetchAnimPublish(filteredPublish = 'Fetch Camera Publish')", width = 230)
cmds.text(label = '', width = 5)
cmds.checkBox('bbbCamPublishCB', label = '', width = 15, value = True)
cmds.button(label = "Crease XML Publish", align = "center", command = "bbbLightTools._fetchAnimPublish(filteredPublish = 'Fetch Crease XML Publish')", width = 230)
cmds.text(label = '', width = 5)
cmds.checkBox('bbbCreaseXMLPublishCB', label = '', width = 15, value = True)
cmds.button(label = "FX Publish", align = "center", command = "bbbLightTools._fetchAnimPublish(filteredPublish = 'Fetch FX Publish')", width = 230)
cmds.text(label = '', width = 5)
cmds.checkBox('bbbFXPublishCB', label = '', width = 15, value = True)

cmds.columnLayout(parent = 'bbb_publishes_frameLayout', adjustableColumn = True)

cmds.button(label = "Fetch All Publish * ", width = 245, align = "center", command = "bbbLightTools.importPublishes()", backgroundColor = [0.33, 1, 0.33], height = 50)

##################
## Import Shaders
##################

cmds.frameLayout(label = '2. Shading', borderStyle = 'in', collapsable = True, collapse = True, parent = 'bbb_genUtils_columnLayout', width = 250)
cmds.columnLayout(adjustableColumn = True)

cmds.button(label = "Fetch All Shader", width = 245, align = "center", command = "bbbLightTools.fetchAllShaders()")
cmds.button(label = "Fetch Shaders on Selection", width = 245, align = "center", command = "bbbLightTools.fetchShadersForSelected()")

######################
## Quick Static import
######################

cmds.frameLayout('bbb_quickImport_frameLayout', label = '3. Import Statics ENV', borderStyle = 'in', collapsable = True, collapse = True, parent = 'bbb_genUtils_columnLayout', width = 250)
cmds.rowColumnLayout(numberOfColumns = 3, width = 250)

cmds.button(label = "(010) Bubble Bath Bay *", align = "center", command = "bbbLightTools._doSTATIC_import(path = '//192.168.5.253/BBB_main/bbb/i/bubblebathbay/episodes/ep000/ep000_sh010/Light/publish/maya', namespace = 'ep000_sh010_ep000sh010_LIGHTENV')", width = 230)
cmds.text(label = '', width = 5)
cmds.checkBox('bubbleBathBayStaticCB', label = '', width = 15, value = True)
cmds.button(label = "(020) West Harbour *", align = "center", command = "bbbLightTools._doSTATIC_import(path = '//192.168.5.253/BBB_main/bbb/i/bubblebathbay/episodes/ep000/ep000_sh020/Light/publish/maya', namespace = 'ep000_sh020_ep000sh020_LIGHTENV')", width = 230)
cmds.text(label = '', width = 5)
cmds.checkBox('westHarbourStaticCB', label = '', width = 15, value = True)
cmds.button(label = "(030) Big Town *", align = "center", command = "bbbLightTools._doSTATIC_import(path = '//192.168.5.253/BBB_main/bbb/i/bubblebathbay/episodes/ep000/ep000_sh030/Light/publish/maya', namespace = 'ep000_sh030_ep000sh030_LIGHTENV')", width = 230)
cmds.text(label = '', width = 5)
cmds.checkBox('bigTownStaticCB', label = '', width = 15, value = True)
cmds.button(label = "(040) The Heads *", align = "center", command = "bbbLightTools._doSTATIC_import(path = '//192.168.5.253/BBB_main/bbb/i/bubblebathbay/episodes/ep000/ep000_sh040/Light/publish/maya', namespace = 'ep000_sh040_ep000sh040_LIGHTENV')", width = 230)
cmds.text(label = '', width = 5)
cmds.checkBox('theHeadsStaticCB', label = '', width = 15, value = True)
cmds.button(label = "(050) Hidden Cove *", align = "center", command = "bbbLightTools._doSTATIC_import(path = '//192.168.5.253/BBB_main/bbb/i/bubblebathbay/episodes/ep000/ep000_sh050/Light/publish/maya', namespace = 'ep000_sh050_ep000sh050_LIGHTENV')", width = 230)
cmds.text(label = '', width = 5)
cmds.checkBox('hiddenCoveStaticCB', label = '', width = 15, value = True)
cmds.button(label = "(060) Dock_Addon *", align = "center", command = "bbbLightTools._doSTATIC_import(path = '//192.168.5.253/BBB_main/bbb/i/bubblebathbay/episodes/ep000/ep000_Docks_Addon/Light/publish/maya', namespace = 'ep000_sh050_ep000sh060_LIGHTENV')", width = 230)
cmds.text(label = '', width = 5)
cmds.checkBox('DockAddonCB', label = '', width = 15, value = True)

cmds.columnLayout(parent = 'bbb_quickImport_frameLayout', adjustableColumn = True)

cmds.button(label = "Clean-up Statics!", width = 245, align = "center", command = "bbbLightTools.cleanupStatics()", backgroundColor = [1, 0.5, 0.5])
cmds.button(label = "Import Static(s)", height = 50, width = 245, align = "center", command = "bbbLightTools.importStaticEnv()", backgroundColor = [0.33, 1, 0.33])
cmds.button(label = "Import Ripple Layer", height = 50, width = 245, align = "center", command = "bbbLightTools.importRippleLayer()", backgroundColor = [0.33, 1, 0.33])

## TOD Setup
cmds.frameLayout(label = '4. Time of Day', borderStyle = 'in', collapsable = True, collapse = False, parent = 'bbb_genUtils_columnLayout', width = 250)

cmds.columnLayout(adjustableColumn = True)
cmds.button(label = "Delete Setup!", align = "center", command = "bbbLightTools.deleteSetup()", width = 230, backgroundColor = [1, 0.5, 0.5])

cmds.rowColumnLayout(numberOfColumns = 8, width = 250)
cmds.iconTextButton(annotation = 'Dawn', style = 'iconOnly', image1 = 'T:/bubblebathbay_APPDIR/deepesh/2013.5-x64/scripts/icons/1TOD_Dawn4.png', width = 31.25, height = 20, command = 'bbbLightTools.setTOD(TODay = "dawn")')
cmds.iconTextButton(annotation = 'Sunrise', style = 'iconOnly', image1 = 'T:/bubblebathbay_APPDIR/deepesh/2013.5-x64/scripts/icons/2TOD_Sunrise4.png', width = 31.25, height = 20, command = 'bbbLightTools.setTOD(TODay = "sunrise")')
cmds.iconTextButton(annotation = 'Morning', style = 'iconOnly', image1 = 'T:/bubblebathbay_APPDIR/deepesh/2013.5-x64/scripts/icons/3TOD_Morning5.png', width = 31.25, height = 20, command = 'bbbLightTools.setTOD(TODay = "morning")')
cmds.iconTextButton(annotation = 'Midday', style = 'iconOnly', image1 = 'T:/bubblebathbay_APPDIR/deepesh/2013.5-x64/scripts/icons/4TOD_Midday7.png', width = 31.25, height = 20, command = 'bbbLightTools.setTOD(TODay = "midday")')
cmds.iconTextButton(annotation = 'Afternoon', style = 'iconOnly', image1 = 'T:/bubblebathbay_APPDIR/deepesh/2013.5-x64/scripts/icons/5TOD_Afternoon3.png', width = 31.25, height = 20, command = 'bbbLightTools.setTOD(TODay = "afternoon")')
cmds.iconTextButton(annotation = 'Sunset', style = 'iconOnly', image1 = 'T:/bubblebathbay_APPDIR/deepesh/2013.5-x64/scripts/icons/6TOD_Sunset3.png', width = 31.25, height = 20, command = 'bbbLightTools.setTOD(TODay = "sunset")')
cmds.iconTextButton(annotation = 'Dusk', style = 'iconOnly', image1 = 'T:/bubblebathbay_APPDIR/deepesh/2013.5-x64/scripts/icons/7TOD_Dusk3.png', width = 31.25, height = 20, command = 'bbbLightTools.setTOD(TODay = "dusk")')
cmds.iconTextButton(annotation = 'Night', style = 'iconOnly', image1 = 'T:/bubblebathbay_APPDIR/deepesh/2013.5-x64/scripts/icons/8TOD_Night7.png', width = 31.25, height = 20, command = 'bbbLightTools.setTOD(TODay = "night")')

## Render Setup
cmds.button(label = "RENDER SETUP", height = 50, align = "center", parent = 'bbb_genUtils_columnLayout', backgroundColor = [0.33, 1, 0.33], command = "bbbLightTools.RenderSetup()")

## Preview and Render Quality Settings
renQlty = cmds.rowLayout(numberOfColumns = 3, columnWidth3 = (80, 50, 50), columnAlign = (1, "center"), parent = 'bbb_genUtils_columnLayout')
cmds.button(label = "Preview Quality", command = "bbbLightTools.previewSettings()", align = "center", width = 125, height = 20, parent = renQlty, backgroundColor = [0.65, 0.65, 1])
cmds.button(label = "Render Quality", command = "bbbLightTools.finalSettings()", align = "center", width = 125, height = 20, parent = renQlty, backgroundColor = [0.5, 0.5, 1])

## DoRivet
cmds.button(label = "Add Rivet Locator", align = "center", command = "bbbLightTools.doRivet()",parent = 'bbb_genUtils_columnLayout',width = 244, backgroundColor = [0.65, 0.65, 1])
#####################
## Render Layer Setup
#####################

cmds.frameLayout(label = 'Render Layer setups', borderStyle = 'in', collapsable = True, collapse = True, parent = 'bbb_genUtils_columnLayout', width = 250)
cmds.columnLayout(adjustableColumn = True)

## Ripple_Lyr
cmds.button(label = "Ripple Layer", align = "center", command = "bbbLightTools.setRippleLYR()")
## BGHills_Lyr
cmds.button(label = "BGHills Layer", align = "center", command = "bbbLightTools.setBGHills()")
## StormFoam_Lyr
cmds.button(label = "StormFoam Layer", align = "center", command = "bbbLightTools.setStormFoamLYR()")
## OceanFoamSep_Lyr
cmds.button(label = "OceanFoamSep Layer", align = "center", command = "bbbLightTools.setOceanFoamSepLYR()")
## OceanFoamSep_Lyr
cmds.button(label = "Waterfall Layer", align = "center", command = "bbbLightTools.setWaterfallLYR()")
## FeatherEdge_Lyr
cmds.button(label = "FeatherEdge Layer", align = "center", command = "bbbLightTools.setupOceanIntegrationMatteLayer()")
## BuoyTop_Lyr
cmds.button(label = "BuoyTop Layer", align = "center", command = "bbbLightTools.BuoyTopFix()")
## Extra Light Layer
cmds.button(label = "Extra Light Layer", align = "center", command = "bbbLightTools.extraLightSetup()")
## Write Nuke Camera
# cmds.button(label = "NukeCameraWriter", width = 90, align = "center", parent = 'bbb_genUtils_columnLayout', command = "bbbLightTools.NukeCameraWriter()", backgroundColor = [1, 0.5, 0.5])	

#####################
## Matte on selection
#####################

cmds.frameLayout(label = 'Mattes on selection', borderStyle = 'in', collapsable = True, collapse = True, parent = 'bbb_genUtils_columnLayout', width = 250)
cmds.rowColumnLayout(numberOfColumns = 5, width = 250)

cmds.button(label = "", width = 50, align = "center", command = "bbbLightTools.attachColorMattes(color = [0, 0, 0])", backgroundColor = [0, 0, 0])
##
cmds.button(label = "", width = 50, align = "center", command = "bbbLightTools.attachColorMattes(color = [1, 1, 1])", backgroundColor = [1, 1, 1])
##
cmds.button(label = "", width = 50, align = "center", command = "bbbLightTools.attachColorMattes(color = [1, 0, 0])", backgroundColor = [1, 0, 0])
##
cmds.button(label = "", width = 50, align = "center", command = "bbbLightTools.attachColorMattes(color = [0, 1, 0])", backgroundColor = [0, 1, 0])
##
cmds.button(label = "", width = 50, align = "center", command = "bbbLightTools.attachColorMattes(color = [0, 0, 1])", backgroundColor = [0, 0, 1])
##
# cmds.button(label = "Shading matte on selected", width = 230, align = "center", command = "bbbLightTools.attachShadingMatte(ocean = False)", backgroundColor = [1, 1, 1], parent = frameChildColumnLayout)
##
# cmds.button(label = "Shading matte for ocean", width = 230, align = "center", command = "bbbLightTools.attachShadingMatte(ocean = True)", backgroundColor = [1, 1, 1], parent = frameChildColumnLayout)
##
# cmds.button(label = "Red Point Light", width = 230, align = "center", command = "bbbLightTools.setupExtraLight(decayRate = 3, rgb = [1, 0, 0], useRayTraceShadows = True)", backgroundColor = [1, 0, 0], parent = frameChildColumnLayout)
##
# cmds.button(label = "Green Point Light", width = 230, align = "center", command = "bbbLightTools.setupExtraLight(decayRate = 3, rgb = [0, 1, 0], useRayTraceShadows = True)", backgroundColor = [0, 1, 0], parent = frameChildColumnLayout)
##
# cmds.button(label = "Blue Point Light", width = 230, align = "center", command = "bbbLightTools.setupExtraLight(decayRate = 3, rgb = [0, 0, 1], useRayTraceShadows = True)", backgroundColor = [0, 0, 1], parent = frameChildColumnLayout)
##
# cmds.button(label = "Red Spot Light", width = 230, align = "center", command = "bbbLightTools.setupExtraSpotLight(intensity = 50, decayRate = 3, rgb = [1, 0, 0], useRayTraceShadows = True, coneAngle = 50.872, penumbra = 20, dropOff = 10)", backgroundColor = [1, 0, 0], parent = frameChildColumnLayout)
##
# cmds.button(label = "Blue Spot Light", width = 230, align = "center", command = "bbbLightTools.setupExtraSpotLight(intensity = 50, decayRate = 3, rgb = [0, 1, 0], useRayTraceShadows = True, coneAngle = 50.872, penumbra = 20, dropOff = 10)", backgroundColor = [0, 1, 0], parent = frameChildColumnLayout)
##
# cmds.button(label = "Green Spot Light", width = 230, align = "center", command = "bbbLightTools.setupExtraSpotLight(intensity = 50, decayRate = 3, rgb = [0, 0, 1], useRayTraceShadows = True, coneAngle = 50.872, penumbra = 20, dropOff = 10)", backgroundColor = [0, 0, 1], parent = frameChildColumnLayout)
##

################
## Render Status
################

cmds.frameLayout(label = 'Selection-Based Operation', borderStyle = 'in', collapsable = True, collapse = True, parent = 'bbb_genUtils_columnLayout', width = 250)
cmds.rowColumnLayout(numberOfColumns = 3, width = 250)

## Cast-Shadow
cmds.text(label = "Cast Shadow", width = 100)
cmds.button(label = "On", command = "bbbLightTools.turnOnCastShad()", width = 75)
cmds.button(label = "Off", command = "bbbLightTools.turnOffCastShad()", width = 75)
## Receive-Shadow
cmds.text(label = "Receive Shadow", width = 100)
cmds.button(label = "On", command = "bbbLightTools.turnOnRecShad()", width = 75)
cmds.button(label = "Off", command = "bbbLightTools.turnOffRecShad()", width = 75)
## Visible in Reflection
cmds.text(label = "Vis In Reflection", width = 100)
cmds.button(label = "On", command = "bbbLightTools.turnOnVisRefl()", width = 75)
cmds.button(label = "Off", command = "bbbLightTools.turnOffVisRefl()", width = 75)
## Visible in Refraction
cmds.text(label = "Vis In Refraction", width = 100)
cmds.button(label = "On", command = "bbbLightTools.turnOnVisRefr()", width = 75)
cmds.button(label = "Off", command = "bbbLightTools.turnOffVisRefr()", width = 75)
## Bounding Box Controls Selected
cmds.text(label = "BBox Selected", width = 100)
cmds.button(label = "On", command = "bbbLightTools.bbxSelectedOn()", width = 75)
cmds.button(label = "Off", command = "bbbLightTools.bbxSelectedOff()", width = 75)
## Bounding Box Controls All
cmds.text(label = "BBox All", width = 100)
cmds.button(label = "On", command = "bbbLightTools.bbxAllOn()", width = 75)
cmds.button(label = "Off", command = "bbbLightTools.bbxAllOff()", width = 75)
## SwapFullResTexture
cmds.text(label = "Geo's Textures", width = 100)
cmds.button(label = "Full > Low", command = "bbbLightTools.fullToLowRes()", width = 75)
cmds.button(label = "Low > Full", command = "bbbLightTools.lowToFullRes()", width = 75)

################
## Object Mattes
################

cmds.frameLayout(label = 'Object Mattes', borderStyle = 'in', collapsable = True, collapse = True, parent = 'bbb_genUtils_columnLayout', width = 250)
cmds.rowColumnLayout(numberOfColumns = 3, width = 250)

cmds.button(label = "Character Mattes *", align = "center", command = "bbbLightTools.createCharMattes()", width = 230)
cmds.text(label = '', width = 5)
cmds.checkBox('createCharMattesCB', label = '', width = 15, value = True)
cmds.button(label = "Character Eye Mattes *", align = "center", command = "bbbLightTools.createEyeMattes()", width = 230)
cmds.text(label = '', width = 5)
cmds.checkBox('createEyeMattesCB', label = '', width = 15, value = True)
cmds.button(label = "Character Eyelash Mattes *", align = "center", command = "bbbLightTools.createEyelashMattes()", width = 230)
cmds.text(label = '', width = 5)
cmds.checkBox('createEyelashMattesCB', label = '', width = 15, value = True)
cmds.button(label = "Character Tongue Mattes *",  align = "center", command = "bbbLightTools.createCharTongueMattes()", width = 230)
cmds.text(label = '', width = 5)
cmds.checkBox('createCharTongueMattesCB', label = '', width = 15, value = True)
cmds.button(label = "Sydney Sail Mattes *", align = "center", command = "bbbLightTools.createSydneySailMattes()", width = 230)
cmds.text(label = '', width = 5)
cmds.checkBox('createSydneySailMattesCB', label = '', width = 15, value = True)
cmds.button(label = "Prop Mattes *", align = "center", command = "bbbLightTools.createPropMattes()", width = 230)
cmds.text(label = '', width = 5)
cmds.checkBox('createPropMattesCB', label = '', width = 15, value = True)
cmds.button(label = "CProp Mattes *", align = "center", command = "bbbLightTools.createCPropMattes()", width = 230)
cmds.text(label = '', width = 5)
cmds.checkBox('createCPropMattesCB', label = '', width = 15, value = True)
cmds.button(label = "Building Mattes *", align = "center", command = "bbbLightTools.createBuildingMattes()", width = 230)
cmds.text(label = '', width = 5)
cmds.checkBox('createBuildingMattesCB', label = '', width = 15, value = True)
cmds.button(label = "Ocean Mattes *", align = "center", command = "bbbLightTools.createOceanMattes()", width = 230)
cmds.text(label = '', width = 5)
cmds.checkBox('createOceanMattesCB', label = '', width = 15, value = True)
cmds.button(label = "Land Mattes *", align = "center", command = "bbbLightTools.createLandMattes()", width = 230)
cmds.text(label = '', width = 5)
cmds.checkBox('createLandMattesCB', label = '', width = 15, value = True)
cmds.button(label = "Core Archive Mattes *", align = "center", command = "bbbLightTools.createCoreArchiveMattes()", width = 230)
cmds.text(label = '', width = 5)
cmds.checkBox('createCoreArchiveMattesCB', label = '', width = 15, value = True)
cmds.button(label = "Lights Mattes", align = "center", command = "bbbLightTools.createLightsMattes()", width = 230)
cmds.text(label = '', width = 5)
#cmds.separator(height = 5, style = 'in')
cmds.text(label = '', width = 5)
#cmds.button(label = " Extra Light * (dobule - click)", align = "center", command = "EZ_Light_Tools_Command.EZ_Light_Tools_Extra_Light_Spam1()", backgroundColor = [0.13, 0.53, 0.8], width = 30) #height = 160)
#cmds.button(label = " Extra Light * (dobule - click)", align = "center", command = "bbbLightTools.LLL()", backgroundColor = [0.13, 0.53, 0.8], width = 30, height = 160)
cmds.button(label = "Extra Light", align = "center", command = "EZ_Light_Tools_Command.EZ_Light_Tools_Extra_Light_Spam1()", backgroundColor = [0.13, 0.53, 0.8])

############
## Clean-ups
############

cmds.frameLayout(label = 'Clean-ups', borderStyle = 'in', collapsable = True, collapse = True, parent = 'bbb_genUtils_columnLayout', width = 250)
cmds.rowColumnLayout(numberOfColumns = 3, width = 250)

## Clean-up Non-Manifold Geometry
cmds.button(label = "Non-Manifold Geometry *", width = 230, align = "center", command = "bbbLightTools.cleanupNonManifoldGeometry()")
cmds.text(label = '', width = 5)
cmds.checkBox('cleanupNonManifoldGeometryCB', label = '', width = 15, value = True)
## Core archives at origin translate Y -50k
cmds.button(label = "Send Core Archives at origin to Hell *", width = 230, align = "center", command = "bbbLightTools.removeCoreArchiveOfOrigin()")
cmds.text(label = '', width = 5)
cmds.checkBox('removeCoreArchiveOfOriginCB', label = '', width = 15, value = True)
## FixBGOccShadows
cmds.button(label = "BG Occlusion Override *", width = 230, align = "center", command = "bbbLightTools.fixBgOcc()")
cmds.text(label = '', width = 5)
cmds.checkBox('fixBgOccCB', label = '', width = 15, value = True)
## UV Transfer Tool
cmds.button(label = "UV Transfer Tool", width = 230, align ="center", command = "bbbLightTools.UvTransferTool()")
cmds.text(label = '')
cmds.text(label = '')
## Ocean SRF to Poly Preview Tool
cmds.button(label = "Ocean SRF Preview Tool", width = 230, align ="center", command = "bbbLightTools.oceanSrfToPolyPreview()")
cmds.text(label = '')
cmds.text(label = '')
## Clean-Up Core Archive's Roots
cmds.button(label = "Clean-up CoreArchive Roots", width = 230, align ="center", command = "bbbLightTools.cleanupCoreArchiveRoots()")
cmds.text(label = '')
cmds.text(label = '')

##############
## Ocean State
##############

cmds.frameLayout(label = 'Ocean State', borderStyle = 'in', collapsable = True, collapse = True, parent = 'bbb_genUtils_columnLayout', width = 250)
cmds.scrollLayout(horizontalScrollBarThickness = 16)
cmds.columnLayout(adjustableColumn = True, height = 300)

oceanPresetPath = 'T:/bubblebathbay_APPDIR/deepesh/2013.5-x64/presets/attrPresets/oceanShader/Final'
[cmds.button(label = each.split('.')[0], width = 225, align ="center", command = "bbbLightTools.applyOceanState(path = '%s/%s')" % (oceanPresetPath, each)) for each in os.listdir(oceanPresetPath) if each.endswith('.mel')]

###############
## Delete ENV's CoreArchives
###############

cmds.frameLayout(label = "Delete ENV's CoreArchives", borderStyle = 'in', collapsable = True, collapse = True, parent = 'bbb_genUtils_columnLayout')
cmds.columnLayout(adjustableColumn = True)

cmds.button(label = "Generate", width = 225, align = "center", command = 'bbbLightToolsUI.manageCoreArchives.CoreArchiveGenerator()')
cmds.button(label = "CleanUp CoreArchives Empty Groups", width = 225, align = "center", command = "bbbLightToolsUI.manageCoreArchives.CleanUpCoreArchives()", visible=True)

## List of Environment Names
cmds.optionMenuGrp('bbb_ca_envList', label="Environments",width = 225)
cmds.menuItem("ep010", label="ep010")
cmds.menuItem("ep020", label="ep020")
cmds.menuItem("ep030", label="ep030")
cmds.menuItem("ep040", label="ep040")
cmds.menuItem("ep050", label="ep050")

## List of RaidoButton to eaither select or delete coreArchives
cmds.radioCollection('bbb_ca_radioCollection')
rb1 = cmds.radioButton(False, label='Select Core Archives Only', select=True)
rb2 = cmds.radioButton(True, label='Select && Delete Core Archives')

###############
## Build XML of ENV's CoreArchives
###############

cmds.frameLayout(label = "Build XML of ENV's CoreArchives", borderStyle = 'in', collapsable = True, collapse = True, parent = 'bbb_genUtils_columnLayout')
cmds.columnLayout(adjustableColumn = True)

cmds.button(label = "Override main XML!!!", width = 100, align = "left", command = 'bbbLightToolsUI.manageCoreArchives.CoreArchiveBuilder()', enable=False)
#List of Environment Names
cmds.optionMenuGrp('bbb_ca_BuildEnvList',label="Environemnts")
cmds.menuItem("ep010", label="ep010")
cmds.menuItem("ep020", label="ep020")
cmds.menuItem("ep030", label="ep030")
cmds.menuItem("ep040", label="ep040")
cmds.menuItem("ep050", label="ep050")

###############
## Retakes Tab
###############

cmds.columnLayout(adjustableColumn = True, parent = 'bbb_retakes_columnLayout')
	
##
cmds.button(label = "Selection to meshes", width = 230, align = "center", command = "bbbLightTools.selectionToMeshes()")
##
cmds.button(label = "Character Dark Eyes | Eye/Tongue Mattes", width = 230, align = "center", command = "bbbLightTools.fixDarkEye()")
##
cmds.button(label = "Subdiv meshes with smoothed attribute", width = 230, align = "center", command = "bbbLightTools.subdivSmoothedAttr()")
##
cmds.button(label = "Setup foam incandescence", width = 230, align = "center", command = "bbbLightTools.setupFoamOnlyShader()")
##
cmds.button(label = "Delete unused nodes", width = 230, align = "center", command = "bbbLightTools.deleteUnusedJunks()")
##
cmds.button(label = "Render settings for matte/foam", width = 230, align = "center", command = "bbbLightTools.optimizedRenderSettings()")
cmds.button(label = "Setup ExtraLight Layer", width = 245, align = "center", command = "bbbLightTools.customRenderLayerSetup(renderLayer = 'ExtraLight')", backgroundColor = [0.5, 0.5, 0.5])
cmds.button(label = "Setup AuroraFogLight Layer", width = 245, align = "center", command = "bbbLightTools.auroraFogRenderLayerSetup()", backgroundColor = [0.5, 0.5, 0.5])
# cmds.button(label = "Submit To Deadline", width = 245, align = "center", command = "bbbLightTools.submitToDeadline()", backgroundColor = [0.5, 0.5, 0.5])
cmds.separator(height = 5, style = 'in')
cmds.button(label = "LookThruCamera", width = 245, align = "center", command = "bbbLightTools.LookThruCamera()", backgroundColor = [0, 0, 0])

cmds.separator(height = 5, style = 'in')
#temparory
cmds.button(label = "Temporary:EyeBallFix", width = 245, align = "center", command = "bbbLightTools.EyeBallFix()")
## Delete hidden nodes
cmds.button(label = 'Delete Hidden Nodes', width = 245, align = 'center', command = "bbbLightTools.deleteHiddenNodes()")
###################

##################
## Scene Optimizer
##################

cmds.frameLayout('bbb_frameOptimizer_frameLayout', label = 'Scene Optimizer', borderStyle = 'in', collapsable = True, collapse = True, parent = 'bbb_retakes_columnLayout', width = 250)
cmds.rowColumnLayout(numberOfColumns = 3, width = 250, columnWidth = [(1, 122), (2, 4), (3, 122)], parent = 'bbb_frameOptimizer_frameLayout')

cmds.text('bbbOptimizerStillText', label = 'Still', align = 'right')
cmds.text(label = '')
cmds.checkBox('bbbOptimizerStillCB', label = '', value = True, changeCommand = 'bbbLightToolsUI.sceneOptimizerCheckbox()')

cmds.text(label = '')
cmds.text(label = '')
cmds.separator(height = 5, style = 'in')

cmds.text(label = 'Range step', align = 'right')
cmds.text(label = '')
cmds.intField('bbbOptimizerIntField', min = 1, max = 50, value = 5, step = 1, enable = False, changeCommand = "cmds.intSlider('bbbOptimizerIntSlider', e = True, value = cmds.intField('bbbOptimizerIntField', q = True, value = True))")

cmds.text(label = '')
cmds.text(label = '')
cmds.intSlider('bbbOptimizerIntSlider', min = 1, max = 50, value = 5, step = 1, enable = False, changeCommand = "cmds.intField('bbbOptimizerIntField', e = True, value = cmds.intSlider('bbbOptimizerIntSlider', q = True, value = True))")

cmds.text(label = '')
cmds.text(label = '')
cmds.separator(height = 5, style = 'in')

cmds.text(label = 'Camera extend', align = 'right')
cmds.text(label = '')
cmds.floatField('bbbOptimizerFloatField', min = 1, max = 1000, value = 1, changeCommand = "cmds.floatSlider('bbbOptimizerFloatSlider', e = True, value = cmds.floatField('bbbOptimizerFloatField', q = True, value = True))")

cmds.text(label = '')
cmds.text(label = '')
cmds.floatSlider('bbbOptimizerFloatSlider', min = 1, max = 1000, value = 1, changeCommand = "cmds.floatField('bbbOptimizerFloatField', e = True, value = cmds.floatSlider('bbbOptimizerFloatSlider', q = True, value = True))")

cmds.columnLayout(parent = 'bbb_frameOptimizer_frameLayout', adjustableColumn = True)
cmds.button(label = 'Select CoreArchive', command = 'bbbLightToolsUI.optimizerButton()')

###############

verifiedLogin = False
cmds.tabLayout('bbb_tab_layout', edit = True, tabLabel = (('bbb_genUtils_columnLayout', 'General Utilities'), ('bbb_retakes_columnLayout', 'Retakes')) )
cmds.showWindow('bbb_light_tools')

def sceneOptimizerCheckbox():
	cmds.intField( 'bbbOptimizerIntField', e = True, enable = not cmds.checkBox('bbbOptimizerStillCB', q = True, value = True) ) 
	cmds.intSlider( 'bbbOptimizerIntSlider', e = True, enable = not cmds.checkBox('bbbOptimizerStillCB', q = True, value = True) )

def optimizerButton():
	still = cmds.checkBox('bbbOptimizerStillCB', q = True, value = True)
	step = cmds.intField('bbbOptimizerIntField', q = True, value = True)
	offset = cmds.floatField('bbbOptimizerFloatField', q = True, value = True)

	bbbLightTools.optimizeScene(still = still, step = step, offset = offset)

def lockTab(password = 'fuckyoubitch'):
	global verifiedLogin
	if not verifiedLogin:
		currentTab = cmds.tabLayout('bbb_tab_layout', q = True, selectTab = True)
		if currentTab == 'bbb_retakes_columnLayout':
			cmds.tabLayout('bbb_tab_layout', edit = True, selectTab = 'bbb_genUtils_columnLayout')
			
			result = cmds.promptDialog(title = 'Password', message = 'Enter Password:', button = ['OK'], defaultButton = 'OK')
			if result:
				if not cmds.promptDialog(q = True, text = True) == password:
					cmds.tabLayout('bbb_tab_layout', edit = True, selectTab = 'bbb_genUtils_columnLayout')
					verifiedLogin = False
				else:
					cmds.tabLayout('bbb_tab_layout', edit = True, selectTab = 'bbb_retakes_columnLayout')
					verifiedLogin = True
			else:
				cmds.tabLayout('bbb_tab_layout', edit = True, selectTab = 'bbb_genUtils_columnLayout')
				verifiedLogin = False