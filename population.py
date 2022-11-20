from random import randint, random
import chromosome

def fitness_function(chromosome, other_args = None):
    __ZERO__ = ('0', '0')
    __ONE__ = ('1', '1')
    # other args is a list of circuit, simulator, fault, test_sequence
    circuit = other_args[0]
    simulator = other_args[1]
    fault = other_args[2]
    test_sequence = other_args[3]
    fitness = 0
    FFs = circuit.getDFFs()
    init_map = {}
    
    chromosome_list = chromosome.get_chromosome()

    for i in range(len(FFs)):
        if (chromosome_list[i] == 0):
            init_map[FFs[i]] = __ZERO__
        elif (chromosome_list[i] == 1):
            init_map[FFs[i]] = __ONE__
    
    # Now that the dictionary is initialized I can run the simulation
    simulator.simulate(test_sequence=test_sequence, ff_init_values=init_map, fault=fault)
    # Give a result depending on the number of faults detected at the output
    fitness = simulator.numberDetectedOutputs()

    return fitness

class population():
    def __init__(self,number_of_genes,number_of_initial_pop,threshold,mutation_prob) -> None:
        # define empty population set
        self._population = []
        self._threshold = threshold
        self._mutation = mutation_prob

        for i in range(0,number_of_initial_pop):
            self._population.append(chromosome.chromosome(number_of_genes))

    
    def selection(self,top_n_chromosomes, fitness_f_args):
        new_population = []
        
        for i in range(0,top_n_chromosomes):
            max_fit = 0
            max_chromo = 0
            for chromosome in self._population:
                fitness_value = fitness_function(chromosome, fitness_f_args)
                if ( fitness_value >= max_fit):
                    max_fit = fitness_value
                    max_chromo = chromosome
            # at the end add to the new population
            new_population.append(max_chromo)
            # remove it from the old population
            self._population.remove(max_chromo)
        
        # at the end, overwrite the old population with the new
        self._population = new_population
    
    def crossover(self):
        new_offspring = []
        ret_val = 0

        for i in range(0,len(self._population)):
            for j in range(i,len(self._population)):
                if (i != j):
                    # i can't reproduce with myself
                    tmp_offspring = self._population[i].crossover(self._population[j])
                    for offspring in tmp_offspring:
                        new_offspring.append(offspring)
        # after crossover perform mutation
        for offspring in new_offspring:
            # mutate with 50% probability
            offspring.mutate(self._mutation)
        
        ret_val = self.terminate(new_offspring)
        # add the new offspring to the existing population
        self._population.extend(new_offspring)

        return ret_val
    
    #threshold is a number ranging from 0 to 1
    def terminate(self, new_pop):
        equal = 0

        for offspring in new_pop:
            for parent in self._population:
                if (offspring.get_chromosome() == parent.get_chromosome()):
                    equal += 1
                    break
        
        # at the end compute the percentile
        equal /= len(new_pop)
        if (equal >= self._threshold):
            return 1
        
        return 0
