import numpy as np

def get_single_sample(headset, index, data, quality):
  '''
  TODO:
  packet = headset.dequeue()
  while packet is None:
  packet = headset.dequeue()
  '''
  while True:
    packet = headset.dequeue()
    if packet is not None:
      data[0][index] = packet.sensors['O1']['value']
      data[1][index] = packet.sensors['O2']['value']
      data[2][index] = packet.sensors['P7']['value']
      data[3][index] = packet.sensors['P8']['value']

      quality[0][index] = packet.sensors['O1']['quality']
      quality[1][index] = packet.sensors['O2']['quality']
      quality[2][index] = packet.sensors['P7']['quality']
      quality[3][index] = packet.sensors['P8']['quality']
      break

def read(headset, no_of_seconds):
  data = np.empty([4, no_of_seconds * 128])
  quality = np.empty([4, no_of_seconds * 128])
  
  for i in range(no_of_seconds*128):
    get_single_sample(headset, i, data, quality)

  return (data, quality)
