import time
import math
import random
import numpy as np
from sklearn.linear_model import LinearRegression
import pybind11_example as m

def linear_regression(x, y):
  model = LinearRegression()
  x = np.array(x).reshape(-1, 1)
  y = np.array(y)
  model.fit(x, y)
  return (model.intercept_, model.coef_[0])

def generate_input():
  data = []
  for _ in range(40):
    xs = []
    ys = []
    slope = random.uniform(-10., 10.)
    intercept = random.uniform(-10., 10.)
    for i in range(100):
      x = random.uniform(0., 1000.)
      y = x * slope + intercept + random.gauss(0., 5.)
      xs.append(x)
      ys.append(y)
    data.append((xs, ys))
  return data

def measure_pybind11(data):
  start_time = time.perf_counter()
  ret = []
  for row in data:
    s, i = m.linear_regression(row[0], row[1])
    ret.append((s, i))
  time_taken = time.perf_counter() - start_time
  print("pybind11 time {}".format(time_taken))
  return ret

def measure_python(data):
  start_time = time.perf_counter()
  ret = []
  for row in data:
    s, i = linear_regression(row[0], row[1])
    ret.append((s, i))
  time_taken = time.perf_counter() - start_time
  print("python time {}".format(time_taken))
  return ret

def main():
  data = generate_input()
  fpython = measure_python(data)
  fpybind11 = measure_pybind11(data)
  for i in range(len(fpython)):
    print("python result: {} {} | pybind11 result: {} {}".format(fpython[i][0], fpython[i][1], fpybind11[i][0], fpybind11[i][1]))

if __name__ == '__main__':
  main()
