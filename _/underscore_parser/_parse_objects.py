from string import digits
from _.nodes import ValueNode
from _.exceptions import UnderscoreCouldNotConsumeError, \
    UnderscoreIncorrectParserError, UnderscoreSyntaxError
from ._whitespace import surrounding_whitespace_removed


@surrounding_whitespace_removed
def parse_object(self, next_parsers_to_try_first=[]):
    valid_parsers = [
        self._parse_float,
        self._parse_integer,
        self._parse_boolean,
        self._parse_string,
        self._parse_none,
        self._parse_reference,
        self._parse_function_or_template,
    ]
    return self._try_parsers(
        valid_parsers,
        'object',
        item_to_pass=next_parsers_to_try_first
    )


@surrounding_whitespace_removed
def parse_float(self, *args):
    string_of_float = self._parse_digits(consume_sign=True)
    if self._peek() == '.':
        string_of_float += '.'
        self.position_in_program += 1
        string_of_float += self._parse_digits(consume_sign=False)
    else:
        # It's an integer.
        raise UnderscoreIncorrectParserError
    if string_of_float[-1] == '.':
        raise UnderscoreIncorrectParserError
    return ValueNode(float(string_of_float))


def parse_digits(self, consume_sign):
    """
    Consumes as many digits as it can, but, may also first consume a single '+'
    or '-' if consume_sign is True. It then returns the string of what it has
    consumed.
    """
    string_of_integer = ''
    if self._peek() is None:
        raise UnderscoreIncorrectParserError
    if self._peek() in ['+', '-'] and consume_sign:
        string_of_integer += self._peek()
        self.position_in_program += 1
    self._consume_whitespace()
    if self._peek() not in digits:
        raise UnderscoreIncorrectParserError(
            'expected one of {}, got {}'.format(
                digits,
                self._peek() if self._peek() is not None else 'end of file',
            ),
            self.position_in_program,
        )
    while self._peek() is not None and self._peek() in digits:
        string_of_integer += self._peek()
        self.position_in_program += 1
    return string_of_integer


@surrounding_whitespace_removed
def parse_integer(self, *args):
    return ValueNode(int(self._parse_digits(consume_sign=True)))


@surrounding_whitespace_removed
def parse_boolean(self, *args):
    try:
        self._try_consume('true')
    except UnderscoreCouldNotConsumeError:
        pass
    else:
        return ValueNode(True)
    try:
        self._try_consume('false')
    except UnderscoreCouldNotConsumeError:
        raise UnderscoreIncorrectParserError()
    else:
        return ValueNode(False)


@surrounding_whitespace_removed
def parse_string(self, *args):
    string_starters = ['"""', "'''", '"', "'"]
    string_starter_used = None
    first_character = self._peek()
    for string_starter in string_starters:
        try:
            self._try_consume(string_starter)
        except UnderscoreCouldNotConsumeError:
            pass
        else:
            string_starter_used = string_starter
    if string_starter_used is None:
        raise UnderscoreIncorrectParserError()
    string = ''
    while self._peek(len(string_starter_used)) != string_starter_used:
        if self._peek() is None:
            raise UnderscoreSyntaxError(
                'expected {}, got end of file'.format(string_starter_used),
                self.position_in_program
            )
        string += self._peek()
        self.position_in_program += 1
    for _ in string_starter_used:
        self.position_in_program += 1
    return ValueNode(string)


@surrounding_whitespace_removed
def parse_none(self, *args):
    try:
        self._try_consume('none')
    except UnderscoreCouldNotConsumeError:
        raise UnderscoreIncorrectParserError
    return ValueNode(None)
