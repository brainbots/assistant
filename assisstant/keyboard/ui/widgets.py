import os
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUiType

dir_path = os.path.dirname(os.path.realpath(__file__))
xmlPath = "{}/keyboard.ui".format(dir_path)
uiKeyboard, _ = loadUiType(xmlPath)

class KeyboardWindow(QMainWindow, uiKeyboard):
  def __init__(self):
    QMainWindow.__init__(self)
    self.setupUi(self)
