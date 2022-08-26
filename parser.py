import re
import circuit as cr

# Parser module, used to read the file line by line

class Parser(object):
  def __init__(self):
    pass

  # Reads file and returns the circuit stored into a datastructure
  def readFile(self,filename):
    # Assign a new circuit object
    circuit = cr.Circuit(filename)
    
    with open(filename, "r") as f:
      # Get all the lines in the file
      lines = f.readlines()
      for line in lines:
        # Get a new circuit object
        new_circ_object = self._parseLine(line)
        # Add the object to the circuit
        circuit.addNode(new_circ_object)
      

    # At the end the circuit was built, so just return it
    return circuit
   
  # Use RegExp to parse and create a circuit object which is returned
  def _parseLine(self,line):
    result = self._checkCase(line)
    if (result == 0):
      return self._getNewInput(line)
    elif (result == 1):
      return self._getNewOutput(line)
    elif (result == 2):
      return self._getNewGate(line)

  # The line can be of 3 types:
  # 0) input
  # 1) output
  # 2) assignment
  # This function returns the value 0,1 or 2 depending on the current line
  def _checkCase(self, line):
    # Define regexpes
    output_ptrn = re.compile("\s*OUTPUT\(\s*([\w']+)\s*\)\s*",re.IGNORECASE)
    input_ptrn = re.compile("\s*INPUT\(\s*([\w']+)\s*\)\s*",re.IGNORECASE)
    assign_ptrn = re.compile("\s*([\w']+)\s*=\s*([\w']+)\((.*)\)",re.IGNORECASE)

    # Now check for the matching of the 3 cases
    result = input_ptrn.match(line)
    if (result is not None):
      return 0
    
    result = output_ptrn.match(line)
    if (result is not None):
      return 1
    
    result = assign_ptrn.match(line)
    if (result is not None):
      return 2

  # Parse a line which contains an input and create an object
  def _getNewInput(self,line):
    input_ptrn = re.compile("\s*INPUT\(\s*([\w']+)\s*\)\s*",re.IGNORECASE)

    match_object = input_ptrn.match(line)

    input_name = match_object.group(1)

    # Create input object with no fanout nodes for the moment
    input_node = cr.InputNode(input_name)

    return input_node

  def _getNewOutput(self,line):
    output_ptrn = re.compile("\s*OUTPUT\(\s*([\w']+)\s*\)\s*",re.IGNORECASE)

    match_object = output_ptrn.match(line)

    output_name = match_object.group(1)

    # Create output object with no fan in nodes for the moment
    output_node = cr.OutputNode(output_name)

    return output_node

  def _getNewGate(self,line):
    assign_ptrn = re.compile("\s*([\w']+)\s*=\s*([\w']+)\((.*)\)",re.IGNORECASE)
    match_object = assign_ptrn.match(line)
    assigned_node = match_object.group(1)
    gate_name = match_object.group(2)
    # Strip whitespaces from string and then split in a list of arguments
    fan_in_nodes = str(match_object.group(3)).strip().split(',')
    # Create the new circuit object
    gate_node = cr.GateNode(assigned_node,fan_in_nodes)

    if (gate_name == "AND"):
      gate_node.function = cr.__AND__
    elif (gate_name == "OR"):
      gate_node.function = cr.__OR__
    # so on...

    return gate_node