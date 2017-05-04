from nlp.intent import Intent
from nlp.backends.api_ai import ApiaiBackend
from nlp.backends.nlp_backend import NlpBackend

class NlpManager:
	def __init__(self):
		self.NlpBackend = ApiaiBackend()
		# TODO: Handle session in a smart way
		self.session_id = 1

	def get_intent(self, query):
		return self.NlpBackend.get_intent(query,self.session_id)
