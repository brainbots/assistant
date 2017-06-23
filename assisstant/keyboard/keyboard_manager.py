from PyQt5.QtCore import Qt, QObject, QTimer, pyqtSignal
from keyboard.ui.keyboard_window import KeyboardWindow
from keyboard.autocomplete.autocomplete_manager import AutoCompleteManager
from keyboard.input import device
import settings
from keyboard.classification import cca, itcca
from keyboard.datasets.reader import getUserDatasets
from random import randint
import traceback

class KeyboardManager(QObject):
  send_query_signal = pyqtSignal(str)

  def __init__(self, is_virtual, parent=None):
    super(KeyboardManager, self).__init__(parent)

    self.keyboard_window = KeyboardWindow()
    self.keyboard_window.showMaximized()

    self.autocomplete_manager = AutoCompleteManager()
    self.is_virtual = is_virtual

    # self.keyboard_window.ui_pause.connect(self.pause_handler)
    # self.keyboard_window.ui_freeze.connect(self.freeze_handler)
    # self.keyboard_window.autocomplete_signal.connect(self.predict_word)

    # the loop goes like this
    # device starts collecting -> call update to start flashing
    # device finishes collecting -> call update to stop flashing, pause then call device.collect again
    self.device = device.Device(callback=self.device_update,
                                collect_time=settings.TIME_FLASH_SEC,
                                is_virtual=self.is_virtual)

    self.device.collect_signal.connect(self.device_update)

    # self.freeze = False
    self.paused = False
    self.old_data = getUserDatasets()

    # predetermined sequence of choices for testing
    self.seq = [1,1,1,1,3,3,3,3,3,3]

    # initial delay
    QTimer.singleShot(settings.TIME_REST_SEC * 1000, Qt.PreciseTimer, self.device.collect)

  # The passed boolean can be omitted as the function toggles the flashing each time
  def device_update(self, collecting, data=None):
    print("device update ", collecting)

    # toggle flashing
    self.keyboard_window.flash_handler(collecting)

    # recording finished
    if not collecting:
      sample, _quality = data
      if self.is_virtual:
        if len(self.seq) > 0:
          result = self.seq.pop(0)
        else:
          result = randint(0, 3)
      else:
        result = cca.classify(sample, settings.FREQ, settings.TIME_FLASH_SEC, self.old_data)

      char = self.keyboard_window.update(result)

      if char:
        self.char_selected(char)

      # Problem is this gets called after char is selected and device is started before intent response and so a new selection occurs without flashing
      QTimer.singleShot(settings.TIME_REST_SEC * 1000, Qt.PreciseTimer, self.device.collect)

  def char_selected(self, char):
        print("Selected Character: ", char)
        query = self.keyboard_window.get_input() + char
        self.predict_word(query)

        if char == "⏎":
          self.send_query_signal.emit(self.keyboard_window.get_input())

  def predict_word(self, query):
    print(query)
    try:
      words = self.autocomplete_manager.complete(query)
      print(words)
      self.keyboard_window.receive_predicted_words(words)
    except Exception as e:
      # print(e)
      traceback.print_tb(e.__traceback__)
      self.keyboard_window.receive_predicted_words([])

  #TODO: move to keyboard/manager
  #TODO: add proper action_handler
  def bot_action_handler(self, action):
    if action:
      print(action.type)
      print(action.body)
      
      self.keyboard_window.update_text("")

    if action and action.type != 'embed':
      self.keyboard_window.update_prompt(str(action.body))
      # QTimer.singleShot(5000, Qt.PreciseTimer, self.unfreeze)
    elif action and action.type == 'embed':
      self.keyboard_window.embedWindow(action.body['hwnd'], action.body['commands'])