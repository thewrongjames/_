import string
from _ import nodes
from _ import exceptions


class UnderscoreParser:
    VALID_NAME_FIRST_CHARACTER_CHARACTERS = string.ascii_letters + '_'
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
    READ_ONLY_NAMES = ['container', 'set', 'get', 'delete']

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

    def _is_before(self, items_to_check_for, items_to_check_is_before):
        """
        This function is currently unused. It may later have uses in parser
        optimisation.

        Reads from self.position_in_program, and returns True any of
        items_to_check_for appear before the first items_to_check_is_before
        appear.
        """
        earliest_item_to_check_for = len(self.program)
        earliest_item_to_check_is_before = len(self.program)
        for item in items_to_check_for:
            item_position = self.program.find(item, self.position_in_program)
            if item_position < earliest_item_to_check_for:
                earliest_item_to_check_for = item_positon
        for item in items_to_check_is_before:
            item_position = self.program.find(item, self.position_in_program)
            if item_position < earliest_item_to_check_is_before:
                earliest_item_to_check_is_before = item_positon
        return earliest_item_to_check_for < earliest_item_to_check_is_before

    from ._try_consume import try_consume as _try_consume
    from ._whitespace import consume_whitespace as _consume_whitespace
    from ._parse import parse, parse_sections as _parse_sections
    from ._parse_statement import parse_statement as _parse_statement
    from ._parse_single_name import parse_single_name as _parse_single_name
    from ._parse_expression import parse_expression as _parse_expression
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
        _parse_bracketed_expression, parse_term as _parse_term, \
        parse_non_expandable_term as _parse_non_expandable_term, \
        parse_multiplication as _parse_multiplication, parse_division as \
        _parse_division
    from ._boolean_expressions import parse_boolean_expression as \
        _parse_boolean_expression, parse_boolean_statement as \
        _parse_boolean_statement
    from ._controls import parse_control as _parse_control, parse_if as \
        _parse_if, parse_while as _parse_while
    from ._try_parsers import try_parsers as _try_parsers
    from ._parse_return import parse_return as _parse_return
