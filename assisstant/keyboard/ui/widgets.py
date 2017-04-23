from PyQt5.QtWidgets import QMainWindow
from .keyboard_ui import Ui_KeyboardWindow
from keyboard import config

class KeyboardWindow(QMainWindow, Ui_KeyboardWindow):
  def __init__(self):
    super(KeyboardWindow, self).__init__()
    self.setupUi(self)
    self.boxes = [self.top_left, self.top_right, self.bottom_left, self.bottom_right, self.undo]

    for index, box in enumerate(self.boxes):
      box.setFreq(config.FREQ[index])
      box.setColor(config.COLOR[index])
