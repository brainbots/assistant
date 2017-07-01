from .abstract_bot import AbstractBot
from bots.action import Action
class CalculatorBot(AbstractBot):
	def __init__(self, id):
		# TODO: Improve the manually-added calculator.calculate intent
		actions = ['calculator.calculate']
		super().__init__(id, actions)
		# REQUIRED
		self.expr = None

	def extract_attr(self, intent):
		# TODO: Handle sqrt and trignometric operations
		self.expr = intent.query_string

	def execute(self):
		try:
			result = eval(self.expr)
			return Action(
			    action_type = 'message',
			    body = result,
			    bot = self.id,
			    keep_context = False)

		except Exception as e:
			# Raise the exception e
			raise(e)

	def request_missing_attr(self):
	    #TODO: Check for missing attr
	    return

	def has_missing_attr(self):
	    return

	def is_long_running(self):
	    return False
