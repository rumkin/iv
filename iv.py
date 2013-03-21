#!/usr/bin/python
# -*- coding: utf-8 -*-
# python2.7
#------------------------------------------------

'''
  TODOLIST
  . Removing
  . Renaming
  . Drag'n'drop to folder
  + Removing unexistant files from roll
  . Selecting (flagging) images
  =
'''

#------------------------------------------------
import sys
import os
import json
import re
from PyQt4 import QtCore, QtGui, Qt, uic

class MainWindow(QtGui.QMainWindow):
  def __init__(self):
    QtGui.QMainWindow.__init__(self)
    uic.loadUi('iv.ui', self)

    self.actionOpen.triggered.connect(self.openDir)

  def openDir(self):
    print "THERE"



app = QtGui.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())