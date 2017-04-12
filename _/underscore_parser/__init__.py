import string
from _ import nodes
from _ import exceptions
from ._try_consume import try_consume
from ._whitespace import consume_whitespace
from ._parse import parse, parse_sections
from ._parse_statement import parse_statement
from ._parse_single_name import parse_single_name
from ._parse_expression import parse_expression
from ._parse_objects import parse_object, parse_digits, parse_integer, \
    parse_float, parse_boolean, parse_string, parse_none
from ._parse_references import parse_reference, \
    parse_single_name_or_instantiation_or_call, parse_instantiation_or_call
from ._parse_passable_expressions import parse_passable_expressions
from ._parse_template import parse_template
from ._parse_function import parse_function
from ._parse_maths import parse_addition, parse_subtraction, \
    parse_bracketed_expression, parse_term, parse_non_expandable_term, \
    parse_multiplication, parse_division
from ._parse_boolean_expressions import parse_boolean_expression, \
    parse_boolean_statement
from ._parse_control import parse_control
from ._try_parsers import try_parsers


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

    _try_consume = try_consume
    _consume_whitespace = consume_whitespace
    parse = parse
    _parse_sections = parse_sections
    _parse_statement = parse_statement
    _parse_single_name = parse_single_name
    _parse_expression = parse_expression
    _parse_object = parse_object
    _parse_digits = parse_digits
    _parse_integer = parse_integer
    _parse_float = parse_float
    _parse_boolean = parse_boolean
    _parse_string = parse_string
    _parse_none = parse_none
    _parse_reference = parse_reference
    _parse_single_name_or_instantiation_or_call = \
        parse_single_name_or_instantiation_or_call
    _parse_instantiation_or_call = parse_instantiation_or_call
    _parse_passable_expressions = parse_passable_expressions
    _parse_template = parse_template
    _parse_function = parse_function
    _parse_addition = parse_addition
    _parse_subtraction = parse_subtraction
    _parse_bracketed_expression = parse_bracketed_expression
    _parse_term = parse_term
    _parse_non_expandable_term = parse_non_expandable_term
    _parse_multiplication = parse_multiplication
    _parse_division = parse_division
    _parse_boolean_expression = parse_boolean_expression
    _parse_boolean_statement = parse_boolean_statement
    _parse_control = parse_control
    _try_parsers = try_parsers
