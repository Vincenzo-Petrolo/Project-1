from fileinput import filename
import os
import parser as p
import simulation as sim
import random
import scoap

# Fault coverage of 1-10 TVs
def program():
  # Clear the screen from previous output
  os.system("clear")
  print("SCOAP Controllability computation")
  # Create the parser object
  parser = p.Parser()
  # Ask the user for the filename
  print("[1] p2.bench")
  print("[2] c1908.bench")
  print("[3] reconv.bench")
  number = int(input("Select which bench to use: "))

  if (number not in [1,2,3]):
    print("Error, not valid!!")
    return -1

  os.system("clear")
  if (number == 1):
    filename = "p2.bench"
  elif (number == 2):
    filename = "c1908.bench"
  elif (number == 3):
    filename = "reconv.bench"

  # Now load the file into the circuit data structure
  circuit = parser.readFile(filename)

  s = scoap.SCOAP(circuit)
  controllability = s.getControllability()

  input_width = len(circuit.inputs)

  simulator = sim.Simulation(circuit)

  # Now let's perform 10 runs
  output_dictionaries = []

  for j in range(0,10):
    # Create our dictionary to store data
    output_activations_dict = {}

    for output in circuit.outputs.keys():
      output_activations_dict[output] = {'0' : 0, '1': 0}

    # Montecarlo simulation
    # Generate 100 different input patterns
    for i in range(0, 100):
      # Generate random test vector and add it to the circuit
      simulator._get_inputs(generateBitVector(input_width))
      # Perform simulation
      simulator.simulate()
      # Collect the results
      for output in circuit.outputs.keys():
        output_activations_dict[output][simulator.simTable[output]] += 1
    
    # Now append the output activation dictionary
    output_dictionaries.append(output_activations_dict)

  averaged_dictionary = {}
  # initialize this dictionary
  for output in circuit.outputs.keys():
    averaged_dictionary[output] = {'0' : 0, '1': 0}

  # Now take the avg
  for node in circuit.outputs.keys():
    sum_n0 = 0
    sum_n1 = 0
    for i in range(0,10):
      sum_n0 += output_dictionaries[i][node]['0']
      sum_n1 += output_dictionaries[i][node]['1']
    averaged_dictionary[node]['0'] = sum_n0/10
    averaged_dictionary[node]['1'] = sum_n1/10

  print("\n\nThe average after 10 runs is:\n\n")
  print_activations_dict(averaged_dictionary)


  for output in circuit.outputs.keys():
    if (controllability[output][0] > controllability[output][1]):
      if (averaged_dictionary[output]['0'] > averaged_dictionary[output]['1']):
        print(f"Controllability for node {output} is not corresponding to the simulation: (C0, C1) : ({controllability[output][0]},{controllability[output][1]}) | (n0,n1) : ({averaged_dictionary[output]['0']},{averaged_dictionary[output]['1']})")
    elif (controllability[output][0] < controllability[output][1]):
      if (averaged_dictionary[output]['0'] < averaged_dictionary[output]['1']):
        print(f"Controllability for node {output} is not corresponding to the simulation: (C0, C1) : ({controllability[output][0]},{controllability[output][1]}) | (n0,n1) : ({averaged_dictionary[output]['0']},{averaged_dictionary[output]['1']})")



  return


def print_activations_dict(activation_dict):
  print(f"Activation times")
  print(f"Output\t|\t(n0,n1)\t")
  print(f"------\t|\t-------\t")

  for node in activation_dict.keys():
      print(f"{node}\t|\t({activation_dict[node]['0']},{activation_dict[node]['1']})")


def generateBitVector(length):
  letters = "01"
  result_str = ''.join(random.choice(letters) for i in range(length))

  return result_str