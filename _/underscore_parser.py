import string
from .nodes import ProgramNode, StatementNode, ValueNode, ReferenceNode
from .exceptions import UnderscoreError, UnderscoreIncorrectParserError, \
    UnderscoreNotImplementedError, UnderscoreSyntaxError, \
    UnderscoreCouldNotConsumeError


class UnderscoreParser:
    VALID_NAME_FIRST_CHARACTER_CHARACTERS = string.ascii_letters + '_-'
    VALID_NAME_NON_FIRST_CHARACTER_CHARACTERS = \
        VALID_NAME_FIRST_CHARACTER_CHARACTERS + string.digits

    def __init__(self, program):
        self.program = program
        self.length_of_program = len(program)
        self.position_in_program = 0

    def _peek(self, look_ahead_distance=1):
        if self.position_in_program < len(self.program):
            return self.program[
                self.position_in_program:
                self.position_in_program+look_ahead_distance
            ]
        # If you are at or past the end of the program, this will return none.

    def _next(self):
        self.position_in_program += 1

    def _try_consume(self, string_to_consume):
        starting_position = self.position_in_program
        for character in string_to_consume:
            if self._peek() != character:
                self.position_in_program = starting_position
                raise UnderscoreCouldNotConsumeError(
                    'could not consume',
                    string_to_consume
                )
            self._next()

    def surrounding_whitespace_removed(function):
        def decorated(self, *args, **kwargs):
            while (
                    self._peek() is not None
                    and self._peek() in string.whitespace
            ):
                self._next()
            result = function(self, *args, **kwargs)
            while (
                    self._peek() is not None
                    and self._peek() in string.whitespace
            ):
                self._next()
            return result

        return decorated

    @surrounding_whitespace_removed
    def parse(self, memory_limit=None, time_limit=None):
        sections = []

        while True:
            if self._peek() is None:
                break

            starting_position = self.position_in_program
            valid_parsers = [
                self._parse_statement,
                self._parse_expression,
                self._parse_control,
            ]
            none_worked_error = UnderscoreSyntaxError(
                'expected end of file, got {}'.format(self._peek()),
                starting_position
            )
            parsed_something = False

            for parser in valid_parsers:
                try:
                    sections.append(parser())
                except UnderscoreIncorrectParserError:
                    self.position_in_program = starting_position
                else:
                    parsed_something = True
                    break

            if not parsed_something:
                raise none_worked_error

        return ProgramNode(sections, memory_limit, time_limit)

    @surrounding_whitespace_removed
    def _parse_statement(self):
        name = self._parse_name()
        if self._peek() != '=':
            raise UnderscoreIncorrectParserError()
        # If we get to here, we know the next character is '='
        self._next()
        expression = self._parse_expression()
        return StatementNode(name, expression)

    @surrounding_whitespace_removed
    def _parse_name(self):
        name = ''

        if self._peek() is None or self._peek() not in \
                UnderscoreParser.VALID_NAME_FIRST_CHARACTER_CHARACTERS:
            raise UnderscoreIncorrectParserError(
                'expected one of {}, got {}'.format(
                    UnderscoreParser.VALID_NAME_FIRST_CHARACTER_CHARACTERS,
                    self._peek() if self._peek() is not None else 'end of file',
                ),
                self.position_in_program,
            )
        # As UnderscoreParser.VALID_NAME_FIRST_CHARACTER_CHARACTERS is a subset
        # of UnderscoreParser.VALID_NAME_NON_FIRST_CHARACTER_CHARACTERS, we can
        # now move straight on to taking any non first character character,
        # because that will also take the first character.
        while self._peek() is not None and self._peek() in \
                UnderscoreParser.VALID_NAME_NON_FIRST_CHARACTER_CHARACTERS:
            name += self._peek()
            self._next()
        return name

    @surrounding_whitespace_removed
    def _parse_expression(self):
        valid_parsers = [
            self._parse_object,
            self._parse_addition,
            self._parse_subtraction,
        ]

        expression = self._try_parsers(valid_parsers, 'expression')

        if self._peek() is not ';':
            raise UnderscoreSyntaxError(
                "expected ';', got {}".format(
                    self._peek() if self._peek() is not None else 'end of file',
                ),
                self.position_in_program,
            )
        self._next()
        return expression

    @surrounding_whitespace_removed
    def _parse_object(self):
        starting_position = self.position_in_program
        valid_parsers = [
            self._parse_float,
            self._parse_integer,
            self._parse_boolean,
            self._parse_string,
            self._parse_reference,
            self._parse_template,
        ]
        return self._try_parsers(valid_parsers, 'object')

    def _parse_digits(self, consume_sign):
        """
        Consumes as many digits as it can, but, may also first consume a single
        '+' or '-' if consume sign is True. It then returns the string of what
        it has consumed.
        """
        string_of_integer = ''
        if self._peek() is None:
            raise UnderscoreIncorrectParserError
        if self._peek() in ['+', '-'] and consume_sign:
            string_of_integer += self._peek()
            self._next()
        if self._peek() not in string.digits:
            raise UnderscoreIncorrectParserError(
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

    @surrounding_whitespace_removed
    def _parse_integer(self):
        return ValueNode(int(self._parse_digits(consume_sign=True)))

    @surrounding_whitespace_removed
    def _parse_float(self):
        string_of_float = self._parse_digits(consume_sign=True)
        if self._peek() == '.':
            string_of_float += '.'
            self._next()
            string_of_float += self._parse_digits(consume_sign=False)
        return ValueNode(float(string_of_float))

    @surrounding_whitespace_removed
    def _parse_boolean(self):
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
    def _parse_string(self):
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
            self._next()
        for _ in string_starter_used:
            self._next()
        return ValueNode(string)

    @surrounding_whitespace_removed
    def _parse_reference(self):
        name = self._parse_name()
        return ReferenceNode(name)

    @surrounding_whitespace_removed
    def _parse_template(self):
        raise UnderscoreNotImplementedError()

    @surrounding_whitespace_removed
    def _parse_addition(self):
        raise UnderscoreNotImplementedError()

    @surrounding_whitespace_removed
    def _parse_subtraction(self):
        raise UnderscoreNotImplementedError()

    @surrounding_whitespace_removed
    def _parse_control(self):
        raise UnderscoreNotImplementedError()

    def _try_parsers(self, parsers, expected=None, needed=False):
        # If there is no value given to expected, this can silently return None.
        starting_position = self.position_in_program
        one_worked = False
        if expected is not None:
            if needed:
                none_worked_error = UnderscoreSyntaxError(
                    'expected {}'.format(expected),
                    starting_position
                )
            else:
                none_worked_error = UnderscoreIncorrectParserError()
        else:
            none_worked_error = None

        for parser in parsers:
            try:
                return parser()
            except UnderscoreIncorrectParserError:
                self.position_in_program = starting_position
            else:
                one_worked = True
                break

        if not one_worked and none_worked_error is not None:
            raise none_worked_error
