import os
import parser as p
import simulation as sim
import random
import matplotlib.pyplot as plt

# Single TV - Single Fault program
def program1():
  # Clear the screen from previous output
  os.system("clear")
  print("Single TV - Single Fault program")
  # Create the parser object
  parser = p.Parser()
  # Ask the user for the filename
  filename = input("Insert the name of the file you want to load [default circ.bench]: ")
  os.system("clear")
  # default to circ.bench
  if (len(filename) == 0):
    filename = "circ.bench"
  # Now load the file into the circuit data structure
  circuit = parser.readFile(filename)
  # Print informations about the circuit
  print(f"Circuit {filename}:")
  print(f"Input vector size: {len(circuit.inputs)}")
  print(f"Output vector size: {len(circuit.outputs)}")
 
  # Show more detailed informations
  input("Press Enter to continue and show detailed description of the circuit...")
  os.system("clear")
  print(circuit)
  # Simulate the circuit given 1 input test vector
  input("Press Enter to enter the simulation phase...")
  os.system("clear")
  simulation = sim.Simulation(circuit)
  simulation._get_inputs()
  simulation.simulate()
  print(simulation.simTable)
  # Perform fault simulation
  input("Press Enter to enter the fault simulation phase...")
  os.system("clear")
  fault = input("Write a single stuck-at fault (e.g. g-c-1) : ")
  simulation._get_inputs()
  simulation.simulate([fault])
  print(simulation.simTable)
  print(f"Fault detected: {simulation._isFaultDetected()}")
  
  
# Single TV - All faults
def program2():
  print("Program 2 starting...")
  # Clear the screen from previous output
  os.system("clear")
  print("Single TV - Single Fault program")
  # Create the parser object
  parser = p.Parser()
  # Ask the user for the filename
  filename = input("Insert the name of the file you want to load [default circ.bench]: ")
  os.system("clear")
  # default to circ.bench
  if (len(filename) == 0):
    filename = "circ.bench"
  # Now load the file into the circuit data structure
  circuit = parser.readFile(filename)
  fault_list = circuit.getFullFaultList()
  print(fault_list)
  print(f"Total number of faults: {len(fault_list)}")
  
  input("Press Enter to enter the perform fault coverage...")
  os.system("clear")

  simulator = sim.Simulation(circuit)
  simulator._get_inputs()

  simulator.simulate(fault_list)
  
      
# Fault coverage of 1-10 TVs
def program3():
  print("Program 3 starting...")
  # Clear the screen from previous output
  os.system("clear")
  print("Single TV - Single Fault program")
  # Create the parser object
  parser = p.Parser()
  # Ask the user for the filename
  filename = input("Insert the name of the file you want to load [default circ.bench]: ")
  os.system("clear")
  # default to circ.bench
  if (len(filename) == 0):
    filename = "circ.bench"
  # Now load the file into the circuit data structure
  circuit = parser.readFile(filename)
  # Now generate random inputs, and get fault coverage
  input_width = len(circuit.inputs)
  # Create a dictionary to store coverage for each TV
  coverage_series = []

  # Get fault list
  fault_list = circuit.getFullFaultList()
  print(circuit.fault_list)
  circuit._wireEquivalenceCollapse()
  print(circuit.fault_list)
  return
  simulator = sim.Simulation(circuit)
  for i in range(0,10):
    # Generate a random test vector
    test_vector = generateBitVector(input_width)
    # provide it to the simulator
    simulator._get_inputs(test_vector)
    # perform the simulation on the fault list
    simulator.simulate(fault_list)
    # get the fault coverage
    coverage_series.append(simulator.getFaultCoverage())
  
  # After generate the plot
  generatePlot(10, coverage_series)
  
  

def generateBitVector(length):
  letters = "01"
  result_str = ''.join(random.choice(letters) for i in range(length))

  return result_str

def generatePlot(series_length, series):
  x = range(1, series_length+1)
  y = series

  # plotting the points 
  plt.plot(x, y)
    
  # naming the x axis
  plt.xlabel('Number of test vectors')
  # naming the y axis
  plt.ylabel('Fault coverage (%)')
    
  plt.savefig("fault_coverage_plot.jpg")
