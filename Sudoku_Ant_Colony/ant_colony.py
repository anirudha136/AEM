__author__ = 'anirudha'
import numpy as np
from random import shuffle,choice,seed,random
#import matplotlib.pyplot as plt


def Ant_Colony(sudoku,temp,n_ants,n_iter):
    seed(1234)
    best_pheromone_matrix = 0.5*np.ones((9,9,9))
    for x in range(9):
        for y in range(9):
            for z in range(9):
                if temp[x,y,z] == 0:
                    best_pheromone_matrix[x,y,z] = 0
    ant_len = 81-len(sudoku[np.nonzero(sudoku)])
    zero_indices = zip(np.where(sudoku == 0)[0],np.where(sudoku == 0)[1])
    fitness_record = []
    min_fitness = 1000
    for iteration in range(n_iter):
        zero_indices_1st_iter = zero_indices
        shuffle(zero_indices_1st_iter)
        pheromone_matrix = best_pheromone_matrix
        for ants in range(n_ants):
            path = zero_indices
            shuffle(path)
            ant = np.zeros((ant_len))
            #start_index_row,start_index_column = zero_indices_1st_iter[ants]
            #options = temp[start_index_row,start_index_column,:]
            count = 0
            #for 1st iteration select randomly
            if iteration == 0:
                #ant[count] = choice(options[np.where(options!=0)])

                for index_row,index_column in path:
                    #count = count+1
                    ant[count] = choice(np.squeeze(temp[index_row,index_column,np.where(temp[index_row,index_column,:]!=0)]))
                    count = count+1
                    #print(count)
            else:
                #max_pheromone_index = np.where(np.max((pheromone_matrix[start_index_row,start_index_column,:]))
                #                               ==pheromone_matrix[start_index_row,start_index_column,:])
                #print choice(max_pheromone_index[0])
                #ant[count] = temp[start_index_row,start_index_column,choice(max_pheromone_index[0])]
                #count = count+1
                for index_row,index_column in path:
                    #introduce randomness
                    random_num = random()
                    rand_pher = 0
                    if random_num>0.1:
                        max_pheromone_index = list(np.where(np.max((pheromone_matrix[index_row,index_column,:]))
                                                   == pheromone_matrix[index_row,index_column,:]))
                    else:
                        while rand_pher==0:
                            rand_pher = choice(pheromone_matrix[index_row,index_column,:])
                        max_pheromone_index = list(np.where(rand_pher == pheromone_matrix[index_row,index_column,:]))
                    #count = count + 1
                    #print(max_pheromone_index[0],index_row,index_column)

                    if len(max_pheromone_index[0])>1:
                        ant[count] = temp[index_row,index_column,choice(max_pheromone_index[0])]
                    else:
                        ant[count] = temp[index_row,index_column,max_pheromone_index[0]]
                    count = count + 1
                #print(ant)
            #fill the values of the ant in sudoku
            count = 0
            #print(ant)
            new_sudoku = sudoku
            for ind in range(len(path)):      # doubt in -1
                #if ind == 0:
                    #new_sudoku[start_index_row,start_index_column] = ant[ind]
                    new_sudoku[path[ind]] = ant[ind]

            fit_val = fitness(new_sudoku)
            #print(fit_val)
            for cnt in range(ant_len):
                #introduce randomness

                random_num = random()
                if random_num>0.01:
                    pheromone_matrix[path[cnt][0],path[cnt][1],np.where(temp[path[cnt][0],path[cnt][1],:]==ant[cnt])] \
                        = pheromone_matrix[path[cnt][0],path[cnt][1],np.where(temp[path[cnt][0],path[cnt][1],:]==ant[cnt])] *pow(1.71,1/(1+float(fit_val)))
                else:
                    pheromone_matrix[path[cnt][0],path[cnt][1],np.where(temp[path[cnt][0],path[cnt][1],:]==ant[cnt])] \
                        = pheromone_matrix[path[cnt][0],path[cnt][1],choice(np.squeeze(np.where(temp[path[cnt][0],path[cnt][1],:]>0)[0]))]\
                          *pow(1.71,1/(1+float(fit_val)))
                    #pheromone_matrix[path[cnt][0],path[cnt][1],np.where(temp[path[cnt][0],path[cnt][1],:]==ant[cnt])] = 0.5*pow(1.71,1/(1+float(fit_val)))

                #pheromone_matrix[path[cnt][0],path[cnt][1],np.where(temp[path[cnt][0],path[cnt][1],:]==ant[cnt])] \
                #        = pheromone_matrix[path[cnt][0],path[cnt][1],np.where(temp[path[cnt][0],path[cnt][1],:]==ant[cnt])] *pow(1.71,1/(1+float(fit_val)))
            #decrease the pheromone level  10% decrement

            if fit_val<min_fitness:
                min_fitness = fit_val
                best_pheromone_matrix = pheromone_matrix
                best_sudoku = new_sudoku
        best_pheromone_matrix = best_pheromone_matrix*0.95
        #print(best_pheromone_matrix[8,3,:])

        print('min fitness of ') + str(iteration), 'generation is '+ str(min_fitness) #+ str(best_sudoku)
        fitness_record.append(min_fitness)
        print(best_sudoku)
    #plt.plot(fitness_record)
    #plt.show()
    print(fitness_record)
    return best_sudoku

def fitness(sudoku):
    penalty = 0
    for i in range(9):
        penalty = penalty + repetation(sudoku[i,:].tolist()) + repetation(sudoku[:,i].tolist())
        #if np.sum(sudoku[i,:])!=45 or np.sum(sudoku[i,:])!=45:
            #penalty = penalty + 1
    for a in range(0,3):
        for k in range(0,3):
            subgrid = []
            for j in range(3):
                subgrid= np.append(subgrid,sudoku[3*k+j,3*a+np.arange(3)])
            #print(subgrid)
            penalty = penalty + repetation(subgrid.tolist())
            #if np.sum(subgrid)!=45:
             #   penalty = penalty+1
    return penalty



def repetation(mylist):
    ans = [i for i, x in enumerate(mylist) if mylist.count(x) > 1]
    return len(ans)-1