from markov_autocomplete.autocomplete import Autocomplete
import os
from keyboard.ui import config

class MarkovAutocomplete:
    def __init__(self):
        sentences = []
        training_directory = 'training_files'
        for file_name in config.AUTOCOMPLETE_TRAINING_FILE_NAMES:
            file_path = os.path.join(training_directory,file_name)
            training_file = open(file_path,'r')
            sentences.append(training_file.read())

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
