from PyQt5.QtCore import Qt

USER = "AmrMohamed"

# === Keyboard Settings ===
INITIAL_FONT = 17

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

TIME_FLASH_SEC     = 3
TIME_REST_SEC      = 4
ANIMATION_DURATION = 300
GRIDLAYOUT_MARGIN  = 0
GRIDLAYOUT_SPACING = 100

CHARS = ["abcdqrst",
         "efghuvwx",
         "ijklyz.,",
         "mnop\"'?&",
         "1234⌫@$!",
         "5678~_{}",
         "90-+()[␣",
         "*/^=<>]⏎"]

VIRTUAL_QUERIES =  [
    # 'Search google for emotiv',
    'What is the weather?',
    'in cairo',
    'in egypt',
    'weather in london,gb?'
]

VIRTUAL_SEQUENCE = [1,1,1,0,0,0,0,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]

# === Autocomplete Settings ===

AUTOCOMPLETE_BACKEND = "keyboard.autocomplete.backends.autocomplete.AutoComplete"


# === NLP Settings ===

NLP_BACKEND = "nlp.backends.api_ai.ApiaiBackend"

# === Bots Settings ===

# Default msg when no bot or intent found.
FALLBACK_PROMPTS = [
    "Sorry, I don't quite understand.",
    "Sorry, I don't understand.",
    "I don't understand.",
    "Please state what you want more clearly."
]

# Module path for each active bot
REGISTERED_BOTS = [
	'bots.bots.calculator.CalculatorBot',
	'bots.bots.weather.WeatherBot',
	'bots.bots.chrome.ChromeBot',
	'bots.bots.mail.MailBot',
	# 'bots.bots.search.SearchBot',
]
