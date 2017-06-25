from PyQt5.QtCore import Qt, QObject, QTimer
import settings
import keyboard.keyboard_manager as Keyboard
import nlp.nlp_manager as NLP
import bots.bots_manager as Bots
import random
import traceback

class Assistant(QObject):

    def __init__(self, is_virtual, parent=None):
        super(Assistant, self).__init__(parent)

        self.keyboard_manager = Keyboard.KeyboardManager(is_virtual)
        self.nlp_manager = NLP.NlpManager()
        self.bots_manager = Bots.BotManager()

        self.keyboard_manager.direct_bot_command.connect(self.handle_direct_bot_commands)
        self.keyboard_manager.send_query_signal.connect(self.analyze_query)

    def handle_direct_bot_commands(self, command_index):
        if command_index == -1:
            self.bots_manager.terminate_bot()
            self.keyboard_manager.begin_rest()
        else:
            action = self.bots_manager.resume_bot(command_index)
            self.keyboard_manager.bot_action_handler(action)

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
            traceback.print_tb(e.__traceback__)
            print(e)
            # self.keyboard_manager.bot_action_handler(None)
            self.keyboard_manager.prompt(random.choice(settings.FALLBACK_PROMPTS))
            return
        try:
            action = self.bots_manager.run_action(intent)
            if action.keep_context:
                self.nlp_manager.keep_contexts()
            else:
                self.nlp_manager.reset_contexts()
        #Call or emit a signal to the keyboard
            self.keyboard_manager.bot_action_handler(action)
        except Exception as e:
            #TODO: Bots manager failed to find the appropriate bot
            # Notify the user that input is ambiguous
            traceback.print_tb(e.__traceback__)
            print(e)
            self.keyboard_manager.prompt(random.choice(settings.FALLBACK_PROMPTS))
            # pass
