import importlib
import settings

class AutoCompleteManager:
	def __init__(self):
		be = settings.AUTOCOMPLETE_BACKEND
		*module, classname = be.split(".")
		module = ".".join(module)
		module = importlib.import_module(module)
		be_class = getattr(module, classname)
		self.backend = be_class()

	def complete(self, query):
		return self.backend.predict(query)
