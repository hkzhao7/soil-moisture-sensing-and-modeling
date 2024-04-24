# Write the sink terms with soil moisture limitation 

import numpy as np
import os
import re
import string
from F_root_fraction import root_fr


def et2sinks_lim(E_max, T_max, theta, theta0, theta1, theta2):
    fw = open('E3_sink_dry.txt','w')
    n = 30
    dz =0.05

    # root distributionX
    z = np.linspace(dz/2,n*dz-dz/2,n)
    dz = dz+np.zeros(30)
    dr = root_fr(z, dz) # Distribution according to the root distribution
    df = dr 
    
    # soil moisture limitation for T 
    # .............. transpiration is linear to soil moisture
    idx = np.where((theta>theta1)&(theta<theta2))
    idx = np.array(idx)
    gamma = (theta - theta1)/(theta2 - theta1)
    df[n-1-idx] = dr[n-1-idx]*gamma[n-1-idx]
    
    # .............. soil moisture is too low for T; no transpiration            
    idx = np.where(theta<theta1)
    idx = np.array(idx)
    df[n-1-idx] = 0

    dT = T_max*df

    # soil moisture limitation for E                                                                                                     
    # .............. transpiration is linear to soil moisture                                                                            
    if (theta[n-1]>theta0)&(theta[n-1]<theta1):
        gamma = (theta[n-1] - theta0)/(theta1 - theta0)
        E = E_max*gamma
    # .............. soil moisture is too low for T; no transpiration                                                                     
    elif theta[n-1]<theta0:
        E = 0
    else:
        E = E_max
        
    dT[0] = dT[0]+E

    for i in range(n):
        fw.write('FLOW_CONDITION sink'+str(i+1)+'\n')
        fw.write('TYPE\n')
        fw.write('RATE SCALED_VOLUMETRIC_RATE PERM\n/\n')
        fw.write('RATE '+str(dT[n-1-i])+' m^3/hr\n')
        fw.write('END\n\n')
    fw.close()

    
#E  = -5.17e-5
#T  = -1.0e-4
#et2sinks(E,T)
