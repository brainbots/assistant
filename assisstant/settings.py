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

VIRTUAL_SEQUENCE = [1,1,1,0,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]

# === Autocomplete Settings ===

AUTOCOMPLETE_BACKEND = "keyboard.autocomplete.backends.autocomplete.AutoComplete"


# === NLP Settings ===

NLP_BACKEND = "nlp.backends.api_ai.ApiaiBackend"

APIAI_ACCESS_TOKEN='8dda3e91a2b240e1b16d48aa57433ece'

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

SENDGRID_ACCESS_TOKEN = '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'
WEATHER_CLIENT_ID = 'UdLRojHnKB0m0b6ysMvKj'
WEATHER_CLIENT_SECRET = '3Kdd7KK6vCcLFhIA9RigNdiCGoB6JdkIjweHi4zy'
