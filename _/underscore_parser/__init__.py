import string
from _ import nodes
from _ import exceptions

class UnderscoreParser:
    from .constants import VALID_NAME_FIRST_CHARACTER_CHARACTERS, \
        VALID_NAME_NON_FIRST_CHARACTER_CHARACTERS, RESERVED_NAMES, \
        READ_ONLY_NAMES

    def __init__(self, program):
        self.program = program
        self.length_of_program = len(program)
        self.position_in_program = 0

    #Get rid of this later.
    from ._surrounding_whitespace_removed import _surrounding_whitespace_removed

    from ._peek import _peek
    from ._next import _next
    from ._try_consume import _try_consume
    from ._consume_whitespace import _consume_whitespace
    from ._parse_sections import _parse_sections
    from .parse import parse
    from ._parse_statement import _parse_statement
    from ._parse_single_name import _parse_single_name
    from ._parse_expression import _parse_expression
    from ._parse_object import _parse_object
    from ._parse_digits import _parse_digits
    from ._parse_integer import _parse_integer
    from ._parse_float import _parse_float
    from ._parse_boolean import _parse_boolean
    from ._parse_string import _parse_string
    from ._parse_none import _parse_none
    from ._parse_reference import _parse_reference
    from ._parse_single_name_or_instantiation_or_call import \
        _parse_single_name_or_instantiation_or_call
    from ._parse_passable_expressions import _parse_passable_expressions
    from ._parse_instantiation_or_call import _parse_instantiation_or_call
    from ._parse_template import _parse_template
    from ._parse_function import _parse_function
    from ._parse_addition import _parse_addition
    from ._parse_subtraction import _parse_subtraction
    from ._parse_bracketed_expression import _parse_bracketed_expression
    from ._parse_term import _parse_term
    from ._parse_non_expandable_term import _parse_non_expandable_term
    from ._parse_multiplication import _parse_multiplication
    from ._parse_division import _parse_division
    from ._parse_boolean_expression import _parse_boolean_expression
    from ._parse_boolean_statement import _parse_boolean_statement
    from ._parse_control import _parse_control
    from ._try_parsers import _try_parsers
