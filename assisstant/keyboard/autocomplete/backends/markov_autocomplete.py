from markov_autocomplete.autocomplete import Autocomplete

class MarkovAutocomplete:
    def __init__(self):
        sentences = ['''I WAS born in the year 1632, in the city of York, of a good family,\
        though not of that country, my father being a foreigner of Bremen,\
        who settled first at Hull. He got a good estate by merchandise,\
        and leaving off his trade, lived afterwards at York,\
        from whence he had married my mother, whose relations were named Robinson,\
        a very good family in that country, and from whom I was called Robinson Kreutznaer;\
        but, by the usual corruption of words in England, we are now called - nay we call\
        ourselves and write our name - Crusoe; and so my companions always called me.",\
        "I had two elder brothers, one of whom was lieutenant-colonel to an English\
        regiment of foot in Flanders, formerly commanded by the famous Colonel Lockhart,\
        and was killed at the battle near Dunkirk against the Spaniards. What became of my\
        second brother I never knew, any more than my father or mother knew what became of me.''']
        self.ac = Autocomplete(model_path = "ngram",
                      sentences = sentences,
                      n_model=3,
                      n_candidates=10,
                      match_model="middle",
                      min_freq=0,
                      punctuations="",
                      lowercase=True)

    def predict(self, query):
        sen = self.ac.predictions(query)[0]
        sen = [st
               for s in sen
               for st in s.lower().replace(',',' ').split(' ')
               if st.startswith(query)]
        return list(set(sen))[:3]
