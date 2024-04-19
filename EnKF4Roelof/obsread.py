# Write the initial condition at each grind point

import os
import re
import string
import numpy as np

def obsread(n):
    f  = open('pflotran-obs-0.pft')    # changed from .tec to .pft
    c = f.readline()
    for c in f:
        if len(c)>0:
            pres = re.split(r"[\s,\"]+",c)	
    f.close()

#    print(pres[1])
    pres = pres[1:len(pres)-1]
    pres = [float(pres[i*2+1]) for i in range(n)]
    pres = np.array(pres)
    end_time = float(pres[1])
    return pres, end_time
    
