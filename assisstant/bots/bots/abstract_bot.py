from abc import ABC, abstractmethod, abstractproperty
class AbstractBot(ABC):
	def __init__(self, id, actions):
		self.id = id
		self.actions = actions

	@abstractmethod
	def extract_attr(self, intent):
		pass

	@abstractmethod
	def execute(self):
		pass

	@abstractmethod
	def has_missing_attr(self):
		pass

	@abstractmethod
	def request_missing_attr(self):
		pass

	@abstractmethod
	def is_long_running(self):
		pass
