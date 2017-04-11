from _ import nodes
from _ import exceptions
from ._surrounding_whitespace_removed import _surrounding_whitespace_removed

@_surrounding_whitespace_removed
def _parse_string(self):
    string_starters = ['"""', "'''", '"', "'"]
    string_starter_used = None
    first_character = self._peek()
    for string_starter in string_starters:
        try:
            self._try_consume(string_starter)
        except exceptions.UnderscoreCouldNotConsumeError:
            pass
        else:
            string_starter_used = string_starter
    if string_starter_used is None:
        raise exceptions.UnderscoreIncorrectParserError()
    string = ''
    while self._peek(len(string_starter_used)) != string_starter_used:
        if self._peek() is None:
            raise exceptions.UnderscoreSyntaxError(
                'expected {}, got end of file'.format(string_starter_used),
                self.position_in_program
            )
        string += self._peek()
        self._next()
    for _ in string_starter_used:
        self._next()
    return nodes.ValueNode(string)
