# Project 1 main

from programs import experimentFanout

def main():  
  for test_bench in [ "seq_benches/s27.bench",
                      "seq_benches/s208.bench",
                      "seq_benches/s298.bench",
                      "seq_benches/s344.bench",
                      "seq_benches/s1423.bench"]:
    print(test_bench)
    for ts_len in [1, 3, 5, 7, 10]:
      # Perform experiment 3 times
      for i in range(3):
        experimentFanout(
          circuit_name=test_bench,
          n_runs=10,
          n_test_sequence=100,
          test_sequence_length=ts_len,
          fanout_th=3,
          init_value=('0','0')
        )


if __name__ == "__main__":
  main()

