import string
from . import nodes
from . import exceptions


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
        'false',
        'function'
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

    def _try_consume(self, string_to_consume, needed=False, needed_for_this=False):
        starting_position = self.position_in_program
        string_read = ''
        for character in string_to_consume:
            string_read += self._peek() if self._peek() is not None else ''
            if self._peek() != character:
                self.position_in_program = starting_position
                if needed:
                    raise exceptions.UnderscoreSyntaxError(
                        'expected {}, got {}'.format(
                            string_to_consume,
                            string_read if self._peek() is not None else \
                                'end of file'
                        ),
                        starting_position
                    )
                if needed_for_this:
                    raise exceptions.UnderscoreIncorrectParserError
                raise exceptions.UnderscoreCouldNotConsumeError(
                    'could not consume',
                    string_to_consume
                )
            self._next()

    def _consume_whitespace(self):
        while (self._peek() is not None and self._peek() in string.whitespace):
            self._next()

    def _surrounding_whitespace_removed(function):
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
            none_worked_error = exceptions.UnderscoreCouldNotConsumeError(
                'found no parsable input'
            )
            parsed_something = False

            for parser in valid_parsers:
                try:
                    sections.append(parser())
                except exceptions.UnderscoreIncorrectParserError:
                    self.position_in_program = starting_position
                else:
                    parsed_something = True
                    break

            if not parsed_something:
                raise none_worked_error

        return sections

    @_surrounding_whitespace_removed
    def parse(self, memory_limit=None, time_limit=None):
        sections = self._parse_sections()
        return nodes.ProgramNode(sections, memory_limit, time_limit)

    @_surrounding_whitespace_removed
    def _parse_statement(self):
        reference = self._parse_reference()
        if reference.name in self.READ_ONLY_NAMES:
            raise exceptions.UnderscoreSyntaxError(
                "cannot assign to name '{}'".format(reference.name),
                self.position_in_program
            )
        if self._peek() != '=':
            raise exceptions.UnderscoreIncorrectParserError()
        # If we get to here, we know the next character is '='
        self._next()
        expression = self._parse_expression()
        return nodes.StatementNode(reference, expression)

    @_surrounding_whitespace_removed
    def _parse_single_name(self):
        name = ''

        if self._peek() is None or self._peek() not in \
                UnderscoreParser.VALID_NAME_FIRST_CHARACTER_CHARACTERS:
            raise exceptions.UnderscoreIncorrectParserError(
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
            raise exceptions.UnderscoreIncorrectParserError('name was in reserved words')
        return name

    @_surrounding_whitespace_removed
    def _parse_expression(self, requires_semi_colon=True):
        valid_parsers = [
            self._parse_addition,
            self._parse_subtraction,
            self._parse_term,
            self._parse_boolean_expression,
            self._parse_object,
        ]

        expression = self._try_parsers(valid_parsers, 'expression')

        if self._peek() != ';' and requires_semi_colon:
            raise exceptions.UnderscoreSyntaxError(
                "expected ';', got {}".format(
                    self._peek() if self._peek() is not None else 'end of file',
                ),
                self.position_in_program,
            )
        # If requires_semi_colon is False, it still can end in a semi_colon.
        if self._peek() == ';':
            self._next()
        return expression

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

    @_surrounding_whitespace_removed
    def _parse_integer(self):
        return nodes.ValueNode(int(self._parse_digits(consume_sign=True)))

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
            self._next()
        for _ in string_starter_used:
            self._next()
        return nodes.ValueNode(string)

    @_surrounding_whitespace_removed
    def _parse_none(self):
        try:
            self._try_consume('none')
        except exceptions.UnderscoreCouldNotConsumeError:
            raise exceptions.UnderscoreIncorrectParserError
        return nodes.ValueNode(None)

    @_surrounding_whitespace_removed
    def _parse_reference(self):
        starting_position = self.position_in_program
        names = [self._parse_single_name_or_instantiation_or_call()]
        while self._peek() == '.':
            self._next()
            # It is possible that a function is added and is not at the end.
            # The error for that will be raised by the ReferenceNode.
            names.append(self._parse_single_name_or_instantiation_or_call())
        return nodes.ReferenceNode(names, starting_position)

    def _parse_single_name_or_instantiation_or_call(self):
        starting_position = self.position_in_program
        try:
            return self._parse_instantiation_or_call()
        except exceptions.UnderscoreIncorrectParserError:
            self.position_in_program = starting_position
            return self._parse_single_name()

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

    @_surrounding_whitespace_removed
    def _parse_instantiation_or_call(self):
        """
        This will return either a reference node a template, or a function.
        These will be fed to a reference node which will work out what to do
        with them.
        """
        starting_position = self.position_in_program
        try:
            instantiation_or_call = self._parse_template()
        except exceptions.UnderscoreIncorrectParserError:
            try:
                instantiation_or_call = self._parse_function()
            except exceptions.UnderscoreIncorrectParserError:
                self.position_in_program = starting_position
                instantiation_or_call = nodes.ReferenceNode(
                    [self._parse_single_name()],
                    starting_position
                )
        # The below stuff should eventually be assigned to something.
        try:
            self._parse_passable_expressions()
        except exceptions.UnderscoreIncorrectParserError:
            self.position_in_program = starting_position
            raise
        return instantiation_or_call

    @_surrounding_whitespace_removed
    def _parse_template(self):
        try:
            self._try_consume('template')
        except exceptions.UnderscoreCouldNotConsumeError:
            raise exceptions.UnderscoreIncorrectParserError()
        # The below stuff should eventually be assigned to something.
        self._parse_passable_expressions()
        # The above line may error, but, that is okay. Until you are past that
        # line, you do not know that you are definately in a template, and not
        # in, say, a name or reference that begins with 'template'
        self._try_consume('{', needed=True)
        self._consume_whitespace()
        sections = self._parse_sections(['}'])
        self._try_consume('}', needed=True)
        return nodes.TemplateFunctionNode(sections, None)

    @_surrounding_whitespace_removed
    def _parse_function(self):
        try:
            self._try_consume('function')
        except exceptions.UnderscoreCouldNotConsumeError:
            raise exceptions.UnderscoreIncorrectParserError()
        self._parse_passable_expressions()
        self._try_consume('{', needed=True)
        self._consume_whitespace()
        sections = self._parse_sections(['}', 'return'])
        returns = nodes.ValueNode(None)
        try:
            self._try_consume('return')
        except exceptions.UnderscoreCouldNotConsumeError:
            pass
        else:
            self._consume_whitespace()
            self._try_consume('(', needed=True)
            returns = self._parse_expression(requires_semi_colon=False)
            self._try_consume(')', needed=True)
            self._consume_whitespace()
            self._try_consume(';', needed=True)
            self._consume_whitespace()
        self._try_consume('}', needed=True)
        return nodes.TemplateFunctionNode(sections, returns)

    @_surrounding_whitespace_removed
    def _parse_addition(self):
        first_term = self._parse_term()
        self._try_consume('+', needed_for_this=True)
        second_term = self._parse_term()
        return nodes.AdditionNode(first_term, second_term)

    @_surrounding_whitespace_removed
    def _parse_subtraction(self):
        first_term = self._parse_term()
        self._try_consume('-', needed_for_this=True)
        second_term = self._parse_term()
        return nodes.SubtractionNode(first_term, second_term)

    @_surrounding_whitespace_removed
    def _parse_bracketed_expression(self):
        self._try_consume('(', needed_for_this=True)
        self._consume_whitespace()
        expression = self._parse_expression(requires_semi_colon=False)
        self._consume_whitespace()
        self._try_consume(')', needed_for_this=True)
        return expression

    @_surrounding_whitespace_removed
    def _parse_term(self):
        valid_parsers = [
            self._parse_multiplication,
            self._parse_division,
            self._parse_non_expandable_term,
        ]
        return self._try_parsers(valid_parsers, 'term')

    @_surrounding_whitespace_removed
    def _parse_non_expandable_term(self):
        valid_parsers = [
            self._parse_object,
            self._parse_bracketed_expression,
        ]
        return self._try_parsers(valid_parsers, 'non expandable term')

    @_surrounding_whitespace_removed
    def _parse_multiplication(self):
        first_term = self._parse_non_expandable_term()
        self._consume_whitespace()
        self._try_consume('*', needed_for_this=True)
        self._consume_whitespace()
        second_term = self._parse_term()
        return nodes.MultiplicationNode(first_term, second_term)

    @_surrounding_whitespace_removed
    def _parse_division(self):
        first_term = self._parse_non_expandable_term()
        self._consume_whitespace()
        self._try_consume('/', needed_for_this=True)
        self._consume_whitespace()
        second_term = self._parse_term()
        return nodes.DivisionNode(first_term, second_term)

    @_surrounding_whitespace_removed
    def _parse_boolean_expression(self):
        raise exceptions.UnderscoreNotImplementedError

    @_surrounding_whitespace_removed
    def _parse_control(self):
        raise exceptions.UnderscoreNotImplementedError

    def _try_parsers(self, parsers, expected=None, needed=False):
        # If there is no value given to expected, this can silently return None.
        starting_position = self.position_in_program
        one_worked = False
        if expected is not None:
            if needed:
                none_worked_error = exceptions.UnderscoreSyntaxError(
                    'expected {}'.format(expected),
                    starting_position
                )
            else:
                none_worked_error = exceptions.UnderscoreIncorrectParserError()
        else:
            none_worked_error = None

        for parser in parsers:
            try:
                return parser()
            except exceptions.UnderscoreIncorrectParserError:
                self.position_in_program = starting_position
            else:
                one_worked = True
                break

        if not one_worked and none_worked_error is not None:
            raise none_worked_error
