from abc import ABC, abstractmethod
class NlpBackend(ABC):
	@abstractmethod
	def get_intent(self,query,sessionID):
		pass
