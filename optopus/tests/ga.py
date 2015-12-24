"""The Genetic Algorithm module.

"""

import random
import time
import signal
import sys
from sudoku import SOLUTION_GIVEN,PUZZLE_GIVEN
import numpy as np

bestfit = []
fit_value = []
class GA:
    """A Genetic Algorithm.
    
    A Genetic Algorithm is an optimization technique for global non-linear
    optimization. All you need to supply is a way to represent your solutions
    and a "fitness function" that measures how good the solutions are. In
    computer science, lower fitness traditionally means better.

    In pseudo code the algorithm works like this:
    1) Create a population of random solutions
    2) Pick a few solutions and sort them according to fitness
    3) Replace the worst solution with a new solution, which is either
       a copy of the best solution, a mutation (perturbation) of the best
       solution, an entirely new randomized solution or a cross between the two
       best solutions.
    4) Check if you have a new global best fitness, if so, store the solution.
    5) If too many iterations go by without improvement, the entire population
       might be stuck in a local minimum (a small hole, with a possible ravine
       somewhere else). If so, kill everyone and start over at 1.
    6) Else, go to 2.

    When performing global optimization you want to be wary of too rapid
    convergence of your solution. Generally you will want to set parameters
    so that you get a solution slowly but surely. For most problems you can use
    the default parameters and one of the standard genome classes and just worry
    about your fitness function.
    """
    def __init__(self, fitfun, genome, pop_size=10000,
                 local_size=20, tourney_size=15, verbose=True,
                 solution = SOLUTION_GIVEN,problem = PUZZLE_GIVEN,print_sudoku = False):
        """Constructor of GA.

        @param fitfun: The fitness function. Takes a genome object and returns a
        fitness value. Lower is better.

        @param genome: An object that represents your solution. It has to
        implement the methods spawn and fresh. Spawn creates a new genome derived
        from this genome and another parent. Fresh creates a completely
        new random genome. This object is passed to fitfun.

        @param pop_size: The size of the GA population. A larger size means slower
        convergence. Reasonable values might be between 100 and 1000000,
        depending on local_size.

        @param local_size: Size of the local neighbourhood. The population is a
        circular list, where solutions only compete against nearby solutions.
        This makes convergence slower. Also crossover is more likely to give fit
        solutions when made between similar genomes. If set to None, tournaments
        will be global, as in a traditional GA.

        @param tourney_size: The number of solutions that compete for the
        privilege of getting an offspring. A lower value means slower
        convergence, but lower then 3 would be silly.

        @param verbose: If true (default), allow progress printing.
        """
        self.fitfun = fitfun
        self.pop = []
        self.first_genome = genome
        self.verbose = verbose
        self.solution = solution
        self.problem = problem
        self.print_sudoku = print_sudoku

        self.iterations = 0
        self.pop_size = pop_size
        self.local_size = local_size
        self.tourney_size = tourney_size
        self.best_found = 0
        self.best_genome = None
        self.best_fitness = 0
        self.last_eden = 0
        self.userstop = False

        self.eden_state()
        
    def eden_state(self):
        """Kill population and create a new with with random solutions.
        """
        self.best_fitness = 0
        self.last_eden = self.iterations
        self.best_genome = None
        self.pop = []
        for _ in xrange(self.pop_size):
            self.pop.append(self.first_genome.fresh())

        for guy in self.pop:
            self._check_best(guy)

    def seed(self, solution):
        """Add a custom solution, that you want to be a part of the population.

        @param solution: The solution to add."""
        flag = np.asarray(self.problem)
        zero_indices = zip(np.where(np.asarray(flag[:][:]) == 0)[0],np.where(np.asarray(flag[:][:]) == 0)[1])
        rand_zero_index = random.choice(zero_indices)
        #print(rand_zero_index,offspring)
        solution[rand_zero_index[0]][rand_zero_index[1]] = random.choice(range(1,10))
        self.pop.append(solution)
        self._check_best(solution)

    def _check_best(self, genome):
        """Calculate fitness of genome and check if it is the best found so far.

        @param genome: The solution to check.
        """
        genome.fitness = self.fitfun(genome)
        if genome.fitness < self.best_fitness or self.best_genome is None:
            self.best_fitness = genome.fitness
            self.best_genome = genome.copy()
            self.best_found = self.iterations - self.last_eden
            if self.verbose:
                print 'Best fitness:', genome.fitness, self.iterations
                bestfit = genome.fitness
                fit_value.append([bestfit,self.iterations])
                mismatch = 0
                for i in range(9):
                    flag = []
                    for j in range(9):
                        if self.solution[i][j] == self.best_genome.genes[i*9+j]:
                            flag.append(0)
                        else:
                            flag.append(self.best_genome.genes[i*9+j])
                    if self.print_sudoku:
                        print(flag)
                    mismatch = mismatch + len(np.nonzero(flag)[0])
                print('no of mismatch elements'),mismatch
            sys.stdout.flush()

    def _choose(self):
        """Choose a number of genomes to compete.

        @return: A list of indices of the chosen genomes in self.pop
        """
        if not self.local_size:
            return [random.randrange(len(self.pop))
                    for _ in xrange(self.tourney_size)]

        midpoint = random.randrange(len(self.pop))
        chosen = [midpoint]
        for _ in xrange(self.tourney_size - 1):
            i = midpoint + random.randrange(-self.local_size, self.local_size)
            i %= len(self.pop) #works for negative too!
            chosen.append(i)
        return chosen

    def evolve(self, seconds=0, target_fitness=None, use_restarts=True):
        """Evolve for a number of seconds.

        This method can be called again after it returns, to continue evolving.

        @param seconds: The number of seconds to run. If 0, iterate
        for ever and wait for user to break with Ctrl-C.
        
        @param target_fitness: When the fitness is equal to this value, or less,
        the evolution will stop.

        @param use_restarts: If this parameter is True (which it is per default),
        The search will periodically restart with a new, entirely randomized,
        population. This restart kicks in when there has been no improvement
        for many iterations and one can assume that a local optimum has been
        reached.
        """
        start = time.time()

        self.userstop = False
        def stop(signum, frame):
            """A Ctrl-C signal handler"""
            self.userstop = True
            if self.verbose:
                print '\nexit'
        oldhandler = signal.signal (signal.SIGINT, stop)

        try:
            while ((not seconds) or time.time() - start < seconds) and \
                    not self.userstop and \
                    (self.best_fitness > target_fitness or \
                         target_fitness is None):
                #self.seed(self.solution)
                max_inactive = max(self.best_found * 2, self.pop_size * 10)
                thisrun = self.iterations - 2*self.last_eden
                if use_restarts and thisrun > max_inactive:
                    if self.verbose:
                        print 'Restart!'
                    self.eden_state()

                self.iterations += 1

                fids = [(self.pop[i].fitness,i) for i in self._choose()]
                fids.sort()
            
                self.pop[fids[-1][1]] = self._make_child(fids[0][1], fids[1][1])

                self._check_best(self.pop[fids[-1][1]])
        finally:
            signal.signal(signal.SIGINT, oldhandler)
        print(fit_value)
        print time.time()-start
        return self.best_genome, self.best_fitness,

    def _make_child(self, id1, id2):
        """Create an offspring from the supplied genomes.
        
        @param id1: self.pop[id1] is the tournament winner
        @param id2: self.pop[id2] is the tournament runner-up
        """
        #introduce mutations
        '''
        offspring = self.pop[id1].spawn(self.pop[id2]).genes
        flag = np.asarray(self.problem)
        zero_indices = zip(np.where(np.asarray(flag[:][:]) == 0)[0],np.where(np.asarray(flag[:][:]) == 0)[1])
        rand_zero_index = random.choice(zero_indices)
        #print(rand_zero_index,offspring)
        offspring[9*rand_zero_index[0]+rand_zero_index[1]] = random.choice(range(1,10))
        self.pop[id1].genes = offspring
        '''
        return self.pop[id1].spawn(self.pop[id2])

