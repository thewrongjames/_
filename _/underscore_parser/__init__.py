from string import ascii_letters, digits


class UnderscoreParser:
    VALID_NAME_FIRST_CHARACTER_CHARACTERS = ascii_letters + '_'
    VALID_NAME_NON_FIRST_CHARACTER_CHARACTERS = \
        VALID_NAME_FIRST_CHARACTER_CHARACTERS + digits
    RESERVED_NAMES = [
        'if',
        'else',
        'while',
        'template',
        'function',
        'return',
        'true',
        'false',
        'none',
        'break',
        'continue',
    ]
    READ_ONLY_NAMES = [
        'float',
        'integer',
        'boolean',
        'string',
        'container',
        'set',
        'get',
        'delete'
    ]

    def __init__(self, program):
        self.program = program
        self.position_in_program = 0
        self.EXPRESSION_PARSERS = [
            self._parse_and_or_or,
            self._parse_not,
            self._parse_comparison,
            self._parse_addition,
            self._parse_subtraction,
            self._parse_multiplication,
            self._parse_division,
            self._parse_power,
            self._parse_object_or_contained_expression,
        ]

    def _peek(self, look_ahead_distance=1):
        if self.position_in_program < len(self.program):
            return self.program[
                self.position_in_program:
                self.position_in_program+look_ahead_distance
            ]
        # If you are at or past the end of the program, this will return none.

    from ._try_consume import try_consume as _try_consume
    from ._whitespace import consume_whitespace as _consume_whitespace
    from ._parse import parse, parse_sections as _parse_sections
    from ._parse_statement import parse_statement as _parse_statement
    from ._parse_single_name import parse_single_name as _parse_single_name
    from ._parse_expression import parse_expression as _parse_expression, \
        parse_typical_sub_expression as _parse_typical_sub_expression
    from ._parse_objects import parse_object as _parse_object, \
        parse_digits as _parse_digits, parse_integer as _parse_integer, \
        parse_float as _parse_float, parse_boolean as _parse_boolean, \
        parse_string as _parse_string, parse_none as _parse_none
    from ._references import parse_reference as _parse_reference, \
        parse_single_name_or_instantiation_or_call as \
        _parse_single_name_or_instantiation_or_call, \
        parse_instantiation_or_call as _parse_instantiation_or_call, \
        parse_passable_expressions as _parse_passable_expressions
    from ._functions_and_templates import parse_function_or_template as \
        _parse_function_or_template, parse_passable_names as \
        _parse_passable_names
    from ._maths import parse_addition as _parse_addition, parse_subtraction \
        as _parse_subtraction, parse_bracketed_expression as \
        _parse_bracketed_expression, parse_power as _parse_power, \
        parse_object_or_contained_expression as \
        _parse_object_or_contained_expression, parse_multiplication as \
        _parse_multiplication, parse_division as _parse_division
    from ._boolean_logic import parse_comparison as _parse_comparison, \
        parse_and_or_or as _parse_and_or_or, parse_not as _parse_not
    from ._controls import parse_control as _parse_control, parse_if as \
        _parse_if, parse_while as _parse_while
    from ._try_parsers import try_parsers as _try_parsers
    from ._breaks import parse_return as _parse_return, \
        parse_break_or_continue as _parse_break_or_continue
    from ._parse_comment import parse_comment as _parse_comment
