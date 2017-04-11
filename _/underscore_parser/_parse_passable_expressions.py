from _ import exceptions
from .whitespace import _surrounding_whitespace_removed


@_surrounding_whitespace_removed
def _parse_passable_expressions(self):
    try:
        self._try_consume('(')
    except exceptions.UnderscoreCouldNotConsumeError:
        raise exceptions.UnderscoreIncorrectParserError
    self._consume_whitespace()
    # More stuff should happen in here eventually.
    try:
        self._try_consume(')')
    except exceptions.UnderscoreCouldNotConsumeError:
        raise exceptions.UnderscoreIncorrectParserError
    # This should return something eventually.
