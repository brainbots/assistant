from PyQt5.QtCore import Qt

USER = "AmrMohamed"
FREQ = [
	6.666666666666667,
#	12.195121951219512,
	5.882352941,
	10,
	7.575757575757576
]
# fifth freq 
# 8.620689655172415
# 
# TODO: Adjust colors
COLOR   =   [Qt.green, Qt.green, Qt.green, Qt.green, Qt.black]
TIME_FLASH_SEC  = 3 
TIME_REST_SEC   = 4
ANIMATION_DURATION = 300
GRIDLAYOUT_MARGIN = 0
GRIDLAYOUT_SPACING = 100
# CHARS = ["ABCDQRST",
#          "EFGHUVWX",
#          "IJKLYZ.,",
#          "MNOP\"'?⏎",
#          "1234$@^!",
#          "5678~_|&",
#          "90-+()[]",
#          "*/^=<>{}"]



CHARS = ["abcdqrst",
         "efghuvwx",
         "ijklyz.,",
         "mnop\"'?⏎",
         "1234$@^!",
         "5678~_|&",
         "90-+()[]",
         "*/^=<>{}"]

AUTOCOMPLETE_BACKEND = "keyboard.autocomplete.backends.autocomplete.AutoComplete"
