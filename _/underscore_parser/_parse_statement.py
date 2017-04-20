from _ import nodes
from _ import exceptions
from ._whitespace import surrounding_whitespace_removed


@surrounding_whitespace_removed
def parse_statement(self):
    reference = self._parse_reference()
    if self._peek() != '=':
        raise exceptions.UnderscoreIncorrectParserError()
    # If we get to here, we know the next character is '='
    self.position_in_program += 1
    if reference.name in self.READ_ONLY_NAMES:
        raise exceptions.UnderscoreSyntaxError(
            "cannot assign to name '{}'".format(reference.name),
            self.position_in_program
        )
    expression = self._parse_expression()
    return nodes.StatementNode(reference, expression)
