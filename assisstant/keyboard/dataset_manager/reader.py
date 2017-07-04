import os
import numpy as np

def read(absolute_path, duration):
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
    target_filename = str(duration) + '_target.csv'
    target_path = os.path.join(absolute_path, target_filename)

    channels=("O1", "O2", "P7", "P8")
    channels_data=[]

    for channel in channels:
        sampels_filename = str(duration) + '_' + channel + ".csv"
        samples_path = os.path.join(absolute_path, sampels_filename)
        channels_data.append(np.genfromtxt(samples_path, delimiter=","))

    samples=np.stack(channels_data)
    if len(samples.shape) == 2:
        samples = samples.reshape(4, 1, 128*duration)
    samples=np.transpose(samples, (1, 0, 2))

    target=np.genfromtxt(target_path, delimiter=",", dtype=np.int16)
    return (samples, target)


def getUserDatasets(user,secs):
    directory = os.path.join("dataset", user)
    absolute_directory_path = os.path.abspath(directory)+os.sep

    datasets = []

    for dirname in os.listdir(absolute_directory_path):
        datasets.append(os.path.join(absolute_directory_path,dirname))

    data = np.empty([0,4,128*secs])
    target = np.empty([0])
    for dataset in datasets:
        datai, targeti = read(dataset, secs)
        data = np.concatenate((data,datai))
        target = np.concatenate((target,targeti))
    return (data, target)