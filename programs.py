import os
import parser as p
import simulation as sim
import matplotlib.pyplot as plt

# Single TV - Single Fault program
def program1():
  # Clear the screen from previous output
  os.system("clear")
  print("Program 1 starting")
  # Create the parser object
  parser = p.Parser()
  # Ask the user for the filename
  filename = input("Insert the name of the file you want to load [default seq_test.bench]: ")
  os.system("clear")
  # default to circ.bench
  if (len(filename) == 0):
    filename = "seq_test.bench"
  # Now load the file into the circuit data structure
  circuit = parser.readFile(filename)
  # Print informations about the circuit
  # Show more detailed informations
  input("\nPress Enter to continue and show detailed analysis of the circuit...")
  os.system("clear")
  print(circuit)