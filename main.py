# Project 1 main

from programs import experimentAlternate

def main():  
  for test_bench in [ "seq_benches/s27.bench",
                      "seq_benches/s208.bench",
                      "seq_benches/s208.bench",
                      "seq_benches/s344.bench",
                      "seq_benches/s1423.bench"]:
    print(test_bench)
    for ts_len in [1, 3, 5, 7, 10]:
      # Perform experiment 3 times
      for i in range(3):
        experimentAlternate(
          circuit_name=test_bench,
          n_runs=10,
          n_test_sequence=100,
          test_sequence_length=ts_len,
          starting_value=('1','1')
        )


if __name__ == "__main__":
  main()

