#test
# Ctrl-C

# armageddon

import sys
sys.path.append('..')
import ga, stdgenomes
from stdgenomes import FloatGenome

def fitfun(solution): #a fitness function for a trivial toy problem
    return sum(abs(a - i) for i, a in enumerate(solution.genes))

VERBOSE = True

def testIntGenome():
    RANGE_LENGTH = 10
    genome = stdgenomes.IntGenome(RANGE_LENGTH, range(RANGE_LENGTH))
    solver = ga.GA(fitfun, genome, verbose=VERBOSE)
    best_solution, best_fitness = solver.evolve(target_fitness=0)

    assert best_fitness == 0
    assert best_solution.genes == range(RANGE_LENGTH)

def testPermutateGenome():
    RANGE_LENGTH = 15
    genome = stdgenomes.PermutateGenome(range(RANGE_LENGTH))
    solver = ga.GA(fitfun, genome, verbose=VERBOSE)
    best_solution, best_fitness = solver.evolve(target_fitness=0)

    assert best_fitness == 0
    assert best_solution.genes == range(RANGE_LENGTH)

def testFloatGenome():
    RANGE_LENGTH = 10
    TEST_ACCURACY = 10
    genome = stdgenomes.FloatGenome(RANGE_LENGTH, (-RANGE_LENGTH, RANGE_LENGTH))
    solver = ga.GA(fitfun, genome, verbose=VERBOSE)
    best_solution, best_fitness = solver.evolve(target_fitness=TEST_ACCURACY)

    assert best_fitness <= TEST_ACCURACY

def testFloatSwap():
    RANGE_LENGTH = 10
    TEST_ACCURACY = 10
    chances = ((FloatGenome.fresh, 1),
               (FloatGenome.copy, 1),
               (FloatGenome.crossover, 3),
               (FloatGenome.big_mutate, 1),
               (FloatGenome.swap, 3),
               (FloatGenome.small_mutate, 2))
    genome = stdgenomes.FloatGenome(RANGE_LENGTH, (-RANGE_LENGTH, RANGE_LENGTH),
                                    spawn_chances=chances)
    solver = ga.GA(fitfun, genome, verbose=VERBOSE)
    best_solution, best_fitness = solver.evolve(target_fitness=TEST_ACCURACY)

    assert best_fitness <= TEST_ACCURACY

def testGlobalWindow():
    RANGE_LENGTH = 10
    genome = stdgenomes.IntGenome(RANGE_LENGTH, range(RANGE_LENGTH))
    solver = ga.GA(fitfun, genome, verbose=VERBOSE, local_size=None, tourney_size=20)
    best_solution, best_fitness = solver.evolve(target_fitness=0)

    assert best_fitness == 0
    assert best_solution.genes == range(RANGE_LENGTH)

    return best_solution

def testSeed():
    RANGE_LENGTH = 10
    seed = stdgenomes.IntGenome(range(RANGE_LENGTH), range(RANGE_LENGTH))
    genome = stdgenomes.IntGenome(RANGE_LENGTH, range(RANGE_LENGTH))
    solver = ga.GA(fitfun, genome, verbose=VERBOSE, local_size=None, tourney_size=20)
    solver.seed(seed)

    assert solver.best_fitness == 0
    assert solver.best_genome.genes == range(RANGE_LENGTH)

def testArmageddon():
    RANGE_LENGTH = 10
    TEST_ACCURACY = 10
    genome = stdgenomes.FloatGenome(RANGE_LENGTH, (-RANGE_LENGTH, RANGE_LENGTH))
    solver = ga.GA(lambda _: 100, genome, pop_size=10, verbose=VERBOSE)
    best_solution, best_fitness = solver.evolve(seconds=1)

    assert solver.last_eden != 0
    assert best_fitness == 100

if __name__ == '__main__':
    testArmageddon()
    testGlobalWindow()
    testSeed()
    testFloatSwap()
    testFloatGenome()
    testPermutateGenome()
    testIntGenome()
