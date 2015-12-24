__author__ = 'anirudha'
import pandas as pd
import numpy as np
from random import shuffle
from ant_colony import Ant_Colony

FILE_NAME = 'sudoku.csv'
df = pd.read_csv(FILE_NAME,header=None)
sudoku = df.values
print(sudoku)


#Basic Assignment step
def basic_assignment(sudoku):
    '''

    :param sudoku: The raw sudoku matrix, empty spaces filled with zeros
    :return: 3D matrix of possible characters
    '''
    temp = np.zeros((9,9,9))
    for i in range(9):
        for j in range(9):
            if sudoku[i,j]==0:
                temp[i,j,:] = range(1,10)
                row = sudoku[i,:]
                column = sudoku[:,j]
                # check in rows
                for k in row:
                    if k!=0:
                        for m in range(len(temp[i,j,:])):
                            if temp[i,j,m]==k:
                                temp[i,j,m] = 0
                #check in columns
                for k in column:
                    if k!=0:
                        for m in range(len(temp[i,j,:])):
                            if temp[i,j,m]==k:
                                temp[i,j,m] = 0
                # check in subgrid
                a = i/3
                b = j/3
                for p in range(3):
                    for q in range(3):
                        if sudoku[3*a+p,3*b+q] != 0:
                            for r in range(len(temp[i,j,:])):
                                if temp[i,j,r] == sudoku[3*a+p,3*b+q]:
                                    temp[i,j,r] = 0
    return temp

#Improved Assignment Step
def improved_assignment_old(sudoku,temp):
    n_old = 1
    n_new = 0
    count = 0
    while n_new!=n_old:
        n_old  = temp[np.nonzero(temp)].size
        for i in range(9):
            for j in range(9):
                #print(temp[i,j,np.nonzero(temp[i,j,:])])
                if temp[i,j,np.nonzero(temp[i,j,:])].size == 1 and sudoku[i,j]==0:
                    sudoku[i,j] = temp[i,j,np.nonzero(temp[i,j,:])]    # some problem in this step
                    print(temp[i,j,np.nonzero(temp[i,j,:])])
                    print(i,j)
                    print(sudoku)
                    temp = basic_assignment(sudoku)
        temp_new = temp
        n_new = temp_new[np.nonzero(temp_new)].size
        temp = temp_new
        count = count+1
        #print(sudoku[np.nonzero(sudoku)].size)
        print 'Round--->'+str(count)
    return temp_new,sudoku

def improved_assignment_step_new(sudoku,temp):
    for i in range(9):
        for j in range(9):
            if sudoku[i,j]==0:
                for num in temp[i,j,:]:
                    #row checking
                    indices = zip(np.where(temp[:,j,:]==num)[0],np.where(temp[:,j,:]==num)[1])
                    if len(indices)==0:
                        sudoku[i,j] = num
                        temp = basic_assignment(sudoku)
                    #column checking
                    indices = zip(np.where(temp[i,:,:]==num)[0],np.where(temp[i,:,:]==num)[1])
                    if len(indices)==0:
                        sudoku[i,j] = num
                        temp = basic_assignment(sudoku)
                    #subgrid checking
                    a = i/3
                    b = j/3
                    indices = []
                    for m in range(3):
                        for n in range(3):
                            indices = np.append(indices,np.where(temp[3*a+m,3*b+n,:]==num)[0])
                            print(len(indices),sudoku[i,j],i,j)
                            if len(indices)==1 and sudoku[i,j]==0:
                                #sudoku[i,j] = num
                                temp = basic_assignment(sudoku)
                            indices = []
    #print(sudoku[np.nonzero(sudoku)].size)
    #print(sudoku)
    return sudoku,temp

#heuristic ant colony
def ant_colony(sudoku,temp,n_iter,n_ants):
    zero_indices = zip(np.where(sudoku == 0)[0],np.where(sudoku == 0)[1])
    shuffle(zero_indices)
    #print(len(zero_indices))
    proba = np.ones((len(zero_indices),9))
    #begin the algorithm
    count = -1
    pheromone_matrix = np.ones((9,9,9))
    for iterations in range(n_iter):
        for ant in range(n_ants):
            for i,j in zero_indices:
                #include iterations here
                count = count+1
                possible_numbers = temp[i,j,np.nonzero(temp[i,j,:])]
                possible_numbers_indices = np.nonzero(temp[i,j,:])
                #print(possible_numbers_indices)
                for number in possible_numbers[0]:
                    #print(number)
                    sudoku[i,j] = number
                    temp_new,sudoku_new = improved_assignment_old(sudoku,basic_assignment(sudoku))
                if np.nonzero(sudoku_new) != 81:
                    proba[count,possible_numbers_indices] = 0
                    pheromone_matrix[i,j,possible_numbers_indices] = pheromone_matrix[i,j,possible_numbers_indices]/81.0
                    print(temp[i,j,:])
                    print(proba[count,:])
                    print(np.multiply(proba[count,:],temp[i,j,:]))
                    #exit()

    #print(proba)
    #print(sudoku)
    #print(zero_indices)


if __name__ == '__main__':
    n_iter = 200
    n_ants = 50           #fibonacci no
    X = basic_assignment(sudoku)
    #X_new,sudoku = improved_assignment_old(sudoku,X)
    #sudoku,X_new = improved_assignment_step_new(sudoku,X)
    #print 'Initial no. of possibilities ' + str(X[np.nonzero(X)].size)
    #print 'Final no. of possibilities ' + str(X_new[np.nonzero(X_new)].size)
    #ant_colony(sudoku,X,n_iter,n_ants)
    sudoku_final  = Ant_Colony(sudoku,X,n_ants,n_iter)
    print(sudoku_final)
    #print(sudoku[np.nonzero(sudoku)].size)
    #print(sudoku)
