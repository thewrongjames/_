from _.underscore_parser import UnderscoreParser
from .smart_compile_file import smart_compile_file
from .smart_compile_string import smart_compile_string


def compile_(
        program,
        memory_limit=None,
        time_limit=None,
):
    """
    Compiles underscore code (passed as a string to program) into a ProgramNode
    object which may be run (with the run method). Some errors will be found
    during compilation, and some at runtime.
    """
    program = str(program)
    parser = UnderscoreParser(program)
    compiled = parser.parse(
        memory_limit=memory_limit,
        time_limit=time_limit,
    )
    return compiled


def compile_file(directory, *args, **kwargs):
    """
    Compiles underscore code from a file at the directory passed as directory
    into a ProgramNode object which may be run (with the run method). Some
    errors will be found during compilation, and some at runtime.
    """
    with open(str(directory), 'r') as file_:
        program = file_.read()
    return compile_(program, *args, **kwargs)
