import os
import parser as p
from simulation import * 

from experiment_functions import *

import matplotlib.pyplot as plt

def experimentRandom(circuit_name, n_runs, test_sequence_length, n_test_sequence):
  # Clear the screen from previous output
  parser = p.Parser()
  circuit = parser.readFile(circuit_name)

  # Create the sequential simulator
  seqsim = SequentialSimulation(circuit)

  __ZERO__ = ('0', '0')
  __ONE__ = ('1', '1')

  fault_list = circuit.getFullFaultList()

  report_filename = "report.csv"
  counter_u = 0
  counter_i = 0

  with open(report_filename, "w") as f:
    f.write(f"Fault, FF_init, detected\n")
    for i in range(n_runs):
      ff_init_values = getRandomFFinitValues(circuit=circuit)
      # Pick a random fault
      fault = random.choice(fault_list)
      for j in range(n_test_sequence):
        test_sequence = getRandomTestSequence(circuit=circuit, length=test_sequence_length)
        seqsim.simulate(test_sequence=test_sequence, ff_init_values={}, fault=fault)
        if (seqsim.faultDetected()):
          counter_u += 1
        seqsim.simulate(test_sequence=test_sequence, ff_init_values=ff_init_values, fault=fault)
        if (seqsim.faultDetected()):
          counter_i += 1
        #seqsim._simulationReport()
  
  print(f"#Faults={n_runs}, #Detected[U]={counter_u}, #Detected[I]={counter_i}, length={test_sequence_length}, #TS={n_test_sequence}")


def experimentSolid(circuit_name, n_runs, test_sequence_length, n_test_sequence, value):
  # Clear the screen from previous output
  parser = p.Parser()
  circuit = parser.readFile(circuit_name)

  # Create the sequential simulator
  seqsim = SequentialSimulation(circuit)

  __ZERO__ = ('0', '0')
  __ONE__ = ('1', '1')

  fault_list = circuit.getFullFaultList()

  report_filename = "report.csv"
  counter_u = 0
  counter_i = 0

  with open(report_filename, "w") as f:
    f.write(f"Fault, FF_init, detected\n")
    for i in range(n_runs):
      ff_init_values = getSolidFFInitValues(circuit=circuit, value=value)
      # Pick a random fault
      fault = random.choice(fault_list)
      for j in range(n_test_sequence):
        test_sequence = getRandomTestSequence(circuit=circuit, length=test_sequence_length)
        seqsim.simulate(test_sequence=test_sequence, ff_init_values={}, fault=fault)
        if (seqsim.faultDetected()):
          counter_u += 1
        seqsim.simulate(test_sequence=test_sequence, ff_init_values=ff_init_values, fault=fault)
        if (seqsim.faultDetected()):
          counter_i += 1
        #seqsim._simulationReport()
  
  print(f"#Faults={n_runs}, #Detected[U]={counter_u}, #Detected[I]={counter_i}, length={test_sequence_length}, #TS={n_test_sequence}")


def experimentAlternate(circuit_name, n_runs, test_sequence_length, n_test_sequence, starting_value):
  # Clear the screen from previous output
  parser = p.Parser()
  circuit = parser.readFile(circuit_name)

  # Create the sequential simulator
  seqsim = SequentialSimulation(circuit)

  __ZERO__ = ('0', '0')
  __ONE__ = ('1', '1')

  fault_list = circuit.getFullFaultList()

  report_filename = "report.csv"
  counter_u = 0
  counter_i = 0

  with open(report_filename, "w") as f:
    f.write(f"Fault, FF_init, detected\n")
    for i in range(n_runs):
      ff_init_values = getAlternatedFFInitValues(circuit=circuit, starting_value=starting_value)
      # Pick a random fault
      fault = random.choice(fault_list)
      for j in range(n_test_sequence):
        test_sequence = getRandomTestSequence(circuit=circuit, length=test_sequence_length)
        seqsim.simulate(test_sequence=test_sequence, ff_init_values={}, fault=fault)
        if (seqsim.faultDetected()):
          counter_u += 1
        seqsim.simulate(test_sequence=test_sequence, ff_init_values=ff_init_values, fault=fault)
        if (seqsim.faultDetected()):
          counter_i += 1
        #seqsim._simulationReport()
  
  print(f"#Faults={n_runs}, #Detected[U]={counter_u}, #Detected[I]={counter_i}, length={test_sequence_length}, #TS={n_test_sequence}")


def experimentFanout(circuit_name, n_runs, test_sequence_length, n_test_sequence, fanout_th, init_value):
  # Clear the screen from previous output
  parser = p.Parser()
  circuit = parser.readFile(circuit_name)

  # Create the sequential simulator
  seqsim = SequentialSimulation(circuit)

  __ZERO__ = ('0', '0')
  __ONE__ = ('1', '1')

  fault_list = circuit.getFullFaultList()

  report_filename = "report.csv"
  counter_u = 0
  counter_i = 0

  with open(report_filename, "w") as f:
    f.write(f"Fault, FF_init, detected\n")
    for i in range(n_runs):
      ff_init_values = getFanOutFFInitValues(circuit=circuit, fanout_th=fanout_th, init_value=init_value)
      # Pick a random fault
      fault = random.choice(fault_list)
      for j in range(n_test_sequence):
        test_sequence = getRandomTestSequence(circuit=circuit, length=test_sequence_length)
        seqsim.simulate(test_sequence=test_sequence, ff_init_values={}, fault=fault)
        if (seqsim.faultDetected()):
          counter_u += 1
        seqsim.simulate(test_sequence=test_sequence, ff_init_values=ff_init_values, fault=fault)
        if (seqsim.faultDetected()):
          counter_i += 1
        #seqsim._simulationReport()
  
  print(f"#Faults={n_runs}, #Detected[U]={counter_u}, #Detected[I]={counter_i}, length={test_sequence_length}, #TS={n_test_sequence}")


def experimentGeneticAlgorithm(circuit_name, n_runs, test_sequence_length, n_test_sequence):
  # Clear the screen from previous output
  parser = p.Parser()
  circuit = parser.readFile(circuit_name)

  # Create the sequential simulator
  seqsim = SequentialSimulation(circuit)

  __ZERO__ = ('0', '0')
  __ONE__ = ('1', '1')

  fault_list = circuit.getFullFaultList()

  report_filename = "report.csv"
  counter_u = 0
  counter_i = 0

  with open(report_filename, "w") as f:
    f.write(f"Fault, FF_init, detected\n")
    for i in range(n_runs):
      # Pick a random fault
      fault = random.choice(fault_list)
      for j in range(n_test_sequence):
        test_sequence = getRandomTestSequence(circuit=circuit, length=test_sequence_length)
        ff_init_values = getFFInitValuesUsingGeneticAlgorithm(circuit, seqsim, test_sequence)
        seqsim.simulate(test_sequence=test_sequence, ff_init_values={}, fault=fault)
        if (seqsim.faultDetected()):
          counter_u += 1
        seqsim.simulate(test_sequence=test_sequence, ff_init_values=ff_init_values, fault=fault)
        if (seqsim.faultDetected()):
          counter_i += 1
        #seqsim._simulationReport()
  
  print(f"#Faults={n_runs}, #Detected[U]={counter_u}, #Detected[I]={counter_i}, length={test_sequence_length}, #TS={n_test_sequence}")