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

    self.current_dir = '.'
    self.actionOpen.triggered.connect(self.open_file)
    self.extensions = ['jpg', 'jpeg', 'png']

    # Pre log
    # print "Current dir: %s" % self.current_dir

  def open_file(self):
    filename = unicode(QtGui.QFileDialog.getOpenFileName(self, 'Open image', self.current_dir, "Images (*.png *.jpeg *.jpg)"))
    if not filename : return

    self.current_dir = os.path.dirname(filename)

    # Get current directory images
    images = self.get_images_from_dir(self.current_dir)
    images.sort()

    # Create photo roll
    roll = photoRoll(images)
    roll.set_current(filename)
    
    self.photo_roll = roll
    self.show_image(roll.current)
    # print "Images %s" % roll.images
    # print "Current %s" % roll.current
    # print "First %s" % roll.first
    # print "Last %s" % roll.last
    # print "Next %s" % roll.next
    # print "Prev %s" % roll.prev
    # print "Length %s" % roll.length

  def show_image(self, path):
    pixels = QtGui.QPixmap(path)
    scene  = QtGui.QGraphicsScene()
    rect   = self.imageView.rect()
    
    scene.addPixmap(pixels.scaled(rect.width(), rect.height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
    self.imageView.setScene(scene)
    

  def get_images_from_dir(self, dirname):

    all_files = os.listdir(dirname)
    images    = []

    for file_name in all_files :
      file_path = dirname + "/" + file_name

      if not os.path.isfile(file_path): continue
      
      ext_name = os.path.splitext(file_name)[-1]
      if not len(ext_name): continue

      ext_name = ext_name[1:].lower()
      if not ext_name in self.extensions: continue

      images.append(file_path)

    return images

# Photoroll class holding list of images to show
class photoRoll:
  def __init__(self, images):
    self.images   = images
    self._current = 0

  @property
  def next(self):
    if self._current >= len(self.images) - 1: return None

    self._current += 1
    print "Current %d" % self._current
    print "Length %d" % len(self.images)
    return self.images[self._current]

  @property
  def current(self):
    return self.images[self._current]

  @property
  def prev(self):
    if self._current < 1: return None

    self._current -= 1
    return self.images[self._current]

  @property
  def first(self):
    if (len(self.images) < 1): return None

    return self.images[0]

  @property
  def last(self):
    if not len(self.images): return None

    return self.images[len(self.images) - 1]

  @property
  def length(self):
    return len(self.images)


  def has(self, image):
    return image in self.images

  def set_current(self, filename):
    if not self.has(filename): raise Exception("File not in roll")

    self._current = self.images.index(filename)

app = QtGui.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())