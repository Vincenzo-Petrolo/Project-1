import os
import parser as p
import simulation as sim

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
  pass