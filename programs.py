import os
import parser as p
import simulation as sim
import random
import matplotlib.pyplot as plt
import statistics

# Single TV - Single Fault program
def program1():
  # Clear the screen from previous output
  os.system("clear")
  print("Program 1 starting")
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
  print(f"|\tInput vector size \t|\t{len(circuit.inputs)}")
  print(f"|\tOutput vector size\t|\t{len(circuit.outputs)}")
  # Show more detailed informations
  input("\nPress Enter to continue and show detailed analysis of the circuit...")
  os.system("clear")
  print(circuit)
  #=====================================================================

  # Simulate the circuit given 1 input test vector
  input("Press Enter to enter the simulation phase...")
  os.system("clear")

  simulation = sim.Simulation(circuit)
  # read the inputs to the circuit
  simulation._get_inputs()
  # perform the simulation
  simulation.simulate()
  # print the simulation result
  simulation.printOutputs()
  #=====================================================================
  # Perform fault simulation
  input("Press Enter to enter the fault simulation phase...")
  os.system("clear")

  fault = input("Write a single stuck-at fault (e.g. g-c-1) : ")
  # get the full fault list, needed for the fault simulation
  fault_list = circuit.getFullFaultList()
  # load the fault list into the simulation
  simulation._initFaults(fault_list)
  # perform the simulation using the fault list and the same test vector
  simulation.simulate([fault])
  # Show the internal state
  simulation.showInternalAndOutputNodes()
  # Show if fault is detected
  print(f"Fault detected: {simulation._isFaultDetected()}")
  #=====================================================================
  
  
# Single TV - All faults
def program2():
  # Clear the screen from previous output
  os.system("clear")
  print("Program 2 starting")
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
  # get the full fault list for the circuit
  fault_list = circuit.getFullFaultList()
  # display the full fault list
  circuit.displayFaultList(fault_list)
  # Print the total number of faults
  print(f"\n#Faults\t=\t{len(fault_list)}\n")
  
  input("Press Enter to enter the perform fault coverage...")
  os.system("clear")

  simulator = sim.Simulation(circuit)
  simulator._get_inputs()
  os.system("clear")
  # get the fault list
  fault_list = circuit.getFullFaultList()
  # load the fault list into the simulation
  simulator._initFaults(fault_list)
  print(f"Starting fault simulation, detected faults will be printed as they are discovered...\n")
  # perform the fault simulation
  simulator.simulate(fault_list)
  
      
# Fault coverage of 1-10 TVs
def program3():
  # Clear the screen from previous output
  os.system("clear")
  print("Program 3 starting")
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

  # do fault collapse and get the fault list
  # this will decrease the simulation time
  circuit.doFaultCollapse()
  fault_list = circuit.fault_list

  simulator = sim.Simulation(circuit)
  # load the updated fault list into the simulator
  simulator._initFaults(fault_list)

  # perform 10 simulations
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

  input("Press Enter if you want to get the mean and variance")
  os.system("clear")

  iterations = input("Number of iterations: ")
  os.system("clear")
  
  # this is a time consuming operation, so perform it over small circuits
  # perform 10 times the same thing as above, and get mean and variance and display it
  advancedComputations(simulator, fault_list, input_width, int(iterations))
  

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

def generateManyPlot(series_of_coverage_series, mean_series, variance_series):
  # generate the plot for many series
  plt.close()

  x = range(1, 11)
  for series in series_of_coverage_series:
    # plotting the points 
    plt.plot(x, series)
  
    
  # naming the x axis
  plt.xlabel('Number of test vectors')
  # naming the y axis
  plt.ylabel('Fault coverage (%)')
  plt.title("Fault coverage saturation for random test vectors")
    
  plt.savefig("advanced_series.jpg")

  plt.close()

  # generate the plot for the mean series
  plt.plot(x, mean_series)

  # naming the x axis
  plt.xlabel('Number of test vectors')
  # naming the y axis
  plt.ylabel('Fault coverage (%)')
  plt.title("Mean fault coverage saturation")
    
  plt.savefig("mean.jpg")

  # generate the plot for the variance
  plt.close()
  plt.plot(x, variance_series)

  # naming the x axis
  plt.xlabel('Number of test vectors')
  # naming the y axis
  plt.ylabel('Fault coverage (%)')
  plt.title("Variance of fault coverage saturation at each step between the series")
    
  plt.savefig("variance.jpg")

  # generate the plot for the variance & mean
  plt.close()
  plt.plot(x, variance_series)
  plt.plot(x, mean_series)

  # naming the x axis
  plt.xlabel('Number of test vectors')
  # naming the y axis
  plt.ylabel('Fault coverage (%)')
  plt.title("Variance and mean of the fault coverage saturation effect")
    
  plt.savefig("variance_and_mean.jpg")




def average(input_list):
  return sum(input_list)/len(input_list)

def advancedComputations(simulator, fault_list, input_width, iterations):
  series_of_coverage_series = []

  for j in range(0,iterations):
    coverage_series = []
    # re init the fault list
    simulator._initFaults(fault_list)
    # perform 10 simulations
    for i in range(0,10):
      # Generate a random test vector
      test_vector = generateBitVector(input_width)
      # provide it to the simulator
      simulator._get_inputs(test_vector)
      # perform the simulation on the fault list
      simulator.simulate(fault_list)
      # get the fault coverage
      coverage_series.append(simulator.getFaultCoverage())
    series_of_coverage_series.append(coverage_series)
  
  # at the end, plot them and get the mean coverage
  mean_coverage_series = []
  variance_coverage_series = []
  for i in range(0,10):
    values_from_series = []
    for coverage_series in series_of_coverage_series:
      # append the value from the series
      values_from_series.append(coverage_series[i])
    mean_coverage_series.append(average(values_from_series))
    variance_coverage_series.append(statistics.variance(values_from_series))

  generateManyPlot(series_of_coverage_series, mean_coverage_series, variance_coverage_series) 