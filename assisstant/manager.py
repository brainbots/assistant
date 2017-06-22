from PyQt5.QtCore import Qt, QObject, QTimer
from keyboard import config
from keyboard.ui.widgets import KeyboardWindow
import keyboard.manager as Keyboard
import nlp.nlp_manager as NLP
import bots.manager as Bots
from keyboard.autocomplete.manager import AutoCompleteManager
from pprint import pprint
import traceback

class Manager(QObject):


    def __init__(self, is_virtual, parent=None):

    # signal.signal(signal.SIGINT, signal.SIG_DFL)
    # app = QApplication([])
    # app.setOverrideCursor(Qt.BlankCursor)
        super(Manager, self).__init__(parent)

        self.window = KeyboardWindow()
        self.window.showMaximized()
        self.keyboard_manager = Keyboard.Manager(is_virtual)
        self.nlp_manager = NLP.NlpManager()
        self.bots_manager = Bots.BotManager()
        self.autocomplete_manager = AutoCompleteManager()

        self.keyboard_manager.flash_signal.connect(self.window.flash_handler)
        self.keyboard_manager.update_signal.connect(self.window.update_handler)
        self.window.ui_pause.connect(self.keyboard_manager.pause_handler)
        self.window.ui_freeze.connect(self.keyboard_manager.freeze_handler)
        self.window.send_query_signal.connect(self.analyze_query)
        self.window.autocomplete_signal.connect(self.predict_word)
        QTimer.singleShot(config.TIME_REST_SEC * 1000, Qt.PreciseTimer, self.keyboard_manager.start)

    def predict_word(self, query):
        print(query)
        try:
          words = self.autocomplete_manager.complete(query)
          print(words)
          self.window.receive_predicted_words(words)
        except Exception as e:
          print(e)
          self.window.receive_predicted_words([])

    def analyze_query(self, query):
        print(query)
        try:
            intent = self.nlp_manager.get_intent(query)
            # TODO: Ensure that the nlp_manager
            # doesn't return a None object
            print(intent.action)
            print(intent.score)
            print(intent.parameters)
        except Exception as e:
            # TODO: Retry the request again
            # If request fails, notify the user
            print(e)
            traceback.print_tb(e.__traceback__)
            self.window.receive_query_response(None)
            return
        try:
            action = self.bots_manager.run_action(intent)
            if action.keep_context:
                self.nlp_manager.keep_contexts()
            else:
                self.nlp_manager.reset_contexts()
        #Call or emit a signal to the keyboard
            self.window.receive_query_response(action)
        except Exception as e:
            #TODO: Bots manager failed to find the appropriate bot
            # Notify the user that input is ambiguous
