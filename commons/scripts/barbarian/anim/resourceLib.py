﻿#!/usr/local/bin/python2.7
# encoding: utf-8
'''
Created on 2017.8.25

@author: Serious Sam
'''

import os
from maya import cmds
from xml.dom import minidom
from PySide import QtCore, QtGui
from barbarian.utils import ui, config


def UI(*_):
    ResourceRepository()


class ResourceRepository(ui.resourceLibUI.Ui_resourceLibOption):
    def setupUi(self, win=None):
        super(ResourceRepository, self).setupUi(win)
        
        cmds.scriptJob(conditionChange=["ProjectChanged", self.refreshProject], parent=self.window)
        
        QtCore.QObject.connect(self.resourceLibCBProject, 
                               QtCore.SIGNAL("activated(int)"), 
                               lambda *_: config.setProject(self.resourceLibCBProject.currentText()))
        QtCore.QObject.connect(self.resourceLibRBChar,
                               QtCore.SIGNAL("clicked(bool)"),
                               self.refreshData)
        QtCore.QObject.connect(self.resourceLibRBProp,
                               QtCore.SIGNAL("clicked(bool)"),
                               self.refreshData)
        QtCore.QObject.connect(self.resourceLibRBScene,
                               QtCore.SIGNAL("clicked(bool)"),
                               self.refreshData)
        QtCore.QObject.connect(self.resourceLibBtnLoad,
                               QtCore.SIGNAL("clicked()"),
                               self.load)
        
        self.shelf.itemSelected.connect(self.getCurrent)
        
        self.refreshProject()
        #config.setProject(config.getProject())
    
    def refreshProject(self, *_):
        if config.getProject(): 
            if not self.resourceLibCBProject.count(): 
                projects = config.getProject(all=True)
                for prj in projects: self.resourceLibCBProject.addItem(prj)
            self.resourceLibCBProject.setCurrentText(config.getProject())
        elif config.getProject(all=True): 
            if not self.resourceLibCBProject.count(): 
                projects = config.getProject(all=True)
                for prj in projects: self.resourceLibCBProject.addItem(prj)
                self.resourceLibCBProject.setCurrentIndex(-1)
            return
        else: 
            while self.resourceLibCBProject.count(): 
                self.resourceLibCBProject.removeItem(0)
            return
        
        try: dom = minidom.parse(config.getPath(config.kConfig, config.getConfig("resourceLocator")))
        except: 
            self.root = None
            self.clearData()
        else: 
            self.clearData()
            
            Asset.pathDefine = {}
            self.assets = []
            self.root = dom.documentElement
            for path in self.root.getElementsByTagName("path"):
                Asset.pathDefine[path.getAttribute("name")] = path.childNodes[0].nodeValue
            
            for item in self.root.getElementsByTagName("item"):
                self.assets.append(Asset(item))
        
            self.shelf.setup(*self.assets)
        
        self.refreshData()
        
    def refreshData(self, *_):
        if not self.root: return
        
        if self.resourceLibRBChar.isChecked(): resType = 'character'
        elif self.resourceLibRBProp.isChecked(): resType = 'property'
        elif self.resourceLibRBScene.isChecked(): resType = 'scene'
        else: return
        
        self.shelf.itemFilter(resType)
        
    def clearData(self):
        self.current = None
        self.shelf.cleanUp()
        self.resourceLibBtnLoad.setEnabled(False)
            
    def getCurrent(self, item):
        self.resourceLibBtnLoad.setEnabled(True)
        self.current = item
        
    def load(self, *_):
        for asset in self.assets:
            if asset.path == self.current:
                if asset.path.count('.ma'): typ = "mayaAscii"
                elif asset.path.count('.mb'): typ = "mayaBinary"
                else: cmds.error('文件类型错误')
                cmds.file(asset.path, r=True, iv=True, typ=typ, ns=asset.namespace)
                return
        

class Asset():
    
    pathDefine = {}
    
    def __init__(self, item):
        self.__tag   = item.getAttribute("tag")
        self.__name  = item.getAttribute("name")
        self.__file  = item.getAttribute("file")
        self.__thumb = item.getAttribute("thumbnail")
        self.__dic   = {}
        
        for p in Asset.pathDefine:
            strList = self.__file.split("%%%s%%"%p)
            if len(strList) > 1: self.__file = Asset.pathDefine[p] + strList[-1]
            
            strList = self.__thumb.split("%%%s%%"%p)
            if len(strList) > 1: self.__thumb = Asset.pathDefine[p] + strList[-1]
        
        self.__dic[ui.QShelfView.kName] = self.label
        self.__dic[ui.QShelfView.kIcon] = self.image
        self.__dic[ui.QShelfView.kData] = self.path
        self.__dic[ui.QShelfView.kType] = self.__tag
    
    def __str__(self):
        return "%s_%s"%(ResourceRepository.UI().window, self.__file.split('/')[-1].split('.ma')[0])
    
    def __getitem__(self, key):
        return self.__dic[key]
        
    def filter(self, *tags):
        for tag in tags:
            if not self.__tag.count(tag):
                return False
        return True
    
    @property
    def label(self):
        if not self.__name:
            return self.__file.split('/')[-1].split('.ma')[0]
        return self.__name
    
    @property
    def image(self):
        if not os.path.isfile(self.__thumb):
            for tp in ["character", "property", "scene"]:
                if self.__tag.count(tp): return config.getPath(config.kIcon, "empty_%s.png"%tp)
            return ""
        return self.__thumb
    
    @property
    def path(self):
        return self.__file
    
    @property
    def namespace(self):
        fileName = self.__file.split('/')[-1]
        if len(fileName.split('.ma')) > 1: return fileName.split('.ma')[0]
        else: return fileName.split('.mb')[0]
        