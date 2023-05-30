import numpy as np

def statistical_features(arr):
    vmin = np.amin(arr)
    vmax = np.amax(arr)
    mean = np.mean(arr)
    std = np.std(arr)
    rms = np.sqrt(np.mean(np.square(np.ediff1d(arr))))
    return vmin, vmax, mean, std, rms