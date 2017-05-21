from _.nodes import StatementNode
from _.exceptions import UnderscoreIncorrectParserError, UnderscoreSyntaxError
from ._whitespace import SurroundingWhitespaceRemover


@SurroundingWhitespaceRemover()
def parse_statement(self):
    reference = self._parse_reference()
    if self._peek() != '=':
        raise UnderscoreIncorrectParserError()
    # If we get to here, we know the next character is '='
    self.position_in_program += 1
    if reference.name in self.READ_ONLY_NAMES:
        raise UnderscoreSyntaxError(
            "cannot assign to name '{}'".format(reference.name),
            self.position_in_program
        )
    expression = self._parse_expression()
    return StatementNode(reference, expression)
