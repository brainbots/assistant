from scipy.signal import butter, lfilter

def butter_bandpass(lowcut, highcut, fs, order=5):
    fnyq = 0.5 * fs
    low = lowcut / fnyq
    high = highcut / fnyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def filter(data, lowcut=6, highcut=42, fs=128, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y
