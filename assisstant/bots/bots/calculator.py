from .abstract_bot import AbstractBot

class CalculatorBot(AbstractBot):
	# id = 5
	def __init__(self):
		self.actions = ['calculate']
		# self.id = 2
		# super().id = 5
		# print(self.id)

	def validate_intent(self):
		pass

	def execute(self):
		pass