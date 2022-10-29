from fileinput import filename
import os
import parser as p
import simulation as sim
import random
import matplotlib.pyplot as plt
import statistics
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
  number = int(input("Select which bench to use: "))

  if (number not in [1,2]):
    print("Error, not valid!!")
    return -1

  os.system("clear")
  if (number == 1):
    filename = "p2.bench"
  elif (number == 2):
    filename = "c1908.bench"

  # Now load the file into the circuit data structure
  circuit = parser.readFile(filename)

  s = scoap.SCOAP(circuit)
  controllability = s.getControllability()

  input_width = len(circuit.inputs)

  simulator = sim.Simulation(circuit)

  # Montecarlo simulation
  input_patterns = []
  # Generate 100 different input patterns
  for i in range(0, 100):
    simulator._get_inputs(generateBitVector(input_width))




  return




  simulator = sim.Simulation(circuit)

  # perform 10 simulations
  for i in range(0,10):
    # Generate a random test vector
    test_vector = generateBitVector(input_width)
    # provide it to the simulator
    simulator._get_inputs(test_vector)
  
  ## After generate the plot
  #generatePlot(10, coverage_series)

  #input("Press Enter if you want to get the mean and variance...")
  #os.system("clear")

  #iterations = input("Number of iterations [time consuming operation, be careful!]: ")
  #os.system("clear")
  
  # this is a time consuming operation, so perform it over small circuits
  # perform 10 times the same thing as above, and get mean and variance and display it
  

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
      simulator.simulate(fault_list, tune=True)
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