# pressure to theta
import numpy as np

def pres2theta(pres, m, s_lr, alpha, por):
    Pgas = 1.013250030728884e+05
    n = 1/(1-m)

    Pc = Pgas - pres
    s  = s_lr + (1-s_lr)/((Pc*alpha)**n+1)**m
    s  = s*por

    idx = np.where(pres>Pgas)
    s[idx] = por
    return s

def theta2pres(theta, m, s_lr, alpha, por):
    Pgas = 1.013250030728884e+05
    n = 1/(1-m)
    s = theta/por

    s = (s - s_lr)/(1 - s_lr)
    Pc = 1/alpha*(s**(-1/m)-1)**(1/n) 

    pres = Pgas - Pc
    return pres
    

    
