from _ import nodes
from _ import exceptions
from ._whitespace import surrounding_whitespace_removed

@surrounding_whitespace_removed
def parse_addition_or_subtraction(self):
    first_expression = self._parse_term()
    try:
        self._try_consume('+')
    except exceptions.UnderscoreCouldNotConsumeError:
        self._try_consume('-', needed_for_this=True)
        is_addition = False
    else:
        is_addition = True
    second_expression = self._parse_expression(
            has_semi_colon=False,
            parsers_to_not_allow=[
                self._parse_and_or_or,
                self._parse_not,
                self._parse_comparison
            ]
        )
    if is_addition:
        return nodes.AdditionNode(first_expression, second_expression)
    return nodes.SubtractionNode(first_expression, second_expression)


@surrounding_whitespace_removed
def parse_multiplication_or_division(self):
    first_expression = self._parse_object_or_contained_expression()
    try:
        self._try_consume('*')
    except exceptions.UnderscoreCouldNotConsumeError:
        self._try_consume('/', needed_for_this=True)
        is_multiplication = False
    else:
        is_multiplication = True
    second_expression = self._parse_term()
    if is_multiplication:
        return nodes.MultiplicationNode(first_expression, second_expression)
    return nodes.DivisionNode(first_expression, second_expression)


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
        self._parse_multiplication_or_division,
        self._parse_object_or_contained_expression,
    ]
    return self._try_parsers(valid_parsers, 'term')
