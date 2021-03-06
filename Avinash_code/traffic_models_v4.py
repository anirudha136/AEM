# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 10:53:07 2015

@author: Avinash
"""
import numpy
from numpy import *

def model1(g,dir_detect,idmat,flow_init,queue_init):
    # One Way arteriel network with 20 signals

    
    
    
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
    K=1 # Total cycle
    gamma=0.5 # Platoon Dispersion Factor
    N=numpy.shape(g)[1]/2 # No of intersections/signals 
    K=numpy.shape(g)[0] # No of time samples
    Tau=4 # Cruise Travel Time
    F=1/(1+gamma*Tau)        # Smoothing factor 
    street_length=3280
    #L=street_length
    green_start=numpy.zeros(shape=(1,N))[0] # 0 for N/S and 1 for E/W. It defines the starting phase of the signal 
    
    # To find the reference signal     
    NS_close=0
    EW_close=0    
    i=0
    ref_no=0
    while i<N:
        if g[0][2*i]==-10000:
            i+=1
            NS_close+=1
        elif g[0][2*i+1]==-10000:
            i+=1
            EW_close+=1
        else:
            ref=i  # Stores the reference signal 
            i+=1            
            ref_no+=1
            if ref_no>1:
                print 'Error: More than 1 reference'
                return(0)
                
    green_start[ref]=1      # Reference signal's start phase
    print 'Reference signal= ',ref       
    close_sig=[ref]    
    # To find the closing path direction
    if NS_close<=EW_close:
        j=0
    else:
        j=2
    if flow_init[ref][j]!=-10000:
        j+=1
    i=ref
    while abs(idmat[i][j])!=21:
        close_sig.append(int(abs(idmat[i][j]))-1)  
        print close_sig
        i=int(abs(idmat[i][j]))-1
        
    close_dir=j # Stores the closing signal's direction   
    
    D=numpy.zeros(shape=(K+1,4*N))
    A=D.copy()
    queue=D.copy() 
    phi=D.copy()
    
          
    for i in range(N):  #Initial queue calculation
        for j in range(4):
            queue[0][i*4+j]=queue_init[i][j]
            
            
    for k in range(K):
        for i in range(shape(close_sig)[0]):
            if close_dir<2:
                opp_dir=1-close_dir
            else:
                opp_dir=2+(3-close_dir)
            opp_sig=abs(idmat[close_sig[i]][opp_dir])-1
            queue[k+1][close_sig[i]*4+opp_dir]=queue[k][close_sig[i]*4+opp_dir]+A[k][close_sig[i]*4+opp_dir]-D[k][close_sig[i]*4+opp_dir]
            if opp_sig!=21-1:
                A[k+1][close_sig[i]*4+opp_dir]=D[k+1][opp_sig*4+opp_dir]
                D[k+1][close_sig[i]*4+opp_dir]=Departure(queue[k+1][close_sig[i]*4+opp_dir],A[k+1][close_sig[i]*4+opp_dir],g[k][opp_sig*2+int(close_dir/2)],g[k][close_sig[i]*2+close_dir%2],saturation_flow)
            else:
                D[k+1][close_sig[i]*4+opp_dir]=(flow_init[close_sig[i]][opp_dir]/3600)*g[k][close_sig[i]*2+int(close_dir/2)]              
        
        for i in range(shape(close_sig)[0]-1):
            if k==0:
                green_start[close_sig[i+1]]=green_start[ref]
            phi[k+1][close_sig[i+1]*4+close_dir]=phi_h_star(queue[k+1][close_sig[i+1]*4+close_dir],street_length,speed_lim)
            g[k][close_sig[i+1]*2+(1-close_dir/2)]=g[k][ref*2+(1-close_dir/2)]
        
        for i1 in range(shape(close_sig)[0]):
            refn=close_sig[i1]
            close_sign=[refn]    
            j=3-close_dir
            if flow_init[ref][j]!=-10000:
                if j<2:
                    j=1-j
                else:
                    j=5-j
            sig=refn
            rev=0
            while abs(idmat[sig][j])!=21:
                if rev==0 and idmat[sig][j]>=0:
                    rev=1
                close_sign.append(int(abs(idmat[sig][j]))-1)  
                sig=int(abs(idmat[sig][j]))-1

            if rev==1:
                close_sign.reverse()


                
            close_dirn=j # Stores the closing signal's direction 
        
            for i in range(shape(close_sign)[0]):
                if close_dirn<2:
                    opp_dirn=1-close_dirn
                else:
                    opp_dirn=2+(3-close_dirn)
                print i,opp_dirn,close_dirn
                opp_sign=abs(idmat[close_sign[i]][opp_dirn])-1
                queue[k+1][close_sign[i]*4+opp_dirn]=queue[k][close_sign[i]*4+opp_dirn]+A[k][close_sign[i]*4+opp_dirn]-D[k][close_sign[i]*4+opp_dirn]
                if opp_sign!=21-1:
                    A[k+1][close_sign[i]*4+opp_dirn]=D[k+1][opp_sign*4+opp_dirn]
                    D[k+1][close_sign[i]*4+opp_dirn]=Departure(queue[k+1][close_sign[i]*4+opp_dirn],A[k+1][close_sign[i]*4+opp_dirn],g[k][opp_sign*2+int(close_dirn/2)],g[k][close_sign[i]*2+close_dirn%2],saturation_flow)
                else:
                    D[k+1][close_sign[i]*4+opp_dirn]=(flow_init[close_sign[i]][opp_dirn]/3600)*g[k][close_sign[i]*2+int(close_dirn/2)]              
             
            for i in range(shape(close_sign)[0]-1):
                if k==0:
                    green_start[close_sign[i+1]]=green_start[ref]
                phi[k+1][close_sign[i+1]*4+close_dirn]=phi_h_star(queue[k+1][close_sign[i+1]*4+close_dirn],street_length,speed_lim)
                g[k][close_sign[i+1]*2+(1-close_dirn/2)]=g[k][ref*2+(1-close_dirn/2)]
                
                        
        
    return(close_sig)




def signal_status_v2(g,T,dT,dir_detect):

    
    '''
    :param g: Effective green time[16X40]
    :param T: Total time
    :param dT: sample time
    :param dir_detect: binary array for initial direction detection
    :return: an array of all the signal conditions on east and north bound traffic
    '''
    n_cycles,n_signals = numpy.array(g).shape
    time_stamp = []
    zeros = numpy.zeros(T/dT)
    time_stamp_all=numpy.array([zeros]).T
    for i in range(n_signals/2):
        if dir_detect[i]==0:
            for j in range(n_cycles):
                a = g[j][2*i]
                b = g[j][2*i+1]
                if a==-10000:
                    n2 = b/dT
                    for k in range(n1):
                        time_stamp.append(-10000)
                    for k in range(n2):
                        time_stamp.append(0)
                elif b==-10000:
                    n1 = a/dT
                    for k in range(n1):
                        time_stamp.append(1)
                    for k in range(n2):
                        time_stamp.append(-10000)
                else:
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
                if a==-10000:
                    n2 = b/dT
                    for k in range(n2):
                        time_stamp.append(0)
                    for k in range(n2):
                        time_stamp.append(-10000)
                elif b==-10000:
                    n1 = a/dT
                    #print a,b,n1,n2
                    for k in range(n1):
                        time_stamp.append(-10000)
                    for k in range(n1):
                        time_stamp.append(1)
                else:
                    n1 = a/dT
                    n2 = b/dT
                    #print a,b,n1,n2
                    for k in range(n2):
                        time_stamp.append(0)
                    for k in range(n1):
                        time_stamp.append(1)
                #time_stamp.append(numpy.ndarray.tolist(np.ones(n1)))[0]
                #time_stamp.append(numpy.ndarray.tolist(np.zeros(n2)))[0]
        
        print time_stamp,numpy.array(time_stamp).T
        time_stamp_all = numpy.hstack((time_stamp_all,numpy.array([time_stamp]).T))
        time_stamp=[]
        
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

def Departure(q,a,g_i,g_j,s):
    '''
    
    :param q: queue length between signal i and j
    :param a: Arrival from signal i to j
    :param g_i: green time of signal i
    :param g_j: green time of signal j
    '''
    temp=(a/g_i)*(g_j-q/s)
    if temp>a:
        return(q+a)
    else:
        return(q+temp)
    