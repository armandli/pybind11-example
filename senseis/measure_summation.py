import time
import math
import random
import pybind11_example as m

def summation(lst):
  s = 0.
  for v in lst:
    if not math.isnan(v):
      s += v
  return s

def generate_input():
  data = [[random.random() for _ in range(2000)] for _ in range(8000)]
  return data

def measure_pybind11(data):
  start_time = time.perf_counter()
  total = 0.
  for row in data:
    total += m.summation(row)
  time_taken = time.perf_counter() - start_time
  print("pybind11 time {}".format(time_taken))
  return total

def measure_python(data):
  start_time = time.perf_counter()
  total = 0.
  for row in data:
    total  += summation(row)
  time_taken = time.perf_counter() - start_time
  print("python time {}".format(time_taken))
  return total

def main():
  data = generate_input()
  fpython = measure_python(data)
  fpybind11 = measure_pybind11(data)
  print("{} == {}".format(fpython, fpybind11))

if __name__ == '__main__':
  main()
