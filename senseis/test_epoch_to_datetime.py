import time
from datetime import datetime
import pytz
import pybind11_example as m

def epoch_to_datetime(epoch, datetime_format):
  utc = pytz.timezone("UTC")
  dt = utc.localize(datetime.utcfromtimestamp(epoch)).strftime(datetime_format)
  return dt

def test1():
  epoch = 1672618120
  f = "%Y-%m-%dT%H:%M:%S %Z"
  python_datetime = epoch_to_datetime(epoch, f);
  pybind11_datetime = m.epoch_to_datetime(epoch, f)
  print("python: {}".format(python_datetime))
  print("pybind11: {}".format(pybind11_datetime))

def main():
  test1()

if __name__ == '__main__':
  main()
