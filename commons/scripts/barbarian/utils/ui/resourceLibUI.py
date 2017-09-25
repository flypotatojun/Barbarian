# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:/workspace/PutaoTools/commons/ui/resourceLib.ui'
#
# Created: Mon Sep 25 09:22:57 2017
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
from barbarian.utils import ui, config

class Ui_resourceLibOption(ui.QtUI):
    def setupUi(self, resourceLibOption):
        resourceLibOption.setObjectName("resourceLibOption")
        resourceLibOption.resize(810, 690)
        resourceLibOption.setMinimumSize(QtCore.QSize(810, 690))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        resourceLibOption.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(config.getPath(config.kIcon, "logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        resourceLibOption.setWindowIcon(icon)
        
        self.resourceLibCentralwidget = QtGui.QWidget(resourceLibOption)
        self.resourceLibCentralwidget.setObjectName("resourceLibCentralwidget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.resourceLibCentralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout_2.setObjectName("formLayout_2")
        self.Label = QtGui.QLabel(self.resourceLibCentralwidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.Label.setFont(font)
        self.Label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Label.setObjectName("Label")
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.Label)
        self.resourceLibCBProject = ui.QOptionMenu(self.resourceLibCentralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.resourceLibCBProject.sizePolicy().hasHeightForWidth())
        self.resourceLibCBProject.setSizePolicy(sizePolicy)
        self.resourceLibCBProject.setMinimumSize(QtCore.QSize(85, 30))
        self.resourceLibCBProject.setMaximumSize(QtCore.QSize(85, 16777215))
        self.resourceLibCBProject.setObjectName("resourceLibCBProject")
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.resourceLibCBProject)
        self.Label_2 = QtGui.QLabel(self.resourceLibCentralwidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.Label_2.setFont(font)
        self.Label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Label_2.setObjectName("Label_2")
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.Label_2)
        self.frame_2 = QtGui.QFrame(self.resourceLibCentralwidget)
        self.frame_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame_2)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.resourceLibRBChar = QtGui.QRadioButton(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.resourceLibRBChar.setFont(font)
        self.resourceLibRBChar.setChecked(True)
        self.resourceLibRBChar.setObjectName("resourceLibRBChar")
        self.horizontalLayout.addWidget(self.resourceLibRBChar)
        self.resourceLibRBProp = QtGui.QRadioButton(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.resourceLibRBProp.setFont(font)
        self.resourceLibRBProp.setObjectName("resourceLibRBProp")
        self.horizontalLayout.addWidget(self.resourceLibRBProp)
        self.resourceLibRBScene = QtGui.QRadioButton(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.resourceLibRBScene.setFont(font)
        self.resourceLibRBScene.setObjectName("resourceLibRBScene")
        self.horizontalLayout.addWidget(self.resourceLibRBScene)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.frame_2)
        self.verticalLayout_2.addLayout(self.formLayout_2)
        
        self.shelf = ui.QShelfView(self.resourceLibCentralwidget)
        self.verticalLayout_2.addWidget(self.shelf)
        
        self.resourceLibBtnLoad = QtGui.QPushButton(self.resourceLibCentralwidget)
        self.resourceLibBtnLoad.setMinimumSize(QtCore.QSize(0, 50))
        self.resourceLibBtnLoad.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.resourceLibBtnLoad.setFont(font)
        self.resourceLibBtnLoad.setObjectName("resourceLibBtnLoad")
        self.verticalLayout_2.addWidget(self.resourceLibBtnLoad)
        self.verticalLayout_2.setStretch(1, 1)
        resourceLibOption.setCentralWidget(self.resourceLibCentralwidget)

        self.retranslateUi(resourceLibOption)
        QtCore.QMetaObject.connectSlotsByName(resourceLibOption)

    def retranslateUi(self, resourceLibOption):
        resourceLibOption.setWindowTitle(QtGui.QApplication.translate("resourceLibOption", "资产库", None, QtGui.QApplication.UnicodeUTF8))
        self.Label.setText(QtGui.QApplication.translate("resourceLibOption", "项目：", None, QtGui.QApplication.UnicodeUTF8))
        self.Label_2.setText(QtGui.QApplication.translate("resourceLibOption", "类型：", None, QtGui.QApplication.UnicodeUTF8))
        self.resourceLibRBChar.setText(QtGui.QApplication.translate("resourceLibOption", "角色", None, QtGui.QApplication.UnicodeUTF8))
        self.resourceLibRBProp.setText(QtGui.QApplication.translate("resourceLibOption", "道具", None, QtGui.QApplication.UnicodeUTF8))
        self.resourceLibRBScene.setText(QtGui.QApplication.translate("resourceLibOption", "场景", None, QtGui.QApplication.UnicodeUTF8))
        self.resourceLibBtnLoad.setText(QtGui.QApplication.translate("resourceLibOption", "加载", None, QtGui.QApplication.UnicodeUTF8))
