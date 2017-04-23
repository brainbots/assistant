def get_single_sample(headset, data, quality):
  '''
  TODO:
  packet = headset.dequeue()
  while packet is None:
  packet = headset.dequeue()
  '''
  while True:
    packet = headset.dequeue()
    if packet is not None:
      data['O1'].append(packet.sensors['O1']['value'])
      data['O2'].append(packet.sensors['O2']['value'])
      data['P7'].append(packet.sensors['P7']['value'])
      data['P8'].append(packet.sensors['P8']['value'])

      quality['O1'].append(packet.sensors['O1']['quality'])
      quality['O2'].append(packet.sensors['O2']['quality'])
      quality['P7'].append(packet.sensors['P7']['quality'])
      quality['P8'].append(packet.sensors['P8']['quality'])
      break

def read(headset, no_of_seconds):
  data={'O1':[],'O2':[],'P7':[],'P8':[]}
  quality={'O1':[],'O2':[],'P7':[],'P8':[]}
  for i in range(no_of_seconds*128):
    get_single_sample(headset, data, quality)
  return (data, quality)
