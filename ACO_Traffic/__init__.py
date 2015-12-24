__author__ = 'anirudha'

import numpy as np
import random
from traffic_models_v6 import model1
import math

g_min = 30
g_max = 90
interval_length = 5
n_nodes = (g_max-g_min)/interval_length+1
n_var = 315
pheromone_matrix = np.ones((n_nodes,n_var))
n_ants = 40
n_iter = 1000
rho = 0.5
idmat=np.genfromtxt('model1_id.csv', delimiter=',')
flow_init=np.genfromtxt('model1_a.csv', delimiter=',')
queue_init=np.genfromtxt('model1_q.csv', delimiter=',')
g_cond=np.genfromtxt('g_cond.csv', delimiter=',')

D=21*15
maxit=500
mainerrmat=np.zeros(shape=(10,maxit+1))
mainrunno=0
partpos=np.zeros(shape=(10,maxit+1,D))

g_c_min=30
g_c_max=90
g_nc_min=20
g_nc_max=60

def sigmoid(value):
    return 1/(1+math.exp(value/100))

for iter in range(n_iter):
    Ant = np.zeros((n_ants,n_var))
    for ants in range(n_ants):
        if iter == 0:
            for path in range(n_var):
                node_number = random.choice(range(n_nodes))
                Ant[ants,path] = g_min + node_number*interval_length
        else:
            for path in range(n_var):
                toss = random.random
                if toss>0.9:
                    node_number = np.where(pheromone_matrix[:,path]== np.max(pheromone_matrix[:,path]))[0][0]
                else:
                    node_number = random.choice(range(n_nodes))
                Ant[ants,path] = g_min + node_number*interval_length

        #print( Ant)
        fit_val = model1(Ant[ants,:],g_cond,idmat,flow_init,queue_init,g_nc_min,g_nc_max,g_c_min,g_c_max,K=15,cont=1,g_form=1)
        print(fit_val)
        #pheromone update

    for i in range(n_ants):
        for nodes in range(n_var):
            node_number = int((Ant[i,nodes]-g_min)/interval_length)
            pheromone_matrix[node_number,nodes] =(1-rho)*pheromone_matrix[node_number,nodes]+sigmoid(fit_val)
            #print(pheromone_matrix[node_number,nodes])





