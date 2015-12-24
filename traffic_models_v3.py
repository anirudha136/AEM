# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 09:43:24 2015

@author: Avinash
"""
from numpy import *
import numpy
from math import *


def model1(g,dir_detect,idmat,flow_init,queue_init,K=15):
    # One Way arteriel network with 20 signals
    from numpy import *
    
    
    
    gt_min_c=30 # max green time in coordinated streets in seconds
    gt_max_c=90 # min green time in coordinated streets in seconds
    gt_min_nc=20 # min green time in non coordinated streets in seconds
    gt_max_nc=60 # max green time in non coordinated streets in seconds
    lost_gt=5 # Lost green time in seconds    
    veh_len=2.5 # Effective vehicle length in feet
    speed_lim=40 # in feet/sec
    acceleration=4 # in feet/(sec^2) vehicle acceleration/deceleration    
    vanes=2 # No of aretrial vanes
    saturation_flow=1800 # Saturation flows in vehicles/hr
    lamda_start=16 # Statting shock wave speed 
    lamda_stop=14 # Stopping shock wave speed
    dT=5 # sample time in sec
    T=15*60 # Total Saturation time, 15 in min, T in sec
    #K=15 # Total cycles
    gc=signal_status(g,T,dT,dir_detect)
    gamma=0.5 # Platoon Dispersion Factor
    N=shape(gc)[1]/2 # No of intersections/signals 
    T_sample=shape(gc)[0] # No of time samples
    Tau=4 # Cruise Travel Time
    F=1/(1+gamma*Tau)        # Smoothing factor 
    street_length=3280
    L=street_length
    

    capacity_eff_green=numpy.zeros(shape=(K+1,N)) # capacity during effective green interval
    for i in range(K+1):
        for j in range(N):
            capacity_eff_green[i][j]=((g[i][j*2]+g[i][j*2+1])/(g[i][j*2]+g[i][j*2+1]+lost_gt))*saturation_flow
    
    offset=numpy.zeros(shape=(K+1,N*2))
    A=numpy.zeros(shape=(T_sample,N*4))
    beta = offset.copy()
    D=A.copy()
    I=A.copy()
    q=A.copy()
    D_sum=0
    q_sum=0
    c1_sum=0
    c2_sum=0
    c3_sum=0

    cycle_no=numpy.zeros(N)
    cycle_time=numpy.zeros(N)
    for i in range(N):
        cycle_time[i]=g[0][i*2]+g[0][i*2+1]
            
    for i in range(N):
        for j in range(4):
            if flow_init[i][j]==NaN:
                A[0][i*4+j]=NaN
                D[0][i*4+j]=NaN
                q[0][i*4+j]=NaN

            else:
                if gc[0][i]==1:
                    if j%4==0 or (j-1)%4==0:
                        A[0][i*4+j]=flow_init[i][j]
                        D[0][i*4+j]=A[0][i*4+j]+queue_init[0][i*4+j]/dT
                        if D[0][i*4+j]>capacity_eff_green[0][i]:
                            D[0][i*4+j]=capacity_eff_green[0][i]
                        q[0][i*4+j]=queue_init[i][j]+(A[0][i*4+j]-D[0][i*4+j])*dT
                        if q[0][i*4+j]<0:
                            q[0][i*4+j]=0
                    else:
                        A[0][i*4+j]=flow_init[i][j]
                        D[0][i*4+j]=0
                        q[0][i*4+j]=queue_init[i][j]+(A[0][i*4+j]-D[0][i*4+j])*dT
                        if q[0][i*4+j]<0:
                            q[0][i*4+j]=0
                else:
                    if (j-2)%4==0 or (j-3)%4==0:
                        A[0][i*4+j]=flow_init[i][j]
                        D[0][i*4+j]=A[0][i*4+j]+queue_init[0][i*4+j]/dT
                        if D[0][i*4+j]>capacity_eff_green[0][i]:
                            D[0][i*4+j]=capacity_eff_green[0][i]
                        q[0][i*4+j]=queue_init[i][j]+(A[0][i*4+j]-D[0][i*4+j])*dT
                    else:
                        A[0][i*4+j]=flow_init[i][j]    
                        D[0][i*4+j]=0
                        q[0][i*4+j]=queue_init[i][j]
                        if q[0][i*4+j]<0:
                            q[0][i*4+j]=0        
        cycle_time[i]-=5

                        
    for i in range(N):
        for j in range(4):
            if flow_init[i][j]==NaN:
                I[0][i*4+j]=NaN
            else:
                injector_sig=idmat[i][j]                
                if gc[0][injector_sig]==1:
                    if j%4==0 or (j-1)%4==0:
                        if injector_sig<21:
                            I[0][i*4+j]=D[0][injector_sig*4+j]
                    else:
                        I[0][i*4+j]=0
                else:
                    if (j-2)%4==0 or (j-3)%4==0:
                        if injector_sig<21:
                            I[0][i*4+j]=D[0][injector_sig*4+j]
                    else:
                        I[0][i*4+j]=0
    t=1        
    while t<T_sample:
        for i in range(N):
            for j in range(4):
                if A[t-1][i*4+j]==NaN:
                    A[t][i*4+j]=NaN
                    D[t][i*4+j]=NaN
                    q[t][i*4+j]=NaN
    
                else:
                    if gc[t][i]==1:
                        if j%4==0 or (j-1)%4==0:
                            if t-Tau<0:
                                A[t][i*4+j]=F*I[0][i*4+j]+(1-F)*A[t-1][i*4+j]
                            else:
                                A[t][i*4+j]=F*I[t-Tau][i*4+j]+(1-F)*A[t-1][i*4+j]
                            
                            D[t][i*4+j]=A[t][i*4+j]+q[t-1][i*4+j]/dT
                            if D[t][i*4+j]>capacity_eff_green[cycle_no][i]:
                                D[t][i*4+j]=capacity_eff_green[cycle_no][i]
                            q[t][i*4+j]=q[t-1][i*4+j]+(A[t][i*4+j]-D[t][i*4+j])*dT
                            if q[t][i*4+j]<0:
                                q[t][i*4+j]=0
                        else:
                            if t-Tau<0:
                                A[t][i*4+j]=F*I[0][i*4+j]+(1-F)*A[t-1][i*4+j]
                            else:
                                A[t][i*4+j]=F*I[t-Tau][i*4+j]+(1-F)*A[t-1][i*4+j]
                            D[t][i*4+j]=0
                            q[t][i*4+j]=q[t-1][i*4+j]+(A[t][i*4+j]-D[t][i*4+j])*dT
                            if q[t][i*4+j]<0:
                                q[t][i*4+j]=0 
                    else:
                        if (j-2)%4==0 or (j-3)%4==0:
                            if t-Tau<0:
                                A[t][i*4+j]=F*I[0][i*4+j]+(1-F)*A[t-1][i*4+j]
                            else:
                                A[t][i*4+j]=F*I[t-Tau][i*4+j]+(1-F)*A[t-1][i*4+j]

                            D[t][i*4+j]=A[t][i*4+j]+q[t-1][i*4+j]/dT
                            if D[t][i*4+j]>capacity_eff_green[cycle_no][i]:
                                D[t][i*4+j]=capacity_eff_green[cycle_no][i]
                            q[t][i*4+j]=q[t-1][i*4+j]+(A[t][i*4+j]-D[t][i*4+j])*dT
                            if q[t][i*4+j]<0:
                                q[t][i*4+j]=0   
                        else:
                            if t-Tau<0:
                                A[t][i*4+j]=F*I[0][i*4+j]+(1-F)*A[t-1][i*4+j]
                            else:
                                A[t][i*4+j]=F*I[t-Tau][i*4+j]+(1-F)*A[t-1][i*4+j]    
                            D[t][i*4+j]=0
                            q[t][i*4+j]=q[t-1][i*4+j]+(A[t][i*4+j]-D[t][i*4+j])*dT
                            if q[t][i*4+j]<0:
                                q[t][i*4+j]=0        

            cycle_time[i]-=5
            if cycle_time[i]==0:
                if gc[t]==1:
                    if A[t][4*i]==NaN:
                        offset[cycle_no[i]][i*2+1]=phi_h_star(q[t][4*i+1],L)
                        beta[cycle_no[i]][i*2+1]=calc_beta(q[t][4*i+1],L,speed_lim)
                        D_sum+=D[t][4*i+1]
                        q_temp=q[t][4*i+1]-130
                        if q_temp>0:
                            q_sum+=q_temp
                        c1_temp=(street_length/speed_lim)-((speed_lim+lamda_start)*veh_len/(speed_lim*lamda_start)*q[t][4*i+1])
                        c1_sum+=(offset[cycle_no[i]][i*2+1]-c1_temp)**2
                                                              
                        
                    else:
                        offset[cycle_no[i]][i*2+1]=phi_h_star(q[t][4*i],L)
                        beta[cycle_no[i]][i*2+1]=calc_beta(q[t][4*i],L,speed_lim)                        
                        D_sum+=D[t][4*i]
                        q_temp=q[t][4*i]-130
                        if q_temp>0:
                            q_sum+=q_temp
                        c1_temp=(street_length/speed_lim)-((speed_lim+lamda_start)*veh_len/(speed_lim*lamda_start)*q[t][4*i])
                        c1_sum+=(offset[cycle_no[i]][i*2+1]-c1_temp)**2
                else:
                    if A[t][4*i+2]==NaN:
                        offset[cycle_no[i]][i*2+1]=phi_h_star(q[t][4*i+3],L)
                        beta[cycle_no[i]][i*2+1]=calc_beta(q[t][4*i+3],L,speed_lim)                        
                        D_sum+=D[t][4*i+3]
                        q_temp=q[t][4*i+3]-130
                        if q_temp>0:
                            q_sum+=q_temp
                        c1_temp=(street_length/speed_lim)-((speed_lim+lamda_start)*veh_len/(speed_lim*lamda_start)*q[t][4*i+3])
                        c1_sum+=(offset[cycle_no[i]][i*2+1]-c1_temp)**2
                    else:
                        offset[cycle_no[i]][i*2+1]=phi_h_star(q[t][4*i+2],L)
                        beta[cycle_no[i]][i*2+1]=calc_beta(q[t][4*i+2],L,speed_lim)
                        D_sum+=D[t][4*i+2]
                        q_temp=q[t][4*i+2]-130
                        if q_temp>0:
                            q_sum+=q_temp
                        c1_temp=(street_length/speed_lim)-((speed_lim+lamda_start)*veh_len/(speed_lim*lamda_start)*q[t][4*i+2])
                        c1_sum+=(offset[cycle_no[i]][i*2+1]-c1_temp)**2
                cycle_no[i]+=1
                cycle_time[i]=g[cycle_no[i]][i*2]+g[cycle_no[i]][i*2+1]
            if cycle_time[i]-g[cycle_no[i]][i*2]==0:
                if gc[t]==1:
                    if A[t][4*i]==NaN:
                        offset[cycle_no[i]][i*2]=phi_h_star(q[t][4*i+1],L)
                        beta[cycle_no[i]][i*2]=calc_beta(q[t][4*i+1],L,speed_lim) 
                        D_sum+=D[t][4*i+1]
                        q_temp=q[t][4*i+1]-130
                        if q_temp>0:
                            q_sum+=q_temp
                        c1_temp=(street_length/speed_lim)-((speed_lim+lamda_start)*veh_len/(speed_lim*lamda_start)*q[t][4*i+1])
                        c1_sum+=(offset[cycle_no[i]][i*2]-c1_temp)**2
                    else:
                        offset[cycle_no[i]][i*2]=phi_h_star(q[t][4*i],L)
                        beta[cycle_no[i]][i*2]=calc_beta(q[t][4*i],L,speed_lim)
                        D_sum+=D[t][4*i]
                        q_temp=q[t][4*i]-130
                        if q_temp>0:
                            q_sum+=q_temp
                        c1_temp=(street_length/speed_lim)-((speed_lim+lamda_start)*veh_len/(speed_lim*lamda_start)*q[t][4*i])
                        c1_sum+=(offset[cycle_no[i]][i*2]-c1_temp)**2
                else:
                    if A[t][4*i+2]==NaN:
                        offset[cycle_no[i]][i*2]=phi_h_star(q[t][4*i+3],L)
                        beta[cycle_no[i]][i*2]=calc_beta(q[t][4*i+3],L,speed_lim)
                        D_sum+=D[t][4*i+3]
                        q_temp=q[t][4*i+3]-130
                        if q_temp>0:
                            q_sum+=q_temp
                        c1_temp=(street_length/speed_lim)-((speed_lim+lamda_start)*veh_len/(speed_lim*lamda_start)*q[t][4*i+3])
                        c1_sum+=(offset[cycle_no[i]][i*2]-c1_temp)**2
                    else:
                        offset[cycle_no[i]][i*2]=phi_h_star(q[t][4*i+2],L)  
                        beta[cycle_no[i]][i*2]=calc_beta(q[t][4*i+2],L,speed_lim)
                        D_sum+=D[t][4*i+2]
                        q_temp=q[t][4*i+2]-130
                        if q_temp>0:
                            q_sum+=q_temp
                        c1_temp=(street_length/speed_lim)-((speed_lim+lamda_start)*veh_len/(speed_lim*lamda_start)*q[t][4*i+2])
                        c1_sum+=(offset[cycle_no[i]][i*2]-c1_temp)**2
                
                

        for i in range(N):
            for j in range(4):
                if A[t][i*4+j]==NaN:
                    I[t][i*4+j]=NaN
                else:
                    injector_sig=idmat[i][j]                
                    if gc[0][injector_sig]==1:
                        if j%4==0 or (j-1)%4==0:
                            if injector_sig<21:
                                I[t][i*4+j]=D[t][injector_sig*4+j]
                        else:
                            I[t][i*4+j]=0
                    else:
                        if (j-2)%4==0 or (j-3)%4==0:
                            if injector_sig<21:
                                I[t][i*4+j]=D[t][injector_sig*4+j]
                        else:
                            I[t][i*4+j]=0
        t+=1

    for cycle_no in range(K):
        for i in range(N):
            if A[0][i*4]==NaN:
                id1=idmat[i][1]
            else:
                id1=idmat[i][0]
            if A[0][i*4+2]==NaN:
                id2=idmat[i][3]
            else:
                id2=idmat[i][2]
            c2_sum+=g[cycle_no][id1]+g[cycle_no][id2]-2*g[cycle_no][i]-offset[cycle_no][i*2]-offset[cycle_no][i*2+1]-beta[cycle_no][i*2]-beta[cycle_no][i*2+1]
            
    u1=1800
    u2=1800
    delta=2    
    fval=D_sum-delta*q_sum-u1*c1_sum-u2*c2_sum
    
    return(-fval)
        
    
    
    
    
    
    
    
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