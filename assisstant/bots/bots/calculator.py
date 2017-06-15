from .abstract_bot import AbstractBot
from bots.action import Action
class CalculatorBot(AbstractBot):
	def __init__(self, id):
		# TODO: Improve the manually-added calculator.calculate intent 
		actions = ['calculator.calculate']
		super().__init__(id, actions)

	def validate_intent(self, intent):
		# TODO: Handle sqrt and trignometric operations
		return True

	def execute(self, intent):
		num_expr = intent.query_string
		try:
			result = eval(num_expr)
			return Action(
			    action_type = 'message',
			    body = result,
			    bot = self.id,
			    keep_context = False)

		except Exception as e:
			# Raise the exception e
			raise(e)
