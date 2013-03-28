from PyQt4 import QtCore

'''
  TODOLIST
  - Add zoom center
  - Save zoom on resize
  =
'''

class zoom:
  
  zoom   = 1
  config = {}

  def __init__(self, iv, config):
    self.iv     = iv
    self.config = config
    for name in config:
      self.config[name] = config[name]
    
    iv.actionZoom_In.triggered.connect(self.on_zoom_in)
    iv.actionZoom_Out.triggered.connect(self.on_zoom_out)
    iv.on("image.changed", self.on_restore)
  

  def on_restore(self, event):
    self.zoom = 1

  def on_zoom_in(self, event):
    iv = self.iv

    if not iv.current_pixmap:
      return

    zoom = self.zoom * 1.5
    rect = iv.imageView.rect()

    if (rect.width() * zoom > self.config['max_width']):
      return
    if (rect.height() * zoom > self.config['max_height']):
      return

    pixmap    = iv.current_pixmap.scaled(rect.width() * zoom, rect.height() * zoom, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
    self.zoom = zoom
    iv.show_pixmap(pixmap)
    # TODO scroll to previous center

  def on_zoom_out(self, event):
    iv = self.iv
    if not iv.current_pixmap:
      return

    zoom = self.zoom / 1.5
    rect = iv.imageView.rect()

    if (rect.width() * zoom < self.config['min_width']):
      return

    if (rect.height() * zoom < self.config['min_height']):
      return

    self.zoom = zoom
    pixmap = iv.current_pixmap.scaled(rect.width() * zoom, rect.height() * zoom, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
    iv.show_pixmap(pixmap)
