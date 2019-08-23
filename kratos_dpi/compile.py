import os
import shutil
import subprocess
from .pyast import extract_arg_name_order_from_fn, getsource
from .func import DPIFunctionCall


def compile_src(target_name, funcs, dirname):
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    # generate the code for the target
    with open(os.path.join(dirname, target_name + ".cc"), "w+") as f:
        f.write('#include "pybind11/include/pybind11/embed.h"\n')
        f.write('#include "pybind11/include/pybind11/eval.h"\n')
        f.write('namespace py = pybind11;\n')
        f.write('\npy::scoped_interpreter guard;\n')

        f.write("\n")
        # generate each function
        for func_name, func_src in funcs.items():
            # get arg names
            args = extract_arg_name_order_from_fn(func_src)
            # print out the function
            # int args
            # TODO: read out from the calling definition
            int_args = ["int " + arg for arg in args]
            f.write("int " + func_name + "(" + ", ".join(int_args) + ") {\n")
            # prepare the local variable
            f.write("  auto locals = py::dict();\n")
            dict_value = []
            for arg in args:
                f.write('  locals["__' + arg + '"] = ' + arg + ";\n")

            # append the result line
            call_args = ["__" + arg for arg in args]
            func_src += "__result = " + func_name + "(" + ", ".join(
                call_args) + ")\n"
            f.write(
                '  py::exec(R"(\n' + func_src + '  )", py::globals(), locals);')

            f.write('  return locals["__result"].cast<int>();\n}')

    # copy pybind and cmake files over
    pybind_dir = os.path.join(os.path.dirname(__file__), "pybind11")
    cmake_file = os.path.join(os.path.dirname(__file__), "CMakeLists.txt")
    if not os.path.isdir(pybind_dir):
        shutil.copytree(pybind_dir, os.path.join(dirname, "pybind11"))
    shutil.copyfile(cmake_file, os.path.join(dirname, "CMakeLists.txt"))

    # run cmake command
    # make the build dir
    build_dir = os.path.join(dirname, "build")
    if not os.path.isdir(build_dir):
        os.mkdir(build_dir)
    subprocess.check_call(["cmake", "-DTARGET=" + target_name, ".."],
                          cwd=build_dir)
    # built it!
    subprocess.check_call(["make"], cwd=build_dir)
    # make sure it produces the desired output
    # we force cmake to compile as *.so file
    so_file = os.path.join(build_dir, target_name + ".so")
    if not os.path.isfile(so_file):
        raise FileNotFoundError("Not able to compile " + so_file)
    return so_file


def dpi_compile(target_name, output_dir):
    funcs = DPIFunctionCall.fn_calls
    fn_srcs = {}
    for name, fn in funcs.items():
        fn_srcs[name] = getsource(fn)
    return compile_src(target_name, fn_srcs, output_dir)
