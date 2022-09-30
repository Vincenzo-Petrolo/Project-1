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
        self.fault = {"node": "", "input": "", "fault": "", "type": 0}
        for node_name in sorted(self.circuit.levels, key=self.circuit.levels.get):
          self.simTable[node_name] = 'X'
        self.simTableCopy = self.simTable.copy()
        self.fault_detected = False

    def simulate(self, faults=None, tune = False):
        # Initialize the simulation table
        self._initialize()
        # reset the table to its original value, this is used if
        # running many simulations without getting new inputs
        for initialInput in self.initialSimTable.keys():
          self.simTable[initialInput] = self.initialSimTable[initialInput]

        # check if i need to perform fault simulation or not
        if (faults is not None):
          self._faultSimulation(faults, tune)
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

        for node_name in self.simTable.keys():
          self.simTable[node_name] = 'X'
    
    def _resetTable(self):
        self.fault = {"node": "", "input": "", "fault": "", "type": 0}
        self.simTable = self.simTableCopy.copy()

    def _compute(self, node_name):
        # Avoid computing already computed gates
        if (self.simTable[node_name] in ['0', '1', 'U', 'D', "D'"]):
            return
        # get the node
        node = self.circuit.nodes[node_name]
        inputs_names = node.getFanIn().copy()
        inputs = []

        for i in inputs_names:
            inputs.append(self.simTable[i])
        output = node.function(inputs)
        # Now update the table
        self.simTable[node_name] = output
    
    def _canActivate(self, fault):
        return self.fault_activated 

    def _normalSimulation(self):
        # I use levelization based ordering to go through the loop once
        # for each level i could spawn threads to take care of each single gate
        while (self._goalIsReached() == False):
            for node in self.simTable:
                self._compute(node)
    
    def _faultIsReached(self):
        if (self.simTable[self.fault["node"]] != 'X'):
            return True
        return False

    def _activate(self):
        for node in self.simTable:
            if(self._faultIsReached() == False):
                self._compute(node)        
        # when i finish, it means i computed the faulty node
        # now i need to check if i activate works
        if (self.fault["type"] == 1):
            if (self.fault["fault"] == 'D' and self.simTable[self.fault["node"]] in ['0','U']):
                return False
            elif (self.fault["fault"] == "D'" and self.simTable[self.fault["node"]] in ['1','U']):
                return False
            # if i observe a difference in the node then update the simTable
            self.simTable[self.fault["node"]] = self.fault["fault"]
        elif (self.fault["type"] == 2):
            if (self.fault["fault"] == 'D' and self.simTable[self.fault["input"]] in ['0','U'] ):
                return False
            elif (self.fault["fault"] == "D'" and self.simTable[self.fault["input"]] in ['1','U']):
                return False
            # if i observe a difference in the node then update the simTable
            node = self.circuit.nodes[self.fault["node"]]
            inputs_names = node.getFanIn().copy()
            inputs = []
            inputs_names.remove(self.fault["input"])
            for i in inputs_names:
                inputs.append(self.simTable[i])

            inputs.append(self.fault["fault"])
            output = node.function(inputs)
            self.simTable[self.fault["node"]] = output
        # if none of above triggers, then the fault was correctly activated 
        return True

    def _faultSimulation(self, fault_list, tune = False):
      totalDetectedFaults = 0
      # this for takes O(faults)
      for fault in fault_list:
        # reset the fault detected and activation flags
        self.fault_detected = False
        self.fault_activated = True
        # if fault was already detected, then skip simulation
        if (self.faults[fault] == 1):
            continue
        # reset the simTable
        self._resetTable()

        for initialInput in self.initialSimTable.keys():
          self.simTable[initialInput] = self.initialSimTable[initialInput]

        # update the fault data structure with the new fault
        if (self._updateFault(fault, tune=tune) == False):
            print("Bad fault insertion, aborting simulation")
            return
        # Start the simulation
        self.fault_activated = self._activate()
        if (tune == True and self.fault_activated == False):
            # skip and avoid propagation
            continue
        # now propagate
        self._normalSimulation()
        # increase the counter
        if (self._isFaultDetected() and self.fault_activated):
            self.fault_detected = True
            if (tune != True):
                self._showDetectedFault(fault)
            self.faults[fault] = 1
            totalDetectedFaults += 1
      # eventually print the result of the fault simulation
      print(f"Total new faults detected: {totalDetectedFaults} ({int(totalDetectedFaults/len(fault_list) * 100)}%)")
    
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

    def _updateFault(self, newFault, tune=False):
        # Not in the correct format
        fault_type = newFault.count('-')
        if (fault_type != 2 and fault_type != 1):
            return False
        fault = newFault.split('-')
        if (fault_type == 1):
            # Now validate the fault
            # if tune is true, skip validity check and go greedy
            if (tune == False):
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
            return True
        else:
            # Now validate the fault
            if (tune == False):
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
