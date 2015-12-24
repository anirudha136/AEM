__author__ = 'anirudha'

import ga, stdgenomes
import numpy as np

#Now we choose a representation. We know that the answer to the puzzle must be some permutation of the digits 1 to 9, each used nine times.

init_vect = sum([range(1,10)] * 9, []) # A vector of 81 elements
genome = stdgenomes.PermutateGenome (init_vect)
print(genome.genes)
#I made a few functions to calculate how many conflicts a potential Sudoku solution has. I'll show them later, but for now let us just import the package. I also found a puzzle somewhere and put it in the PUZZLE constant.

import sudoku
solver = ga.GA(sudoku.ga_sudoku(sudoku.PUZZLE_GIVEN) , genome)

#And now, when we have supplied the GA with a fitness function (ga_sudoku, which counts Sudoku conflicts) and a representation (genome), let us just let the solver do its magic.

a,b,c = solver.evolve(target_fitness=0)
for i in range(9):
    print(a.genes[9*i:9*i+9])
print(c)