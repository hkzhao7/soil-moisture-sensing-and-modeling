# Functions related to EnKF

import numpy as np

def hx(H,x):
    # Measurement function 
    # Measurement is defined by the measurement matrix H
    z = np.dot(H,x)
    return z              

def H_mat(n, idx_dep):
    # Create the measurement matrix (n by m)
    # if j-th grid block is i-th measurement
    # -------------
    # n: # grid blocks
    # idx_dep: index of grid block measured 
    # H: measurement matrix
    H = np.zeros((len(idx_dep),n))
    for i in range(len(idx_dep)):
        H[i,idx_dep[i]]=1
    return H

def theta2psi(theta,alpha, theta_S, theta_R, n):
    Psi = ((theta_S-theta_R)/(theta - theta_R))**(n/(n-1)) 
    Psi = (Psi-1)**(1/n)
    Psi = -Psi/alpha/100
    return(Psi)

def rain2timesteps(rain_data,dt):
    time = rain_data[:,0]
    value = rain_data[:,1]
    dt_rain = time[1]-time[0]
    n = int(dt_rain/dt)
    rain = np.zeros((len(time),n))
    for i in range(n):
        rain[:,i] = value/n
    rain = rain.flatten()
    return(rain)
    
def Tmax2timesteps(Tmax_data,dt):
    time = Tmax_data[:,0]
    value = Tmax_data[:,1]
    dt_rain = (time[1]-time[0])*24   #hr
    n = int(dt_rain/dt)
    Tmax_dt = np.zeros((len(time),n))
    for i in range(n):
        Tmax_dt[:,i] = value
    Tmax_dt = Tmax_dt.flatten()
    return(Tmax_dt)    

def sensor2obs(sensor_data, dn_time): # less frequent temporal data 
    idx = [int(i*dn_time) for i in range(int(sensor_data.shape[1]/dn_time))]
    sensor=sensor_data[:,idx]
    return(sensor)
    
    
