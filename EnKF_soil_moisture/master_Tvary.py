# Run PFLOTRAN sequentially
import os, sys, time, math
import subprocess
from et2sinks_lim import *
from et2sinks import *
from Kalman_functions import *
from obsread import *
from pres2initial import*
from rain2window import *
from Tseries2T import *
from pres_theta import*
# ----------------
# Parameters
# ----------------
E_max  = -3.64e-4

# Read variable T
Tseries = np.genfromtxt('T_columbia_winter.txt', skip_header=2)

# Rainfall                                                                                                                  
rain = np.genfromtxt('rainfall_columbia_winter.txt', skip_header=2)

n  = 30 #30 grid blocks
std_noise = 0.0005 # Measurement error in the measurement function

# Time steps
dt = 1 # hr, observation time steps
n_t  = 2327  # # time steps

#  Measurements 
idx_dep = [4] # measured gridblocks (from bottom to top = surface)

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
H   = H_mat(n, idx_dep)

# ----------------            
# Initial Conditio
# ----------------
T_max = Tseries[0,1]
et2sinks(E_max, T_max)
os.popen('cp  pf_initial.in pflotran.in')
os.system('~/pflotran/src/pflotran/pflotran > log')
pres, end_time = obsread(n)
theta = pres2theta(pres, m, s_lr, alpha, por)
pres2initial(pres)

# ----------------                                                                                                            # Simulation                                                                                                                  # ---------------- 
os.popen('cp pf_seq.in pflotran.in')
for i in range(n_t):
    time = i*dt
    rain2window(rain,time)
    T_max = (-1)*Tseries2T(Tseries,time)
    et2sinks_lim(E_max, T_max, theta, s_lr, theta1,theta2)
    pres2initial(pres)
    os.system('~/pflotran/src/pflotran/pflotran > log')
    pres, end_time = obsread(n)
    theta = pres2theta(pres, m, s_lr, alpha, por)
    sensor_data[:,i]  = np.dot(H,theta) + np.random.normal(0, std_noise, len(idx_dep))   
    theta_save[:,i]   = theta
    print('Run #:'+str(i))
        
np.savetxt('sensor_data_Tvary.csv', sensor_data, delimiter=',')
np.savetxt('synthetic_theta_Tvary.csv', theta_save, delimiter=',')
