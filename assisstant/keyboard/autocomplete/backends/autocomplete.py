import autocomplete

class AutoComplete:
	def __init__(self):
		autocomplete.load()

	def predict(self, query):
		*prev, word = query.split(" ")
		if len(prev) > 1:
			prev = prev[-1]
		else:
			prev = prev[0]
		return autocomplete.predict(prev, word)[:3]

