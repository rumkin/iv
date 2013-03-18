#!/usr/bin/python
# -*- coding: utf-8 -*-
# python2.7
#------------------------------------------------

'''
  TODOLIST
  - Removing
  - Renaming
  - Drag'n'drop to folder
  - Removing unexistant files from roll
  - Selecting (flagging) images
  =
'''

#------------------------------------------------
import sys
import os
from PyQt4 import QtCore, QtGui, uic

Qt = QtCore.Qt

class MainWindow(QtGui.QMainWindow):
  def __init__(self):
    QtGui.QMainWindow.__init__(self)
    uic.loadUi('iv.ui', self)
    self.setWindowTitle()
    self.actionExit.triggered.connect(self.close)
    self.actionOpen.triggered.connect(self.openImageFile)

    self.actionNext.triggered.connect(self.nextImage)
    self.actionPrev.triggered.connect(self.prevImage)

    self.currentDir  = '.'
    self.currentFile = None
    self.pixmap      = False
    self.needRedraw  = False


  def changeDir(self):
    dirname = os.path.dirname("%s" % QtGui.QFileDialog.getOpenFileName(self, 'Open file directory', self.dir))

    if dirname :
      self.currentDir = dirname

  def openImageFile(self):
    imagePath = "%s" % QtGui.QFileDialog.getOpenFileName(self, 'Open image', self.currentDir, "Images (*.png *.jpeg *.jpg)")

    if not imagePath:
      return

    self.setCurrentDir(os.path.dirname(imagePath))
    self.showImageFile(imagePath)

  def setCurrentDir(self, dir):
    if self.currentDir == dir:
      return

    self.currentDir = dir
    self.images = self.getImagesFromDir(dir)
    # TODO trigger changeDir event

  def getImagesFromDir(self, dir):
    files  = os.listdir(dir)
    images = []

    for file in files:
      filepath = u"%s/%s" % (dir, file)

      if not os.path.isfile(filepath):
        continue

      extname = os.path.splitext(file)[-1][1:]
      if not (extname in ["png", "jpg", "jpeg"]):
        continue

      images.append(filepath)


    images.sort()
    return images

  def showImageFile(self, path):
    index = self.images.index(path) + 1
    length = len(self.images)
    self.setWindowTitle("%s - %d/%d" % (os.path.basename(path), index, length))
    self.currentFile = path
    pixmap = QtGui.QPixmap(path)
    self.pixmap = pixmap
    
    self.needRedraw = True
    self.showImage()


  def resizeEvent(self, event):
    if not self.pixmap:
      return

    self.showImage()

  def showImage(self):
    sceneSize = self.imageView.size()
    size = QtCore.QSize(sceneSize.width(), sceneSize.height())

    if size.width() > self.pixmap.width() and size.height() > self.pixmap.height():
      pixmap = self.pixmap
    else:
      pixmap = self.pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    # ambilight = pixmap.transformed(QtGui.QTransformation(), Qt.SmoothTransformation)
    scene  =  QtGui.QGraphicsScene()
    scene.addPixmap(pixmap)
    self.imageView.setScene(scene)

    self.needRedraw = False

  def nextImage(self):
    currentFile = self.currentFile
    if not currentFile:
      return

    index = self.images.index(currentFile)
    if (index < 0 or index >= len(self.images) - 1):
      return

    index += 1

    self.showImageFile(self.images[index])

  def prevImage(self):
    currentFile = self.currentFile
    if not currentFile:
      return

    index = self.images.index(currentFile)
    if (index <= 0 or index > len(self.images)):
      return

    index -= 1

    self.showImageFile(self.images[index])

  def setWindowTitle(self, title = None):
    if title :
      title = "%s - iv" % title
    else:
      title = "iv"

    QtGui.QMainWindow.setWindowTitle(self, title)
   
app = QtGui.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())