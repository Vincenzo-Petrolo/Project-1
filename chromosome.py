import random

class chromosome():
    def __init__(self, length=None,chromosome_sequence=None) -> None:
        self._chromosome = []

        if (chromosome_sequence):
            self._chromosome = chromosome_sequence  
            #print(f"The generated chromosome is: {self._chromosome}")
        else:
            for i in range(0,length):
                self._chromosome.append(random.choice([0,1]))
            
            #print(f"The random generated chromosome is: {self._chromosome}")

    
    def get_chromosome(self):
        return self._chromosome
    
    def crossover(self, parentB):
        # generate random crossover point
        crossover_point = random.randint(0, len(self._chromosome)-1)
        offspringA = list.copy(self._chromosome)
        offspringB = list.copy(parentB.get_chromosome())

        for i in range(0,crossover_point):
            offspringA[i] = offspringB[i]
            offspringB[i] = self._chromosome[i]

        print(f"From parentA: {self._chromosome} and parentB: {parentB.get_chromosome()} with crossover point {crossover_point} => {offspringA} and {offspringB}")
        # return two offsprings
        return [chromosome(None, offspringA), chromosome(None,offspringB)]
    
    #probability is a number between 0 and 1
    def mutate(self, probability):
        for i in range(0,len(self._chromosome)):
            if (random.random() <= probability):
                print("Mutation occurred!")
                # flip the bit
                if (self._chromosome[i] == 0):
                    self._chromosome[i] = 1
                else:
                    self._chromosome[i] = 0
        
        # print(f"After mutation is: {self._chromosome}")
