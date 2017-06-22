from PyQt5.QtCore import Qt

USER = "AmrMohamed"

# === Keyboard Settings ===

FREQ = [
	6.666666666666667,
	5.882352941,
	10,
	7.575757575757576
]
# fifth freq 
# 12.195121951219512,
# 8.620689655172415
# 

COLOR   =   [Qt.green, Qt.green, Qt.green, Qt.green, Qt.black]

TIME_FLASH_SEC  = 1
TIME_REST_SEC   = 0.3
ANIMATION_DURATION = 300
GRIDLAYOUT_MARGIN = 0
GRIDLAYOUT_SPACING = 100

CHARS = ["abcdqrst",
         "efghuvwx",
         "ijklyz.,",
         "mnop\"'?&",
         "1234⌫@$!",
         "5678~_{}",
         "90-+()[␣",
         "*/^=<>]⏎"]

# === Autocomplete Settings ===

AUTOCOMPLETE_BACKEND = "keyboard.autocomplete.backends.autocomplete.AutoComplete"


# === Bots Settings ===

# Module path for each active bot
REGISTERED_BOTS = [
	'bots.bots.calculator.CalculatorBot',
	'bots.bots.weather.WeatherBot',
    'bots.bots.chrome.ChromeBot',
	# 'bots.bots.search.SearchBot',
]
