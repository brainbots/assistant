from abc import ABC, abstractmethod, abstractproperty
class AbstractBot(ABC):
	def __init__(self, id, actions):
		self.id = id
		self.actions = actions

	@abstractmethod
	def extract_attr(self, intent):
		return

	@abstractmethod
	def execute(self):
		return

	@abstractmethod
	def has_missing_attr(self):
		return

	@abstractmethod
	def request_missing_attr(self):
		return
