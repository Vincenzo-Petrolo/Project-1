import random
from population import population

__ZERO__ = ('0', '0')
__ONE__ = ('1', '1')

# ========================================================================================
# Random utility functions to help in research
# ========================================================================================

# Returns a randomized test sequence of given length


def getRandomTestSequence(circuit, length):

  test_sequence = []

  for i in range(length):
    input_pattern = {}

    for input in circuit.getInputs():
      input_pattern[input] = random.choice([__ZERO__, __ONE__])

    test_sequence.append(input_pattern)

  return test_sequence


# Returns an initialization map for the FFs of a circuit
# Initialize only a given percentage of randomly picked FFs
def getRandomFFinitValues(circuit):
    init_map = {}

    FFs = circuit.getDFFs()

    for FF in FFs:
        # Randomly initialize the FF
        init_map[FF] = random.choice([__ZERO__, __ONE__])


    return init_map

def getSolidFFInitValues(circuit, value):
    FFs = circuit.getDFFs()
    init_map = {}

    for FF in FFs:
        init_map[FF] = value
    
    return init_map

def getAlternatedFFInitValues(circuit, starting_value):
    FFs = circuit.getDFFs()
    init_map = {}

    for i in range(len(FFs)):
        if (i % 2 == 0):
            init_map[FFs[i]] = starting_value
        else:
            init_map[FFs[i]] = negate(starting_value)

def getFanOutFFInitValues(circuit, fanout_th, init_value):
    FFs = circuit.getDFFSortedByFanOut()
    init_map = {}

    for FF_name, fan_out in FFs.items():
        if (fan_out >= fanout_th):
            init_map[FF_name] = init_value

    return init_map

def getFFInitValuesUsingGeneticAlgorithm(circuit, simulator, test_sequence):
    FFs = circuit.getDFFs()
    init_map = {}
    # I create a population with chromosomes of length same as the number of FFs
    # Starting population is 10
    # The threshold for termination is 80%
    # The chance of mutation during crossover is 50%
    p = population(len(FFs),10,0.8,0.5)

    terminate = 0
    i = 1
    while (terminate == 0):
        # select top 3 parents for crossover
        p.selection(3, [circuit, simulator, "", test_sequence])
        # perform crossover
        terminate = p.crossover()
        i += 1
    
    p.selection(1, [circuit, simulator, "", test_sequence])

    final_chromosome = p._population[0].get_chromosome()

    for i in range(len(FFs)):
        if (final_chromosome[i] == 0):
            init_map[FFs[i]] = __ZERO__
        elif (final_chromosome[i] == 1):
            init_map[FFs[i]] = __ONE__

    return init_map




# =============================================================================================
# Utility functions
# =============================================================================================
def negate(value):
    if (value == __ZERO__):
        return __ONE__
    
    return __ZERO__
