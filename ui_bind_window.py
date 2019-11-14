# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_bind_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_BindWindow(object):
    def setupUi(self, BindWindow):
        BindWindow.setObjectName("BindWindow")
        BindWindow.resize(330, 400)
        self.verticalLayout = QtWidgets.QVBoxLayout(BindWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listWidget = QtWidgets.QListWidget(BindWindow)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)

        self.retranslateUi(BindWindow)
        QtCore.QMetaObject.connectSlotsByName(BindWindow)

    def retranslateUi(self, BindWindow):
        _translate = QtCore.QCoreApplication.translate
        BindWindow.setWindowTitle(_translate("BindWindow", "Bind Window"))

