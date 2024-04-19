# Write the sink terms

import numpy as np
import os
import re
import string
from F_root_fraction import root_fr


def et2sinks(E, T):
    fw = open('E3_sink_dry.txt','w')
    n = 30
    dz =0.05

    z = np.linspace(dz/2,n*dz-dz/2,n)
    dz = dz+np.zeros(30)
    dr = root_fr(z, dz)
    dT = dr*T
#    print(sum(dT))
    
    for i in range(n):
        fw.write('FLOW_CONDITION sink'+str(i+1)+'\n')
        fw.write('TYPE\n')
        fw.write('RATE SCALED_VOLUMETRIC_RATE PERM\n/\n')

        if i==(n-1):
            fw.write('RATE '+str(dT[n-1-i]+E)+' m^3/hr\n')
        else:
            fw.write('RATE '+str(dT[n-1-i])+' m^3/hr\n')
        fw.write('END\n\n')
    fw.close()

    
#E  = -5.17e-5
#T  = -1.0e-4
#et2sinks(E,T)
