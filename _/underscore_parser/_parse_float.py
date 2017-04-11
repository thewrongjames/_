from _ import nodes
from _ import exceptions
from ._surrounding_whitespace_removed import _surrounding_whitespace_removed

@_surrounding_whitespace_removed
def _parse_float(self):
    string_of_float = self._parse_digits(consume_sign=True)
    if self._peek() == '.':
        string_of_float += '.'
        self._next()
        string_of_float += self._parse_digits(consume_sign=False)
    else:
        # It's an integer.
        raise exceptions.UnderscoreIncorrectParserError
    if string_of_float[-1] == '.':
        raise exceptions.UnderscoreIncorrectParserError
    return nodes.ValueNode(float(string_of_float))
