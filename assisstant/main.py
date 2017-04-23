#!/usr/bin/env python3
import sys
import signal
from PyQt5.QtWidgets import QApplication
from keyboard.ui.widgets import KeyboardWindow

if __name__ == '__main__':
  signal.signal(signal.SIGINT, signal.SIG_DFL)
  app = QApplication([])
  window = KeyboardWindow()
  window.showMaximized()
  sys.exit(app.exec())
