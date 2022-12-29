import time
from datetime import datetime
import pytz
import pybind11_example as m

def datetime_to_epoch(datetime_str, datetime_format):
  utc = pytz.timezone("UTC")
  dt = datetime.strptime(datetime_str, datetime_format).replace(tzinfo=utc)
  return dt.timestamp()

def datetime_to_epoch2(datetime_str, datetime_format):
  dt = datetime.strptime(datetime_str, datetime_format)
  return dt.timestamp()

def test1():
  datetime_str = "2022-12-25T01:02:59.999 UTC"
  datetime_format = "%Y-%m-%dT%H:%M:%S %Z"
  datetime_format_py = "%Y-%m-%dT%H:%M:%S.%f %Z"
  pybind11_epoch = m.datetime_to_epoch(datetime_str, datetime_format)
  python_epoch = datetime_to_epoch(datetime_str, datetime_format_py)
  print("test1 pybind11 epoch: {}".format(pybind11_epoch))
  print("test1 python epoch: {}".format(python_epoch))

# pybind11 always assume it's UTC time by default, not local time by default
def test2():
  datetime_str = "2022-10-01T08:00:00"
  datetime_format = "%Y-%m-%dT%H:%M:%S"
  datetime_format_py = "%Y-%m-%dT%H:%M:%S"
  pybind11_epoch = m.datetime_to_epoch(datetime_str, datetime_format)
  python_epoch = datetime_to_epoch(datetime_str, datetime_format_py)
  print("test2 pybind11 epoch: {}".format(pybind11_epoch))
  print("test2 python epoch: {}".format(python_epoch))

def test3():
  datetime_str = "1999-05-19T14:45:23.123 EST"
  datetime_format = "%Y-%m-%dT%H:%M:%S %Z"
  datetime_format_py = "%Y-%m-%dT%H:%M:%S.%f %Z"
  pybind11_epoch = m.datetime_to_epoch(datetime_str, datetime_format)
  python_epoch = datetime_to_epoch2(datetime_str, datetime_format_py)
  print("test2 pybind11 epoch: {}".format(pybind11_epoch))
  print("test2 python epoch: {}".format(python_epoch))

def main():
  test1()
  test2()
  test3()

if __name__ == '__main__':
  main()
