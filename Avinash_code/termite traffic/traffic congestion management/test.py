# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 20:16:23 2015

@author: Avinash
"""
import numpy
from numpy import *

from traffic_models_v5 import model1 as func
#g=numpy.array([[10,-10000,20,-10000,10,-10000,20,-10000,-10000,10,20,-10000,10,-10000,20,-10000,10,-10000,-10000,30,10,-10000,20,-10000,10,-10000,20,-10000,-10000,49,20,-10000,10,-10000,20,-10000,10,-10000,20,30]])
g=numpy.array([[10,-10000,20,-10000,10,-10000,20,-10000,10,-10000,20,-10000,10,-10000,20,-10000,10,-10000,30,-10000,10,-10000,20,-10000,10,-10000,20,-10000,49,-10000,20,-10000,10,-10000,20,-10000,10,-10000,20,30]])
idmat=numpy.genfromtxt('model1_id.csv', delimiter=',')
flow_init=numpy.genfromtxt('model1_a.csv', delimiter=',')
queue_init=numpy.genfromtxt('model1_q.csv', delimiter=',')

#for i in range(shape(flow_init)[0]):
#    for j in range(shape(flow_init)[1]):
#        if flow_init[i][j]==nan:
#            flow_init[i][j]=-10000
temp=func(g=g,dir_detect=1,idmat=idmat,flow_init=flow_init,queue_init=queue_init)   
