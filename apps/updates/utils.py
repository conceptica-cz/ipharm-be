import importlib


def get_function_by_name(dotted_path: str):
    module_name, func_name = dotted_path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    return getattr(module, func_name)
