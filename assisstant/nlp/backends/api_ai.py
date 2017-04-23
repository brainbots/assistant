from .nlp_backend import NlpBackend
from nlp.intent import Intent
import apiai
import socket
import json
from datetime import datetime

class ApiaiBackend(NlpBackend):
	def __init__(self):
		# We should separate configurations like this in separate settings file to avoid later headaches
		CLIENT_ACCESS_TOKEN='31dc1846968d441b950e3a6b15797bff'
		self.ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

	def get_intent(self, query, session_id):
		resp = self.make_request(query, session_id)
		intent = self._parse_response(resp)
		return intent

	def make_request(self, query, session_id):
		if not self._check_connection():
			raise ConnectionError("No internet connection, please connect to the internet.")

		request = self.ai.text_request()
		request.lang = 'en'		# optional, default value equal 'en'
		request.session_id = session_id
		request.query = query
		response = request.getresponse()
		data = response.read()
		data = json.loads(data.decode('utf-8'))
		return data

	def _parse_response(self, response):
		if response["status"]["code"] == 200:
			# Contexts and sessions are not handeled
			data = {
				"action": response["result"]["action"],
				"parameters": response["result"]["parameters"],
				"score": response["result"]["score"],
				"query": response["result"]["resolvedQuery"],
				"timestamp": datetime.strptime(response["timestamp"], '%Y-%m-%dT%H:%M:%S.%fZ'),
			}
			intent = Intent(**data)
			return intent
		else:
			# Not handled, need to know what other responses are available
			pass

	def _check_connection(self,host="8.8.8.8", port=53, timeout=3):
		# Try to call host by ip address to prevent DNS lookup
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(timeout)
		try:
			sock.connect((host, port))
			return True
		except:
			# Try to call host by domain name in case ip address is no longer valid
			try:
				host = "google.com"
				port = 80
				sock.connect((host, port))
			except:
				return False
