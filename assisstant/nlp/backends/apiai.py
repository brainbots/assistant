from nlp_backend import NlpBackend
import socket

class ApiaiBackend(NlpBackend):
	def get_intent(self, query, session_id):
		if not self._check_connection():
			raise ConnectionError("No internet connection, please connect to the internet.")

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