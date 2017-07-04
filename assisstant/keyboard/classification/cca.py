import numpy as np
from keyboard.preprocessing import butter
from keyboard.classification.abstract_classifier import AbstractClassifier
from . import rcca
from assisstant import settings
class CCAClassifier(AbstractClassifier):
    #Returns a list of matrices where each row in each matrix is a sin or cos with frequency = freqs[i] , the number of harmonics = Nharmonics and row length = sample_length
    def classify(self, sample):
        freqs = np.array(self.freqs)
        n_harmonics = 3
        ref = self.getArtificialRefSignal(freqs, n_harmonics, self.duration, 128)
        sample = butter.filter(sample)
        return self.getBestFrequency(sample, ref)

    def getArtificialRefSignal(self, freqs,Nharmonics,n_secs,fs):
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

    def getBestFrequency(self, eeg_data,ref_data):
        bestfreq = 0
        bestcanoncorr = -100000000
        cca = rcca.CCA(kernelcca = False, reg = 0., numCC = 2)
        for i in range(len(ref_data)):
            cca.train([np.transpose(eeg_data), np.transpose(ref_data[i])])
            if  cca.cancorrs[0]+cca.cancorrs[1] > bestcanoncorr:
                bestcanoncorr = cca.cancorrs[0]+cca.cancorrs[1]
                bestfreq = i
        return bestfreq

    def load_model(self):
        pass

    def train(self, data):
        pass

