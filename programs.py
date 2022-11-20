import os
import parser as p
from simulation import * 

from experiment_functions import *

import matplotlib.pyplot as plt

def experimentRandom(circuit_name, n_runs, test_sequence_length, n_test_sequence, percentage):
  # Clear the screen from previous output
  parser = p.Parser()
  circuit = parser.readFile(circuit_name)

  # Create the sequential simulator
  seqsim = SequentialSimulation(circuit)

  __ZERO__ = ('0', '0')
  __ONE__ = ('1', '1')

  fault_list = circuit.getFullFaultList()

  report_filename = "report_" + circuit.name + ".csv"

  with open(report_filename, "w") as f:
    f.write(f"Fault, #run, TS_length, #TS, percentage, FF_init, detected\n")
    for i in range(n_runs):
      ff_init_values = getRandomFFinitValues(circuit=circuit, percentage=percentage)
      # Pick a random fault
      fault = random.choice(fault_list)
      for j in range(n_test_sequence):
        test_sequence = getRandomTestSequence(circuit=circuit, length=test_sequence_length)
        seqsim.simulate(test_sequence=test_sequence, ff_init_values={}, fault=fault)
        f.write(f"{fault}, {i}, {test_sequence_length}, {j}, {percentage}, /, {seqsim.faultDetected()}\n")
        seqsim.simulate(test_sequence=test_sequence, ff_init_values=ff_init_values, fault=fault)
        f.write(f"{fault}, {i}, {test_sequence_length}, {j}, {percentage}, Yes, {seqsim.faultDetected()}\n")
        #seqsim._simulationReport()

