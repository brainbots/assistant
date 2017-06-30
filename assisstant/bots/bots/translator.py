from .abstract_bot import AbstractBot
from bots.action import Action
import settings
from translate import Translator
import bots.data.translator.lang as data

class TranslationBot(AbstractBot):
    def __init__(self, id):
        actions = ['translate.text']
        super().__init__(id, actions)
        #REQUIRED
        self.attr = {
            "lang-from": settings.TRANSLATOR_LANG_FROM,
            "lang-to": settings.TRANSLATOR_LANG_TO,
            "text": None
        }

    def extract_attr(self, intent):
        for key, value in self.attr.items():
            if not value and key in intent.parameters and not intent.parameters[key] == "":
                self.attr[key] = intent.parameters[key]

    def request_missing_attr(self):
        msgs = {
            "lang-to": "Please specify the source language\n",
            "lang-from": "Please specify the destination language\n",
            "text": "Please specify text\n",
        }
        print(self.attr)
        for key, value in self.attr.items():
            if not value:
                return Action(
                    action_type = 'inquiry',
                    body = msgs[key],
                    bot = self.id,
                    keep_context = True
                )

    def is_long_running(self):
        return False

    def has_missing_attr(self):
        for key, value in self.attr.items():
            if not value:
                return True 
        return False

    def execute(self):
        to_code = data.LANG_PAIR[self.attr['lang-to']]
        from_code = data.LANG_PAIR[self.attr['lang-from']]
        translator= Translator(to_lang=to_code, from_lang=from_code)
        translation = translator.translate(self.attr['text'])
        self.clear()
        return Action(
            action_type = 'message',
            body = translation,
            bot = self.id,
            keep_context = False)

    def clear(self):
      for key, value in self.attr.items():
        self.attr[key] = None
