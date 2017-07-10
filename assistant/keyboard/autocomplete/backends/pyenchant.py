import enchant
import re

class Enchant:
  def __init__(self):
    self.d = enchant.Dict("en")

  def check(self, word):
    return self.d.check(word)

  def suggest(self, word):
    words = []
    len_word = len(word)
    for w in self.d.suggest(word):
      w = re.sub(r"[ -]+", "", w)
      if w != word:
        words.append(w)
    #words = sorted(words, key = lambda w: abs(len_word - len(w)))
    return words
      

