import random

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
def getRandomFFinitValues(circuit, percentage):
    current_percentage = 0
    init_map = {}

    if (percentage < 0 or percentage > 1):
        raise Exception

    FFs = circuit.getDFFs()
    step = 1/len(FFs)

    while (current_percentage < percentage):
        # Try to pick always a new FF
        chosen_FF = random.choice(FFs)
        while (chosen_FF in init_map):
            chosen_FF = random.choice(FFs)
        
        # Randomly initialize the FF
        init_map[chosen_FF] = random.choice([__ZERO__, __ONE__])

        # Increase the step
        current_percentage += step
    
    return init_map

def getSolidFFInitValues(circuit, value):
    FFs = circuit.getDFFs()
    init_map = {}

    for FF in FFs:
        init_map[FF] = value

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
    print(FFs)
    init_map = {}

    for FF_name, fan_out in FFs.items():
        if (fan_out >= fanout_th):
            init_map[FF_name] = init_value

    return init_map




# =============================================================================================
# Utility functions
# =============================================================================================
def negate(value):
    if (value == __ZERO__):
        return __ONE__
    
    return __ZERO__
