from _ import nodes
from ._whitespace import surrounding_whitespace_removed


@surrounding_whitespace_removed
def parse_addition(self):
    first_term = self._parse_term()
    self._try_consume('+', needed_for_this=True)
    second_term = self._parse_expression(has_semi_colon=False)
    return nodes.AdditionNode(first_term, second_term)


@surrounding_whitespace_removed
def parse_division(self):
    first_term = self._parse_object_or_contained_expression()
    self._try_consume('/', needed_for_this=True)
    second_term = self._parse_expression(has_semi_colon=False)
    return nodes.DivisionNode(first_term, second_term)


@surrounding_whitespace_removed
def parse_multiplication(self):
    first_term = self._parse_object_or_contained_expression()
    self._try_consume('*', needed_for_this=True)
    second_term = self._parse_expression(has_semi_colon=False)
    return nodes.MultiplicationNode(first_term, second_term)


@surrounding_whitespace_removed
def parse_subtraction(self):
    first_term = self._parse_term()
    self._try_consume('-', needed_for_this=True)
    second_term = self._parse_expression(has_semi_colon=False)
    return nodes.SubtractionNode(first_term, second_term)


@surrounding_whitespace_removed
def parse_bracketed_expression(self):
    self._try_consume('(', needed_for_this=True)
    self._consume_whitespace()
    expression = self._parse_expression(has_semi_colon=False)
    self._consume_whitespace()
    self._try_consume(')', needed_for_this=True)
    return expression


@surrounding_whitespace_removed
def parse_object_or_contained_expression(self):
    valid_parsers = [
        self._parse_bracketed_expression,
        self._parse_object,
    ]
    return self._try_parsers(valid_parsers, 'non expandable term')


@surrounding_whitespace_removed
def parse_term(self):
    valid_parsers = [
        self._parse_multiplication,
        self._parse_division,
        self._parse_object_or_contained_expression,
    ]
    return self._try_parsers(valid_parsers, 'term')
