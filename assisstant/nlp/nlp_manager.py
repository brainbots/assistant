from nlp.intent import Intent
from nlp.backends.api_ai import ApiaiBackend
from nlp.backends.nlp_backend import NlpBackend

class NlpManager:
    def __init__(self):
	    self.NlpBackend = ApiaiBackend()
	    # TODO: Session id should be related to the current user
	    self.session_id = 1
	    self.reset_context = True

    def get_intent(self, query):
	    return self.NlpBackend.get_intent(
		            query,self.session_id,self.reset_context)

    def keep_contexts(self):
	    self.reset_contexts = False

    def reset_contexts(self):
	    self.reset_contexts = True
