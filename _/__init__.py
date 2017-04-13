from .underscore_parser import UnderscoreParser


def compile_(program, memory_limit=None, time_limit=None):
    """
    Compiles underscore code (passed as a string to program) into a ProgramNode
    object which may be run (with the run method). Some errors will be found
    during compilation, and some at runtime.
    """
    program = str(program)
    parser = UnderscoreParser(program)
    compiled = parser.parse()
    return compiled
