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
import shutil
from time import strftime, localtime
from PyQt4 import QtCore, QtGui, Qt, uic

# /home/YOURUSERFOLDER/.local/share/Trash/files/

trashDir = os.getenv("HOME") + "/.local/share/Trash"

def moveToTrash(filename):
  if not os.path.exists(filename):
    return

  if not os.path.exists(trashDir):
    return

  trashInfo  = trashDir + "/info/" + os.path.basename(filename) + ".trashinfo"
  trashFiles = trashDir + "/files"

  with open(trashInfo, "w") as info:
    content = '[Trash Info]\r\nPath=' + filename +'\r\nDeletetionDate=' + strftime("%Y-%m-%dT%H:%M:%S", localtime()) + '\r\n'
    info.write(content)
  info.closed

  shutil.move(filename, trashFiles)


class MainWindow(QtGui.QMainWindow):
  def __init__(self):
    QtGui.QMainWindow.__init__(self)
    uic.loadUi('iv.ui', self)
    self.setWindowTitle()
    self.actionExit.triggered.connect(self.close)
    self.actionOpen.triggered.connect(self.openImageFile)

    self.actionNext.triggered.connect(self.nextImage)
    self.actionPrev.triggered.connect(self.prevImage)
    self.actionRemove.triggered.connect(self.removeImage)
    self.actionRefresh.triggered.connect(self.refresh)

    self.currentDir  = '.'
    self.currentFile = None
    self.currentImageIndex = 0
    self.pixmap      = False
    self.needRedraw  = False

    self.loadPlugins()

  def loadPlugins(self):
    # TODO Specify directory

    pluginDir = "plugins"
    
    files = os.listdir(pluginDir)
    for file in files:
      pluginPath = pluginDir + "/" + file + "/" + file
      
      if os.path.exists(pluginPath + ".py"):
        sys.path.append(pluginDir + "/" + file + "/")
        plugin = __import__(file)
        getattr(plugin, file)(self)


  def openImageFile(self):

    dialog = QtGui.QFileDialog()
    dialog.setFileMode(QtGui.QFileDialog.AnyFile)

    imagePath = unicode(dialog.getOpenFileName(self, 'Open image', self.currentDir, "Images (*.png *.jpeg *.jpg)"))

    if not imagePath:
      return

    self.setCurrentDir(os.path.dirname(imagePath))
    index = self.images.index(imagePath)
    self.showImageAt(index)

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
    images = self.images

    if (not path in images):
      return

    index  = self.images.index(path) + 1
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
      pixmap = self.pixmap.scaled(size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

    # ambilight = pixmap.transformed(QtGui.QTransformation(), Qt.SmoothTransformation)
    scene  =  QtGui.QGraphicsScene()
    scene.addPixmap(pixmap)
    self.imageView.setScene(scene)

    self.needRedraw = False

  def clearImageView(self):
    scene = QtGui.QGraphicsScene()
    self.imageView.setScene(scene)
    self.needRedraw = False

  def fileNotFoundDisplay(self, filepath):
    self.setWindowTitle("Not found: %s - %d/%d" % (os.path.basename(filepath), self.currentImageIndex + 1, len(self.images)))
    self.clearImageView()

  def showImageAt(self, index) :

    if (index >= len(self.images)):
      index = len(self.images) -1
    elif (index < 0):
      index = 0

    filepath = self.images[index]
    if (self.currentFile == filepath):
      return
    self.currentFile       = filepath
    self.currentImageIndex = index

    if not os.path.exists(filepath):
      self.actionRemove.setEnabled(False)
      self.fileNotFoundDisplay(filepath)
    else :
      self.actionRemove.setEnabled(True)
      self.showImageFile(filepath)

  def nextImage(self):
    currentFile = self.currentFile
    if not currentFile:
      return

    index = self.images.index(currentFile)
    if (index < 0 or index >= len(self.images) - 1):
      return

    index += 1

    self.showImageAt(index)

  def prevImage(self):
    currentFile = self.currentFile
    if not currentFile:
      return

    index = self.images.index(currentFile)
    if (index <= 0 or index > len(self.images)):
      return

    index -= 1

    self.showImageAt(index)

  def refresh(self):
    dir = self.currentDir
    filename = self.currentFile
    index    = self.currentImageIndex
    images   = self.getImagesFromDir(dir)

    self.images = images
    imagesLength = len(images)

    if (filename in images):
      self.showImageFile(filename)
    elif (len(images) > index):
      self.showImageAt(index)
    elif (index > imagesLength and imagesLength > 0):
      self.showImageAt(imagesLength - 1)
    else :
      self.showImageAt(0)

  def setWindowTitle(self, title = None):
    if title :
      title = "%s - iv" % title
    else:
      title = "iv"

    QtGui.QMainWindow.setWindowTitle(self, title)

  def removeImage(self):
    result = Qt.QMessageBox(Qt.QMessageBox.Warning, "Move to Trash",
       "Are you sure to move this file to trash?",
       Qt.QMessageBox.Ok|Qt.QMessageBox.Cancel,
       self).exec_()

    if (result != Qt.QMessageBox.Ok) :
      return

    # Remove image
    moveToTrash(self.currentFile)
    self.refresh()




app = QtGui.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())