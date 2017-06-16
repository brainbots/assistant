from abc import ABC, abstractmethod, abstractproperty
class AbstractBot(ABC):
	def __init__(self, id, actions):
		self.id = id
		self.actions = actions

	@abstractmethod
	def validate_intent(self, intent):
		return

	@abstractmethod
	def execute(self, intent):
		return

	@abstractmethod
	def request_missing_attr(self, intent):
		return
