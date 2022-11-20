# Project 1 main

from programs import experimentRandom

def main():  
  # Perform experiment
  experimentRandom(
    circuit_name="seq_benches/s27.bench",
    n_runs=10,
    n_test_sequence=100,
    test_sequence_length=1
  )


if __name__ == "__main__":
  main()

