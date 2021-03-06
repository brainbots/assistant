from PyQt5.QtCore import Qt, QObject, QTimer, pyqtSignal
from keyboard.ui.keyboard_window import KeyboardWindow
from keyboard.autocomplete.autocomplete_manager import AutoCompleteManager
from keyboard.autocomplete.backends.pyenchant import Enchant
from keyboard.input import device
import settings
from keyboard.classification import cca, itcca
from random import randint
import importlib
import traceback

class KeyboardManager(QObject):
  send_query_signal = pyqtSignal(str)
  direct_bot_command = pyqtSignal(int)

  def __init__(self, is_virtual, parent=None):
    super(KeyboardManager, self).__init__(parent)

    self.keyboard_window = KeyboardWindow()
    self.keyboard_window.showFullScreen()

    self.autocomplete_manager = AutoCompleteManager()
    self.autocorrect = Enchant()
    self.is_virtual = is_virtual

    self.keyboard_window.ui_reloaded_signal.connect(self.after_reload)

    # the loop goes like this
    # device starts collecting -> call update to start flashing
    # device finishes collecting -> call update to stop flashing, pause then call device.collect again
    self.device = device.Device(callback=self.device_update,
                                collect_time=settings.TIME_FLASH_SEC,
                                is_virtual=self.is_virtual)

    self.device.collect_signal.connect(self.device_update)

    self.paused = False
    self.classifier = self.load_classifier()
    # self.old_data = getUserDatasets("S1",3)
    # print(self.old_data)

    # predetermined sequence of choices for testing
    self.virtual_sequence = settings.VIRTUAL_SEQUENCE
    self.virtual_queries = settings.VIRTUAL_QUERIES
    # initial delay
    self.begin_rest()

  def load_classifier(self):
    ca = settings.CLASSIFICATION_ALGORITHM
    *module, classname = ca.split(".")
    module = ".".join(module)
    module = importlib.import_module(module)
    classifier_class = getattr(module, classname)
    return classifier_class(freqs=settings.FREQ, duration=settings.TIME_FLASH_SEC)

  def begin_rest(self):
    QTimer.singleShot(settings.TIME_REST_SEC * 1000, Qt.PreciseTimer, self.device.collect)
    if not self.keyboard_window.embedded_mode:
      self.keyboard_window.show_timer()

  # The passed boolean can be omitted as the function toggles the flashing each time
  def device_update(self, collecting, data=None):
    print("device update ", collecting)

    # toggle flashing
    self.keyboard_window.flash_handler(collecting)

    # recording finished
    if not collecting:
      sample, _quality = data
      if self.is_virtual:
        if len(self.virtual_sequence) > 0:
          result = self.virtual_sequence.pop(0)
        else:
          result = randint(0, 3)
      else:
        result = self.classifier.classify(sample)
        # result = cca.classify(sample, settings.FREQ, settings.TIME_FLASH_SEC, self.old_data)

      if self.keyboard_window.embedded_mode:
        if result == 0:
          self.keyboard_window.unembedWindow()
        self.direct_bot_command.emit(result-1)
        return

      char, predicted = self.keyboard_window.update_handler(result)
      print("Selected Character: ", char)

      if char and not predicted:
        self.char_selected(char)

      elif not char:
        self.begin_rest()

  def char_selected(self, char):
    query = self.keyboard_window.get_input() + char
    self.predict_word(query)

  def after_reload(self, selected):
    if selected == "⏎":
      if self.is_virtual:
        if len(self.virtual_queries) > 1:
          query = self.virtual_queries.pop(0)
        else:
          query = self.virtual_queries[0]
      else:
        query = self.keyboard_window.get_input()
      
      self.reset_prompt()
      self.send_query_signal.emit(query)
    else:
      # Start after rest if no action to be taken
      self.begin_rest()


  def predict_word(self, query):
    print(query)
    try:
      word = query.rstrip().split(' ')[-1] 
      print(word) 
      # trigger auto-correct if the word ends with spaced and has a misspelling
      if query.endswith(' ') and not self.autocorrect.check(word):
        words = self.autocorrect.suggest(word)[0:2] + ['⌫'] 
        print(words) 
      else: 
        words = self.autocomplete_manager.complete(query) 
        print(words) 

      self.keyboard_window.receive_predicted_words(words) 
    except Exception as e:
      # print(e)
      traceback.print_tb(e.__traceback__)
      print(e)
      self.keyboard_window.receive_predicted_words([])

  #TODO: add proper action_handler
  def bot_action_handler(self, action):
    if action:
      print(action.type)
      print(action.body)
      
      self.keyboard_window.update_input("")

      if action.type == 'embed':
        self.keyboard_window.embedWindow(action.body['hwnd'], ['x'] + action.body['commands'])
      elif action.type == 'keyboard_event':
        self.keyboard_window.execKeyboardEvent(action.body['fn'])
      else:
        self.keyboard_window.update_prompt(str(action.body))

    self.begin_rest()
    # QTimer.singleShot(5000, Qt.PreciseTimer, self.unfreeze)

  def prompt(self, p):
    self.keyboard_window.update_prompt(p)
    self.keyboard_window.update_input("")
    self.begin_rest()

  def reset_prompt(self):
    self.keyboard_window.update_prompt("")
