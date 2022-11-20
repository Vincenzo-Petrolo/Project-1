# Project 1 main

from programs import experimentRandom

def main():  
  # Perform experiment
  experimentRandom(
    circuit_name="seq_test.bench",
    n_runs=1,
    n_test_sequence=5,
    percentage=1,
    test_sequence_length=3
  )


if __name__ == "__main__":
  main()

