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
    self.setWindowTitle()

    self.actionOpen.triggered.connect(self.open_file)
    self.actionNext.triggered.connect(self.next_image)
    self.actionPrev.triggered.connect(self.prev_image)
    # TODO move to "refresh" package
    self.actionRefresh.triggered.connect(self.refresh)
    
    self.current_dir = '.'
    self.extensions = ['jpg', 'jpeg', 'png']
    self.photo_roll = photoRoll([])

    self.init_packages()

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

  def show_dir(self, dir):
    self.current_dir = dir

    images = self.get_images_from_dir(self.current_dir)
    images.sort()

    # Create photo roll
    roll = photoRoll(images)
    
    self.photo_roll = roll
    if not roll.length:
      self.clear_view()
    else:
      self.show_image(roll.current)

  def next_image(self):
    image = self.photo_roll.next
    if not image: return

    self.show_image(image)

  def prev_image(self):
    image = self.photo_roll.prev
    if not image: return

    self.show_image(image)

  def show_image(self, path):
    index  = self.photo_roll.index_of(path)
    length = self.photo_roll.length

    if index is False:
      self.setWindowTitle("%s" % os.path.basename(path))
    else :
      self.setWindowTitle("%s - %s/%s" % (os.path.basename(path), index + 1, length))

    scene  = QtGui.QGraphicsScene()
    try:
      rect   = self.imageView.rect()
      pixmap = QtGui.QPixmap(path)
      if pixmap.width() > rect.width() or pixmap.height() > rect.height():
        pixmap = pixmap.scaled(rect.width(), rect.height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

      scene.addPixmap(pixmap)
    except Exception, e:
      raise e
    finally:
      self.imageView.setScene(scene)

  def clear_view(self):
    scene = QtGui.QGraphicsScene()
    self.imageView.setScene(scene)
  
  def refresh(self):
    self.show_dir(self.current_dir)

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


  @property
  def iv_dirs(self):
    return [
      os.getenv('HOME') + '/.config/iv',
      '/usr/local/iv',
      '.'
    ]

  #----------------------------------------------------------------------------
  # packages
  #----------------------------------------------------------------------------
  
  def find_packages(self):
    found_packages = {}
    
    for iv_dir in self.iv_dirs :
      package_dir = iv_dir + "/packages"
      if not os.path.isdir(package_dir): continue

      packages = os.listdir(package_dir)
      for package in packages:
        if package in found_packages: continue

        package_file = package_dir + "/" + package + "/" + package + ".py"
        if not os.path.isfile(package_file) : continue

        found_packages[package] = package_dir + "/" + package

    return found_packages



  def init_packages(self):
    packages          = {}
    package_list      = self.find_packages()
    self.package_list = package_list

    for package in package_list:
      package_path = package_list[package]
      # import package
      sys.path.append(package_path)
      module = __import__(package)

      # TODO remove path from sys.path (?)
      config = self.get_package_config(package)
      # initialize package
      instance = getattr(module, package)(self, config)
      packages[package] = instance
      print "Package %s" % (package)

  # Load currently found package's config json file
  def get_package_config(self, package):
    config = ""
    config_path = self.package_list[package] + "/" + package + ".json"
    
    if not os.path.isfile(config_path): return {}

    comment_re = re.compile('\s*//')
    with open(config_path, "r") as f:
      for line in f:
        if not comment_re.match(line):
          config += line
    f.closed

    return json.loads(config)



  #----------------------------------------------------------------------------
  # QtGui.QWindow functions overloading
  #----------------------------------------------------------------------------
  
  def resizeEvent(self, event):
    image = self.photo_roll.current
    if not image: return

    self.show_image(image)
    

  def setWindowTitle(self, title = None):
    if title:
      title = "%s - iv" % title
    else:
      title = "iv"

    return QtGui.QMainWindow.setWindowTitle(self, title)



# Photoroll class holding list of images to show
class photoRoll:
  def __init__(self, images):
    self.images   = images
    self._current = 0

  @property
  def next(self):
    if self._current >= len(self.images) - 1: return None

    self._current += 1
    return self.images[self._current]

  @property
  def current(self):
    if self._current >= len(self.images) : return None
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

  def index_of(self, image):
    if not image in self.images: return False
    return self.images.index(image)

  def set_current(self, filename):
    if not self.has(filename): raise Exception("File not in roll")

    self._current = self.images.index(filename)

app = QtGui.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())