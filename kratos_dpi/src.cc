#include "pybind11/include/pybind11/embed.h" // everything needed for embedding
namespace py = pybind11;

// global guard to speed up the simulation
py::scoped_interpreter guard;

PYBIND11_EXPORT int TEST() {
    py::print("Hello, World!"); // use the Python API
    return 1;
}
