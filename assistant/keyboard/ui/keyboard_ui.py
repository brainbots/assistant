# -*- coding: utf-8 -*-

import settings
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont
from .components import FlashingBox

class Ui_KeyboardWindow(object):
    def setupUi(self, KeyboardWindow):
        KeyboardWindow.setObjectName("KeyboardWindow")
        KeyboardWindow.resize(769, 506)
        KeyboardWindow.setStyleSheet("background: black")
        self.centralWidget = QtWidgets.QWidget(KeyboardWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.vertLayout = QtWidgets.QVBoxLayout()
        self.vertLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.vertLayout.setContentsMargins(0, 0, 0, 0)
        self.vertLayout.setSpacing(0)
        self.vertLayout.setObjectName("vertLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        
        self.gridLayout.setContentsMargins(settings.GRIDLAYOUT_MARGIN,
                                           settings.GRIDLAYOUT_MARGIN,
                                           settings.GRIDLAYOUT_MARGIN,
                                           settings.GRIDLAYOUT_MARGIN)
        self.gridLayout.setSpacing(settings.GRIDLAYOUT_SPACING)
        self.gridLayout.setObjectName("gridLayout")
        self.top_left = FlashingBox(self.centralWidget)
        self.top_left.setObjectName("top_left")
        self.gridLayout.addWidget(self.top_left, 0, 0, 1, 1)
        self.top_right = FlashingBox(self.centralWidget)
        self.top_right.setObjectName("top_right")
        self.gridLayout.addWidget(self.top_right, 0, 1, 1, 1)
        self.bottom_left = FlashingBox(self.centralWidget)
        self.bottom_left.setObjectName("bottom_left")
        self.gridLayout.addWidget(self.bottom_left, 1, 0, 1, 1)
        self.bottom_right = FlashingBox(self.centralWidget)
        self.bottom_right.setObjectName("bottom_right")
        self.gridLayout.addWidget(self.bottom_right, 1, 1, 1, 1)
        self.vertLayout.addLayout(self.gridLayout)
        self.horzLayout = QtWidgets.QHBoxLayout()
        self.horzLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horzLayout.setContentsMargins(0, 0, 0, 0)
        self.horzLayout.setSpacing(0)
        self.horzLayout.setObjectName("horzLayout")
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        # sizePolicy.setHeightForWidth(self.lblCmd.sizePolicy().hasHeightForWidth())
        # sizePolicy.setFixedSize(True)

        self.lblCmd = QtWidgets.QTextEdit(self.centralWidget)
        self.lblCmd.setSizePolicy(sizePolicy)
        self.lblCmd.setStyleSheet("color: white;")
        self.lblCmd.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        # self.lblCmd.setWordWrap(True)
        self.lblCmd.setMinimumSize(QtCore.QSize(0, 100))
        self.lblCmd.setMaximumSize(QtCore.QSize(2000, 100))
        self.lblCmd.setObjectName("lblCmd")
        self.lblCmd.setFont(QFont("Mono", 40))
        self.lblCmd.setFrameStyle(1)
        self.lblCmd.setReadOnly(True)
        self.horzLayout.addWidget(self.lblCmd)
        
        self.undo = QtWidgets.QLabel(self.centralWidget)
        self.undo.setSizePolicy(sizePolicy)
        self.undo.setMinimumSize(QtCore.QSize(0, 100))
        self.undo.setObjectName("undo")
        self.horzLayout.addWidget(self.undo)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setVerticalStretch(4)
        # self.gridLayout.setSizePolicy(sizePolicy)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setVerticalStretch(1)
        # self.horzLayout.setSizePolicy(sizePolicy)
        self.vertLayout.addLayout(self.horzLayout)
        
        self.verticalLayout_2.addLayout(self.vertLayout)
        self.undo.setStyleSheet("color: white;")
        self.undo.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.undo.setWordWrap(True)
        self.undo.setObjectName("undo")
        self.undo.setFont(QFont("Mono", 26))
        self.undo.setFrameStyle(1)

        self.timer_lbl = QtWidgets.QLabel(self.centralWidget)
        self.timer_lbl.setStyleSheet("color: white;")
        self.timer_lbl.setText("5")
        self.timer_lbl.setFont(QFont("Mono", 26))
        self.timer_lbl.hide()


        KeyboardWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(KeyboardWindow)
        QtCore.QMetaObject.connectSlotsByName(KeyboardWindow)

    def retranslateUi(self, KeyboardWindow):
        _translate = QtCore.QCoreApplication.translate
        KeyboardWindow.setWindowTitle(_translate("KeyboardWindow", "Brain Keyboard"))
        self.lblCmd.setText(_translate("KeyboardWindow", ""))

