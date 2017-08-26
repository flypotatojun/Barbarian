﻿#!/usr/local/bin/python2.7
# encoding: utf-8
'''
Created on 2017.8.25

@author: Serious Sam
'''

import os
from maya import cmds
from xml.dom import minidom
from barbarian.utils import ui, config


def UI(*_):
    ResourceRepository("resourceLib",
                       opMnuProject="resourceLibCBProject",
                       rbChar="resourceLibRBChar",
                       rbProp="resourceLibRBProp",
                       rbScene="resourceLibRBScene",
                       container="resourceLibMayaControlLocator",
                       btnLoad="resourceLibBtnLoad")


class ResourceRepository(ui.QtUI):
    def setup(self):
        cmds.optionMenu(self.opMnuProject, e=True, changeCommand=config.setProject)
        cmds.radioButton(self.rbChar, e=True, onCommand=self.refreshData)
        cmds.radioButton(self.rbProp, e=True, onCommand=self.refreshData)
        cmds.radioButton(self.rbScene, e=True, onCommand=self.refreshData)
        cmds.button(self.btnLoad, e=True, command=self.load)
        self.shelf = cmds.shelfLayout(parent=self.container, cellHeight=100, cellWidth=150, spacing=5)
        
        cmds.scriptJob(conditionChange=["ProjectChanged", self.refreshProject], parent=self.window)
        
        self.refreshProject()
    
    def refreshProject(self, *_):
        if config.getProject(): 
            cmds.optionMenu(self.opMnuProject, e=True, l=u"")
            if not cmds.optionMenu(self.opMnuProject, q=True, numberOfItems=True): 
                projects = config.getProject(all=True)
                for prj in projects: cmds.menuItem(l=prj, parent=self.opMnuProject)
            cmds.optionMenu(self.opMnuProject, e=True, v=config.getProject())
        elif config.getProject(all=True): 
            cmds.optionMenu(self.opMnuProject, e=True, l=u"<选择项目>")
            if not cmds.optionMenu(self.opMnuProject, q=True, numberOfItems=True): 
                projects = config.getProject(all=True)
                for prj in projects: cmds.menuItem(l=prj, parent=self.opMnuProject)
            return
        else: 
            cmds.optionMenu(self.opMnuProject, e=True, l=u"<配置异常>")
            if cmds.optionMenu(self.opMnuProject, q=True, numberOfItems=True): 
                for mi in cmds.optionMenu(self.opMnuProject, q=True, itemListLong=True): 
                    cmds.deleteUI(mi)
            return
        
        try: dom = minidom.parse(config.getPath(config.kConfig, config.getConfig("resourceLocator")))
        except:
            self.root = None
            self.clearData()
            return
        
        self.root = dom.documentElement
        self.refreshData()
        
    def refreshData(self, *_):
        if not self.root: return
        
        if cmds.radioButton(self.rbChar, q=True, select=True): resType = 'character'
        elif cmds.radioButton(self.rbProp, q=True, select=True): resType = 'property'
        elif cmds.radioButton(self.rbScene, q=True, select=True): resType = 'scene'
        else: 
            self.clearData()
            return
        
        self.clearData()
        
        for asset in self.root.getElementsByTagName("asset"):
            if asset.getAttribute('type') == resType:
                self.path = asset.getAttribute('path')
                self.items = asset.getElementsByTagName("item")
                self.itrc = cmds.iconTextRadioCollection(parent=self.shelf)
                for item in self.items:
                    resName = item.getAttribute('name')
                    resFile = item.getAttribute('file').split('.ma')[0]
                    resPic = item.getAttribute('thumbnail')
                    resPicPath = self.path + resPic  
                    if not (resPic and os.path.isfile(resPicPath)):
                        resPicPath = config.getPath(config.kIcon, "empty_%s.png"%resType)
                    cmds.iconTextRadioButton(resFile, label=resName, parent=self.shelf, style='iconAndTextVertical',
                                             image=resPicPath, font="smallFixedWidthFont", onCommand=self.getCurrent)
                break
        
    def clearData(self):
        self.current = None
        self.path = None
        cmds.button(self.btnLoad, e=True, enable=False)
        
        if not cmds.shelfLayout(self.shelf, q=True, childArray=True): return
        for btn in cmds.shelfLayout(self.shelf, q=True, childArray=True):
            cmds.deleteUI(btn)
            
    def getCurrent(self, *_):
        cmds.button(self.btnLoad, e=True, enable=True)
        self.current = cmds.iconTextRadioCollection(self.itrc, q=True, select=True)
        
    def load(self, *_):
        cmds.file("%s%s.ma"%(self.path, self.current), r=True, iv=True, typ='mayaAscii', ns=self.current)
        