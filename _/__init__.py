from .underscore_parser import UnderscoreParser


def compile_underscore(program, memory_limit=None, time_limit=None):
    program = str(program)
    parser = UnderscoreParser(program)
    compiled = parser.parse()
    return compiled
