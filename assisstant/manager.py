from PyQt5.QtCore import Qt, QObject
from keyboard.ui.widgets import KeyboardWindow
import keyboard.manager as Keyboard
import nlp.nlp_manager as NLP
import bots.manager as Bots
from pprint import pprint

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

		self.keyboard_manager.flash_signal.connect(self.window.flash_handler)
		self.keyboard_manager.update_signal.connect(self.window.update_handler)
		self.window.ui_pause.connect(self.keyboard_manager.pause_handler)
		self.window.ui_freeze.connect(self.keyboard_manager.freeze_handler)
		self.window.send_query_signal.connect(self.analyze_query)
		self.keyboard_manager.start()

	def analyze_query(self, query):
		print(query)
		intent = self.nlp_manager.get_intent(query)
		print(intent.action)
		print(intent.score)
		print(intent.parameters)
		try:
		    action = self.bots_manager.run_action(intent)
		    if action.keep_context:
		        self.nlp_manager.keep_contexts()
		    else:
		        self.nlp_manager.reset_contexts()
		    #Call or emit a signal to the keyboard
		    self.window.receive_query_response(action)
		except Exception as e:
		    raise(e)

