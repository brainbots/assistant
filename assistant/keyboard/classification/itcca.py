import numpy as np
from keyboard.preprocessing import butter
from keyboard.classification.abstract_classifier import AbstractClassifier
from keyboard.dataset_manager.reader import getUserDatasets
from . import rcca
import os
import settings

class ITCCAClassifier(AbstractClassifier):
    def classify(self,sample):
        sample = butter.filter(sample)
        freqs = np.array(self.freqs)
        n_harmonics = 3
        ref = self.getArtificialRefSignal(freqs, n_harmonics, self.duration, 128)
        sample = butter.filter(sample)
        return self.getBestFrequency(sample, ref)

    #Returns a list of matrices where each row in each matrix is a sin or cos with frequency = freqs[i] , the number of harmonics = Nharmonics and row length = sample_length
    def getArtificialRefSignal(self,freqs,Nharmonics,n_secs,fs):
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

    def getCorrelationVector(self,X,Xcap,Y):
        cca = rcca.CCA(kernelcca = False, reg = 0, numCC = 1)
        cca.train([np.transpose(X),np.transpose(Xcap)])
        Wxxcap = cca.ws[0] #WX(X,Xcap)
        Wxcapx = cca.ws[1] #WXcap(X,Xcap)
        cca.train([np.transpose(Xcap),np.transpose(Y)])
        Wxcapy = cca.ws[0] #Wxcap(Xcap,Y)
        cca.train([np.transpose(X),np.transpose(Y)])
        Wxy = cca.ws[0]    #WX(X,Y)
        r1 = cca.cancorrs[0]
        r2 = np.corrcoef(np.dot(Wxxcap.T,X),np.dot(Wxxcap.T,Xcap))[0,1]
        #r3 = np.corrcoef(np.dot(Wxy.T,X),np.dot(Wxy.T,Xcap))[0,1]
        r4 = np.corrcoef(np.dot(Wxcapy.T,X),np.dot(Wxcapy.T,Xcap))[0,1]
        r5 = np.corrcoef(np.dot(Wxxcap.T,Xcap),np.dot(Wxcapx.T,Xcap))[0,1]
        return np.array([r1,r2,0,r4,r5])

    def getRho(self,corr_vec):
        rho = 0
        for i in range(5):
            rho += np.sign(corr_vec[i]) * (corr_vec[i]**2)
        return rho

    def getBestFrequency(self,eeg_data, ref_data):
        bestfreq = 0
        bestrho= -100000000
        for target_idx in range(len(ref_data)):
            Xcap = self.load_model(target_idx)
            Y = ref_data[target_idx]
            vec = self.getCorrelationVector(eeg_data,Xcap,Y)
            rho = self.getRho(vec)
            if  rho > bestrho:
                bestrho = rho
                bestfreq = target_idx
        return bestfreq

    def train(self,data,target):
        for target_idx in range(4):
            indices = np.where(target == target_idx)
            target_data = data[indices, :, :][0]
            Xcap = np.mean(target_data, 0)
            self.save_model(Xcap, target_idx)

    def save_model(self, model, target_idx):
        path = self.get_file_path(target_idx)
        np.savetxt(path, model, delimiter=",")

    def load_model(self,target_idx):
        path = self.get_file_path(target_idx)
        return np.loadtxt(path, delimiter=",")

    def get_file_path(self, target_idx):
        model_path = self.get_model_path()
        filename = settings.USER + '_target' + str(target_idx)
        path = os.path.abspath(os.path.join(model_path, filename + ".csv"))
        return path