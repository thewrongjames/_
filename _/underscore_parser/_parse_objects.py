import string
from _ import nodes
from _ import exceptions
from .whitespace import _surrounding_whitespace_removed


@_surrounding_whitespace_removed
def _parse_object(self):
    valid_parsers = [
        self._parse_float,
        self._parse_integer,
        self._parse_boolean,
        self._parse_string,
        self._parse_none,
        self._parse_reference,
        self._parse_template,
        self._parse_function,
    ]
    return self._try_parsers(valid_parsers, 'object')


@_surrounding_whitespace_removed
def _parse_float(self):
    string_of_float = self._parse_digits(consume_sign=True)
    if self._peek() == '.':
        string_of_float += '.'
        self.position_in_program += 1
        string_of_float += self._parse_digits(consume_sign=False)
    else:
        # It's an integer.
        raise exceptions.UnderscoreIncorrectParserError
    if string_of_float[-1] == '.':
        raise exceptions.UnderscoreIncorrectParserError
    return nodes.ValueNode(float(string_of_float))


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
        self.position_in_program += 1
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
        self.position_in_program += 1
    return string_of_integer


@_surrounding_whitespace_removed
def _parse_integer(self):
    return nodes.ValueNode(int(self._parse_digits(consume_sign=True)))


@_surrounding_whitespace_removed
def _parse_boolean(self):
    try:
        self._try_consume('true')
    except exceptions.UnderscoreCouldNotConsumeError:
        pass
    else:
        return nodes.ValueNode(True)
    try:
        self._try_consume('false')
    except exceptions.UnderscoreCouldNotConsumeError:
        raise exceptions.UnderscoreIncorrectParserError()
    else:
        return nodes.ValueNode(False)


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
        self.position_in_program += 1
    for _ in string_starter_used:
        self.position_in_program += 1
    return nodes.ValueNode(string)


@_surrounding_whitespace_removed
def _parse_none(self):
    try:
        self._try_consume('none')
    except exceptions.UnderscoreCouldNotConsumeError:
        raise exceptions.UnderscoreIncorrectParserError
    return nodes.ValueNode(None)
