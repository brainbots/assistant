from PyQt5.QtWidgets import QMainWindow
from .keyboard_ui import Ui_KeyboardWindow

class KeyboardWindow(QMainWindow, Ui_KeyboardWindow):
  def __init__(self):
    super(KeyboardWindow, self).__init__()
    self.setupUi(self)
    self.top_left.startFlashing()
    self.top_right.startFlashing()
    self.bottom_left.startFlashing()
    self.bottom_right.startFlashing()
    self.undo.startFlashing()
