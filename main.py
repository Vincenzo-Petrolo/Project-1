# Project 1 main

from programs import *

menu = [  "[0] Random DFF initialization experiment",
          "[1] Solid0 DFF initialization experiment",
          "[2] Solid1 DFF initialization experiment",
          "[3] Alternate01 DFF initialization experiment",
          "[4] Alternate10 DFF initialization experiment",
          "[5] Fanout sorted DFF initialization experiment",
          "[6] Genetic Algorithm DFF initialization experiment",
]

def main():  
  test_files = [ "seq_benches/s27.bench",
                      "seq_benches/s208.bench",
                      "seq_benches/s298.bench",
                      "seq_benches/s344.bench",
                      "seq_benches/s1423.bench"]
  test_sequence_lengths = [1, 3, 5, 7, 10]

  os.system("clear")
  print("###### Welcome to DFF initialization experiment program ######")
  for entry in menu:
    print(entry)

  choice = input("Please choose an experiment to perform: ")
  os.system("clear")
  print("Starting experiment")

  if (choice == '0'):
    for test_bench in test_files:
      print(test_bench)
      for ts_len in test_sequence_lengths:
        # Perform experiment 3 times
        for i in range(3):
          experimentRandom(
            circuit_name=test_bench,
            n_runs=10,
            n_test_sequence=100,
            test_sequence_length=ts_len
          )
  elif (choice == '1'):
    for test_bench in test_files:
      print(test_bench)
      for ts_len in test_sequence_lengths:
        # Perform experiment 3 times
        for i in range(3):
          experimentSolid(
            circuit_name=test_bench,
            n_runs=10,
            n_test_sequence=100,
            test_sequence_length=ts_len,
            value=('0','0')
          )
  elif (choice == '2'):
    for test_bench in test_files:
      print(test_bench)
      for ts_len in test_sequence_lengths:
        # Perform experiment 3 times
        for i in range(3):
          experimentSolid(
            circuit_name=test_bench,
            n_runs=10,
            n_test_sequence=100,
            test_sequence_length=ts_len,
            value=('1','1')
          )
  elif (choice == '3'):
    for test_bench in test_files:
      print(test_bench)
      for ts_len in test_sequence_lengths:
        # Perform experiment 3 times
        for i in range(3):
          experimentAlternate(
            circuit_name=test_bench,
            n_runs=10,
            n_test_sequence=100,
            test_sequence_length=ts_len,
            starting_value=('0','0')
          )
  elif (choice == '4'):
    for test_bench in test_files:
      print(test_bench)
      for ts_len in test_sequence_lengths:
        # Perform experiment 3 times
        for i in range(3):
          experimentAlternate(
            circuit_name=test_bench,
            n_runs=10,
            n_test_sequence=100,
            test_sequence_length=ts_len,
            starting_value=('1','1')
          )
  elif (choice == '5'):
    os.system("clear")
    fanout_th = int(input("Threshold value: "))
    for test_bench in test_files:
      print(test_bench)
      for ts_len in test_sequence_lengths:
        # Perform experiment 3 times
        for i in range(3):
          experimentFanout(
            circuit_name=test_bench,
            n_runs=10,
            n_test_sequence=100,
            test_sequence_length=ts_len,
            fanout_th=fanout_th,
            init_value=('0','0')
          )
  elif (choice == '6'):
    print("Be patient as this process might take long time to converge!")
    for test_bench in test_files:
      print(test_bench)
      for ts_len in test_sequence_lengths:
        # Perform experiment 3 times
        for i in range(3):
          experimentGeneticAlgorithm(
            circuit_name=test_bench,
            n_runs=10,
            n_test_sequence=100,
            test_sequence_length=ts_len
          )



if __name__ == "__main__":
  main()

