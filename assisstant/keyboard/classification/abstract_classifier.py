from abc import ABC, abstractmethod, abstractproperty
from assisstant import settings

class AbstractClassifier(ABC):
  def __init__(self, freqs, duration, data=None):
      self.freqs = freqs
      self.duration = duration
      if data:
          self.data = data
          self.train(data)

  @abstractmethod
  def classify(self, sample):
    pass

  @abstractmethod
  def load_model(self,sample):
      pass

  @abstractmethod
  def train(self, data):
    pass
