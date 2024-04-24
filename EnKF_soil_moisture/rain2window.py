# Write the initial condition at each grind point

import os
import re
import string
import numpy as np

def rain2window(rain,t):
    time = rain[:,0]
    value = rain[:,1]
    
    time = time - t
    idx = np.where(time>0)
    idx = np.array(idx)
    
    # the first rain value
    if idx.shape[1]==0:
        t = np.array([0.0])
        v = np.array([value[len(value)-1]])
    else:
        t = time[idx]
        v = value[idx]
        if time[idx[0,0]]>0:
            t = np.insert(t, 0,  0.0)
            v = np.insert(v, 0, value[(idx[0,0]-1)])
        
#    print(t)
#    print(v)
#    print('-')
    fw = open('rain_window.txt','w')
    fw.write('TIME_UNITS hr\n')
    fw.write('DATA_UNITS m/hr\n')
    for i in range(len(t)):
        fw.write(str(t[i])+'   '+str(v[i])+'\n');
    fw.close()
