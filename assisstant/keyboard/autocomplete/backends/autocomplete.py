import autocomplete

class AutoComplete:
	def __init__(self):
		autocomplete.load()

	def predict(self, query):
		*sentence, word = query.split(" ")
		sentence = " ".join(sentence)
		return autocomplete.predict(sentence, word)[:3]

