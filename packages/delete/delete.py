# /home/YOURUSERFOLDER/.local/share/Trash/files/

import os
from time import strftime, localtime
import shutil
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
  	print config['message']

  def close(self):
    print "Delete is closed"
