class refresh:
  def __init__(self, iv, config):
    iv.actionRefresh.triggered.connect(self.refresh)
    self.iv = iv
    iv.on("initiated", self.ivReady)

  def refresh(self):
    iv = self.iv
    if not iv.current_dir: return

    iv.show_dir(iv.current_dir)

  def ivReady(self, event):

  	print "Refresh packages knows what you did last summer. Event type is '" + event.type + "'"

