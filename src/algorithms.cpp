#include <cassert>
#include <cmath>
#include <string>
#include <string_view>
#include <utility>
#include <chrono>
#include <vector>
#include <unordered_map>
#include <sstream>
#include <iostream>

// simdjson enable production optimized code
#define __OPTIMIZE__

#include "date/date.h"
#include "simdjson.h"
#include "rapidjson/document.h"

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
namespace s = std;
namespace c = s::chrono;
namespace d = date;
namespace sj = simdjson;
namespace rj = rapidjson;

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

//float is not accurate enough
double datetime_to_epoch(s::string_view datetime_str, s::string_view format){
  s::stringstream ss; ss << datetime_str;
  d::sys_time<c::milliseconds> ms;
  ss >> d::parse(format.data(), ms);
  if (not ss.fail() and not ss.bad())
    return ms.time_since_epoch().count() / 1000.;
  else {
    s::cout << "Failed to convert " << datetime_str << " with format " << format << s::endl;
    return 0.;
  }
}

// use rapidjson
s::unordered_map<s::string, s::vector<float>> parse_example_json1(s::string_view jstr){
  s::unordered_map<s::string, s::vector<float>> ret;
  rj::Document document; document.Parse(jstr.data());
  for (rj::Value::ConstMemberIterator it = document.MemberBegin(); it != document.MemberEnd(); ++it){
    s::string key = it->name.GetString();
    s::vector<float> value;
    if (it->value.GetType() != 4){
      ret[key] = value;
      continue;
    }
    for (auto& v : it->value.GetArray()){
      value.push_back(v.GetDouble());
    }
    ret[key] = value;
  }
  return ret;
}

sj::ondemand::parser parser;

// use simdjson
s::unordered_map<s::string, s::vector<float>> parse_example_json2(const s::string& jstr){
  s::unordered_map<s::string, s::vector<float>> ret;
  sj::padded_string pjstr(jstr);
  sj::ondemand::document doc;
  auto error = parser.iterate(pjstr).get(doc);
  if (error) return ret;
  sj::ondemand::object obj; error = doc.get(obj);
  if (error) return ret;
  int count = 0;
  for (auto field : obj){
    s::string_view key_view; error = field.unescaped_key().get(key_view);
    if (error) continue;
    //wrong
    //s::string key(key_view.data());
    s::string key = {key_view.begin(), key_view.end()};
    sj::ondemand::array array;
    error = field.value().get(array);
    if (error) continue;
    s::vector<float> vec;
    for (sj::ondemand::value v : array){
      //TODO: deal with infinity, NaN etc
      sj::ondemand::number num = v.get_number();
      sj::ondemand::number_type ty = num.get_number_type();
      switch (ty){
      break; case sj::ondemand::number_type::signed_integer: {
        int64_t val = num.get_int64();
        vec.push_back(val);
      }
      break; case sj::ondemand::number_type::unsigned_integer: {
        uint64_t val = num.get_uint64();
        vec.push_back(val);
      }
      break; case sj::ondemand::number_type::floating_point_number: {
        double val = num.get_double();
        vec.push_back(val);
      }
      break; default: assert(false);
      }
    }
    ret[key.data()] = vec;
  }
  return ret;
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

  m.def("datetime_to_epoch", &datetime_to_epoch, R"pbdoc(
          convert datetime string to epoch
  )pbdoc");

  m.def("parse_example_json1", &parse_example_json1, R"pbdoc(
          parse json using rapidjson
  )pbdoc");

  m.def("parse_example_json2", &parse_example_json2, R"pbdoc(
          parse json using simdjson
  )pbdoc");
}
