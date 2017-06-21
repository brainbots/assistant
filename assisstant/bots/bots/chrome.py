from time import sleep
from PyQt5.QtCore import QProcess
from .abstract_bot import AbstractBot
from bots.action import Action
from bots.utility import getWindow

class ChromeBot(AbstractBot):
  def __init__(self, id):
    actions = ['web.search']
    super().__init__(id, actions)
    #REQUIRED
    self.query = None
    self.process = QProcess()

  def extract_attr(self, intent):
    self.query = intent.query_string

  def execute(self):
    try:
      self.process.start("/usr/bin/google-chrome-stable")
      pid = self.process.pid()
      criteria = {'pid': pid}
      wnd = None
      while True:
        wnd = getWindow(criteria)
        if wnd is None:
          sleep(1)
        else:
          break

      return Action(action_type = 'embed', body = {'hwnd': wnd['hwnd'], 'commands': ['x', 'y', 'z', 'a']}, bot = self.id, keep_context = False)
    except Exception as e:
      raise(e)

  def request_missing_attr(self):
    #TODO: Check for missing attr
    pass

  def has_missing_attr(self):
    return False
