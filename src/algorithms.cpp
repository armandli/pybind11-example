#include <cmath>
#include <vector>
#include <utility>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
namespace s = std;

float summation(const s::vector<float>& v){
  float s = 0.;
  for (float f : v)
    if (not isnan(f))
      s += f;
  return s;
}

float mean(const s::vector<float>& v){
  float s = 0.;
  for (float f : v)
    if (not isnan(f))
      s += f;
  return s / v.size();
}

s::pair<float,float> linear_regression(const s::vector<float>& x, const s::vector<float>& y){
  s::pair<float, float> ret;

  float mx = mean(x);
  float my = mean(y);

  float sxx = 0., sxy = 0.;
  for (int i = 0; i < x.size(); ++i){
    if (not isnan(x[i]) and not isnan(y[i])){
      sxy += x[i] * y[i];
      sxx += x[i] * x[i];
    }
  }
  sxy -= x.size() * mx * my;
  sxx -= x.size() * mx * mx;
  float slope = sxy / sxx;
  return s::make_pair(my - slope * mx, slope);
}

PYBIND11_MODULE(pybind11_example, m){
  m.doc() = R"pbdoc(
          Pybind11 example plugin
          -----------------------
          .. currentmodule:: pybind11_example

          .. autosummary::
             :toctree: _generate

             summation
  )pbdoc";

  m.def("summation", &summation, R"pbdoc(
          Sum vector of floats
  )pbdoc");

  m.def("mean", &mean, R"pbdoc(
          Mean of vector of floats
  )pbdoc");

  m.def("linear_regression", &linear_regression, R"pbdoc(
          Compute slope and intercept of line
  )pbdoc");
}
