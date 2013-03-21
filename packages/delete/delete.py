# /home/YOURUSERFOLDER/.local/share/Trash/files/

import os
from time import strftime, localtime
import shutil
from PyQt4 import QtCore, QtGui, Qt

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


class delete:
  def __init__(self, iv, config):
    self.iv = iv
    print "Config is loaded:"
    print config['message']

    iv.actionRemove.triggered.connect(self.delete_file)

  def delete_file(self):
    iv = self.iv
    file_path = iv.photo_roll.current

    if not file_path: return
    #confirm dialog
    confirm = Qt.QMessageBox(Qt.QMessageBox.Warning, "Move to Trash",
       "Are you sure to move this file to trash?",
       Qt.QMessageBox.Ok|Qt.QMessageBox.Cancel,
       iv).exec_()
    
    if confirm != Qt.QMessageBox.Ok: return

    moveToTrash(file_path)
    iv.packages['refresh'].refresh()

  def close(self):
    print "Delete is closed"
