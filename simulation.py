class Simulation(object):
  def __init__(self, circuit):
    self.inputs = circuit.inputs
    self.outputs = circuit.outputs
    self.circuit = circuit
    self.simTable = {}
    self._initialize()
  
  def _goalIsReached(self):
    for node in self.simTable.keys():
      if (self.simTable[node] == "X"):
        return False

    return True

  def _initialize(self):
    # reset the fault if any
    self.fault = {
      "node" : "",
      "input" : "",
      "fault" : ""
    }
     # Initialize everything to X
    for node_name in self.circuit.nodes.keys():
      self.simTable[node_name] = "X"

  def _compute(self, node_name):
    # Avoid computing already computed gates
    if (self.simTable[node_name] in ['0','1','U','D',"D'"]):
      return
    # get the node
    node = self.circuit.nodes[node_name]
    inputs_names = node.getFanIn()
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
    
  def simulate(self, fault = None):
    self._initialize()
    # update the circuit with input vector
    self._get_inputs()
    if (fault is not None):
      # update the fault dictionary
      if (self._updateFault(fault) == False):
        print("Bad fault insertion, aborting simulation")
        return
    
    # now start the simulation
    while (self._goalIsReached() == False):
      for node in self.simTable:
        self._compute(node)

    print(self.simTable)
    print(f"Fault detected: {self._isFaultDetected()}")
  
  def _get_inputs(self):
    inputs_names = ""
    for i in self.inputs:
      inputs_names += i
    formatted_string = "Write the input test vector " + inputs_names + "= "
    input_string = input(formatted_string)

    i = 0
    for input_node in inputs_names:
      self.simTable[input_node] = input_string[i]
      i += 1

  def _updateFault(self, newFault):
    # Not in the correct format
    if (newFault.count('-') != 2):
      return False
    # Now i should have at position:
    # 0 - the node which is faulty
    # 1 - the input at which there's the fault
    # 2 - the type of fault
    
    fault = newFault.split('-')

    # Now validate the fault
    if (fault[0] not in self.simTable.keys()):
      return False
    if (fault[1] not in self.circuit.nodes[fault[0]].getFanIn()):
      return False
    if (fault[2] not in "01"):
      return False
    # Update the internal dictionary
    self.fault = {
      "node" : fault[0],
      "input" : fault[1],
      "fault" : 'D' if (fault[2] == '0') else "D'"
    }
    return True

  def _isFaultDetected(self):
    for output_name in self.outputs:
      if self.simTable[output_name] == "D" or self.simTable[output_name] == "D'":
        return True
    return False