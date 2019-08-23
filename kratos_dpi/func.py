from .pyast import extract_arg_name_order_from_fn


class DPIFunctionCall:
    cache_ordering = {}
    fn_calls = {}

    def __init__(self, width=0):
        self.width = width

    def __call__(self, fn):
        width = self.width

        class _DPIFunctionCall:
            def __init__(self):
                self.width = width
                self.__fn = fn

            def __call__(self, *args):
                fn_name = self.__fn.__name__
                if fn_name not in DPIFunctionCall.fn_calls:
                    # only store when called
                    DPIFunctionCall.fn_calls[fn_name] = self.__fn
                cache = DPIFunctionCall.cache_ordering
                arg_types = []
                gen = None
                for arg in args:
                    arg_types.append((arg.width, arg.signed))
                    if gen is None:
                        gen = arg.generator
                if not gen.has_function(fn_name):
                    func = gen.dpi_function(fn_name)
                    func.set_return_width(self.width)
                else:
                    func = gen.get_function(fn_name)
                if fn_name not in DPIFunctionCall.cache_ordering:

                    assert gen is not None, "Unable to determine args"
                    args_order = extract_arg_name_order_from_fn(self.__fn)
                    for idx, name in enumerate(args_order):
                        name = args_order[idx]
                        w, signed = arg_types[idx]
                        func.input(name, w, signed)
                    func.set_port_ordering(args_order)
                    cache[fn_name] = args_order, gen, arg_types
                else:
                    args_order, gen, arg_types = cache[fn_name]
                mapping = {}
                for idx, value in enumerate(args):
                    var_name = args_order[idx]
                    mapping[var_name] = value

                return gen.call(fn_name, mapping)

        return _DPIFunctionCall()


dpi_python = DPIFunctionCall
