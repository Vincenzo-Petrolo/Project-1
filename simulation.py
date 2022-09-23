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
     # Initialize everything to X
    for node_name in self.circuit.nodes.keys():
      self.simTable[node_name] = "X"

  def _compute(self, node_name):
    # Avoid computing already computed gates
    if (self.simTable[node_name] in ['0','1','U']):
      return
    # get the node
    node = self.circuit.nodes[node_name]
    inputs = node.getFanIn()
    output = node.function(inputs)
    # Now update the table
    self.simTable[node_name] = output
    
  def simulate(self):
    self._initialize()
    # update the circuit with input vector
    self._get_inputs()
    
    # now start the simulation
    while (self._goalIsReached() == False):
      for node in self.simTable:
        self._compute(node)

    print(self.simTable)
    
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
    