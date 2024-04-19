# Run PFLOTRAN sequentially
import os, sys, time, math
import subprocess
from et2sinks import *
from Kalman_functions import *
from obsread import *
from pres2initial import*
from rain2window import*
from pres_theta import*
from et2sinks_lim import*

from scipy.sparse import diags
from scipy.sparse import dia_matrix
from scipy.sparse.linalg import spsolve
from scipy import linalg

# ----------------
# Input
# ----------------
E_max  = -4.17e-5
T_max  = -2.0e-4

# Prior distribtuion of T_max, which is used for EnKF
T_max_mu    = 0.2*1e-3 # m/hr
T_max_sigma = 0.1*1e-3

# Domain
n  = 30 #30 grid blocks

# Time steps
dt = 2 # hr, observation time steps
n_t = 100 # # rain timesteps

#  Measurements 
sensor_data = np.genfromtxt('sensor_data_Tvary.csv',delimiter=',')    # synthetic dataset
idx_dep = [10,17,23,29] # measured gridblocks    
std_noise = 0.001 # Measurement error in the measurement function

# Rainfall data in PFLOTRAN format
rain = np.genfromtxt('rainfall_v1.txt',skip_header=2)

# Parameters                                                                                                                  
m = 0.5
s_lr = 0.05
alpha = 1.0e-3
por = 0.4
theta1 = 0.1
theta2 = 0.2

#................... EnKalman filter
n_rand = 200 # # of random samples for emsemble  

# ----------------                                                                                                            # Initialization                        
# ----------------
H   = H_mat(n, idx_dep) # the matrix to transfer grids to measurements 

#................... Kalman Filter Initialization    
P_prior         = np.eye(n)*0.0
P_posterior     = np.eye(n)*0.0
R               = np.eye(len(idx_dep))*std_noise**2
theta_estimated = np.zeros((n,n_t));
T_est = np.zeros((n_t,1))

# ----------------
# Simulation                                                                                                                  # ----------------
# Initial condition
et2sinks(E_max, T_max)
os.popen('cp  pf_initial.in pflotran.in') # initial condition is in pf_initial.in
os.system('~/pflotran/src/pflotran/pflotran > log')
pres, end_time = obsread(n)
theta_n_posterior = pres2theta(pres, m, s_lr, alpha, por)  
pres2initial(pres)

# Simulation starts
os.popen('cp pf_seq.in pflotran.in')    # pf_seq read by python
for i in range(n_t):
    print('Run #:'+str(i))
    time =i*dt
    rain2window(rain,time)
    T_sample      = np.random.normal(T_max_mu, T_max_sigma, n_rand) # Tmax from prior
    theta_init_sample = np.random.multivariate_normal(theta_n_posterior, P_posterior, n_rand) # Tmax from prior 
    theta_sample      = np.zeros((n,n_rand));
    for i_rand in range(n_rand):
        T_max = (-1)*T_sample[i_rand]
        pres = theta2pres(theta_init_sample[i_rand,:], m, s_lr, alpha, por)
        pres2initial(pres)
        et2sinks_lim(E_max, T_max, theta_init_sample[i_rand,:], s_lr, theta1,theta2)
        os.system('~/pflotran/src/pflotran/pflotran > log')
        pres, end_time = obsread(n)
        theta = pres2theta(pres, m, s_lr, alpha, por)
        theta_sample[:,i_rand]    = theta
        
    # ---------------------------
    P_prior  = np.cov(theta_sample)
    theta_n_prior = np.mean(theta_sample.transpose(),axis=0)
    print(theta_n_prior)
    print(np.dot(H,theta_n_prior))
    # Kalman update 
    K0 = np.dot(H, P_prior)
    K0 = np.dot(K0, H.T)
    K0 = K0 + R
    print(sensor_data[:,i])
    y = sensor_data[:,i] - np.dot(H,theta_n_prior) 
    K = linalg.solve(K0, y)
    K = np.dot(H.T,K)
    theta_n_posterior = theta_n_prior + np.dot(P_prior,K)
    
    K = linalg.solve(K0,H)
    K = np.dot(H.T,K)
    K = np.dot(P_prior,K)
    P_posterior = P_prior - np.dot(K,P_prior)
    
    # Goal is to calculate this
    # K = P_prior*H'*inv(H*P_prior*H'+ R);
    # x_posterior = x_prior + K*(data - H*x_prior);
    # P = P - K*H*P_prior;
    # Parts
    # K0 = H*P_prior*H'+ R
    # y = data - H*x_prior
    # x_posterior = x_prior + P_prior*H'*(K0\y)
    # P = P - P_prior*H'*(K0\H)*P_prior;

    theta_estimated[:,i]      = theta_n_posterior

    np.savetxt('theta_estimated.csv', theta_estimated, delimiter=',')
