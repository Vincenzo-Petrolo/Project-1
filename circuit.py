# Circuit module, it aims at representing the circuit read from the file
class Circuit(object):
  def __init__(self, name):
    # Name for the current circuit
    self.name = name
    # Initialize an empty dictionary of inputs
    self.inputs = {}
    # Initialize an empty dictionary of outputs
    self.outputs = {}
    # Initialize an empty dictionary of nodes, useful for graph traversal
    self.nodes = {}
    # this list will hold the fanout nodes
    self.fanout_nodes = []
    # this list is garbage, it holds inputs to nodes
    # it is used for searching the already taken nodes
    self.garbage = []

  def _addInput(self, input_node):
    self.inputs[input_node.name] = input_node

  def _addOutput(self, output_node):
    self.outputs[output_node.name] = output_node

  def addNode(self, node):
    if isinstance(node, InputNode):
      self._addInput(node)
    elif isinstance(node, OutputNode):
      self._addOutput(node)
    else:
      for input_name in node.getFanIn():
        if (input_name in self.garbage):
          # we flag it as fanout
          self.fanout_nodes.append(input_name)
        else:
          self.garbage.append(input_name)
      self.nodes[node.getName()] = node

  def __str__(self):
    formatted_string =  f"|\tCircuit\t|\t{self.name}"
    inputs_string =     f"|\tIn     \t|\t{sorted(self.inputs.keys())}"
    outputs_string =    f"|\tOut    \t|\t{sorted(self.outputs.keys())}"
    nodes_string =       "----------------Nodes-----------------\n"


    for node in self.nodes.values():
      if isinstance(node, GateNode):
        nodes_string += str(node)

    final_string = formatted_string + '\n' \
        + inputs_string + '\n' \
        + outputs_string + '\n'\
        + nodes_string +'\n'
    
    return final_string
  
  def displayFaultList(self, fault_list):
    print(f"Fault list")
    for fault in fault_list:
      print(f"|\t{fault}\t|")


  def levelize(self):
    finish = False
    # create a dictionary for the levels
    self.levels = {}
    # assign default value to all inputs
    for nodeName in self.nodes.keys():
      self.levels[nodeName] = -1
    # initialize the input level to 0
    for nodeName in self.inputs.keys():
      self.levels[nodeName] = 0
    # initialize all FFs to level 0
    for dff in self.getDFFs():
      self.levels[dff] = 0
    # until every gate is not assigned
    # with a valid level do the loop
    while finish is False:
      finish = True
      for node in self.nodes.values():
        # get the inputs from the node
        inputs = node.fan_in
        if (self._nodeIsValid(inputs) is True):
          self.levels[node.name] = self._computeLevel(inputs)
        else:
          finish = False
          continue

  def displayLevelize(self):
    # first levelize the circuit
    self.levelize()
    # Create a list of lists using the maximum level
    max_level = max(self.levels.values())
    print("#"*30)
    print("Circuit levels")
    for i in range(0, max_level+1):
      node_names = [k for k, v in self.levels.items() if v == i]
      print(f"LEVEL({i}): {'[%s]' % ', '.join(map(str, node_names))}")
    print("#"*30)

  def _computeLevel(self, inputs):
    # create an empty list of levels
    levels = []

    for input in inputs:
      levels.append(self.levels[input])

    return max(levels) + 1

  def _nodeIsValid(self, inputs):
    for input in inputs:
      if (self.levels[input] < 0):
        return False

    return True

  def getFullFaultList(self):
    self.fault_list = []

    for gate_node in self.nodes.values():
      for fan_in in gate_node.getFanIn():
        self.fault_list.append(f"{gate_node.name}-{fan_in}-0")
        self.fault_list.append(f"{gate_node.name}-{fan_in}-1")

      self.fault_list.append(f"{gate_node.name}-0")
      self.fault_list.append(f"{gate_node.name}-1")

    # now print the faults for the inputs
    for input_name in self.inputs:
      self.fault_list.append(f"{input_name}-0")
      self.fault_list.append(f"{input_name}-1")
    for output_name in self.outputs:
      self.fault_list.append(f"{output_name}-0")
      self.fault_list.append(f"{output_name}-1")

    return self.fault_list
  
  # this method applies wire equivalence on
  # nodes with no fanout
  def _wireEquivalenceCollapse(self):
    for node in self.nodes.values():
      # get the input list for the node
      node_inputs = node.getFanIn()
      for node_input in node_inputs:
        if (node_input not in self.fanout_nodes):
          # then i can apply fault equivalence
          #i generate the faults i want to remove from the list
          sa0_input = node_input + '-0'
          sa1_input = node_input + '-1'
          # now remove them from the list
          self.fault_list.remove(sa0_input)
          self.fault_list.remove(sa1_input)

  def _gateEquivalenceCollapse(self):
    for node in self.nodes.values():
      node_inputs = node.getFanIn()
      dropped_faults = []
      if (node.function == __AND__):
        for node_input in node_inputs:
          dropped_faults.append(node.name + '-' + node_input + '-0')
        dropped_faults.append(node.name+'-0')
      elif (node.function == __NAND__):
        for node_input in node_inputs:
          dropped_faults.append(node.name + '-' + node_input + '-0')
        dropped_faults.append(node.name+'-1')
      elif (node.function == __OR__):
        for node_input in node_inputs:
          dropped_faults.append(node.name + '-' + node_input + '-1')
        dropped_faults.append(node.name+'-1')
      elif (node.function == __NOR__):
        for node_input in node_inputs:
          dropped_faults.append(node.name + '-' + node_input + '-1')
        dropped_faults.append(node.name+'-0')
      elif (node.function == __NOT__):
        dropped_faults.append(node.name+'-0')
        dropped_faults.append(node.name+'-1')
      elif (node.function == __BUF__):
        dropped_faults.append(node.name+'-0')
        dropped_faults.append(node.name+'-1')

      # if i can't drop anything, return
      if (len(dropped_faults) == 0):
        return
      # keep the first fault of the equivalence class
      dropped_faults.pop(0)
      # remove the fault from the full fault list
      for dropped_fault in dropped_faults:
        if (dropped_fault in self.fault_list):
          self.fault_list.remove(dropped_fault)
      
  def _gateDominanceCollapse(self):
    for node in self.nodes.values():
      dropped_fault = ""

      if (node.function == __AND__):
        # in AND gate i can drop the node-1 fault
        # because it's dominated by its inputs
        dropped_fault = node.name+'-1'
      elif (node.function == __NAND__):
        # in AND gate i can drop the node-1 fault
        # because it's dominated by its inputs
        dropped_fault = node.name+'-0'
      elif (node.function == __OR__):
        # in AND gate i can drop the node-1 fault
        # because it's dominated by its inputs
        dropped_fault = node.name+'-0'
      elif (node.function == __NOR__):
        # in AND gate i can drop the node-1 fault
        # because it's dominated by its inputs
        dropped_fault = node.name+'-1'

      if (dropped_fault in self.fault_list):
        self.fault_list.remove(dropped_fault)
  
  def doFaultCollapse(self):
    # compute first the full fault list
    self.getFullFaultList()
    # apply the three methods for fault collapse
    self._wireEquivalenceCollapse()
    self._gateEquivalenceCollapse()
    self._gateDominanceCollapse()
  
  def getDFFs(self):
    FF_list = []

    for node in self.nodes.values():
      if (node.function == __DFF__):
        FF_list.append(node.name)

    return FF_list

  def getDFFSortedByFanOut(self):
    scoreboard = {}
    for FF in self.getDFFs():
      scoreboard[FF] = 0

    for node in self.nodes.values():
      for input in node.getFanIn():
        if (input in scoreboard):
          scoreboard[input] += 1
    
    return scoreboard
  
  def getInputs(self):
    return self.inputs.keys()


class Node(object):
  def __init__(self, node_name):
    self.name = node_name
    self.fan_in = []  # Inputs to the node
    self.fan_out = []  # Outputs from the node

  def getName(self):
    return self.name

  # Return the fanout of the current node
  def getFanout(self):
    return self.fan_out

  # Return the fanin of the current node
  def getFanIn(self):
    return self.fan_in

  def __str__(self):
    return f"Simple node of name: {self.name}\nFan-in: {self.fan_in}\nFan-out: {self.fan_out}"

# Input node class, inherits from Node


class InputNode(Node):
  def __init__(self, node_name, fan_out_nodes=[]):
    super().__init__(node_name)
    # the input to an input node is the node itself
    self.fan_in.append(self)

    # Push into the list, the names of the next nodes
    self.fan_out = fan_out_nodes

  def __str__(self):
    output_string =     "|\tName\t|\tFan-in\t|\tFan-out\t|\tType\t|\n"
    output_string +=    "|\t----\t|\t------\t|\t-------\t|\t----\t|\n"
    output_string +=    f"|\t{self.name}\t|\t{self.fan_in}\t|\t{self.fan_out}\t|\tIn\t|"
    return output_string

# Output Node class, inherits from Node


class OutputNode(Node):
  def __init__(self, node_name, fan_in_nodes=[]):
    super().__init__(node_name)
    # the output to an output node is the node itself
    self.fan_out.append(self)

    self.fan_in = fan_in_nodes

  def __str__(self):
    output_string =     "|\tName\t|\tFan-in\t|\tFan-out\t|\tType\t|\n"
    output_string +=    "|\t----\t|\t------\t|\t-------\t|\t----\t|\n"
    output_string +=    f"|\t{self.name}\t|\t{self.fan_in}\t|\t{self.fan_out}\t|\tOut\t|"
    return output_string


class GateNode(Node):
  def __init__(self, node_name, fan_in_nodes=[], fan_out_nodes=[], gateFunctionality=None):
    super().__init__(node_name)

    self.fan_in = fan_in_nodes
    self.fan_out = fan_out_nodes

    if (gateFunctionality is not None):
      self.function = gateFunctionality

  # This function must be overriden
  def function(self):
    return None

  def __str__(self):
    output_string = f"|\t{self.name}\t|\t{self.function.__name__.strip('_')}("
    for fan_in in self.fan_in:
      output_string += f"{fan_in},"
    # replace the last comma with a parenthesis
    output_string = output_string[:-1]
    output_string += ")\n"
    return output_string


# Those functions implement the D-algebra operations
# Their supported alphabet is [0,1,U]

def __AND__(inputs_list):
  if ('0' in inputs_list):
    return '0'
  # if there's no 0 in the inputs
  # we check if there's at least one Unknown
  if ('U' in inputs_list):
    return 'U'

  return '1'


def __NAND__(inputs_list):
  if ('0' in inputs_list):
    return '1'
  # if there's no 0 in the inputs
  # we check if there's at least one Unknown
  if ('U' in inputs_list):
    return 'U'

  return '0'


def __OR__(inputs_list):
  if ('1' in inputs_list):
    return '1'
  # if there's no 0 in the inputs
  # we check if there's at least one Unknown
  if ('U' in inputs_list):
    return 'U'

  return '0'


def __NOR__(inputs_list):
  if ('1' in inputs_list):
    return '0'
  # if there's no 0 in the inputs
  # we check if there's at least one Unknown
  if ('U' in inputs_list):
    return 'U'

  return '1'

def __XOR__(inputs_list):
  if ('U' in inputs_list):
    return 'U'
  
  if ((inputs_list.count('1')) % 2 == 0):
    return '0'
  
  return '1'

def __XNOR__(inputs_list):
  if ('U' in inputs_list):
    return 'U'
  
  if ((inputs_list.count('1')) % 2 == 0):
    return '1'
  
  return '0'

def __NOT__(inputs_list):
  if ('U' in inputs_list):
    return 'U'

  if (inputs_list[0] == '0'):
    return '1'

  return '0'

def __BUF__(inputs_list):
  return inputs_list[0]

def __DFF__(inputs_list):
  pass