# Project 1 main

from programs import experimentSolid

def main():  
  # Perform experiment
  experimentSolid(
    circuit_name="seq_benches/s1423.bench",
    n_runs=10,
    n_test_sequence=100,
    test_sequence_length=10,
    value=('1','1')
  )


if __name__ == "__main__":
  main()

