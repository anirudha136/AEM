__author__ = 'anirudha'

import ga, stdgenomes
import numpy as np
import random
from traffic_models_v5 import model1
#from traffic_models_v5 import ga_model1
from traffic_models_v6 import ga_model1
import numpy
import pickle

#Now we choose a representation. We know that the answer to the puzzle must be some permutation of the digits 1 to 9, each used nine times.
my_randoms=[]

for i in range (315):

    my_randoms.append(random.randrange(30,90,1))

genome = stdgenomes.FloatGenome (my_randoms,init_limits=(30,90))
print(genome.genes)
#I made a few functions to calculate how many conflicts a potential Sudoku solution has. I'll show them later, but for now let us just import the package. I also found a puzzle somewhere and put it in the PUZZLE constant.
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
solver = ga.GA(ga_model1(genome) , genome)

#And now, when we have supplied the GA with a fitness function (ga_sudoku, which counts Sudoku conflicts) and a representation (genome), let us just let the solver do its magic.

a,b,c = solver.evolve(target_fitness=-10000000000)
print(a.genes,b,c)
file_name = "results_ga(FloatGenome.fresh, 1),(FloatGenome.copy, 1),(FloatGenome.crossover, 2),(FloatGenome.big_mutate, 5),(FloatGenome.medium_mutate, 2),(FloatGenome.small_mutate, 2)"
f = open(file_name, "w")
pickle.dump([[a.genes],[b],[c]],f)
f.close()
#for i in range(9):
    #print(a.genes[9*i:9*i+9])