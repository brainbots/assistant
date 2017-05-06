import time
import numpy as np

def read(no_of_seconds):
  time.sleep(no_of_seconds)
  
  values = np.random.random_sample((4, no_of_seconds * 128))
  quality = np.random.random_sample((4, no_of_seconds * 128))

  return (values, quality)
