from .abstract_bot import AbstractBot

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
			return str(result)
		except Exception as e:
			# Raise the exception e
			raise
