#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import random
from PyQt4 import QtCore, QtGui

class Button(QtGui.QWidget) :

  clicked = QtCore.pyqtSignal()

  def __init__(self):
    QtGui.QWidget.__init__(self)
    self.setMinimumSize(1, 15)
    self.shouldRedraw = True

  def mousePressEvent(self, event):
    self.setFocus(QtCore.Qt.OtherFocusReason)
    event.accept()

  def mouseReleaseEvent(self, event):
    if event.button() == QtCore.Qt.LeftButton:
      self.update()
      self.clicked.emit()
      event.accept()

  def toggleDraw(self) :
    self.shouldRedraw = not self.shouldRedraw

  def paintEvent(self, event):

    if self.shouldRedraw == False: return

    painter = QtGui.QPainter()
    painter.begin(self)

    color = QtGui.QColor(random.randrange(150, 255), random.randrange(150, 255), random.randrange(150, 255))
    rect  = QtCore.QRect(0, 0, self.width(), self.height())
    painter.fillRect(rect, color)

    color = QtGui.QColor(random.randrange(150, 255), random.randrange(150, 255), random.randrange(150, 255))
    rect  = QtCore.QRect(self.width()/2 - 10, self.height()/2 - 10, 20, 20)
    painter.fillRect(rect, color)

    painter.end()


class widget() :

  def __init__(self, iv, config):
    button = Button()
    button.clicked.connect(button.toggleDraw)
    
    # iv.verticalLayout.addWidget(button)
