import autocomplete

class AutoComplete:
	def __init__(self):
		autocomplete.load()

	def predict(self, query):
		*prev, word = query.split(" ")
		if len(prev) > 1:
			prev = prev[-1]
		elif len(prev) == 1:
			prev = prev[0]
		else:
			# TODO find another solution
			prev = "the"
		top = autocomplete.predict(prev, word)[:3]
		return [word for word, score in top]

