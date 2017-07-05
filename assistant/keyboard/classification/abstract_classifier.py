from abc import ABC, abstractmethod, abstractproperty
import os
import settings

class AbstractClassifier(ABC):
  def __init__(self, freqs, duration, data=None):
      self.freqs = freqs
      self.duration = duration
      if data:
        self.data = data["data"]
        self.target = data["target"]
        self.train(self.data, self.target)

  @abstractmethod
  def classify(self, sample):
    pass

  # @abstractmethod
  def save_model(self, model):
    pass

  # @abstractmethod
  def load_model(self):
      pass

  # @abstractmethod
  def train(self, data, target):
    pass

  def get_model_path(self):
    cname = self.__class__.__name__
    directory = os.path.join(settings.MODELS_BASE_PATH, cname)
    if not os.path.exists(directory):
      os.makedirs(directory)
    return directory