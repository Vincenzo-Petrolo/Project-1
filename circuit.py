# Circuit module, it aims at representing the circuit read from the file

class Circuit(object):
  def __init__(self, name):
    # Name for the current circuit
    self.name = name
    # Initialize an empty list of inputs
    self.inputs = []
    # Initialize an empty list of outputs
    self.outputs = []
    # Initialize an empty dictionary of nodes, useful for graph traversal
    self.nodes = {}

  def _addInput(self, input_node):
    self.inputs.append(input_node.name)


  def _addOutput(self, output_node):
    self.outputs.append(output_node.name)


  def addNode(self, node):
    # Add the node to the dictionary
    self.nodes[node.getName()] = node

    if isinstance(node, InputNode):
      self._addInput(node)
    elif isinstance(node, OutputNode):
      self._addOutput(node)

  def __str__(self):
    decorator = "================================"
    formatted_string = f"Circuit name: {self.name}"
    inputs_string = f"Inputs: {self.inputs}"
    outputs_string = f"Outputs: {self.outputs}"

    nodes_string = f"Nodes list: {list(self.nodes.keys())}"
    final_string = formatted_string + '\n' + inputs_string + '\n' + outputs_string + '\n' + nodes_string
    return decorator + '\n' + final_string + '\n' + decorator

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
    return f"Gate node of name: {self.name}\nFunction:{self.function.__name__}\nFan-in: {self.fan_in}\nFan-out: {self.fan_out}"


# And function of a gate
def __AND__(self):
  pass

def __OR__(self):
  pass

# ... more to be added
  