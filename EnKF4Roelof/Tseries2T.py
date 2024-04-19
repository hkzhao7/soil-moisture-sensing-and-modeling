# This function takes the time series of T and identify the T value at the particular time
import numpy as np

def Tseries2T(Tseries,t):
    time  = Tseries[:,0]
    value = Tseries[:,1]

    time = time - t
    idx = np.where(time>0)
    idx = np.array(idx)
    # the first rain value                                                                                                     
    if idx.shape[1]==0:
        v = np.array([value[len(value)-1]])
    else:
        if time[idx[0,0]]>0:
            v = value[(idx[0,0]-1)]
        else:
            v = value[idx[0,0]]
    return v


