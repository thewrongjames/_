from ..exceptions import UnderscoreCouldNotConsumeError
from ._whitespace import surrounding_whitespace_removed


def parse_addition(self, *args):
    return self._parse_typical_sub_expression('+')


def parse_subtraction(self, *args):
    return self._parse_typical_sub_expression('-')


def parse_multiplication(self, *args):
    return self._parse_typical_sub_expression('*')


def parse_division(self, *args):
    return self._parse_typical_sub_expression('/')


def parse_power(self, *args):
    return self._parse_typical_sub_expression('^')


@surrounding_whitespace_removed
def parse_bracketed_expression(self, *args):
    self._try_consume('(', needed_for_this=True)
    self._consume_whitespace()
    expression = self._parse_expression(has_semi_colon=False)
    self._consume_whitespace()
    self._try_consume(')', needed_for_this=True)
    return expression


@surrounding_whitespace_removed
def parse_object_or_contained_expression(self, next_parsers_to_try_first=[]):
    valid_parsers = [
        self._parse_bracketed_expression,
        self._parse_object,
    ]
    value = self._try_parsers(
        valid_parsers,
        'non expandable term',
        next_parsers_to_try_first
    )
    return value
