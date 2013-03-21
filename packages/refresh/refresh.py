class refresh:
  def __init__(self, iv, config):
    iv.actionRefresh.triggered.connect(self.refresh)
    self.iv = iv

  def refresh(self):
    iv = self.iv
    if not iv.current_dir: return

    iv.show_dir(iv.current_dir)

