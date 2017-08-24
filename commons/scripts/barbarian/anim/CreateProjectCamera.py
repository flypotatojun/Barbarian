﻿#!/usr/local/bin/python2.7
# encoding: utf-8

from maya import cmds
from barbarian.utils.config import getConfig

def doIt():
    cameraName = getConfig('camera')
    listCam = cmds.listCameras(perspective=True)
    
    if not cameraName in listCam:
        cmds.camera(name=cameraName, displayResolution=True)
        cmds.rename(cameraName)
        
    cmds.setAttr("defaultResolution.width", getConfig('camResX'))
    cmds.setAttr("defaultResolution.height", getConfig('camResY'))
    cmds.select(cameraName, r=True)
      
    try:
        cmds.addAttr(cameraName, ln='Focal_Length', attributeType='double', defaultValue=35, minValue=0, maxValue=200)
        cmds.setAttr(cameraName+".Focal_Length", edit=True, keyable=True)
        cmds.connectAttr(cameraName+".Focal_Length", cameraName+"Shape.focalLength", force=True)    
    except:    
        pass
 
