import os
import numpy as np
from keyboard import config

def read(folder, duration):
    '''
    from reader import read
    import numpy as np

    data, target = read("subject1", 4) # subject name, duration
    # data is 3d numpy array [readings, channel, length of the sample]

    print(data.shape)

    # get the first sample
    data[0,:,:]

    # get all reading of the first channel
    data[:,0,:]

    # get some samples that meet a cetain criteria knowing the index
    chosen=[0,1]
    data[chosen]

    # transposing
    np.transpose(data, (1, 0, 2)) # permutation of the dimension, i.e swap first and second, and leave third as is

    '''

    target_filename = "{}_target.csv".format(duration)
    target_path = os.path.join(folder, target_filename)

    channels=("O1", "O2", "P7", "P8")
    channels_data=[]

    for channel in channels:
        sampels_filename = str(duration) + '_' + channel + ".csv"
        samples_path = os.path.join(folder, sampels_filename)
        channels_data.append(np.genfromtxt(samples_path, delimiter=","))

    samples=np.stack(channels_data)
    if len(samples.shape) == 2:
        samples = samples.reshape(4, 1, 640)
    samples=np.transpose(samples, (1, 0, 2))

    target=np.genfromtxt(target_path, delimiter=",", dtype=np.int16)
    return (samples, target)

def getUserDatasets():
    directory = os.path.join("keyboard", "datasets", "users", config.USER)
    datasets = []

    for dirname, dirnames, _ in os.walk(directory):
        for subdirname in dirnames:
            folder = os.path.join(dirname, subdirname)
            datasets.append(folder)

    data = np.empty([0,4,640])
    target = np.empty([0])
    for dataset in datasets:        
        datai, targeti = read(dataset, 5)
        data = np.concatenate((data,datai))
        target = np.concatenate((target,targeti))
    return (data, target)
