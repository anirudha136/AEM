# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 09:06:46 2015

@author: Avinash
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 10:53:07 2015

@author: Avinash
"""
import numpy
from numpy import *



def model1(g_temp,g_cond,idmat,flow_init,queue_init,g_nc_min,g_nc_max,g_c_min,g_c_max,K,cont=0,g_form=0,plot=0):
    # One Way arteriel network with 20 signals

    q_pen=10
    beta_pen=10 
    g_pen=100
    fitness_q=0
    fitness_beta=0
    fitness_g=0
    if g_form==1:
        g=numpy.zeros(shape=(15,40))
        h=0
        for i in range(15):
            for j in range(20):
                for k in range(2):
                    if g_cond[j][k]==-10000:
                        g[i][j*2+k]=-10000
                    else:
                        g[i][j*2+k]=g_temp[h]
                        h+=1
    else:
        g=g_temp
                
        
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
    #K=15 # Total cycle
    gamma=0.5 # Platoon Dispersion Factor
    N=numpy.shape(g)[1]/2 # No of intersections/signals 
    #K=numpy.shape(g)[0] # No of time samples
    Tau=4 # Cruise Travel Time
    F=1/(1+gamma*Tau)        # Smoothing factor 
    street_length=3280*2
    #L=street_length
    green_start=numpy.zeros(shape=(1,N))[0] # 0 for N/S and 1 for E/W. It defines the starting phase of the signal 
    
#    if cont==1:
#        for i in range(shape(g)[0]):
#            for j in range(shape(g)[1]):
#                g[i][j]=g[i][j]-g[i][j]%dT
    #print g
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
                return(100000)
                
    green_start[ref]=1      # Reference signal's start phase
    #print 'Reference signal= ',ref       
    close_sig=[ref]    
    # To find the closing path direction
    if NS_close>EW_close:
        j=0
    else:
        j=2
    if flow_init[ref][j]!=-10000:
        j+=1
    i=ref
    
    while abs(idmat[i][j])!=21:
        close_sig.append(int(abs(idmat[i][j]))-1)  
        #print close_sig
        i=int(abs(idmat[i][j]))-1
        
    close_dir=j # Stores the closing signal's direction   
    
    D=numpy.zeros(shape=(K+1,4*N))
    A=D.copy()
    queue=D.copy() 
    phi=D.copy()
    beta=D.copy()
    q_temp=0
    D_temp=0
    beta_con=numpy.zeros(shape=(1,K+1))[0]
    q_con=beta_con.copy()
          
    for i in range(N):  #Initial queue calculation
        for j in range(4):
            queue[0][i*4+j]=queue_init[i][j]
    #print close_sig         
 
    for k in range(K):  # Loop for cycle
        for i in range(shape(close_sig)[0]):    # For closing path
            if close_dir<2: # Direction oppostite to the flow
                opp_dir=1-close_dir
            else:
                opp_dir=2+(3-close_dir)
                
            
            opp_sig=abs(idmat[close_sig[i]][opp_dir])-1     # Signal opposite to the flow
            #print close_sig[i],i,close_dir,opp_dir,opp_sig
            queue[k+1][close_sig[i]*4+opp_dir]=queue[k][close_sig[i]*4+opp_dir]+A[k][close_sig[i]*4+opp_dir]-D[k][close_sig[i]*4+opp_dir]
            if queue[k+1][close_sig[i]*4+opp_dir]<0:
                queue[k+1][close_sig[i]*4+opp_dir]=0
            #print queue[k+1][close_sig[i]*4+opp_dir],k+1,(close_sig[i]*4+opp_dir)
            if opp_sig!=21-1:   # Indexing has been done from 0 not 1
                A[k+1][close_sig[i]*4+opp_dir]=D[k+1][opp_sig*4+opp_dir]
                D[k+1][close_sig[i]*4+opp_dir]=Departure(queue[k+1][close_sig[i]*4+opp_dir],A[k+1][close_sig[i]*4+opp_dir],g[k][opp_sig*2+int(close_dir/2)],g[k][close_sig[i]*2+close_dir/2],saturation_flow)
                phi[k+1][close_sig[i]*4+opp_dir]=phi_h_star(queue[k+1][close_sig[i]*4+opp_dir],street_length,speed_lim)                
                q_temp+=queue[k+1][close_sig[i]*4+opp_dir]
                D_temp+=D[k+1][close_sig[i]*4+opp_dir]*street_length
                beta[k+1][close_sig[i]*4+opp_dir]=calc_beta(queue[k+1][close_sig[i]*4+opp_dir],street_length)
                beta_con[k+1]=g[k][close_sig[i]*2+close_dir/2]-g[k][opp_sig*2+close_dir/2]-phi[k+1][close_sig[i]*4+opp_dir]-beta[k+1][close_sig[i]*4+opp_dir]
                q_con[k+1]=queue[k+1][close_sig[i]*4+opp_dir]-street_length/veh_len
                if beta_con[k+1]>0:
                    fitness_beta+=beta_pen*abs(beta_con[k+1])
                #if q_con[k+1]>0:                    
                    #fitness_q+=q_pen*abs(q_con[k+1])
            
                
            else:
                D[k+1][close_sig[i]*4+opp_dir]=(flow_init[close_sig[i]][opp_dir]/3600)*g[k][close_sig[i]*2+int(close_dir/2)]              
        
        for i in range(shape(close_sig)[0]-1):
            if k==0:
                green_start[close_sig[i+1]]=green_start[ref]
            C_ref=g[k][close_sig[i]*2+(1-close_dir/2)]+g[k][close_sig[i]*2+(close_dir/2)]
            g[k][close_sig[i+1]*2+(1-close_dir/2)]=(C_ref-phi[k][close_sig[i+1]*4+opp_dir])+phi[k+1][close_sig[i+1]*4+opp_dir]-g[k][close_sig[i+1]*2+(close_dir/2)]-2*lost_gt   # Eq.14
#            if g[k][close_sig[i+1]*2+(1-close_dir/2)]>g_c_max:
#                fitness_g+=g_pen*(g_c_max-g[k][close_sig[i+1]*2+(1-close_dir/2)])**2
#            if g[k][close_sig[i+1]*2+(1-close_dir/2)]<g_c_min:
#                fitness_g+=g_pen*(g[k][close_sig[i+1]*2+(1-close_dir/2)]-g_c_min)**2
            #print g[k][close_sig[i+1]*2+(1-close_dir/2)]
            if g[k][close_sig[i+1]*2+(1-close_dir/2)]<g_c_min:
                g[k][close_sig[i+1]*2+(1-close_dir/2)]=g_c_min
            if g[k][close_sig[i+1]*2+(1-close_dir/2)]>g_c_max:
                g[k][close_sig[i+1]*2+(1-close_dir/2)]=g_c_max
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

#            if rev==1:
#                close_sign.reverse()
            #print close_sign

                
            close_dirn=j # Stores the closing signal's direction 
        
            for j in range(shape(close_sign)[0]):
                if rev==0:
                    i=j
                else:
                    i=shape(close_sign)[0]-j-1
                if close_dirn<2:
                    opp_dirn=1-close_dirn
                else:
                    opp_dirn=2+(3-close_dirn)
                opp_sign=abs(idmat[close_sign[i]][opp_dirn])-1
                queue[k+1][close_sign[i]*4+opp_dirn]=queue[k][close_sign[i]*4+opp_dirn]+A[k][close_sign[i]*4+opp_dirn]-D[k][close_sign[i]*4+opp_dirn]
                if queue[k+1][close_sign[i]*4+opp_dirn]<0:
                    queue[k+1][close_sign[i]*4+opp_dirn]=0
                if opp_sign!=21-1:
                    A[k+1][close_sign[i]*4+opp_dirn]=D[k+1][opp_sign*4+opp_dirn]
                    D[k+1][close_sign[i]*4+opp_dirn]=Departure(queue[k+1][close_sign[i]*4+opp_dirn],A[k+1][close_sign[i]*4+opp_dirn],g[k][opp_sign*2+int(close_dirn/2)],g[k][close_sign[i]*2+close_dirn/2],saturation_flow)
                    phi[k+1][close_sign[i]*4+opp_dirn]=phi_h_star(queue[k+1][close_sign[i]*4+opp_dirn],street_length,speed_lim)                
                    q_temp+=queue[k+1][close_sign[i]*4+opp_dirn]
                    D_temp+=D[k+1][close_sign[i]*4+opp_dirn]*street_length
                    beta[k+1][close_sign[i]*4+opp_dirn]=calc_beta(queue[k+1][close_sign[i]*4+opp_dirn],street_length)
                    beta_con[k+1]=g[k][close_sign[i]*2+close_dirn/2]-g[k][opp_sign*2+close_dirn/2]-phi[k+1][close_sign[i]*4+opp_dirn]-beta[k+1][close_sign[i]*4+opp_dirn]
                    q_con[k+1]=queue[k+1][close_sign[i]*4+opp_dirn]-street_length/veh_len  
                    if beta_con[k+1]>0:
                        fitness_beta+=beta_pen*abs(beta_con[k+1])
                    #if q_con[k+1]>0:                    
                        #fitness_q+=q_pen*abs(q_con[k+1])
                else:
                    D[k+1][close_sign[i]*4+opp_dirn]=(flow_init[close_sign[i]][opp_dirn]/3600)*g[k][close_sign[i]*2+int(close_dirn/2)]              
             
            for i in range(shape(close_sign)[0]-1):
                if k==0:
                    green_start[close_sign[i+1]]=green_start[close_sign[i]]
                C_ref=g[k][close_sign[i]*2+(1-close_dirn/2)]+g[k][close_sign[i]*2+(close_dirn/2)]
                g[k][close_sign[i+1]*2+(1-close_dirn/2)]=(C_ref-phi[k][close_sign[i+1]*4+opp_dirn])+phi[k+1][close_sign[i+1]*4+opp_dirn]-g[k][close_sign[i+1]*2+(close_dirn/2)]-2*lost_gt
#                if g[k][close_sign[i+1]*2+(1-close_dirn/2)]>g_nc_max:
#                    fitness_g+=g_pen*(g_nc_max-g[k][close_sign[i+1]*2+(1-close_dirn/2)])**2
#                if g[k][close_sign[i+1]*2+(1-close_dirn/2)]<g_nc_min:
#                    fitness_g+=g_pen*(g[k][close_sign[i+1]*2+(1-close_dirn/2)]-g_nc_min)**2
#                #print g[k][close_sign[i+1]*2+(1-close_dirn/2)] 
                if g[k][close_sign[i+1]*2+(1-close_dirn/2)]<g_nc_min:
                    g[k][close_sign[i+1]*2+(1-close_dirn/2)]=g_nc_min
                if g[k][close_sign[i+1]*2+(1-close_dirn/2)]>g_nc_max:
                    g[k][close_sign[i+1]*2+(1-close_dirn/2)]=g_nc_max
                    
        for i1 in range(shape(close_sign)[0]-1):
            refk=close_sign[i1+1]
            close_sigk=[refk]
            j=3-close_dirn
            if flow_init[ref][j]==-10000:
                if j<2:
                    j=1-j
                else:
                    j=5-j
            sig=refk
            rev=0
            while abs(idmat[sig][j])!=21:
                if rev==0 and idmat[sig][j]>=0:
                    rev=1
                close_sigk.append(int(abs(idmat[sig][j]))-1)  
                sig=int(abs(idmat[sig][j]))-1
            #print close_sigk
            close_dirk=j # Stores the closing signal's direction 
        
            for j in range(shape(close_sigk)[0]):
                if rev==0:
                    i=j
                else:
                    i=shape(close_sigk)[0]-j-1
                if close_dirk<2:
                    opp_dirk=1-close_dirk
                else:
                    opp_dirk=2+(3-close_dirk)
                opp_sigk=abs(idmat[close_sigk[i]][opp_dirk])-1
                queue[k+1][close_sigk[i]*4+opp_dirk]=queue[k][close_sigk[i]*4+opp_dirk]+A[k][close_sigk[i]*4+opp_dirk]-D[k][close_sigk[i]*4+opp_dirk]
                if queue[k+1][close_sigk[i]*4+opp_dirk]<0:
                    queue[k+1][close_sigk[i]*4+opp_dirk]=0
                if opp_sigk!=21-1:
                    A[k+1][close_sigk[i]*4+opp_dirk]=D[k+1][opp_sigk*4+opp_dirk]
                    D[k+1][close_sigk[i]*4+opp_dirk]=Departure(queue[k+1][close_sigk[i]*4+opp_dirk],A[k+1][close_sigk[i]*4+opp_dirk],g[k][opp_sigk*2+int(close_dirk/2)],g[k][close_sigk[i]*2+close_dirk/2],saturation_flow)
                    phi[k+1][close_sig[i]*4+opp_dirk]=phi_h_star(queue[k+1][close_sigk[i]*4+opp_dirk],street_length,speed_lim)                
                    #q_temp+=queue[k+1][close_sigk[i]*4+opp_dirk]
                    D_temp+=D[k+1][close_sigk[i]*4+opp_dirk]*street_length
                    beta[k+1][close_sigk[i]*4+opp_dirk]=calc_beta(queue[k+1][close_sigk[i]*4+opp_dirk],street_length)
                    #beta_con[k+1]=g[k][close_sigk[i]*2+close_dirk/2]-g[k][opp_sigk*2+close_dirk/2]-phi[k+1][close_sigk[i]*4+opp_dirk]-beta[k+1][close_sigk[i]*4+opp_dirk]
                    q_con[k+1]=queue[k+1][close_sigk[i]*4+opp_dirk]-street_length/veh_len                
                    if beta_con[k+1]>0:
                        fitness_beta+=beta_pen*abs(beta_con[k+1])
                    if q_con[k+1]>0:                    
                        fitness_q+=q_pen*abs(q_con[k+1])
                else:
                    D[k+1][close_sigk[i]*4+opp_dirk]=(flow_init[close_sigk[i]][opp_dirk]/3600)*g[k][close_sign[i]*2+int(close_dirk/2)]              
    g_sum_con=0
    g_sum_con2=0
    for i in range(20):
        g_sum=0
        for j in range(15):
            g_sum2=0
            for k in range(2):
                g_sum+=g[j][i*2+k]
                g_sum2=g[j][i*2+k]
            if g_sum2>150:
                g_sum_con2+=10*(g_sum-(150))**2
            if g_sum2<50:
                g_sum_con2+=10*(g_sum-(50))**2

        if g_sum>115*15:
            g_sum_con+=100*(g_sum-(115*15))**2            
    #print g
    D_temp1=D_temp/street_length
    fitness_q/=1000
    fitness_beta/=1000
    fitness_g/=10000  
    g_sum_con/=500
    g_sum_con2/=100000
    if plot==1:
            numpy.savetxt("queue.csv",queue,delimiter=",")             
            numpy.savetxt("D.csv",D,delimiter=",")
            numpy.savetxt("A.csv",A,delimiter=",")
            numpy.savetxt("offset.csv",phi,delimiter=",")
            numpy.savetxt("beta.csv",beta,delimiter=",")
            numpy.savetxt("g.csv",g,delimiter=",")    
    
    fitness=-(D_temp1-q_temp-fitness_q-fitness_beta-fitness_g-g_sum_con-g_sum_con2)
    #print fitness,D_temp1,q_temp,fitness_q,fitness_beta,fitness_g,g_sum_con,g_sum_con2
    return(fitness)

def ga_model1(guy):
    '''
    Returns the fitness value as called by a function
    :param guy:
    :return:
    '''
    idmat=numpy.genfromtxt('model1_id.csv', delimiter=',')
    flow_init=numpy.genfromtxt('model1_a.csv', delimiter=',')
    queue_init=numpy.genfromtxt('model1_q.csv', delimiter=',')
    g_cond=numpy.genfromtxt('g_cond.csv', delimiter=',')

    D=21*15
    maxit=500
    mainerrmat=numpy.zeros(shape=(10,maxit+1))
    mainrunno=0
    partpos=numpy.zeros(shape=(10,maxit+1,D))

    g_c_min=30
    g_c_max=90
    g_nc_min=20
    g_nc_max=60
    def fit(guy):
        """A GA wrapper for sudoku_fitness"""
        #print(guy.genes)
        return model1(guy.genes,g_cond,idmat,flow_init,queue_init,g_nc_min,g_nc_max,g_c_min,g_c_max,K=15,cont=1,g_form=1)

    return fit



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
    
def calc_beta2(queue_length,L):
    '''
    :param queue_length: The length of queue at the end of the signal
    :param L: Length of the street
    :return: The time of stop wave to propagate downwards
    '''
    vel_stop = 14
    beta = (L-queue_length)/vel_stop
    return beta

def phi_h_star2(queue_length,L,vel):
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
    
def calc_beta(queue_length,L):
    '''
    :param queue_length: The length of queue at the end of the signal
    :param L: Length of the street
    :return: The time of stop wave to propagate downwards
    '''
    vel_stop = 14
    beta = (L-queue_length)/vel_stop
    if beta>15:
        return(15)
    #phi = (L/vel)-((vel+vel_start)*l_veh/(vel*l_veh))*queue_length
    if beta<0:
        return(0)
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
    phi=(L-queue_length*l_veh)/vel-queue_length/vel_start
    if phi>15:
        return(15)
    #phi = (L/vel)-((vel+vel_start)*l_veh/(vel*l_veh))*queue_length
    if phi<0:
        return(0)
    return phi
def Departure(q,a,g_i,g_j,s):
    '''
    
    :param q: queue length between signal i and j
    :param a: Arrival from signal i to j
    :param g_i: green time of signal i
    :param g_j: green time of signal j
    '''
    temp=(a/g_i)*(g_j-q/s)
    #print temp+a,q+a,q
    if temp>a:
        if q+a>=0:        
            return(q+a)
        else:
            return(0)
    else:
        if temp+q>=0:
            return(q+temp)
        else:
            return(0)
    