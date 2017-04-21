from PyQt5.QtWidgets import QMainWindow
from .keyboard_ui import Ui_KeyboardWindow

class KeyboardWindow(QMainWindow, Ui_KeyboardWindow):
  def __init__(self):
    QMainWindow.__init__(self)
    self.setupUi(self)
