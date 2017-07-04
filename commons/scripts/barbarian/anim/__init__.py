﻿from pymel.core import *
from barbarian.utils import *
from pymel.internal.pmcmds import file


def cmdCameraOperation(option):
    if option == "create":
        pass
    elif option == "lock":
        pass
    elif option == "delete":
        pass


class PlayblastOption():
    
    win = "playblastOptionDialog"
    textField = "playblastNameInput"
    defaultCB = "playblastCBDefault"
    
    @classmethod
    def UI(cls):
        if window(cls.win, exists=True): deleteUI(cls.win)
        loadUI(f=getPath(kUI, "playblastoption.ui"))
        showWindow(cls.win)
        if not optionVar(exists="PutaoTools_HUD_Animator"):
            checkBox(cls.defaultCB, e=True, value=True)
            textField(cls.textField, e=True, enable=False)
        else:
            checkBox(cls.defaultCB, e=True, value=False)
            textField(cls.textField, e=True, tx=optionVar(q="PutaoTools_HUD_Animator"))
      
    @classmethod
    def changeHUDName(cls, pb=False):
        name = textField(cls.textField, q=True, tx=True)
        if checkBox(cls.defaultCB, q=True, value=True):
            optionVar(remove="PutaoTools_HUD_Animator")
        else:
            optionVar(sv=("PutaoTools_HUD_Animator", name))
            
        if pb: cls.playblast()
        
    @classmethod
    def refreshUI(cls):
        if checkBox(cls.defaultCB, q=True, value=True): 
            textField(cls.textField, e=True, enable=False)
        else: 
            textField(cls.textField, e=True, enable=True)
    
    @classmethod
    def playblast(cls):
        
        cls.__clearHUD__()
        
        headsUpDisplay("HUD_Time", section=1, block=0, label="Date:",
                       dataFontSize="large", 
                       labelFontSize="large", 
                       blockSize="large", 
                       command=cls.__time__, attachToRefresh=True)
        
        headsUpDisplay("HUD_File", section=2, block=0, label="",
                       dataFontSize="large", 
                       labelFontSize="large", 
                       blockSize="large", 
                       command=cls.__file__, attachToRefresh=True)
        
        headsUpDisplay("HUD_Animator", section=4, block=0, label="Animator:",
                       dataFontSize="large", 
                       labelFontSize="large", 
                       blockSize="large", 
                       command=cls.__animator__, attachToRefresh=True)
        
        headsUpDisplay("HUD_Camera", section=7, block=0, label="Camera:",
                       dataFontSize="large", 
                       labelFontSize="large", 
                       blockSize="large", 
                       command=cls.__camera__, attachToRefresh=True)
        
        headsUpDisplay("HUD_Frame", section=9, block=0, label="Frame:",
                       dataFontSize="large", 
                       labelFontSize="large", 
                       blockSize="large", 
                       command=cls.__frame__, attachToRefresh=True)
        
        mel.eval("pyPBMpeg")
        cls.__clearHUD__()
        
    @classmethod
    def __clearHUD__(cls):
        for i in range(0, 10):
            headsUpDisplay(rp=[i,0])
        
    @classmethod
    def __frame__(cls):
        start = playbackOptions(q=True, min=True)
        end = playbackOptions(q=True, max=True)
        return "%d(%d-%d)"%(currentTime(q=True), start, end)
    
    @classmethod
    def __animator__(cls):
        if optionVar(exists="PutaoTools_HUD_Animator"):
            return optionVar(q="PutaoTools_HUD_Animator")
        else:
            import getpass
            return getpass.getuser()
        
    @classmethod
    def __file__(cls):
        return file(q=1, sn=1, shn=1).split(".")[0]
    
    @classmethod
    def __camera__(cls):
        panel = getPanel(withFocus=True)
        panelType = getPanel(typeOf=panel)
        views = getPanel(type="modelPanel")
        if not mel.eval("gmatch \"%s\" \"modelPanel*\";"%panelType):
            panel = views[0]
        
        camera = modelPanel(panel, q=True, camera=True)
        cameraShape = listRelatives(camera, shapes=True)
        if cameraShape: camera = cameraShape[0]
        focalLength = getAttr(camera+".focalLength")
        return "%s/%s"%(modelPanel(panel, q=True, camera=True), focalLength)
    
    @classmethod
    def __time__(cls):
        import datetime
        now = datetime.datetime.now()
        return now.strftime('%Y-%m-%d')


def cmdKeyframe():
    try: offset = int(textField("animOffsetInput", q=True, tx=True))
    except:
        confirmDialog(message=u'请输入有效数值：负值为向左移动，正值为向右移动',ma="center", 
                      icon="information", title=u"", button=['Confirm'], defaultButton='Confirm')
        return
    
    animCurves = []
    for ac in ls(type="animCurveTL"): animCurves.append(ac)
    for ac in ls(type="animCurveTA"): animCurves.append(ac)
    for ac in ls(type="animCurveTU"): animCurves.append(ac)
    
    if not len(animCurves): 
        confirmDialog(message=u'未找到关键帧信息',ma="center", 
                      icon="information", title=u"", button=['Confirm'], defaultButton='Confirm')
        return
    
    progressWindow(title=u"进度", status=u"处理中...")
    progressWindow(e=True, progress=0, max=len(animCurves))
    
    for ac in animCurves:
        select(ac, r=True)
        keyframe(edit=True, relative=True, timeChange=offset)
        progressWindow(e=True, step=1)
        
    select(clear=True)
    progressWindow(endProgress=1)
    
    tc = mel.eval("$tmpVar = $gPlayBackSlider;")
    sound = timeControl(tc, q=True, sound=True)
    if sound: setAttr(sound+".offset", getAttr(sound+".offset")+offset)

