from .smart_compile_file import smart_compile_file
from .smart_compile_string import smart_compile_string
from .terminal import terminal
from .compile_ import compile_


def compile_file(directory, *args, **kwargs):
    """
    Compiles underscore code from a file at the directory passed as directory
    into a ProgramNode object which may be run (with the run method). Some
    errors will be found during compilation, and some at runtime.
    """
    with open(str(directory), 'r') as file_:
        program = file_.read()
    return compile_(program, *args, **kwargs)
