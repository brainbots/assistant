#!/usr/bin/env python3

import getopt
import signal
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QTimer

from assistant import Assistant

if __name__ == '__main__':
  try:
    opts, args = getopt.getopt(sys.argv[1:], "", ['headset', 'virtual'])
    if len(opts) == 0:
      print("--headset or --virtual?")
      sys.exit(2)
    for opt in opts:
      opt = opt[0]
      if opt == '--headset':
        is_virtual = False
      elif opt == '--virtual' or opt == '--v':
        is_virtual = True
  except getopt.GetoptError as err:
    print(err)
    sys.exit(2)

  signal.signal(signal.SIGINT, signal.SIG_DFL)
  app = QApplication([])
  app.setOverrideCursor(Qt.BlankCursor)

  main_manager = Assistant(is_virtual)
  sys.exit(app.exec())