from abc import ABC, abstractmethod, abstractproperty
class AbstractBot(ABC):
	# @abstractmethod
	# @abstractproperty
	# def id(self, id):
	# 	pass

	# @abstractmethod
	def __init__(self, id):
		self.id = id

	@abstractmethod
	def validate_intent(self, intent):
		pass

	@abstractmethod
	def validate_intent(self, intent):
		pass

	@abstractmethod
	def execute(self, intent):
		pass
