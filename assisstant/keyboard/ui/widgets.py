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
      box.setChars(config.CHARS[index])

  def flash(self):
    for box in self.boxes:
      box.startFlashing()

  def unflash(self):
    for box in self.boxes:
      box.stopFlashing()

  def update_handler(self, result):
    new_chars = self.boxes[result].chars
    if len(new_chars) > 1:
      quarter = len(new_chars)//4
      for index in range(4):
        self.boxes[index].setChars(new_chars[index*quarter:index*quarter + quarter])
    else:
      self.lblCmd.setText(self.lblCmd.text() + new_chars)
      for index in range(4):
        self.boxes[index].setChars(config.CHARS[index])

  def flash_handler(self, value):
    if value:
      print("Flash: on")
      self.flash()
    else:
      print("Flash: off")
      self.unflash()
