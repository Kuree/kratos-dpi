from kratos_dpi import dpi_python, dpi_compile


def test_a(a, b):
    print(a)
    print(b)
    return a + b


def test_shared_compile():
    dpi_python.fn_calls["test_a"] = test_a
    dpi_compile("test", "temp")


if __name__ == "__main__":
    test_shared_compile()
