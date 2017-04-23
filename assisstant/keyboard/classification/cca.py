import numpy as np
from scipy.signal import butter, lfilter
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import itertools
from scipy import stats
import assisstant.keyboard.classification.rcca as rcca

#signal processing part
def butter_bandpass(lowcut, highcut, fs, order=5):
    fnyq = 0.5 * fs
    low = lowcut / fnyq
    high = highcut / fnyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut = 6, highcut= 42, fs=128, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

#Returns a list of matrices where each row in each matrix is a sin or cos with frequency = freqs[i] , the number of harmonics = Nharmonics and row length = sample_length 
def getArtificialRefSignal(freqs,Nharmonics,n_secs,fs):
    t = np.linspace(0,n_secs,fs*n_secs)
    mat_list = np.empty(freqs.size,dtype=object)
    for i in range(freqs.size):
        Y = np.array([])
        for j in range(1,Nharmonics+1):
            jth_harmonic = np.sin(2*np.pi*freqs[i]*j*t)
            Y = np.vstack((Y,jth_harmonic)) if Y.size else jth_harmonic
            Y = np.vstack((Y,np.cos(2*np.pi*freqs[i]*j*t)))
        mat_list[i] = Y
    return mat_list


def getBestFrequency(eeg_data,ref_data):
    bestfreq=0;
    bestcanoncorr=-100000000;
    cca = rcca.CCA(kernelcca = False, reg = 0., numCC = 2)
    for i in range(len(ref_data)):
        cca.train([np.transpose(eeg_data), np.transpose(ref_data[i])])
        if  cca.cancorrs[0]+cca.cancorrs[1] > bestcanoncorr:
            bestcanoncorr = cca.cancorrs[0]+cca.cancorrs[1]
            bestfreq = i
    return bestfreq+1

def ccaClassify(sample):
    freqs = np.array([12.195121951219512,10,8.620689655172415,7.575757575757576,6.666666666666667])
    n_secs = 5
    n_harmonics = 3
    ref = getArtificialRefSignal(freqs,n_harmonics,n_secs,128)
    sample = butter_bandpass_filter(sample)
    return getBestFrequency(sample, ref)