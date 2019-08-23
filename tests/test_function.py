from kratos_dpi import dpi_python, dpi_compile
from kratos import Generator, verilog, const
import filecmp
import os


def _test_a(a, b):
    print(a)
    print(b)
    return a + b


def test_shared_compile():
    dpi_python.fn_calls["_test_a"] = _test_a
    dpi_compile("test_a", "temp")


def test_generator_function():
    @dpi_python(16)
    def test_add(a, b):
        return a + b

    gen = Generator("test")
    in_ = gen.input("in", 16)
    out_ = gen.output("out", 16)

    def code():
        out_ = test_add(in_, const(1, 16))

    gen.add_code(code)

    dpi_compile("test", "temp")
    verilog(gen, filename="temp/test.sv")
    base_dir = os.path.dirname(__file__)
    gold_dir = os.path.join(base_dir, "gold")
    assert filecmp.cmp("temp/test.sv",
                       os.path.join(gold_dir, "generator_func.sv"))
    assert filecmp.cmp("temp/test.cc",
                       os.path.join(gold_dir, "generator_func.cc"))


if __name__ == "__main__":
    test_generator_function()
