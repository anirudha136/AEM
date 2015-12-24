# -*- coding: utf-8 -*-
"""
Created on Thu Oct 08 12:38:02 2015

@author: Avinash
"""

import numpy 
from traffic_models_v5 import model1 as func
import pandas as pd
#from my_fun3 import fun1 as func
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


count=0

while mainrunno<1:

    
    Nprt=40 #Number of particles
    Pprt=4 #Number of dead particles 
    Aprt=5 #Number of particles of which average is taken
    Lprt=10
    deathiter=10
        
    #boundary constraints
    ub=numpy.random.random(size=(D,1))
    lb=numpy.random.random(size=(D,1))
    i=0
    while i<D:
        ub[i][0]=g_c_max
        lb[i][0]=g_c_min
        i+=1
        
    
    stagiter=100
    if D==10:
        stagiter=200
    elif D==20:
        stagiter=500
    elif D==30:
        stagiter=800
    
    errmat=numpy.zeros(shape=(1,maxit+1))
    errno=0    
    
    
    
    #Termite particle velocity initializtion
    Trm=numpy.random.uniform(size=(Nprt,D))
    i=0
    while i<Nprt:
        j=0
        while j<D:
            Trm[i][j]=lb[j][0]+Trm[i][j]*(ub[j][0]-lb[j][0])
            j+=1
        i+=1
        
    

    
    #Termite Particle initial fitness evaluation
    Trval=numpy.random.uniform(size=(Nprt,1))
    Trnum=0
    while Trnum<Nprt:
        Trval[Trnum][0]=func(Trm[Trnum],g_cond,idmat,flow_init,queue_init,g_nc_min,g_nc_max,g_c_min,g_c_max,K=15,cont=1,g_form=1)
        count+=1
        Trnum+=1
    
    
    
    #Termite best and Global Best initialization
    Tbestval=Trval.copy()
    Tbestpos=Trm.copy()
    
    Gbestval=Tbestval[0][0].copy()
    Gbestpos=Tbestpos[0].copy()
    i=1
    while i<Nprt:
        if Tbestval[i][0]<Gbestval:
            Gbestval=Tbestval[i][0].copy()
            Gbestpos=Tbestpos[i].copy()
        i+=1
        
    
    
    
    #Stopping Criteria/s
    totalday=0
    totalhr=8
    totalmin=20
    totalsec=20
    maxtime=(totalday*24*60*60)+(totalhr*60*60)+(totalmin*60)+totalsec
    maxiter=maxit
    maxerr=-100000000000000000000
    
    
    
    
    #Previous and Current Velocity's Initializtion 
    Trvel1=numpy.zeros_like(Trm)
    Trvel2=Trvel1.copy()
    Trvel3=Trvel1.copy()
    Trvel4=Trvel1.copy()
    Trvel5=Trvel1.copy()
    vel=Trvel1.copy()
    
    
    #Velocity Usage Matrix/ces initialization
    velmatrix1=numpy.zeros_like(Trval)
    velmatrix2=numpy.zeros_like(Trval)
    velmatrix3=numpy.zeros_like(Trval)
    velmatrix4=numpy.zeros_like(Trval)
    velmatrix5=numpy.zeros_like(Trval)
    velmatrixtemp=numpy.zeros_like(Trval)
    
    
    #Velocity Inertia weight's Initialization 
    initw1=0.8
    initw2=initw1*0.5
    initw3=initw2*0.5
    initw4=initw3*0.5
    initw5=initw4*0.5
    
    finw1i=0.2
    finw1=finw1i
    finw2=finw1*0.5
    finw3=finw2*0.5
    finw4=finw3*0.5
    finw5=finw4*0.5
    
    
    iw1=numpy.zeros_like(Trval)
    iw2=numpy.zeros_like(Trval)
    iw3=numpy.zeros_like(Trval)
    iw4=numpy.zeros_like(Trval)
    iw5=numpy.zeros_like(Trval)
    
    
    for i in range(Nprt):
        iw1[i][0]=initw1
        iw2[i][0]=initw2
        iw3[i][0]=initw3
        iw4[i][0]=initw4
        iw5[i][0]=initw5
    
    c1=1
    c2=1
    
    
    
    it=0
    while it<maxiter and Gbestval>maxerr:
    #    if it<maxiter/5:        
    #        finw1=0.4-(0.4-0.2)*((3*it)/maxiter)
        #velocity update 
        for i in range(Nprt):
            for j in range(D):
                vel[i][j]=velmatrix1[i][0]*iw1[i][0]*Trvel1[i][j]
                vel[i][j]+=velmatrix2[i][0]*iw2[i][0]*Trvel2[i][j]
                vel[i][j]+=velmatrix3[i][0]*iw3[i][0]*Trvel3[i][j]
                vel[i][j]+=velmatrix4[i][0]*iw4[i][0]*Trvel4[i][j]
                vel[i][j]+=velmatrix5[i][0]*iw5[i][0]*Trvel5[i][j]
                vel[i][j]+=(Tbestpos[i][j]-Trm[i][j])*c1*numpy.random.rand()
                vel[i][j]+=(Gbestpos[j]-Trm[i][j])*c2*numpy.random.rand()
    
        #Position Update
        for i in range(Nprt):
            for j in range(D):
                Trm[i][j]+=vel[i][j].copy()
                if Trm[i][j]>ub[j][0]:
                    Trm[i][j]=Trm[i][j]-1.1*(Trm[i][j]-ub[j][0])
                if Trm[i][j]<lb[j][0]:
                    Trm[i][j]=Trm[i][j]-1.1*(Trm[i][j]-lb[j][0])

    
        
        
        Trvalpast1=Trval.copy()        
        Trnum=0
        for Trnum in range(Nprt):
            Trval[Trnum][0]=func(Trm[Trnum],g_cond,idmat,flow_init,queue_init,g_nc_min,g_nc_max,g_c_min,g_c_max,K=15,cont=1,g_form=1)
            count+=1
                
                
        velmatrix5=velmatrix4.copy()
        velmatrix4=velmatrix3.copy()
        velmatrix3=velmatrix2.copy()
        velmatrix2=velmatrix1.copy()
        
        Trvel5=Trvel4.copy()
        Trvel4=Trvel3.copy()
        Trvel3=Trvel2.copy()
        Trvel2=Trvel1.copy()
        
        Trvel1=vel.copy()
        
        iw5[i][0]=iw4[i][0].copy()*0.5
        iw4[i][0]=iw3[i][0].copy()*0.5
        iw3[i][0]=iw2[i][0].copy()*0.5
        iw2[i][0]=iw1[i][0].copy()*0.5
        
        #print Trval     
        
        for i in range(Nprt):
            if Trvalpast1[i][0]<Trval[i][0]:
                velmatrix1[i][0]=1
                iw1[i][0]=finw1
            elif Trvalpast1[i][0]>Trval[i][0]:
                velmatrix1[i][0]=1
                iw1[i][0]=initw1
            else:
                velmatrix1[i][0]=1
                iw1[i][0]=initw1
        for i in range(Nprt):
            if Tbestval[i][0]>Trval[i][0]:
                Tbestval[i][0]=Trval[i][0].copy()
                Tbestpos[i]=Trm[i].copy()
            
                
    #    print Trval
    #    print Trm
        
        if it%deathiter==0:
            for j in range(Nprt-1):
                min_i=j
                i=j+1
                while i<Nprt:
                    if Trval[min_i][0]>Trval[i][0]:
                        min_i=i
                    i+=1                    
                Trval[min_i][0],Trval[j][0]=Trval[j][0].copy(),Trval[min_i][0].copy()
                Trm[min_i],Trm[j]=Trm[j].copy(),Trm[min_i].copy()
                Tbestpos[min_i],Tbestpos[j]=Tbestpos[j].copy(),Tbestpos[min_i].copy()
                Tbestval[min_i][0],Tbestval[j][0]=Tbestval[j][0].copy(),Tbestval[min_i][0].copy()
                velmatrix1[min_i][0],velmatrix1[j][0]=velmatrix1[j][0].copy(),velmatrix1[min_i][0].copy()                
                velmatrix2[min_i][0],velmatrix2[j][0]=velmatrix2[j][0].copy(),velmatrix2[min_i][0].copy()
                velmatrix3[min_i][0],velmatrix3[j][0]=velmatrix3[j][0].copy(),velmatrix3[min_i][0].copy()
                velmatrix4[min_i][0],velmatrix4[j][0]=velmatrix4[j][0].copy(),velmatrix4[min_i][0].copy()
                velmatrix5[min_i][0],velmatrix5[j][0]=velmatrix5[j][0].copy(),velmatrix5[min_i][0].copy()
                Trvalpast1[min_i][0],Trvalpast1[j][0]=Trvalpast1[j][0].copy(),Trvalpast1[min_i][0].copy()
                Trvel1[min_i],Trvel1[j]=Trvel1[j].copy(),Trvel1[min_i].copy()
                Trvel2[min_i],Trvel2[j]=Trvel2[j].copy(),Trvel2[min_i].copy()
                Trvel3[min_i],Trvel3[j]=Trvel3[j].copy(),Trvel3[min_i].copy()
                Trvel4[min_i],Trvel4[j]=Trvel4[j].copy(),Trvel4[min_i].copy()
                Trvel5[min_i],Trvel5[j]=Trvel5[j].copy(),Trvel5[min_i].copy()
                iw1[min_i][0],iw1[j][0]=iw1[j][0].copy(),iw1[min_i][0].copy()
                iw2[min_i][0],iw2[j][0]=iw2[j][0].copy(),iw2[min_i][0].copy()
                iw3[min_i][0],iw3[j][0]=iw3[j][0].copy(),iw3[min_i][0].copy()
                iw4[min_i][0],iw4[j][0]=iw4[j][0].copy(),iw4[min_i][0].copy()
                iw5[min_i][0],iw5[j][0]=iw5[j][0].copy(),iw5[min_i][0].copy()
    #    print Trval
    #    print Trm
        
    #    if it%10==0:    
    #    
    #        for i in range(Nprt):
    #            for j in range(Nprt-1):
    #                if Trval[j][0]>Trval[j+1][0]:
    #                    ttempval=Trval[j+1][0].copy()
    #                    Trval[j+1][0]=Trval[j][0].copy()
    #                    Trval[j][0]=ttempval.copy()
    #                    ttemppos=Trm[j+1].copy()
    #                    Trm[j+1]=Trm[j].copy()
    #                    Trm[j]=ttemppos.copy()
    #                    ttempbpos=Tbestpos[j+1].copy()
    #                    Tbestpos[j+1]=Tbestpos[j].copy()
    #                    Tbestpos[j]=ttempbpos.copy()
    #                    ttempbval=Tbestval[j+1][0].copy()
    #                    Tbestval[j+1][0]=Tbestval[j][0].copy()
    #                    Tbestval[j][0]=ttempbval.copy()
    #    
    #                    velmatrix1[j+1][0],velmatrix1[j][0]=velmatrix1[j][0].copy(),velmatrix1[j+1][0].copy()                
    #                    velmatrix2[j+1][0],velmatrix2[j][0]=velmatrix2[j][0].copy(),velmatrix2[j+1][0].copy()
    #                    velmatrix3[j+1][0],velmatrix3[j][0]=velmatrix3[j][0].copy(),velmatrix3[j+1][0].copy()
    #                    velmatrix4[j+1][0],velmatrix4[j][0]=velmatrix4[j][0].copy(),velmatrix4[j+1][0].copy()
    #                    velmatrix5[j+1][0],velmatrix5[j][0]=velmatrix5[j][0].copy(),velmatrix5[j+1][0].copy()
    #                    Trvalpast1[j+1][0],Trvalpast1[j][0]=Trvalpast1[j][0].copy(),Trvalpast1[j+1][0].copy()
    #                    Trvel1[j+1],Trvel1[j]=Trvel1[j].copy(),Trvel1[j+1].copy()
    #                    Trvel2[j+1],Trvel2[j]=Trvel2[j].copy(),Trvel2[j+1].copy()
    #                    Trvel3[j+1],Trvel3[j]=Trvel3[j].copy(),Trvel3[j+1].copy()
    #                    Trvel4[j+1],Trvel4[j]=Trvel4[j].copy(),Trvel4[j+1].copy()
    #                    Trvel5[j+1],Trvel5[j]=Trvel5[j].copy(),Trvel5[j+1].copy()
    
        
        
        
        if it%deathiter==0:
            for i in range(Pprt):
                Trm[Nprt-1-i]=Trm[i*Aprt].copy()
                velmatrix1[Nprt-1-i][0]=1
                velmatrix2[Nprt-1-i][0]=0
                velmatrix3[Nprt-1-i][0]=0
                velmatrix4[Nprt-1-i][0]=0
                velmatrix5[Nprt-1-i][0]=0
                Trvel1[Nprt-1-i][0]=Trvel1[i*Aprt][0].copy()
                Trvel2[Nprt-1-i][0]=0
                Trvel3[Nprt-1-i][0]=0
                Trvel4[Nprt-1-i][0]=0
                Trvel5[Nprt-1-i][0]=0
                for j in range(Aprt-1):
                    Trm[Nprt-1-i]+=Trm[(i*Aprt)+j].copy()
                    Trvel1[Nprt-1-i][0]+=Trvel1[(i*Aprt)+j][0].copy()
                Trm[Nprt-1-i]/=Aprt
                k=numpy.random.randint(0,D)
                pr=numpy.random.random()
                Trm[Nprt-1-i][k]+=(2*numpy.random.random()-1)*((ub[k][0]-lb[k][0])/2)
                Trvel1[Nprt-1-i][0]/=Aprt
                Trval[Nprt-1-i][0]=func(Trm[Nprt-1-i],g_cond,idmat,flow_init,queue_init,g_nc_min,g_nc_max,g_c_min,g_c_max,K=15,cont=1,g_form=1)
                Tbestpos[Nprt-1-i]=Trm[Nprt-1-i].copy()
                Tbestval[Nprt-1-i][0]=Trval[Nprt-1-i][0].copy()
        
    #    for i in range(Lprt):
    #        if Trvalpast1[Nprt-1-i][0]<Trval[Nprt-1-i][0]:
    #            velmatrix1[i][0]=1
    #            iw1[i][0]=finw1*0.5
    #    
        
            
            
        for i in range(Nprt):
            if Tbestval[i][0]<Gbestval: 
                Gbestval=Tbestval[i][0].copy()
                Gbestpos=Tbestpos[i].copy() 
        for j in range(D):
            if Gbestpos[j]>ub[j][0]:
                Gbestpos[j]=ub[j][0]
            if Gbestpos[j]<lb[j][0]:
                Gbestpos[j]=lb[j][0]
            
        if it>stagiter:
            Pprt=5
            Aprt=2
            deathiter=2                
                
                
        partpos[mainrunno][errno]=Gbestpos
        errmat[0][errno]=Gbestval
        errno+=1
                        
        print it,Gbestval
        it+=1
    
    errmat[0][errno]=Gbestval
    mainerrmat[mainrunno]=errmat.copy()
    mainrunno+=1

numpy.savetxt("result.csv",mainerrmat,delimiter=",")
numpy.savetxt("pos0.csv",partpos[0],delimiter=",")
#numpy.savetxt("pos1.csv",partpos[1],delimiter=",")
#numpy.savetxt("pos2.csv",partpos[2],delimiter=",")
#numpy.savetxt("pos3.csv",partpos[3],delimiter=",")
#numpy.savetxt("pos4.csv",partpos[4],delimiter=",")
#numpy.savetxt("pos5.csv",partpos[5],delimiter=",")
#numpy.savetxt("pos6.csv",partpos[6],delimiter=",")
#numpy.savetxt("pos7.csv",partpos[7],delimiter=",")
#numpy.savetxt("pos8.csv",partpos[8],delimiter=",")
#numpy.savetxt("pos9.csv",partpos[9],delimiter=",")

