#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QApplication
from keyboard.ui.widgets import KeyboardWindow

if __name__ == '__main__':
  app = QApplication([])
  window = KeyboardWindow()
  window.showMaximized()
  sys.exit(app.exec())
