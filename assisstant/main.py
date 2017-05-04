#!/usr/bin/env python3
import sys
import signal
from PyQt5.QtWidgets import QApplication
from keyboard.ui.widgets import KeyboardWindow
from keyboard.manager import Manager

if __name__ == '__main__':
  signal.signal(signal.SIGINT, signal.SIG_DFL)
  app = QApplication([])
  window = KeyboardWindow()
  window.showMaximized()
  manager = Manager()
  manager.flash_signal.connect(window.flash_handler)
  manager.update_signal.connect(window.update_handler)
  window.ui_pause.connect(manager.pause_handler)
  manager.start()
  sys.exit(app.exec())
