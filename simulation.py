import time


class Simulation(object):

    def __init__(self, circuit):
        self.inputs = circuit.inputs
        self.outputs = circuit.outputs
        self.circuit = circuit
        self.simTable = {}
        self.initialSimTable = {}
        # store inside this dictionary the fault, and 0 or 1 if it is detected or not
        self.faults = {}
        # Levelize the circuit to optimize simulation
        circuit.levelize()
        self._initialize()

    def simulate(self, faults=None):
        # Initialize the simulation table
        self._initialize()
        # reset the table to its original value, this is used if
        # running many simulations without getting new inputs
        for initialInput in self.initialSimTable.keys():
          self.simTable[initialInput] = self.initialSimTable[initialInput]

        # check if i need to perform fault simulation or not
        if (faults is not None):
          self._faultSimulation(faults)
        else:  # start the simulation without fault
          self._normalSimulation()
    
    def printOutputs(self):
        output_string =     "|\tOutput\t|\tValue\t|\n"
        output_string +=    "|\t------\t|\t-----\t|\n"
        for output_name in self.outputs:
            output_string += "|\t"+output_name+"\t|\t"+self.simTable[output_name]+"\t|\n"
        
        print(output_string)
    
    def showInternalAndOutputNodes(self):
        output_string =     "|\tNode\t|\tValue\t|\n"
        output_string +=    "|\t----\t|\t-----\t|\n"
        for node_name in self.simTable:
            if (node_name not in self.inputs):
                output_string += "|\t"+node_name + "\t|\t"+ self.simTable[node_name] +"\t|\n"
        
        print(output_string)
    

    def _initFaults(self, fault_list):
        for fault in fault_list:
            self.faults[fault] = 0

    def getFaultCoverage(self):
        # count the number of ones in the dictionary
        return int(list(self.faults.values()).count(1) / len(self.faults.keys()) * 100)

    def _goalIsReached(self):
        for node in self.simTable.keys():
            if (self.simTable[node] == "X"):
                return False

        return True

    def _initialize(self):
        # reset the fault if any
        self.fault = {"node": "", "input": "", "fault": "", "type": 0}

        for node_name in sorted(self.circuit.levels, key=self.circuit.levels.get):
          self.simTable[node_name] = 'X'

    def _compute(self, node_name):
        # Avoid computing already computed gates
        if (self.simTable[node_name] in ['0', '1', 'U', 'D', "D'"]):
            return
        # get the node
        node = self.circuit.nodes[node_name]
        inputs_names = node.getFanIn().copy()
        inputs = []

        if (node_name == self.fault["node"]):
            inputs_names.remove(self.fault["input"])
            for i in inputs_names:
                inputs.append(self.simTable[i])

            inputs.append(self.fault["fault"])
            output = node.function(inputs)
            self.simTable[node_name] = output
        else:
            for i in inputs_names:
                inputs.append(self.simTable[i])

            output = node.function(inputs)
            # Now update the table
            self.simTable[node_name] = output

    def _normalSimulation(self):
        # I use levelization based ordering to go through the loop once
        # for each level i could spawn threads to take care of each single gate
        while (self._goalIsReached() == False):
            for node in self.simTable:
                self._compute(node)

    def _faultSimulation(self, fault_list):
      totalDetectedFaults = 0
      skippedSims = 0
      # this for takes O(faults)
      for fault in fault_list:
        # if fault was already detected, then skip simulation
        if (self.faults[fault] == 1):
            skippedSims += 1
            continue
        # reset the simTable
        self._initialize()
        for initialInput in self.initialSimTable.keys():
          self.simTable[initialInput] = self.initialSimTable[initialInput]
        # update the fault data structure with the new fault
        if (self._updateFault(fault) == False):
            print("Bad fault insertion, aborting simulation")
            return
        # Start the simulation
        self._normalSimulation()
        # increase the counter
        if (self._isFaultDetected()):
            self._showDetectedFault(fault)
            self.faults[fault] = 1
            totalDetectedFaults += 1
      # eventually print the result of the fault simulation
      print(
          f"Total faults detected: {totalDetectedFaults} ({int(totalDetectedFaults/len(fault_list) * 100)}%)")
      print(f"Total fault sims skipped: {skippedSims}")
    
    def _showDetectedFault(self,fault):
        print(f"|\t{fault}\t| Detected by {self.input_string}")


    def _get_inputs(self, tv=None):

        inputs_names = ""
        for i in self.inputs:
            inputs_names += i + ' '

        if (tv is None):
            formatted_string = "Write the input test vector " + inputs_names + "= "
            input_string = input(formatted_string)
        else:
            input_string = tv
        # store for printing purposes
        self.input_string = input_string
        i = 0
        for input_node in self.circuit.inputs:
            self.simTable[input_node] = input_string[i]
            self.initialSimTable[input_node] = input_string[i]
            i += 1

    def _updateFault(self, newFault):
        # Not in the correct format
        fault_type = newFault.count('-')
        if (fault_type != 2 and fault_type != 1):
            return False
        fault = newFault.split('-')
        if (fault_type == 1):
            # Now validate the fault
            if (fault[0] not in self.simTable.keys()):
                return False
            if (fault[1] != '0' and fault[1] != '1'):
                return False
            # Now update the fault
            self.fault = {
                "node": fault[0],
                "input": "",
                "fault": 'D' if (fault[1] == '0') else "D'",
                "type": fault_type
            }
            self.simTable[self.fault["node"]] = self.fault["fault"]
            return True
        else:
            # Now validate the fault
            if (fault[0] not in self.simTable.keys()):
                print("Fualt is not in simtable")
                return False
            if (fault[1] not in self.circuit.nodes[fault[0]].getFanIn()):
                print("Input of the fault not its input")
                return False
            if (fault[2] != '0' and fault[2] != '1'):
                print("bad kind of fault")
                return False
            # Update the internal dictionary
            self.fault = {
                "node": fault[0],
                "input": fault[1],
                "fault": 'D' if (fault[2] == '0') else "D'",
                "type": fault_type
            }
            return True

    def _isFaultDetected(self):
        for output_name in self.outputs:
            if self.simTable[output_name] == "D" or self.simTable[
                    output_name] == "D'":
                return True
        return False
