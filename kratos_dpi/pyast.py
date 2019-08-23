import ast
import textwrap
import inspect


def extract_arg_name_order_from_ast(func_args):
    result = []
    for idx, arg in enumerate(func_args):
        assert arg.arg != "self", "class method not allowed"
        result.append(arg.arg)
    return result


def extract_arg_name_order_from_fn(fn_src):
    if not isinstance(fn_src, str):
        fn_src = inspect.getsource(fn_src)
    func_tree = ast.parse(textwrap.dedent(fn_src))
    fn_body = func_tree.body[0]
    func_args = fn_body.args.args
    return extract_arg_name_order_from_ast(func_args)


getsource = inspect.getsource
