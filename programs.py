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
  input("Press Enter to enter the simulation phase...")
  os.system("clear")
  simulation = sim.Simulation(circuit)
  simulation.simulate()
  input("Press Enter to enter the fault simulation phase...")
  os.system("clear")
  fault = input("Write a single stuck-at fault (e.g. g-c-1) : ")
  simulation.simulate(fault)

  
  
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
  circuit.printFullFaultList()

# Fault coverage of 1-10 TVs
def program3():
  print("Program 3 starting...")
  pass