import os
import xml.sax
import pymel.core as pm

kIcon = "../commons/icons/"
kBinary = "../commons/bin/"
kUI = "../commons/ui/"


def getPath(key="", f=""):
    '''
    --------------------------------------------------------------------------------
    Provide Framework Paths
    --------------------------------------------------------------------------------
    '''
    path = os.getenv("BARBARIAN_LOCATION")
    return path + key + f


def getHelp():
    '''
    --------------------------------------------------------------------------------
    Provide Framework Help
    --------------------------------------------------------------------------------
    '''
    pm.webView(url=(getPath("../commons/config/", "help.htm")))
    

def getConfig(**kwargs):
    '''
    --------------------------------------------------------------------------------
    Provide Project Configuration
    --------------------------------------------------------------------------------
    '''
    attrList = ["time", "linear", "camera", "camResX", "camResY", "playblastScale", "animLibPath", "facialLibPath"]
    for attr in attrList:
        if attr in kwargs and kwargs[attr]:
            for project in __handler__.config:
                if project["name"] == getProject(): return project[attr]
                
    return None


def setProject(name):
    '''
    --------------------------------------------------------------------------------
    Set Current Project
    --------------------------------------------------------------------------------
    '''
    for project in __handler__.config:
        if project["name"] == name:
            pm.optionVar(sv=("PutaoTools_Project", name))
            pm.optionVar(iv=("PutaoTools_Project_Time", project["time"]))
            pm.optionVar(sv=("PutaoTools_Project_Linear", project["linear"]))
            pm.optionVar(sv=("PutaoTools_Project_Camera", project["camera"]))
            pm.optionVar(iv=("PutaoTools_Project_CamResX", project["camResX"]))
            pm.optionVar(iv=("PutaoTools_Project_CamResY", project["camResY"]))
            pm.optionVar(fv=("PutaoTools_Project_PlayblastScale", project["playblastScale"]))
            pm.optionVar(sv=("PutaoTools_Project_AnimLibPath", project["animLibPath"]))
            pm.optionVar(sv=("PutaoTools_Project_FacialLibPath", project["facialLibPath"]))
            
            pm.condition("ProjectChanged", e=True, state=not pm.condition("ProjectChanged", q=True, state=True))


def getProject(**kwargs):
    '''
    --------------------------------------------------------------------------------
    Get Current Project or List of Projects Available
    --------------------------------------------------------------------------------
    '''
    if "all" in kwargs and kwargs["all"]:
        projects = []
        for project in __handler__.config:
            projects.append(project["name"])
        return projects
    else:
        return pm.optionVar(q="PutaoTools_Project")


class ConfigHandler(xml.sax.ContentHandler):
    '''
    --------------------------------------------------------------------------------
    Class Representing the config.xml
    --------------------------------------------------------------------------------
    '''
    def __init__(self):
        
        self.config = []
        
        self.current = ""
        self.time = ""
        self.linear = ""
        self.camera = ""
        self.camResX = ""
        self.camResY = ""
        self.playblastScale = ""
        self.animLibPath = ""
        self.facialLibPath = ""
    
    def startElement(self, name, attrs):
        xml.sax.ContentHandler.startElement(self, name, attrs)
        self.current = name
        if name == "project":
            self.config.append({"name":attrs["name"]})
            
    def endElement(self, name):
        xml.sax.ContentHandler.endElement(self, name)
        if self.current == "time":
            self.config[len(self.config)-1]["time"] = self.time
        elif self.current == "linear":
            self.config[len(self.config)-1]["linear"] = self.linear
        elif self.current == "camera":
            self.config[len(self.config)-1]["camera"] = self.camera
        elif self.current == "camResX":
            self.config[len(self.config)-1]["camResX"] = self.camResX
        elif self.current == "camResY":
            self.config[len(self.config)-1]["camResY"] = self.camResY
        elif self.current == "playblastScale":
            self.config[len(self.config)-1]["playblastScale"] = self.playblastScale
        elif self.current == "animLibPath":
            self.config[len(self.config)-1]["animLibPath"] = self.animLibPath
        elif self.current == "facialLibPath":
            self.config[len(self.config)-1]["facialLibPath"] = self.facialLibPath
        self.current = ""
        
    def characters(self, content):
        xml.sax.ContentHandler.characters(self, content)
        if self.current == "time":
            self.time = int(content)
        elif self.current == "linear":
            self.linear = content
        elif self.current == "camera":
            self.camera = content
        elif self.current == "camResX":
            self.camResX = int(content)
        elif self.current == "camResY":
            self.camResY = int(content)
        elif self.current == "playblastScale":
            self.playblastScale = float(content)
        elif self.current == "animLibPath":
            self.animLibPath = content
        elif self.current == "facialLibPath":
            self.facialLibPath = content


class Renamer(object):
    '''
    --------------------------------------------------------------------------------
    Class Representing the Rename Tool
    --------------------------------------------------------------------------------
    '''
    win              = "renamerWin"
    renameTextField  = "middleInput"
    prefixTextField  = "prefixInput"
    suffixTextField  = "suffixInput"
    prefixOptionMenu = "prefixCmb"
    prefixCheckBox   = "prefixChk"
    suffixCheckBox   = "suffixChk"
    
    def __init__(self):
        if pm.window(Renamer.win, exists=True):
            pm.deleteUI(Renamer.win)
        
        pm.loadUI(f=getPath(kUI, "renamer.ui"))
        pm.showWindow(Renamer.win)
    
    @classmethod
    def rename(cls):

        prefix_dic = {"Middle": "M", "Left": "L", "Right": "R", "Up": "U",
                     "Down": "D", "Front": "F", "Back": "B"}
    
        dag_type_dic = {"mesh": "Geo",
                        "nurbsSurface": "Nbs",
                        "joint": "Jnt",
                        "clusterHandle": "Cus",
                        "multiplyDivide": "Mul",
                        "plusMinusAverage": "Pma",
                        "locator": "Loc",
                        "distanceDimShape": "Dis",
                        "parentConstraint": "Pat",
                        "orientConstraint": "Oct",
                        "pointConstraint": "Pot",
                        "aimConstraint": "Aim",
                        "poleVectorConstraint": "Pvc",
                        "transform": "GRP",
                        "lattice": "Lie",
                        "baseLattice": "Ble",
                        "ikHandle": "Ikh",
                        "ikEffector": "Ike",
                        "nurbsCurve": "Crv",
                        "deformSine": "Sin",
                        "deformBend": "Ben", }
    
        dg_type_dic = {"aiStandard": "Ais",
                       "aiSkin": "Sss",
                       "aiAmbientOcclusion": "Aao",
                       "aiUtility": "Aut",
                       "lambert": "Lam",
                       "blinn": "Bli",
                       "surfaceShader": "Sfs", }
    
        sels = pm.ls(sl=True)
        
        name = pm.textField(cls.renameTextField, q=True, tx=True)
        options = pm.button(cls.prefixOptionMenu, q=True, v=True)
    
        for sel in sels:
    
            pick_walk = pm.pickWalk(sel, d="down")
            pm.select(sel)
            obj_type = pm.objectType(pick_walk)
    
            num = 1
            new_name = ""
            num_str = "%02d" % num
    
            prefix = prefix_dic[options] + "_"
            tmp_dic = dag_type_dic
            
            for key in dg_type_dic:
                if key == obj_type:
                    prefix = ""
                    tmp_dic = dg_type_dic
                    break
            
            if pm.checkBox(cls.prefixCheckBox, q=True, value=True):
                prefix = pm.textField(cls.prefixTextField, q=True, text=True)
                if prefix: prefix = prefix + "_"
                
            suffix = "_" + num_str + "_" + tmp_dic[obj_type]
            useCustomSuffix = pm.checkBox(cls.suffixCheckBox, q=True, value=True)
            if useCustomSuffix:
                suffix = pm.textField(cls.suffixTextField, q=True, text=True)
                if suffix: suffix = "_" + suffix
            
            new_name = prefix + name + suffix
    
            while not useCustomSuffix and pm.objExists(new_name) and new_name != sel:
                num = num + 1
                num_str = "%02d" % num
                new_name = prefix + name + "_" + \
                    num_str + "_" + tmp_dic[obj_type]
    
            pm.rename(sel, new_name)
    
    @classmethod
    def refresh(cls):
        prefChkState = pm.checkBox(cls.prefixCheckBox, q=True, value=True)
        suffChkState = pm.checkBox(cls.suffixCheckBox, q=True, value=True)
        
        pm.textField(cls.prefixTextField, e=True, enable=prefChkState)
        pm.textField(cls.suffixTextField, e=True, enable=suffChkState)
        pm.button(cls.prefixOptionMenu, e=True, enable=not prefChkState)


'''
--------------------------------------------------------------------------------
Configuration Setup at Maya Startup
--------------------------------------------------------------------------------
'''
try: pm.condition("ProjectChanged", delete=True)
except: pass
pm.condition("ProjectChanged", state=True)

__parser__ = xml.sax.make_parser()
__parser__.setFeature(xml.sax.handler.feature_namespaces, 0)

__handler__ = ConfigHandler()
__parser__.setContentHandler(__handler__)
__parser__.parse(getPath("../commons/config/", "config.xml"))

if not pm.optionVar(exists="PutaoTools_Project"):
    pm.optionVar(sv=("PutaoTools_Project", ""))
    pm.optionVar(iv=("PutaoTools_Project_Time", 0))
    pm.optionVar(sv=("PutaoTools_Project_Linear", ""))
    pm.optionVar(sv=("PutaoTools_Project_Camera", ""))
    pm.optionVar(iv=("PutaoTools_Project_CamResX", 0))
    pm.optionVar(iv=("PutaoTools_Project_CamResY", 0))
    pm.optionVar(fv=("PutaoTools_Project_PlayblastScale", 0.0))
    pm.optionVar(sv=("PutaoTools_Project_AnimLibPath", ""))
    pm.optionVar(sv=("PutaoTools_Project_FacialLibPath", ""))

                 



