from _.nodes import StatementNode
from _.exceptions import UnderscoreIncorrectParserError, UnderscoreSyntaxError
from ._whitespace import surrounding_whitespace_removed


@surrounding_whitespace_removed
def parse_statement(self, **kwargs):
    reference = self._parse_reference(next_parsers_to_try_first=[])
    
    if self._peek() != '=':
        # You would think that you might want to raise an incorrect parser error
        # here, put what haven't noticed future human (likely me), is that you
        # have just parsed a completely functional reference, so, while that is
        # really an expression, we are just going to return that here. We do
        # however need to make sure we can consume a semicolon afterwards.
        self._consume_whitespace()
        self._try_consume(';', needed_for_this=True)
        return reference

    # If we get to here, we know the next character is '='
    self.position_in_program += 1

    if reference.name in self.READ_ONLY_NAMES:
        raise UnderscoreSyntaxError(
            "cannot assign to name '{}'".format(reference.name),
            self.position_in_program
        )

    expression = self._parse_expression(**kwargs)
    return StatementNode(reference, expression)
