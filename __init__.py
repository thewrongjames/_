import string
import time


def compile_underscore(program, memory_limit=None, time_limit=None):
    program = str(program)
    parser = UnderscoreParser(program)
    compiled = parser.parse()
    return compiled


class UnderscoreParser:
    VALID_NAME_FIRST_CHARACTER_CHARACTERS = string.ascii_letters + '_-'
    VALID_NAME_NON_FIRST_CHARACTER_CHARACTERS = \
        VALID_NAME_FIRST_CHARACTER_CHARACTERS + string.digits

    def __init__(self, program):
        self.program = program
        for whitespace in string.whitespace:
            self.program = self.program.replace(whitespace, '')
        self.length_of_program = len(program)
        self.position_in_program = 0

    def _peek(self):
        if self.position_in_program < len(self.program):
            return self.program[self.position_in_program]
        # If you are at or past the end of the program, this will return none.

    def _next(self):
        self.position_in_program += 1

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
            error = UnderscoreSyntaxError(
                'expected end of file, got {}'.format(self._peek())
            )
            parsed_something = False

            for parser in valid_parsers:
                try:
                    sections.append(parser())
                except UnderscoreParserError as e:
                    error = e
                    self.position_in_program = starting_position
                else:
                    parsed_something = True
                    break

            if not parsed_something:
                raise error

        return ProgramNode(sections, memory_limit, time_limit)

    def _parse_statement(self):
        name = self._parse_name()
        if self._peek() != '=':
            raise UnderscoreSyntaxError(
                "expected '=', got {}".format(
                    self._peek() if self._peek() is not None else 'end of file',
                ),
                self.position_in_program,
            )
        # If we get to here, we know the next character is '='
        self._next()
        expression = self._parse_expression()
        return StatementNode(name, expression)

    def _parse_name(self):
        name = ''

        if self._peek() not in \
                UnderscoreParser.VALID_NAME_FIRST_CHARACTER_CHARACTERS:
            raise UnderscoreSyntaxError(
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
        while self._peek() in \
                UnderscoreParser.VALID_NAME_NON_FIRST_CHARACTER_CHARACTERS:
            name += self._peek()
            self._next()
        return name

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

    def _parse_object(self):
        starting_position = self.position_in_program
        valid_parsers = [
            self._parse_integer,
            self._parse_float,
            self._parse_boolean,
            self._parse_string,
            self._parse_template,
            self._parse_reference,
        ]
        return self._try_parsers(valid_parsers, 'object')

    def _parse_integer(self):
        string_of_integer = ''
        if self._peek() in ['+', '-']:
            string_of_integer += self._peek()
            self._next()
        if self._peek() not in string.digits:
            raise UnderscoreSyntaxError(
                'expected one of {}, got {}'.format(
                    string.digits,
                    self._peek() if self._peek() is not None else 'end of file',
                ),
                self.position_in_program,
            )
        while self._peek() in string.digits:
            string_of_integer += self._peek()
            self._next()
        return IntegerNode(int(string_of_integer))

    def _parse_float(self):
        raise UnderscoreParserError('Not Implemented', self.position_in_program)

    def _parse_boolean(self):
        raise UnderscoreParserError('Not Implemented', self.position_in_program)

    def _parse_string(self):
        raise UnderscoreParserError('Not Implemented', self.position_in_program)

    def _parse_template(self):
        raise UnderscoreParserError('Not Implemented', self.position_in_program)

    def _parse_reference(self):
        raise UnderscoreParserError('Not Implemented', self.position_in_program)

    def _parse_addition(self):
        raise UnderscoreParserError('Not Implemented', self.position_in_program)

    def _parse_subtraction(self):
        raise UnderscoreParserError('Not Implemented', self.position_in_program)

    def _parse_control(self):
        raise UnderscoreParserError('Not Implemented', self.position_in_program)

    def _try_parsers(self, parsers, expected=None):
        # If there is no value given to expected, this can silently return None.
        starting_position = self.position_in_program
        if expected is not None:
            error = UnderscoreSyntaxError(
                'expected {}'.format(expected),
                starting_position
            )
        else:
            error = None

        for parser in parsers:
            try:
                return parser()
            except UnderscoreParserError as e:
                error = e
                # It is okay to reset this, even on the last one, because the
                # error has already been constructed, and contains the position
                # at which it occoured.
                self.position_in_program = starting_position
            else:
                break

        if error is not None:
            raise error

class ProgramNode:
    def __init__(self, sections, memory_limit=None, time_limit=None):
        self.sections = sections
        self.memory_limit = memory_limit
        self.time_limit = time_limit
        self.memory = {}

    def run(self):
        for section in self.sections:
            # The arguements are keyword arguments, because not all sections
            # will want all of these.
            section.run(
                memory=self.memory,
                memory_limit=self.memory_limit,
                time_limit=self.time_limit,
                start_time=time.time(),
            )
        return self.memory


class StatementNode:
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def run(
            self,
            memory,
            memory_limit=None,
            time_limit=None,
            start_time=None
    ):
        memory[self.name] = self.expression.run()


class IntegerNode:
    def __init__(self, value):
        self.value = value

    def run(self, *args, **kwargs):
        return self.value


class UnderscoreParserError(Exception):
    def __init__(self, message, character_number=None):
        if character_number is not None:
            character_message = ' at character {} (ignoring spaces)'.format(
                character_number
            )
        else:
            character_message = ''
        super(UnderscoreParserError, self).__init__(message+character_message)


class UnderscoreSyntaxError(UnderscoreParserError):
    pass
