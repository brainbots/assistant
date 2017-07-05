from PyQt5.QtCore import Qt
from secrets import *
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

USER = "S1"

# === Keyboard Settings ===
INITIAL_FONT = 40

FREQ = [
    6.666666666666667,
    5.882352941,
    10,
    7.575757575757576,
]
# fifth freq 
# 12.195121951219512,
# 8.620689655172415
# 

COLOR   =   [Qt.green, Qt.green, Qt.green, Qt.green, Qt.black]

TIME_FLASH_SEC     = 3
TIME_REST_SEC      = 5
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
    'translate hello'
    # 'Search google for emotiv',
    # 'Translate give me the apple from english to french',
    # 'What is the weather?',
    # 'in cairo',
    # 'in egypt',
    # 'weather in london,gb?'
]

VIRTUAL_SEQUENCE = [
    3,3,3,
    1,1,1,
    1,0,1,1,
    0,0,0,1,
    0,1,3,
    0,0,2,0,
    3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]

# === Autocomplete Settings ===

AUTOCOMPLETE_BACKEND = "keyboard.autocomplete.backends.autocomplete.AutoComplete"


# === Classification Settings ===
DATASET_PATH = os.path.join(BASE_DIR, 'keyboard/dataset_manager/Datasets')

CLASSIFICATION_ALGORITHM = "keyboard.classification.cca.CCAClassifier"
# CLASSIFICATION_ALGORITHM = "keyboard.classification.itcca.ITCCAClassifier"

# TRAIN_CLASSIFIER = True
TRAIN_CLASSIFIER = False

MODELS_BASE_PATH = os.path.join(BASE_DIR, "keyboard/classification/models")

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
    'bots.bots.translator.TranslationBot'
    # 'bots.bots.search.SearchBot',
]

TRANSLATOR_LANG_TO = "Arabic"
TRANSLATOR_LANG_FROM = "English"
