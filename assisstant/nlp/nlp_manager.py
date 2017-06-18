from nlp.intent import Intent
from nlp.backends.api_ai import ApiaiBackend
from nlp.backends.nlp_backend import NlpBackend

class NlpManager:
    def __init__(self):
	    self.NlpBackend = ApiaiBackend()
	    # TODO: Session id should be related to the current user
	    self.session_id = 1
	    self.__reset_contexts = True

    def get_intent(self, query):
	    return self.NlpBackend.get_intent(
		            query,self.session_id,self.__reset_contexts)

    def reset_contexts(self):
        self.__reset_contexts = True

    def keep_contexts(self):
        self.__reset_contexts = False
