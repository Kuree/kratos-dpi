#include "pybind11/include/pybind11/embed.h"
#include "pybind11/include/pybind11/eval.h"
namespace py = pybind11;

py::scoped_interpreter guard;

extern "C" {
__attribute__((visibility("default"))) int test_add(int a, int b) {
  auto locals = py::dict();
  locals["__a"] = a;
  locals["__b"] = b;
  py::exec(R"(
def test_add(a, b):
    return a + b
__result = test_add(__a, __b)
  )", py::globals(), locals);  return locals["__result"].cast<int>();
}
}
