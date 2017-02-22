import string
from .nodes import ProgramNode, StatementNode, ValueNode, ReferenceNode, \
    TemplateNode, TemplateCallNode
from .exceptions import UnderscoreError, UnderscoreIncorrectParserError, \
    UnderscoreNotImplementedError, UnderscoreSyntaxError, \
    UnderscoreCouldNotConsumeError


class UnderscoreParser:
    VALID_NAME_FIRST_CHARACTER_CHARACTERS = string.ascii_letters + '_-'
    VALID_NAME_NON_FIRST_CHARACTER_CHARACTERS = \
        VALID_NAME_FIRST_CHARACTER_CHARACTERS + string.digits
    RESERVED_NAMES = [
        'if',
        'else',
        'while',
        'template',
        'return',
        'true',
        'false'
    ]
    READ_ONLY_NAMES = ['container']

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

    def _consume_whitespace(self):
        while (self._peek() is not None and self._peek() in string.whitespace):
            self._next()


    def surrounding_whitespace_removed(function):
        def decorated(self, *args, **kwargs):
            self._consume_whitespace()
            result = function(self, *args, **kwargs)
            self._consume_whitespace()
            return result

        return decorated

    def _parse_sections(self, break_at=[]):
        sections = []

        while True:
            if self._peek() is None:
                break
            should_break = False
            for item in break_at:
                if self._peek(len(item)) == item:
                    should_break = True
            if should_break:
                break

            starting_position = self.position_in_program
            valid_parsers = [
                self._parse_statement,
                self._parse_expression,
                self._parse_control,
            ]
            none_worked_error = UnderscoreCouldNotConsumeError(
                'found no parsable input'
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

        return sections

    @surrounding_whitespace_removed
    def parse(self, memory_limit=None, time_limit=None):
        sections = self._parse_sections()
        return ProgramNode(sections, memory_limit, time_limit)

    @surrounding_whitespace_removed
    def _parse_statement(self):
        reference = self._parse_reference()
        if reference.name in self.READ_ONLY_NAMES:
            raise UnderscoreSyntaxError(
                "cannot assign to name '{}'".format(reference.name),
                self.position_in_program
            )
        if self._peek() != '=':
            raise UnderscoreIncorrectParserError()
        # If we get to here, we know the next character is '='
        self._next()
        expression = self._parse_expression()
        return StatementNode(reference, expression)

    @surrounding_whitespace_removed
    def _parse_single_name(self):
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
        if name in self.RESERVED_NAMES:
            raise UnderscoreIncorrectParserError('name was in reserved words')
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
        else:
            # It's an integer.
            raise UnderscoreIncorrectParserError
        if string_of_float[-1] == '.':
            raise UnderscoreIncorrectParserError
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
        starting_position = self.position_in_program
        names = [self._parse_single_name_or_template_call()]
        while self._peek() == '.':
            self._next()
            names.append(self._parse_single_name_or_template_call())
        return ReferenceNode(names, starting_position)

    def _parse_single_name_or_template_call(self):
        starting_position = self.position_in_program
        try:
            return self._parse_template_call()
        except UnderscoreIncorrectParserError:
            self.position_in_program = starting_position
            return self._parse_single_name()

    @surrounding_whitespace_removed
    def _parse_passable_expressions(self):
        try:
            self._try_consume('(')
        except UnderscoreCouldNotConsumeError:
            raise UnderscoreIncorrectParserError
        self._consume_whitespace()
        # More stuff should happen in here eventually.
        try:
            self._try_consume(')')
        except UnderscoreCouldNotConsumeError:
            raise UnderscoreIncorrectParserError
        # This should return something eventually.

    @surrounding_whitespace_removed
    def _parse_template_call(self):
        """
        This will return either a reference node or a template.
        """
        starting_position = self.position_in_program
        try:
            template = self._parse_template()
        except UnderscoreIncorrectParserError:
            self.position_in_program = starting_position
            template = ReferenceNode(
                [self._parse_single_name()],
                starting_position
            )
        # The below stuff should eventually be assigned to something.
        try:
            self._parse_passable_expressions()
        except UnderscoreIncorrectParserError:
            self.position_in_program = starting_position
            raise
        return template

    @surrounding_whitespace_removed
    def _parse_template(self):
        try:
            self._try_consume('template')
        except UnderscoreCouldNotConsumeError:
            raise UnderscoreIncorrectParserError()
        # The below stuff should eventually be assigned to something.
        self._parse_passable_expressions()
        # The above line may error, but, that is okay. Until you are past that
        # line, you do not know that you are definately in a template, and not
        # in, say, a name or reference that begins with 'template'
        try:
            self._try_consume('{')
        except UnderscoreCouldNotConsumeError:
            raise UnderscoreSyntaxError(
                "expected '{{' got {}".format(
                    self._peek() if self._peek() is not None else \
                        'end of file',
                ),
                self.position_in_program
            )
        self._consume_whitespace()
        sections = self._parse_sections(['}', 'return'])
        returns = None
        try:
            self._try_consume('return')
        except UnderscoreCouldNotConsumeError:
            pass
        else:
            self._consume_whitespace()
            try:
                self._try_consume('(')
            except UnderscoreCouldNotConsumeError:
                raise UnderscoreSyntaxError(
                    "expected '(' got {}".format(
                        self._peek() if self._peek() is not None else \
                            'end of file',
                        self.position_in_program
                    )
                )
            returns = self._parse_expression()
            try:
                self._try_consume(')')
                self._consume_whitespace()
                self._try_consume(';')
                self._consume_whitespace()
            except UnderscoreCouldNotConsumeError:
                raise UnderscoreSyntaxError(
                    "expected ')' got {}".format(
                        self._peek() if self._peek() is not None else \
                            'end of file',
                        self.position_in_program
                    )
                )
        try:
            self._try_consume('}')
        except UnderscoreCouldNotConsumeError:
            raise UnderscoreSyntaxError(
                "expected '}}' got {}".format(
                    self._peek() if self._peek() is not None else \
                        'end of file'
                ),
                self.position_in_program
            )
        return TemplateNode(sections, returns)

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