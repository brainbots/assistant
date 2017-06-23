import autocomplete

class AutoComplete:
	def __init__(self):
		autocomplete.load()

	def predict(self, query):
		*prev, word = query.split(" ")

		if len(word) == 1:
		    return []

		if len(prev) > 0:
			prev = prev[-1]
		else:
			# TODO find another solution
			prev = "the"

		return autocomplete.predict(prev, word)[:3]

