# Run PFLOTRAN sequentially
import os, sys, time, math
import subprocess
from et2sinks_lim import *
from et2sinks import *
from Kalman_functions import *
from obsread import *
from pres2initial import*
from rain2window import *
from pres_theta import *

# ----------------
# Parameters
# ----------------
E  = -4.17e-5    # unit changed (1/1000), then unchanged
T  = -2.0e-4    # unit changed (1/1000), then unchanged

n  = 30 # 30 grid blocks
std_noise = 0.001 # Measurement error in the measurement function

# Time steps
dt = 2 # hr, observation time steps
n_t  = 100  # time steps

# Measurements 
idx_dep = [10,17,23,29] # measured gridblocks    

# Rainfall
rain = np.genfromtxt('rainfall_v1.txt',skip_header=2)

# Parameters
m = 0.5
s_lr = 0.05
alpha = 1.0e-3
por = 0.4
theta1 = 0.1
theta2 = 0.2

# ----------------                                                                                                                      
# Setting up                                                                                                                            
# ----------------
sensor_data  = np.zeros((len(idx_dep),n_t)) # soil moisture save array
theta_save   = np.zeros((n,n_t)) # soil moisture save array
H  = H_mat(n, idx_dep)    # H_mat_avg() new function to convert measurements

# ----------------                                                                                                                                     
# Initial Condition                                                                                                                                    
# ----------------
et2sinks(E, T)
os.popen('cp  pf_initial.in pflotran.in')
os.system('~/pflotran/src/pflotran/pflotran > log')
pres, end_time = obsread(n)
pres2initial(pres)
theta = pres2theta(pres, m, s_lr, alpha, por)

# ----------------                                                                                                                     
# Simulation                                                                                                                            
# ---------------- 
os.popen('cp pf_seq.in pflotran.in')
for i in range(n_t):
    time = i*dt
    rain2window(rain,time)
    pres2initial(pres)
    et2sinks_lim(E, T, theta, s_lr, theta1,theta2)
    os.system('~/pflotran/src/pflotran/pflotran > log')
    pres, end_time = obsread(n)
    theta = pres2theta(pres, m, s_lr, alpha, por)
    sensor_data[:,i]  = np.dot(H,theta) + np.random.normal(0, std_noise, len(idx_dep))   
    theta_save[:,i]   = theta     # gets saved into a text file
    print('Run #:'+str(i))
    print(np.dot(H,theta))
    
np.savetxt('sensor_data.csv', sensor_data, delimiter=',')
np.savetxt('synthetic_theta.csv', theta_save, delimiter=',')    # same as the single run
