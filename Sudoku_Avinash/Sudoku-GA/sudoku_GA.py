# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 13:47:50 2015

@author: Avinash
"""

from numpy import *
import numpy
from math import *
from sudoku_fun import fun7 as func
import ga_fun 

sudoku=numpy.genfromtxt('prob1.csv', delimiter=',')
size=shape(sudoku)[0]
order=int(sqrt(size))


list_err=[]
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


D=size**2

lb=numpy.zeros(shape=(1,size**2))
lb=lb[0]
ub=lb+virtual_bounds.copy()

no_genes=40
no_parents=20

genes=numpy.zeros(shape=(no_genes,D))
for i in range(no_genes):
    for j in range(D):
        genes[i][j]=ga_fun.genetic_init(virtual_bounds[j])
best_gen=genes[0]
gene_fitness=numpy.zeros(shape=(1,no_genes))
gene_fitness=gene_fitness[0]
for i in range(no_genes):
    temp=[]
    for j in range(D):
        temp.append(ga_fun.bintodec(genes[i][j])%virtual_bounds[j])
    gene_fitness[i]=func(numpy.array(temp),D,true_bounds,ub,lb)

maxiter=1000
maxerr=0
it=0
err=gene_fitness[0]
while it<maxiter and err>maxerr:
    
#    for j in range(no_genes-1):
#        min_i=j
#        i=j+1
#        while i<no_genes:
#            if gene_fitness[min_i]>gene_fitness[i]:
#                min_i=i
#            i+=1    
#        gene_fitness[min_i],gene_fitness[j]=gene_fitness[j],gene_fitness[min_i]
#        genes[min_i],genes[j]=genes[j],genes[min_i]
    
        
    i=0     
    while i<(no_genes-no_parents):
        r1=numpy.random.randint(0,no_genes)
        r2=numpy.random.randint(0,no_genes)
        while r2==r1:
            r2=numpy.random.randint(0,no_genes)
        rc1=numpy.random.randint(0,no_genes)
        while rc1==r1 or rc1==r2:
            rc1=numpy.random.randint(0,no_genes)
        rc2=numpy.random.randint(0,no_genes)
        while rc2==r1 or rc2==r2 or rc2==rc1:
            rc2=numpy.random.randint(0,no_genes)        
        if gene_fitness[r1]>gene_fitness[rc1]:
            rc1,r1=r1,rc1
        if gene_fitness[r2]>gene_fitness[rc1]:
            rc1,r2=r2,rc1
        if gene_fitness[r1]>gene_fitness[rc1]:
            rc2,r1=r1,rc2
        if gene_fitness[r2]>gene_fitness[rc2]:
            rc2,r2=r2,rc2        
#        parent1=numpy.random.randint(0,no_parents)
#        parent2=numpy.random.randint(0,no_parents)
#        while parent2==parent1:
#            parent2=numpy.random.randint(0,no_parents)
        for j in range(D):
             [genes[rc1][j],genes[rc2][j]]=ga_fun.genetic_crossover(genes[r1][j],genes[r2][j])           
        i+=2
    
    for i in range(no_genes):
        temp=[]
        for j in range(D):
            genes[i][j]=ga_fun.genetic_mutation(genes[i][j])
            temp.append(ga_fun.bintodec(genes[i][j])%virtual_bounds[j])
        gene_fitness[i]=func(numpy.array(temp),D,true_bounds,ub,lb)
        if gene_fitness[i]<err:
            err=gene_fitness[i]
            best_gen=genes[i]
        
    list_err.append(err)        
    print it,err
    it+=1
        