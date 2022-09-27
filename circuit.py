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
      self.nodes[node.getName()] = node

  def __str__(self):
    decorator = "================================"
    formatted_string = f"Circuit name: {self.name}"
    inputs_string = f"Inputs: {sorted(self.inputs.keys())}"
    outputs_string = f"Outputs: {sorted(self.outputs.keys())}"
    nodes_string = "Nodes list:\n"

    for node in self.nodes.values():
      if isinstance(node, GateNode):
        nodes_string += str(node)
    
    final_string = formatted_string + '\n' \
                    + inputs_string + '\n' \
                    + outputs_string + '\n'\
                    + nodes_string
    
    return decorator + '\n' + final_string + '\n' + decorator

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
    for i in range(0,max_level+1):
      node_names = [k for k,v in self.levels.items() if v == i]
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
    fault_list = []
    
    for gate_node in self.nodes.values():
      for fan_in in gate_node.getFanIn():
        fault_list.append(f"{gate_node.name}-{fan_in}-0")
        fault_list.append(f"{gate_node.name}-{fan_in}-1")
        
      fault_list.append(f"{gate_node.name}-0")
      fault_list.append(f"{gate_node.name}-1")


    # now print the faults for the inputs
    for input_name in self.inputs:
      fault_list.append(f"{input_name}-0")
      fault_list.append(f"{input_name}-1")
    for output_name in self.outputs:
      fault_list.append(f"{output_name}-0")
      fault_list.append(f"{output_name}-1")

    return fault_list
    
      
    
class Node(object):
  def __init__(self, node_name):
    self.name = node_name
    self.fan_in = [] # Inputs to the node
    self.fan_out = [] # Outputs from the node
    
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
  def __init__(self, node_name, fan_out_nodes = []):
    super().__init__(node_name)
    # the input to an input node is the node itself
    self.fan_in.append(self)

    # Push into the list, the names of the next nodes
    self.fan_out = fan_out_nodes

  def __str__(self):
    return f"Input node of name: {self.name}\nFan-in: {self.fan_in}\nFan-out: {self.fan_out}"

# Output Node class, inherits from Node
class OutputNode(Node):
  def __init__(self, node_name, fan_in_nodes = []):
    super().__init__(node_name)
    # the output to an output node is the node itself
    self.fan_out.append(self)

    self.fan_in = fan_in_nodes
  
  def __str__(self):
    return f"Output node of name: {self.name}\nFan-in: {self.fan_in}\nFan-out: {self.fan_out}"

class GateNode(Node):
  def __init__(self, node_name, fan_in_nodes = [], fan_out_nodes = [], gateFunctionality = None):
    super().__init__(node_name)

    self.fan_in = fan_in_nodes
    self.fan_out = fan_out_nodes

    if (gateFunctionality is not None):
      self.function = gateFunctionality

  # This function must be overriden
  def function(self):
    return None

  def __str__(self):
    return f"\nGate node of name: {self.name}\n" \
    f"Function: {len(self.fan_in)}-{len(self.fan_out)} {self.function.__name__.strip('_')}\n" \
    f"Fan-in: {self.fan_in}\nFan-out: {self.fan_out}\n"



# Those functions implement the D-algebra operations
# Their supported alphabet is [0,1,U,D,D']

# And function of a gate
def __AND__(inputs_list):
  if ('0' in inputs_list):
    return '0'
  if ('X' in inputs_list):
    return 'X'
  # if there's no 0 in the inputs
  # we check if there's at least one Unknown
  if ('U' in inputs_list):
    return 'U'
  if ('D' in inputs_list and "D'" in inputs_list):
    return '0'
  # At this point I have all 1s or a D/D'
  if ('D' in inputs_list):
    return 'D'
  elif ("D'" in inputs_list):
    return "D'"

  return '1'

def __NAND__(inputs_list):
  if ('0' in inputs_list):
    return '1'
  if ('X' in inputs_list):
    return 'X'
  # if there's no 0 in the inputs
  # we check if there's at least one Unknown
  if ('U' in inputs_list):
    return 'U'
  if ('D' in inputs_list and "D'" in inputs_list):
    return '0'
  # At this point I have all 1s or a D/D'
  if ('D' in inputs_list):
    return 'D'
  elif ("D'" in inputs_list):
    return "D'"  
  return '0'

def __OR__(inputs_list):
  if ('1' in inputs_list):
    return '1'
  if ('X' in inputs_list):
    return 'X'
  # if there's no 0 in the inputs
  # we check if there's at least one Unknown
  if ('U' in inputs_list):
    return 'U'
  if ('D' in inputs_list and "D'" in inputs_list):
    return '1'
    # At this point I have all 1s or a D/D'
  if ('D' in inputs_list):
    return 'D'
  elif ("D'" in inputs_list):
    return "D'"
    
  return '0'

def __NOR__(inputs_list):
  if ('1' in inputs_list):
    return '0'
  if ('X' in inputs_list):
    return 'X'
  # if there's no 0 in the inputs
  # we check if there's at least one Unknown
  if ('U' in inputs_list):
    return 'U'
  if ('D' in inputs_list and "D'" in inputs_list):
    return '0'
    # At this point I have all 1s or a D/D'
  if ('D' in inputs_list):
    return 'D'
  elif ("D'" in inputs_list):
    return "D'"
    
  return '1'

def __XOR__(inputs_list):
  if ('X' in inputs_list):
    return 'X'
  if  ('U' in inputs_list):
    return 'U'
  number_ones = inputs_list.count('1')

  if ("D" in inputs_list or "D'" in inputs_list):
    # we enter in good/bad simulation
    # create two lists of inputs, good & bad
    good_inps = []
    bad_inps = []
    for item in inputs_list:
      if (item == "D"):
        good_inps.append('1')
        bad_inps.append('0')
      elif (item == "D'"):
        good_inps.append('0')
        bad_inps.append('1')
      else:
        good_inps.append(item)
        bad_inps.append(item)
    # now that we have the two lists
    # recursive call to the XOR function
    good_result = __XOR__(good_inps)
    bad_result = __XOR__(bad_inps)

    # now compare the results to produce the D-algebra result
    if (good_result == '1' and bad_result == '1'):
      return '1'
    elif (good_result == '1' and bad_result == '0'):
      return 'D'
    elif (good_result == '0' and bad_result == '1'):
      return "D'"
    else:
      return '0'
    
  else:
    # continue with normal simulatio  
    # if the number of ones is even
    if (number_ones % 2 == 0):
      return '0'
    # if the number of ones is odd
    return '1'
  
def __XNOR__(inputs_list):
  if ('X' in inputs_list):
    return 'X'
  if  ('U' in inputs_list):
    return 'U'
  number_ones = inputs_list.count('1')

  if ("D" in inputs_list or "D'" in inputs_list):
    # we enter in good/bad simulation
    # create two lists of inputs, good & bad
    good_inps = []
    bad_inps = []
    for item in inputs_list:
      if (item == "D"):
        good_inps.append('1')
        bad_inps.append('0')
      elif (item == "D'"):
        good_inps.append('0')
        bad_inps.append('1')
      else:
        good_inps.append(item)
        bad_inps.append(item)
    # now that we have the two lists
    good_result = __XNOR__(good_inps)
    bad_result = __XNOR__(bad_inps)

    # now compare the results to produce the D-algebra result
    if (good_result == '1' and bad_result == '1'):
      return '1'
    elif (good_result == '1' and bad_result == '0'):
      return 'D'
    elif (good_result == '0' and bad_result == '1'):
      return "D'"
    else:
      return '0'
    
  else:
    # continue with normal simulatio  
    # if the number of ones is even
    if (number_ones % 2 == 0):
      return '1'
    # if the number of ones is odd
    return '0'
    
def __NOT__(inputs_list):
  if ('X' in inputs_list):
    return 'X'
  if ('U' in inputs_list):
    return 'U'
  # D-algebra support
  if ('D' in inputs_list):
    return "D'"
  elif ("D'" in inputs_list):
    return "D"
  
  if ('0' in inputs_list):
    return '1'

  return '0'

def __BUF__(inputs_list):
  return inputs_list[0]