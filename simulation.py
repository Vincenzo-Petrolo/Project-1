import circuit
import random

# Sequential simulation class
class SequentialSimulation(object):
    def __init__(self, circuit):
        self.circuit = circuit
        # This will hold all the values of the nodes
        # throught the simulation
        self.simTableHistory = []
    

    def simulate(self, test_sequence = [], ff_init_values = {}):
        first = True
        test_ctr = 0

        for test_vector in test_sequence:
            print(f"Cycle #{test_ctr}")
            # Generate a simTable
            newTable = self._getEmptySimTable()
            self.simTableHistory.append(newTable)

            # Only for the first time
            if (first == True):
                first = False
                self._initFlipFlops(ff_init_values)
            else:
                # If not first cycle, propagate flip flops
                self._updateFlipFlop()

            self._step(test_vector)
            test_ctr += 1
        
        self._simulationReport()

    def _updateFlipFlop(self):
        for node in self.circuit.nodes.values():
            if (node.function == circuit.__DFF__):
                # Get the inputs of a node
                inputs_names = node.getFanIn().copy()
                # Access the previous simTable
                self.simTableHistory[-1][node.name] = self.simTableHistory[len(self.simTableHistory)-2][inputs_names[0]]

    def _step(self, inputs = None):
        # Executes one simulation cycle
        if (inputs is None):
            # If no inputs are given, then treat them as don't care
            inputs = self._generateRandomInputs()

        self._applyInputs(inputs)
        # Compute one cycle
        self._computeNodes()
        print(self.simTableHistory[-1])
    
    def _generateRandomInputs(self):
        # Get random inputs
        generated_inputs = {}

        for input in self.circuit.inputs:
            chosen_bit = random.choice(['0', '1'])
            generated_inputs[input] = (chosen_bit, chosen_bit)
        
        return generated_inputs
    
    def _applyInputs(self, inputs):
        # Copy the inputs into the table
        for key, val in inputs.items():
            self.simTableHistory[-1][key] = val
    
    def _initFlipFlops(self, ff_values):
        for key, val in ff_values.items():
            self.simTableHistory[-1][key] = val

    def _computeNodes(self):
        # Compute until no difference between last simulation
        modified = True

        while (modified == True):
            modified = self._updateNodes()
    
    def _updateNodes(self):
        updated = False

        for node, values in self.simTableHistory[-1].items():
            if (self._alreadyComputed(node)):
                continue
            # For each node compute good and bad value
            new_val = self._theGoodandTheBad(node)
            if (new_val != values):
                updated = True
            # Update the value 
            self.simTableHistory[-1][node] = new_val
        
        return updated

    def _alreadyComputed(self, node_name):
        if ('U' in self.simTableHistory[-1][node_name]):
            return False

        return True

    def _theGoodandTheBad(self, node_name):
        # Get the input of that node
        node = self.circuit.nodes[node_name]
        inputs_names = node.getFanIn().copy()
        good_inputs = []
        bad_inputs = []
        for i in inputs_names:
            good_inputs.append(self.simTableHistory[-1][i][0])
            bad_inputs.append(self.simTableHistory[-1][i][1])
    
        if (node.function != circuit.__DFF__):
            good_output = node.function(good_inputs)
            bad_output = node.function(bad_inputs)
        else:
            # Don't do anything if DFF
            good_output = self.simTableHistory[-1][node_name][0]
            bad_output = self.simTableHistory[-1][node_name][1]

        return (good_output, bad_output)

        
    def _timeDifference(self):
        # If I didn't two simulations yet, then nothing changed
        if (len(self.simTableHistory) < 2):
            return True
        # Use this method to check if the two last simulations gave a different result
        # If not, it means we're stuck
        if (self.simTableHistory[len(self.simTableHistory) - 2] == self.simTableHistory[-1]):
            return False
        
        return True
    
    def _getEmptySimTable(self):
        # Return an initial table
        newTable = {}
        for node_name in list(self.circuit.nodes.keys()) + list(self.circuit.inputs):
          newTable[node_name] = ('U', 'U')
        
        return newTable
    
    def _simulationReport(self):
        self._writeGrid()
        for node in self.simTableHistory[-1]:
            print(f"{node}\t\t|", end='')
            for simTable in self.simTableHistory:
                print(f"{simTable[node]}\t\t|", end='')
            print("")
            
    
    def _writeGrid(self):
        print(f"Node\t\t|", end='')
        for i in range(len(self.simTableHistory)):
            print(f"{i}\t\t\t|", end='')
        print("")
            
