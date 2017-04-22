from nlp_backend import NlpBackend
import apiai

class ApiaiBackend(NlpBackend):
	def __init__(self):
		CLIENT_ACCESS_TOKEN='31dc1846968d441b950e3a6b15797bff'
		self.ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
	def get_intent(self, query, session_id):
		pass
	def make_request(self, query, session_id):
		request = self.ai.text_request()
		request.lang = 'en'		# optional, default value equal 'en'
		request.session_id = session_id
		request.query = query
		response = request.getresponse()
		data = response.read()
		return data

