import json
import pybind11_example as m

def parse_example_json(jstr):
  m = json.loads(jstr)
  return m

def test1():
  js = '{"bids":[100.5, 13.1, 2, 100.6, 24.2, 16],"asks":[100.7, 1.2, 1, 100.8, 12.2, 2]}'.encode(encoding='UTF-8')
  pybind11_obj1 = m.parse_example_json1(js)
  pybind11_obj2 = m.parse_example_json2(js)
  python_obj = parse_example_json(js)
  print("pybind11 obj1 : {}".format(pybind11_obj1))
  print("pybind11 obj2 : {}".format(pybind11_obj2))
  print("python obj : {}".format(python_obj))

def main():
  test1()

if __name__ == '__main__':
  main()
