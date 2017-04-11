from _ import nodes
from .whitespace import _surrounding_whitespace_removed


@_surrounding_whitespace_removed
def _parse_addition(self):
    first_term = self._parse_term()
    self._try_consume('+', needed_for_this=True)
    second_term = self._parse_term()
    return nodes.AdditionNode(first_term, second_term)


@_surrounding_whitespace_removed
def _parse_division(self):
    first_term = self._parse_non_expandable_term()
    self._try_consume('/', needed_for_this=True)
    second_term = self._parse_term()
    return nodes.DivisionNode(first_term, second_term)


@_surrounding_whitespace_removed
def _parse_multiplication(self):
    first_term = self._parse_non_expandable_term()
    self._try_consume('*', needed_for_this=True)
    second_term = self._parse_term()
    return nodes.MultiplicationNode(first_term, second_term)


@_surrounding_whitespace_removed
def _parse_subtraction(self):
    first_term = self._parse_term()
    self._try_consume('-', needed_for_this=True)
    second_term = self._parse_term()
    return nodes.SubtractionNode(first_term, second_term)


@_surrounding_whitespace_removed
def _parse_bracketed_expression(self):
    self._try_consume('(', needed_for_this=True)
    self._consume_whitespace()
    expression = self._parse_expression(has_semi_colon=False)
    self._consume_whitespace()
    self._try_consume(')', needed_for_this=True)
    return expression


@_surrounding_whitespace_removed
def _parse_non_expandable_term(self):
    valid_parsers = [
        self._parse_object,
        self._parse_bracketed_expression,
    ]
    return self._try_parsers(valid_parsers, 'non expandable term')


@_surrounding_whitespace_removed
def _parse_term(self):
    valid_parsers = [
        self._parse_multiplication,
        self._parse_division,
        self._parse_non_expandable_term,
    ]
    return self._try_parsers(valid_parsers, 'term')
