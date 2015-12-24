# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 09:43:24 2015

@author: Avinash
"""

import numpy
from math import *


def model1(g,dir_detect,id_mat,Ainit,queue_init,K=15):
    # One Way arteriel network with 20 signals


    
    
    gt_min_c=30 # max green time in coordinated streets in seconds
    gt_max_c=90 # min green time in coordinated streets in seconds
    gt_min_nc=20 # min green time in non coordinated streets in seconds
    gt_max_nc=60 # max green time in non coordinated streets in seconds
    lost_gt=5 # Lost green time in seconds    
    vel_len=2.5 # Effective vehicle length in feet
    speed_lim=40 # in feet/sec
    acceleration=4 # in feet/(sec^2) vehicle acceleration/deceleration    
    vanes=2 # No of aretrial vanes
    saturation_flow=1800 # Saturation flows in vehicles/hr
    lamda_start=16 # Statting shock wave speed 
    lamda_stop=14 # Stopping shock wave speed
    dT=5 # sample time in sec
    T=15*60 # Total Saturation time, 15 in min, T in sec
    #K=15 # Total cycles
    gamma=0.5 # Platoon Dispersion Factor
    gc = signal_status(g,T,dT,dir_detect)
    N = gc.shape[1]/2 # No of intersections/signals
    T_sample=gc.shape[0] # No of time samples
        
    capacity_eff_green=numpy.zeros(shape=(K+1,N)) # capacity during effective green interval
    for i in range(K+1):
        for j in range(N):
            capacity_eff_green[i][j]=((g[i][j*2]+g[i][j*2+1])/(g[i][j*2]+g[i][j*2+1]+lost_gt))*saturation_flow
    
    A=numpy.zeros(shape=(T_sample,N*4))
    D=A.copy()
    I=A.copy()
            
    
    Dinit=numpy.zeros_like(Ainit)
    
    return(1)
        
    
    
    
    
    
    
    
def signal_status(g,T,dT,dir_detect):
    import numpy as np
    
    '''
    :param g: Effective green time[16X40]
    :param T: Total time
    :param dT: sample time
    :param dir_detect: binary array for initial direction detection
    :return: an array of all the signal conditions on east and north bound traffic
    '''
    n_cycles,n_signals = np.array(g).shape
    time_stamp = []
    zeros = np.zeros(T/dT)
    time_stamp_all=numpy.array([zeros]).T
    for i in range(n_signals/2):
        if dir_detect[i]==0:
            for j in range(n_cycles):
                a = g[j][2*i]
                b = g[j][2*i+1]
                n1 = a/dT
                n2 = b/dT
                for k in range(n1):
                    time_stamp.append(1)
                for k in range(n2):
                    time_stamp.append(0)
                #time_stamp.append(numpy.ndarray.tolist(np.ones(n1)))
                #time_stamp.append(numpy.ndarray.tolist(np.zeros(n2)))
        elif dir_detect[i]==1:
            for j in range(n_cycles):
                b = g[j][2*i]
                a = g[j][2*i+1]
                n1 = a/dT
                n2 = b/dT
                #print a,b,n1,n2
                for k in range(n2):
                    time_stamp.append(0)
                for k in range(n1):
                    time_stamp.append(1)
                #time_stamp.append(numpy.ndarray.tolist(np.ones(n1)))[0]
                #time_stamp.append(numpy.ndarray.tolist(np.zeros(n2)))[0]
        
        print time_stamp,np.array(time_stamp).T
        time_stamp_all = np.hstack((time_stamp_all,np.array([time_stamp]).T))
        time_stamp = []
        
    time_stamp_all = time_stamp_all[:,1:]
    return time_stamp_all

def calc_beta(queue_length,L):
    '''
    :param queue_length: The length of queue at the end of the signal
    :param L: Length of the street
    :return: The time of stop wave to propagate downwards
    '''
    vel_stop = 14
    beta = (L-queue_length)/vel_stop
    return beta

def phi_h_star(queue_length,L,vel):
    '''

    :param queue_length:
    :param L:
    :param vel: Velocity in a particulat street
    :return:The offset between two signals
    '''
    vel_start = 16
    l_veh = 25
    phi = (L/vel)-((vel+vel_start)*l_veh/(vel*l_veh))*queue_length
    return phi