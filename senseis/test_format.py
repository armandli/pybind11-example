import pybind11_example as m

def python_format(s, name):
  return s.format(name)

def test1():
  msg = "hello my name is {}"
  name = "sensei"
  python_str = python_format(msg, name)
  pybind11_str = m.cpp_format(msg, name)
  print("python: {}".format(python_str))
  print("pybind11: {}".format(pybind11_str))

def main():
  test1()

if __name__ == '__main__':
  main()
