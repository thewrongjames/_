import string
from _ import exceptions

def _parse_digits(self, consume_sign):
    """
    Consumes as many digits as it can, but, may also first consume a single
    '+' or '-' if consume sign is True. It then returns the string of what
    it has consumed.
    """
    string_of_integer = ''
    if self._peek() is None:
        raise exceptions.UnderscoreIncorrectParserError
    if self._peek() in ['+', '-'] and consume_sign:
        string_of_integer += self._peek()
        self._next()
    self._consume_whitespace()
    if self._peek() not in string.digits:
        raise exceptions.UnderscoreIncorrectParserError(
            'expected one of {}, got {}'.format(
                string.digits,
                self._peek() if self._peek() is not None else 'end of file',
            ),
            self.position_in_program,
        )
    while self._peek() in string.digits:
        string_of_integer += self._peek()
        self._next()
    return string_of_integer
