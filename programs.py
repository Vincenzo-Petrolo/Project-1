import os
import parser as p
from simulation import * 

from experiment_functions import *

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
  print(circuit)
  # Show more detailed informations
  input("\nPress Enter to continue and show detailed analysis of the circuit...")
  os.system("clear")

  seqsim = SequentialSimulation(circuit)

  __ZERO__ = ('0', '0')
  __ONE__ = ('1', '1')

  test_sequence = getRandomTestSequence(circuit=circuit, length=3)

  ff_init_values = getRandomFFinitValues(circuit=circuit, percentage=0.3)
  getFanOutFFInitValues(circuit=circuit, fanout_th=1, init_value=__ZERO__)
  print(ff_init_values)

  seqsim.simulate(test_sequence=test_sequence, ff_init_values=ff_init_values, fault="y-0")
