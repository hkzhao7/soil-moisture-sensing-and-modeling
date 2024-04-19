# Write the initial condition at each grid point

import os
import re
import string
import numpy as np

def pres2initial(pres):    # actually pressure
    n = len(pres)
    fw = open('E5_obs2initial.txt','w')
    for i in range(n):
        fw.write('FLOW_CONDITION initial'+str(i+1)+'\n')    # define grid
        fw.write('TYPE \n LIQUID_PRESSURE DIRICHLET \n /\n')
        fw.write('LIQUID_PRESSURE '+str(pres[i])+'\n')    # define initial pressure
        fw.write('END\n\n')
    fw.close()
    
