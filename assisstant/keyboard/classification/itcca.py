import numpy as np
from keyboard.preprocessing import butter
from keyboard.datasets.reader import getUserDatasets
from . import rcca

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


def getCorrelationVector(X,Xcap,Y):
    cca = rcca.CCA(kernelcca = False, reg = 0, numCC = 1)
    cca.train([np.transpose(X),np.transpose(Xcap)])
    Wxxcap = cca.ws[0] #WX(X,Xcap)
    Wxcapx = cca.ws[1] #WXcap(X,Xcap)
    cca.train([np.transpose(Xcap),np.transpose(Y)])
    Wxcapy = cca.ws[0] #Wxcap(Xcap,Y)
    cca.train([np.transpose(X),np.transpose(Y)])
    Wxy = cca.ws[0]    #WX(X,Y)
#    Wyx = cca.ws[1]    #WY(X,Y)
    r1 = cca.cancorrs[0]
    r2 = np.corrcoef(np.dot(Wxxcap.T,X),np.dot(Wxxcap.T,Xcap))[0,1]
#    r3 = np.corrcoef(np.dot(Wxy.T,X),np.dot(Wxy.T,Xcap))[0,1]
    r4 = np.corrcoef(np.dot(Wxcapy.T,X),np.dot(Wxcapy.T,Xcap))[0,1]
    r5 = np.corrcoef(np.dot(Wxxcap.T,Xcap),np.dot(Wxcapx.T,Xcap))[0,1]
    return np.array([r1,r2,0,r4,r5])

def getRho(corr_vec):
    rho = 0    
    for i in range(5):
        rho += np.sign(corr_vec[i]) * (corr_vec[i]**2)
    return rho


def getBestFrequency(eeg_data, ref_data, data):
    bestfreq = 0
    bestrho= -100000000
    for i in range(len(ref_data)):
        indices = np.where(target == i)
        target_data = data[indices,:,:][0]
        Xcap = np.mean(target_data,0)
        Y = ref[i]
        vec = getCorrelationVector(sample,Xcap,Y)
        rho = getRho(vec)
        if  rho > bestrho:
            bestrho = rho
            bestfreq = i
    return bestfreq
    
def classify(sample, freqs, duration):
    data, target = getUserDatasets()
    data = butter.filter(data)
    freqs = np.array(freqs)
    n_harmonics = 3
    ref = getArtificialRefSignal(freqs, n_harmonics, duration, 128)
    sample = butter.filter(sample)
    return getBestFrequency(sample, ref, data)




##data, target = read("Amr4", 5)
#data = butter_bandpass_filter(data)

#correct = 0
#for i in range(25):
##    print targett[i]
    #if(target[i] == ITCCA_classify(data[i,:,:])):
        #correct += 1
#    print "-------------------------"
        
#print correct
