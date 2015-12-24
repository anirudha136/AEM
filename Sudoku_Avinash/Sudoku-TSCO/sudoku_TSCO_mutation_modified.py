# -*- coding: utf-8 -*-
"""
Created on Tue Nov 03 14:18:09 2015

@author: Avinash
"""


from numpy import *
import numpy
from math import *
from sudoku_fun import fun6 as func
import sudoku_fun


sudoku=numpy.genfromtxt('prob1.csv', delimiter=',')
size=shape(sudoku)[0]
order=int(sqrt(size))
main_list=[]
for i in range(size):
    main_list.append(i+1)
sudoku_row=numpy.zeros(shape=(1,size**2))
sudoku_row=sudoku_row[0]
for i in range(size):
    for j in range(size):
        sudoku_row[i*size+j]=sudoku[i][j]

true_bounds=numpy.zeros(shape=(size**2,size))
virtual_bounds=numpy.zeros(shape=(1,size**2))
virtual_bounds=virtual_bounds[0]

i=0
while i<(size**2):
    row_no=i/size
    col_no=i%size
    vblock_id=row_no/order
    hblock_id=col_no/order    
    my_list=[]
    my_bounds=[]
    if sudoku_row[i]!=0:
        true_bounds[i][0]=sudoku_row[i]
        virtual_bounds[i]=1
        i+=1
    else:
        for v1 in range(size):
            if sudoku[row_no][v1]!=0:
                my_list.append(sudoku[row_no][v1])
        for v1 in range(size):
            if sudoku[v1][col_no]!=0:
                my_list.append(sudoku[v1][col_no])
        for v1 in range(order):
            for v2 in range(order):
                if sudoku[v1+vblock_id*order][v2+hblock_id*order]!=0:
                    my_list.append(sudoku[v1+vblock_id*order][v2+hblock_id*order])
        my_bounds=list(set(main_list)^set(my_list))
        for v1 in range(shape(my_bounds)[0]):
            true_bounds[i][v1]=my_bounds[v1]
        virtual_bounds[i]=shape(my_bounds)[0]
        i+=1
val=len(sudoku[numpy.nonzero(sudoku)])
diff=1
#print true_bounds
tr=true_bounds.copy()
vr=virtual_bounds.copy()
while diff!=0:
    sudoku=sudoku_fun.sudoku_reduce(sudoku,size,order,true_bounds,virtual_bounds)
    diff=val-len(sudoku[numpy.nonzero(sudoku)])
    val=len(sudoku[numpy.nonzero(sudoku)])
    true_bounds=numpy.zeros(shape=(size**2,size))
    virtual_bounds=numpy.zeros(shape=(1,size**2))
    virtual_bounds=virtual_bounds[0]
    
    main_list=[]
    for i in range(size):
        main_list.append(i+1)
    sudoku_row=numpy.zeros(shape=(1,size**2))
    sudoku_row=sudoku_row[0]
    for i in range(size):
        for j in range(size):
            sudoku_row[i*size+j]=sudoku[i][j]

    i=0
    while i<(size**2):
        row_no=i/size
        col_no=i%size
        vblock_id=row_no/order
        hblock_id=col_no/order    
        my_list=[]
        my_bounds=[]
        if sudoku_row[i]!=0:
            true_bounds[i][0]=sudoku_row[i]
            virtual_bounds[i]=1
            i+=1
        else:
            for v1 in range(size):
                if sudoku[row_no][v1]!=0:
                    my_list.append(sudoku[row_no][v1])
            for v1 in range(size):
                if sudoku[v1][col_no]!=0:
                    my_list.append(sudoku[v1][col_no])
            for v1 in range(order):
                for v2 in range(order):
                    if sudoku[v1+vblock_id*order][v2+hblock_id*order]!=0:
                        my_list.append(sudoku[v1+vblock_id*order][v2+hblock_id*order])
            my_bounds=list(set(main_list)^set(my_list))
            for v1 in range(shape(my_bounds)[0]):
                true_bounds[i][v1]=my_bounds[v1]
            virtual_bounds[i]=shape(my_bounds)[0]
            i+=1
    #[true_bounds,virtual_bounds]=sudoku_fun.sudoku_reduce2(size,order,true_bounds,virtual_bounds)
   # [true_bounds,virtual_bounds]=sudoku_fun.bound_set(tr,vr,true_bounds,virtual_bounds,size)    
    #print true_bounds
    print val,virtual_bounds[0]
#print sudoku
val=len(sudoku[numpy.nonzero(sudoku)])
print val

[true_bounds,virtual_bounds]=sudoku_fun.bound_set(tr,vr,true_bounds,virtual_bounds,size)    
val=len(sudoku[numpy.nonzero(sudoku)])
print val

D=size**2
maxit=10000
mainerrmat=numpy.zeros(shape=(10,maxit+1))
mainrunno=0
partpos=numpy.zeros(shape=(10,maxit+1,D))

Nprt=40 #Number of particles
Pprt=4 #Number of dead particles 
Aprt=5 #Number of particles of which average is taken
Lprt=10
deathiter=2
    
#boundary constraints
lb=numpy.zeros(shape=(1,size**2))
lb=lb[0]
ub=lb+virtual_bounds.copy()

    
stagiter=200


errmat=numpy.zeros(shape=(1,maxit+1))
errno=0    


#Termite particle velocity initializtion
Trm=numpy.random.uniform(size=(Nprt,D))
i=0
while i<Nprt:
    j=0
    while j<D:
        Trm[i][j]=lb[j]+Trm[i][j]*(ub[j]-lb[j])
        j+=1
    i+=1
    



#Termite Particle initial fitness evaluation
Trval=numpy.random.uniform(size=(Nprt,1))
Trnum=0
while Trnum<Nprt:
    Trval[Trnum][0]=func(Trm[Trnum],D,true_bounds,ub,lb)
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
maxerr=0




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
            if Trm[i][j]>ub[j]:
                Trm[i][j]=Trm[i][j]-1.1*(Trm[i][j]-ub[j])
            if Trm[i][j]<lb[j]:
                Trm[i][j]=Trm[i][j]-1.1*(Trm[i][j]-lb[j])


    
    
    Trvalpast1=Trval.copy()        
    Trnum=0
    for Trnum in range(Nprt):
        Trval[Trnum][0]=func(Trm[Trnum],D,true_bounds,ub,lb)
            
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
            k=numpy.random.randint(0,size)
            k1=numpy.random.randint(0,size)
            k2=numpy.random.randint(0,size)
            pr=numpy.random.random()
            Trm[Nprt-1-i][k*size+k1],Trm[Nprt-1-i][k*size+k2]=Trm[Nprt-1-i][k*size+k2],Trm[Nprt-1-i][k*size+k1]
            Trvel1[Nprt-1-i][0]/=Aprt
            Trval[Nprt-1-i][0]=func(Trm[Nprt-1-i],D,true_bounds,ub,lb)
            Tbestpos[Nprt-1-i]=Trm[Nprt-1-i].copy()
            Tbestval[Nprt-1-i][0]=Trval[Nprt-1-i][0].copy()
                    
    for i in range(Nprt):
        if Tbestval[i][0]<Gbestval: 
            Gbestval=Tbestval[i][0].copy()
            Gbestpos=Tbestpos[i].copy() 
    for j in range(D):
        if Gbestpos[j]>ub[j]:
            Gbestpos[j]=ub[j]
        if Gbestpos[j]<lb[j]:
            Gbestpos[j]=lb[j]
        
    if it>stagiter:
        Pprt=5
        Aprt=2
        deathiter=2      
    sudoku1=numpy.zeros(shape=(size,size))
    for i in range(D):
        v_id=i/size
        c_id=i%size
        sudoku1[v_id][c_id]=true_bounds[i][int(Gbestpos[i])]
    print sudoku1          
            
            
    partpos[mainrunno][errno]=Gbestpos
    errmat[0][errno]=Gbestval
    errno+=1
                    
    print it,Gbestval
    it+=1

    
errmat[0][errno]=Gbestval
mainerrmat[mainrunno]=errmat.copy()




numpy.savetxt("result.csv",mainerrmat,delimiter=",")
numpy.savetxt("pos0.csv",partpos[0],delimiter=",")
