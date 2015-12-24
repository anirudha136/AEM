# -*- coding: utf-8 -*-
"""
Created on Wed Nov 04 15:53:09 2015

@author: Avinash
"""
from numpy import * 
import numpy
from math import * 


def fun1(x,D,bounds,ub,lb):
    penalty=0
    for i in range(D):
        if x[i]>ub[i]:
            x[i]=ub[i]
            penalty=+100
        if x[i]<lb[i]:
            x[i]=lb[i]
            penalty=+100
        if x[i]==0:
            penalty+=100
    fval=penalty
    size=int(sqrt(D))
    order=int(sqrt(size))
    x_t=x.copy()
    for i in range(D):
        temp=int(x[i]-x[i]%1)
        if temp>ub[i]:
            temp=ub[i]-1
        x_t[i]=bounds[i][temp]
        
    for i in range(D):
        row_no=i/size
        col_no=i%size
        vblock_id=row_no/order
        hblock_id=col_no/order          
        v1=0
        while v1<size:
            if x_t[row_no*size+v1]==x_t[i] and (row_no*size+v1)!=i:
                fval+=1      
                v1=size
            else:
                v1+=1
        v1=0
        while v1<size:
            if x_t[col_no+v1*size]==x_t[i] and (col_no+v1*size)!=i:
                fval+=1      
                v1=size
            else:
                v1+=1                
        v1=0
        while v1<order:
            v2=0
            while v2<order:
                if x_t[(vblock_id*order+v1)*size+(hblock_id*order+v2)]==x_t[i] and ((vblock_id*order+v1)*size+(hblock_id*order+v2))!=i:
                    fval+=1
                    v1=order
                    v2=order
                else:
                    v2+=1
            v1+=1
    return(fval)
                    
                    



def fun2(x,D,bounds,ub,lb):
    penalty=0
    for i in range(D):
        if x[i]>ub[i]:
            x[i]=ub[i]
            penalty=+10
        if x[i]<lb[i]:
            x[i]=lb[i]
            penalty=+10
    fval=penalty
    size=int(sqrt(D))
    order=int(sqrt(size))
    x_t=x.copy()
    for i in range(D):
        temp=int(x[i]-x[i]%1)
        if temp>ub[i]:
            temp=ub[i]-1
        x_t[i]=bounds[i][temp]
        
    for i in range(D):
        row_no=i/size
        col_no=i%size
        vblock_id=row_no/order
        hblock_id=col_no/order          
        v1=0
        while v1<size:
            if x_t[row_no*size+v1]==x_t[i] and (row_no*size+v1)!=i:
                fval+=1      
            v1+=1
        v1=0
        while v1<size:
            if x_t[col_no+v1*size]==x_t[i] and (col_no+v1*size)!=i:
                fval+=1      
            v1+=1                
        v1=0
        while v1<order:
            v2=0
            while v2<order:
                if x_t[(vblock_id*order+v1)*size+(hblock_id*order+v2)]==x_t[i] and ((vblock_id*order+v1)*size+(hblock_id*order+v2))!=i:
                    fval+=1
                v2+=1
            v1+=1
    return(fval)
                
def fun3(x,D,bounds,ub,lb):
    penalty=0
    for i in range(D):
        if x[i]>ub[i]:
            x[i]=ub[i]
            penalty=+10
        if x[i]<lb[i]:
            x[i]=lb[i]
            penalty=+10
    fval=penalty
    size=int(sqrt(D))
    order=int(sqrt(size))
            
    x_t=x.copy()
    
    for row_no in range(size):
        f1=0
        f2=1
        for i in range(size):
            f1+=x_t[row_no*size+i]
            f2*=x_t[row_no*size+i]
            if f1!=45:
                fval+=20
            if f2!=362880:
                fval+=20

    for col_no in range(size):
        f1=0
        f2=1
        for i in range(size):
            f1+=x_t[i*size+col_no]
            f2*=x_t[i*size+col_no]
            if f1!=45:
                fval+=20
            if f2!=362880:
                fval+=20    

    for i in range(D):
        temp=int(x[i]-x[i]%1)
        if temp>ub[i]:
            temp=ub[i]-1
        x_t[i]=bounds[i][temp]
        
    for i in range(D):
        row_no=i/size
        col_no=i%size
        vblock_id=row_no/order
        hblock_id=col_no/order          
        v1=0
        while v1<size:
            if x_t[row_no*size+v1]==x_t[i] and (row_no*size+v1)!=i:
                fval+=1      
                v1=size
            else:
                v1+=1
        v1=0
        while v1<size:
            if x_t[col_no+v1*size]==x_t[i] and (col_no+v1*size)!=i:
                fval+=1      
                v1=size
            else:
                v1+=1                
        v1=0
        while v1<order:
            v2=0
            while v2<order:
                if x_t[(vblock_id*order+v1)*size+(hblock_id*order+v2)]==x_t[i] and ((vblock_id*order+v1)*size+(hblock_id*order+v2))!=i:
                    fval+=1
                    v1=order
                    v2=order
                else:
                    v2+=1
            v1+=1
    return(fval)
    
def fun4(x,D,bounds,ub,lb):
    penalty=0
    for i in range(D):
        if x[i]>ub[i]:
            x[i]=ub[i]
            penalty=+10
        if x[i]<lb[i]:
            x[i]=lb[i]
            penalty=+10
    fval=penalty
    size=int(sqrt(D))
    order=int(sqrt(size))
            
    x_t=x.copy()
    
    for row_no in range(size):
        f1=0
        f2=1
        for i in range(size):
            f1+=x_t[row_no*size+i]
            f2*=x_t[row_no*size+i]
            if f1!=45:
                fval+=20
            if f2!=362880:
                fval+=20

    for col_no in range(size):
        f1=0
        f2=1
        for i in range(size):
            f1+=x_t[i*size+col_no]
            f2*=x_t[i*size+col_no]
            if f1!=45:
                fval+=20
            if f2!=362880:
                fval+=20   
                                   
    return(fval)
    
def fun5(x,D,bounds,ub,lb):
    penalty=0
    for i in range(D):
        if x[i]>ub[i]:
            x[i]=ub[i]
            penalty=+10
        if x[i]<lb[i]:
            x[i]=lb[i]
            penalty=+10
    fval=penalty
    size=int(sqrt(D))
    order=int(sqrt(size))
            
    x_t=x.copy()
    
    for row_no in range(size):
        f1=0
        f2=1
        for i in range(size):
            f1+=x_t[row_no*size+i]
            f2*=x_t[row_no*size+i]
            if f1!=45:
                fval+=20
            if f2!=362880:
                fval+=20

    for col_no in range(size):
        f1=0
        f2=1
        for i in range(size):
            f1+=x_t[i*size+col_no]
            f2*=x_t[i*size+col_no]
            if f1!=45:
                fval+=20
            if f2!=362880:
                fval+=20   
                
    for i in range(order):
        for j in range(order):
            f1=0
            f2=1
            for k in range(order):
                for l in range(order):
                    f1+=x_t[((3*i)+k)*size+((3*j)+l)]
                    f2*=x_t[((3*i)+k)*size+((3*j)+l)]
                if f1!=45:
                    fval+=20
                if f2!=362880:
                    fval+=20                     
    return(fval)
def fun6(x,D,bounds,ub,lb):
    penalty=0
    for i in range(D):
        if x[i]>ub[i]:
            x[i]=ub[i]
            penalty=+100
        if x[i]<lb[i]:
            x[i]=lb[i]
            penalty=+100
        if x[i]==0:
            penalty+=100
    fval=penalty
    size=int(sqrt(D))
    order=int(sqrt(size))
    x_t=x.copy()
    for i in range(D):
        temp=int(x[i]-x[i]%1)
        if temp>ub[i]:
            temp=ub[i]-1
        x_t[i]=bounds[i][temp]
    main_list=[1,2,3,4,5,6,7,8,9]
    for i in range(size):
        my_list=[]
        for j in range(size):
            my_list.append(x_t[i*size+j])
        extra=list(set(main_list)^set(my_list))
        fval+=shape(extra)[0]
    for i in range(size):
        my_list=[]
        for j in range(size):
            my_list.append(x_t[j*size+i])
        extra=list(set(main_list)^set(my_list))
        fval+=shape(extra)[0]
    for i in range(order):
        for j in range(order):
            my_list=[]
            for k in range(order):
                for h in range(order):
                    my_list.append(x_t[(i*order+k)*size+(j*order+h)])
            extra=list(set(main_list)^set(my_list))
            fval+=shape(extra)[0]                               
    return(fval)   

def fun7(x,D,bounds,ub,lb):
    penalty=0
    for i in range(D):
        if x[i]>ub[i]:
            x[i]=ub[i]
            penalty=+1
        if x[i]<lb[i]:
            x[i]=lb[i]
            penalty=+1
        if x[i]==0:
            penalty+=1
    fval=penalty
    size=int(sqrt(D))
    order=int(sqrt(size))
    x_t=x.copy()
    for i in range(D):
        temp=int(x[i]-x[i]%1)
        if temp>ub[i]:
            temp=ub[i]-1
        x_t[i]=bounds[i][temp]
    main_list=[1,2,3,4,5,6,7,8,9]
    for i in range(size):
        my_list=[]
        for j in range(size):
            my_list.append(x_t[i*size+j])
        extra=list(set(main_list)^set(my_list))
        fval+=shape(extra)[0]
    for i in range(size):
        my_list=[]
        for j in range(size):
            my_list.append(x_t[j*size+i])
        extra=list(set(main_list)^set(my_list))
        fval+=shape(extra)[0]
    for i in range(order):
        for j in range(order):
            my_list=[]
            for k in range(order):
                for h in range(order):
                    my_list.append(x_t[(i*order+k)*size+(j*order+h)])
            extra=list(set(main_list)^set(my_list))
            fval+=shape(extra)[0]                               
    return(fval)   
    
def sudoku_reduce(sudoku,size,order,true_bounds,virtual_bounds):
    for i in range(size):
        for j in range(size):
            flag1=0
            h=0
            while h<(virtual_bounds[i*size+j]):
                flag2=0
                k=0
                while k<size:
                    if k!=j:
                        l=0
                        while l<virtual_bounds[i*size+k]:
                            if true_bounds[i*size+j][h]==true_bounds[i*size+k][l]:
                                l=virtual_bounds[i*size+k]
                                k=size-1
                                flag2=1
                            else:
                                l+=1
                        k+=1
                    else:
                        k+=1
                if flag2==0:
                    sudoku[i][j]=true_bounds[i*size+j][h]
                    h+=virtual_bounds[i*size+j]
                    flag1=1
                else:
                    h+=1
                    
            if flag1==0:
                h=0
                while h<(virtual_bounds[i*size+j]):
                    flag2=0
                    k=0
                    while k<size:
                        if k!=i:
                            l=0
#                            print k,j,k*size+j
#                            print virtual_bounds
#                            print virtual_bounds[k*size+j]
                            while l<virtual_bounds[k*size+j]:
                                if true_bounds[i*size+j][h]==true_bounds[k*size+j][l]:
                                    l=virtual_bounds[k*size+j]
                                    k=size-1
                                    flag2=1
                                else:
                                    l+=1
                            k+=1
                        else:
                            k+=1
                    if flag2==0:
                        sudoku[i][j]=true_bounds[i*size+j][h]
                        h+=virtual_bounds[i*size+j]
                        flag1=1
                    else:
                        h+=1
            
            if flag1==0:
                v_block=i/order
                h_block=j/order
                h=0
                while h<(virtual_bounds[i*size+j]):
                    flag2=0
                    k1=0
                    while k1<order:
                        k2=0
                        while k2<order:
                            if (k1+v_block*order)!=i or (k2+h_block*order)!=j:
                                l=0
                                while l<virtual_bounds[(k1+v_block*order)*size+(k2+h_block*order)]:
                                    if true_bounds[i*size+j][h]==true_bounds[(k1+v_block*order)*size+(k2+h_block*order)][l]:
                                        l=virtual_bounds[(k1+v_block*order)*size+(k2+h_block*order)]
                                        k1=order-1
                                        k2=order-1
                                        flag2=1
                                    else:
                                        l+=1
                                k2+=1
                            else:
                                k2+=1
                        k1+=1
                    if flag2==0:
                        sudoku[i][j]=true_bounds[i*size+j][h]
                        h+=virtual_bounds[i*size+j]
                        flag1=1
                    else:
                        h+=1
    return(sudoku)


def sudoku_reduce2(size,order,true_bounds,virtual_bounds):
    for i in range(size):
        j=0
        while j<size:
            my_list1=[]
            my_list2=[]
            flag1=0
            flag2=0
            if virtual_bounds[i*size+j]==2:
                my_list1.append(j)
                my_list2.append(true_bounds[i*size+j][0])
                my_list2.append(true_bounds[i*size+j][0])
                flag1=1
            if flag1==1:
                flag2=0
                k=0
                while k<size and flag2==0:
                    if k!=my_list1[0] and virtual_bounds[i*size+k]==2 and true_bounds[i*size+k][0]==true_bounds[i*size+j][0] and true_bounds[i*size+k][1]==true_bounds[i*size+j][1]:
                      flag2=1
                      my_list1.append(k)
                      k=size-1
                    k+=1
                if flag2==1:
                    k=0
                    while k<size:
                        if k!=my_list1[0] and k!=my_list1[1]:
#                            temp_arr=true_bounds[i*size+k]
#                            temp_list=temp_arr.tolist()
#                            temp_list.remove(my_list2[0])
#                            temp_list.remove(my_list2[1])                            
#                            temp_list=list(set(temp_list))
#                            temp_list.remove(0)
#                            
#                            for s in range(size):
#                                if s<(shape(temp_list)[0]):
#                                    true_bounds[i*size+k][s]=temp_list[s]
#                                else:
#                                    true_bounds[i*size+k][s]=0
                            temp_list=[]        
                            l=0
                            while l<virtual_bounds[i*size+k]:
                                if true_bounds[i*size+k][l]==my_list2[0] or true_bounds[i*size+k][l]==my_list2[1]:
                                    true_bounds[i*size+k][l]=size+1
                                    virtual_bounds[i*size+k]-=1
                                elif true_bounds[i*size+k][l]==0:
                                    true_bounds[i*size+k][l]=size+1
                                l+=1
                            temp_arr=true_bounds[i*size+k]
                            temp_list=temp_arr.tolist()
                            temp_list.sort()
                            for l in range(size):
                                if temp_list[l]!=size+1:
                                    true_bounds[i*size+k][l]=temp_list[l]
                                else:
                                    true_bounds[i*size+k][l]=0                                    
                              
                        k+=1
            j+=1
        i+=1
        
    for i in range(size):
        j=0
        while j<size:
            my_list1=[]
            my_list2=[]
            flag1=0
            flag2=0
            if virtual_bounds[j*size+i]==2:
                my_list1.append(j)
                my_list2.append(true_bounds[j*size+i][0])
                my_list2.append(true_bounds[j*size+i][0])
                flag1=1
            if flag1==1:
                flag2=0
                k=0
                while k<size and flag2==0:
                    if k!=my_list1[0] and virtual_bounds[k*size+i]==2 and true_bounds[k*size+i][0]==true_bounds[j*size+i][0] and true_bounds[k*size+i][1]==true_bounds[j*size+i][1]:
                      flag2=1
                      my_list1.append(k)
                      k=size-1
                    k+=1
                if flag2==1:
                    k=0
                    while k<size:
                        if k!=my_list1[0] and k!=my_list1[1]:
#                            temp_arr=true_bounds[k*size+i]
#                            temp_list=temp_arr.tolist()
#                            temp_list.remove(my_list2[0])
#                            temp_list.remove(my_list2[1])
#                            temp_list=list(set(temp_list))
#                            temp_list.remove(0)
#                            
#                            for s in range(size):
#                                if s<(shape(temp_list)[0]):
#                                    true_bounds[k*size+i][s]=temp_list[s]
#                                else:
#                                    true_bounds[k*size+i][s]=0
                            temp_list=[]        
                            l=0
                            while l<virtual_bounds[k*size+i]:
                                if true_bounds[k*size+i][l]==my_list2[0] or true_bounds[k*size+i][l]==my_list2[1]:
                                    true_bounds[k*size+i][l]=size+1
                                    virtual_bounds[k*size+i]-=1
                                elif true_bounds[k*size+i][l]==0:
                                    true_bounds[k*size+i][l]=size+1
                                l+=1
                            temp_arr=true_bounds[k*size+i]
                            temp_list=temp_arr.tolist()
                            temp_list.sort()
                            for l in range(size):
                                if temp_list[l]!=size+1:
                                    true_bounds[k*size+i][l]=temp_list[l]
                                else:
                                    true_bounds[k*size+i][l]=0        
                        k+=1
            j+=1
        i+=1
    return([true_bounds,virtual_bounds])
    
def bound_set(true_bounds,virtual_bounds,true_bounds1,virtual_bounds1,size):
    true=numpy.zeros_like(true_bounds1)
    vir=numpy.zeros_like(virtual_bounds1)
    for i in range(size**2):
        if virtual_bounds[i]>virtual_bounds1[i]:
            vir[i]=virtual_bounds1[i]
            for j in range(size):
                true[i][j]=true_bounds1[i][j]
        else:
            vir[i]=virtual_bounds[i]
            for j in range(size):
                true[i][j]=true_bounds[i][j]
    return([true,vir])                    

            
def bound_set2(true_bounds,virtual_bounds,true_bounds1,virtual_bounds1,size):
    true=numpy.zeros_like(true_bounds1)
    vir=numpy.zeros_like(virtual_bounds1)
    for i in range(size**2):
        l=0
        for j in range(size):
           for k in range(size):
               if true_bounds1[i][j]==true_bounds[i][k]:
                   true[i][l]=true_bounds1[i][k]
                   l+=1
                   
        vir[i]=l
    return([true,vir])                    
                
    