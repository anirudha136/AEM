# -*- coding: utf-8 -*-
"""
Created on Sat Nov 07 14:16:57 2015

@author: Avinash
"""
import numpy
from numpy import *
from math import *

def genetic_mutation(gen):
    N=-1
    temp=gen
    while temp!=0:
        temp=int(temp/10)
        N+=1
    # N is number of bits as magnitude of gen
    gen=int(gen)    
    mut_bit=numpy.random.randint(low=0,high=N)
    list1=[]
    for i in range(N+1):
        list1.append(gen%10)
        gen/=10    
    list1[N-mut_bit-1]=1-list1[N-mut_bit-1]
    gen=0
    for i in range(N+1):
        gen=gen*10+list1[N-i]
    return(gen)
    
def genetic_crossover(gen1,gen2):
    N=-1
    temp=gen1
    while temp!=0:
        temp=int(temp/10)
        N+=1
    # N is number of bits as magnitude of gen
    gen1=int(gen1)
    gen2=int(gen2)
    list1=[]
    list2=[]
    for i in range(N+1):
        list1.append(gen1%10)
        list2.append(gen2%10)
        gen1/=10
        gen2/=10
    cross_start1=numpy.random.randint(low=0,high=(N-int(N/2)+1))
    cross_start2=numpy.random.randint(low=0,high=(N-int(N/2)+1))
    for i in range(int(N/2)):
        temp=list1[cross_start1+i]  
        list1[cross_start1+i]=list2[cross_start2+i]
        list2[cross_start2+i]=temp
    for i in range(N+1):
        gen1=gen1*10+list1[N-i]
        gen2=gen2*10+list2[N-i]
    return([gen1,gen2])
        
def genetic_init(N):
    if N<=2:
        k=1
    elif N>2 and N<=4:
        k=2
    else:
        k=3
    num=1
    for i in range(k):
        num=num*10+numpy.random.randint(low=0,high=2)
    return(int(num))

def bintodec(num_bin):
    temp=int(num_bin)
    i=0
    num_dec=0
    while temp!=0:
        num_dec+=(temp%10)*(2**i)
        temp=temp/10
        i+=1
    return(int(num_dec-(2**(i-1))))

def dectobin(num_dec,N=0):
    temp=int(num_dec)
    i=0
    num_bin=0
    while temp!=0:
        num_bin+=(temp%2)*(10**i)
        temp=int(temp/2)
        i+=1
    if N!=0:
        num_bin+=10**N
    return(num_bin)
        
    
    
    
    

     
        
            