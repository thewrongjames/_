import string
from _ import nodes
from _ import exceptions


class UnderscoreParser:
    VALID_NAME_FIRST_CHARACTER_CHARACTERS = string.ascii_letters + '_-'
    VALID_NAME_NON_FIRST_CHARACTER_CHARACTERS = \
        VALID_NAME_FIRST_CHARACTER_CHARACTERS + string.digits
    RESERVED_NAMES = [
        'if',
        'else',
        'while',
        'template',
        'return',
        'true',
        'false',
        'function'
    ]
    READ_ONLY_NAMES = ['container']

    def __init__(self, program):
        self.program = program
        self.position_in_program = 0

    def _peek(self, look_ahead_distance=1):
        if self.position_in_program < len(self.program):
            return self.program[
                self.position_in_program:
                self.position_in_program+look_ahead_distance
            ]
        # If you are at or past the end of the program, this will return none.

    from ._try_consume import _try_consume
    from .whitespace import _consume_whitespace
    from .parse import parse, _parse_sections
    from ._parse_statement import _parse_statement
    from ._parse_single_name import _parse_single_name
    from ._parse_expression import _parse_expression
    from ._parse_objects import _parse_object, _parse_digits, _parse_integer, \
        _parse_float, _parse_boolean, _parse_string, _parse_none
    from ._parse_references import _parse_reference, \
        _parse_single_name_or_instantiation_or_call, \
        _parse_instantiation_or_call
    from ._parse_passable_expressions import _parse_passable_expressions
    from ._parse_template import _parse_template
    from ._parse_function import _parse_function
    from ._parse_maths import _parse_addition, _parse_subtraction, \
        _parse_bracketed_expression, _parse_term, _parse_non_expandable_term, \
        _parse_multiplication, _parse_division
    from ._parse_boolean_expressions import _parse_boolean_expression, \
        _parse_boolean_statement
    from ._parse_control import _parse_control
    from ._try_parsers import _try_parsers
