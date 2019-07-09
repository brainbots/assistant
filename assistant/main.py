#!/usr/bin/env python3

import argparse
import signal
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QTimer

from assistant import Assistant

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Run the keyboard')
  parser.add_argument('--headset', action='store_true', help='collect data from emotiv headset')
  parser.add_argument('--virtual', '--vir', action='store_true', help='get random data')
  parser.add_argument('--flashing_only', action='store_true', help='ignore the bots and nlp parts')
  args = parser.parse_args()
  if not (args.virtual or args.headset or args.flashing_only):
    parser.print_help(sys.stderr)
    sys.exit(2)

  signal.signal(signal.SIGINT, signal.SIG_DFL)
  app = QApplication([])
  app.setOverrideCursor(Qt.BlankCursor)

  main_manager = Assistant(args.virtual, args.flashing_only)
  sys.exit(app.exec())
