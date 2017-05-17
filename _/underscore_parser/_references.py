from _.nodes import ReferenceNode
from _.exceptions import UnderscoreCouldNotConsumeError, \
    UnderscoreIncorrectParserError, UnderscoreSyntaxError
from ._whitespace import surrounding_whitespace_removed


@surrounding_whitespace_removed
def parse_reference(self):
    starting_position = self.position_in_program
    components = [self._parse_single_name_or_instantiation_or_call()]
    while True:
        if self._peek() == '.':
            self.position_in_program += 1
            # It is possible that a function is added and is not at the end.
            # The error for that will be raised by the ReferenceNode.
            components.append(
                self._parse_single_name_or_instantiation_or_call()
            )
        elif self._peek() == '[':
            self.position_in_program += 1
            components.append(
                self._parse_expression(has_semi_colon=False)
            )
            self._try_consume(']', needed=True)
        else:
            break
    return ReferenceNode(components, starting_position)


def parse_single_name_or_instantiation_or_call(self):
    starting_position = self.position_in_program
    try:
        return self._parse_instantiation_or_call()
    except UnderscoreIncorrectParserError:
        self.position_in_program = starting_position
        return self._parse_single_name()


@surrounding_whitespace_removed
def parse_instantiation_or_call(self):
    """
    This will return either a reference node, a template, or a function. These
    will be fed to a reference node which will work out what to do with them.
    """
    starting_position = self.position_in_program
    if self._peek(9) == 'template(' or self._peek(9) == 'function(':
        instantiation_or_call = self._parse_function_or_template()
    else:
        instantiation_or_call = ReferenceNode(
            [self._parse_single_name()],
            starting_position
        )
    try:
        expressions = self._parse_passable_expressions()
    except UnderscoreIncorrectParserError:
        self.position_in_program = starting_position
        raise
    return (instantiation_or_call, expressions)


@surrounding_whitespace_removed
def parse_passable_expressions(self, only_one_expression=False):
    try:
        self._try_consume('(')
    except UnderscoreCouldNotConsumeError:
        raise UnderscoreIncorrectParserError
    expressions = []
    # The while loop has to run twice even if only_one_expression == False, so
    # that the closing ')' is consumed. The case in which there is not closing
    # ')' will be handled in the try/except statement handling its consumption.
    while (
            self._peek() is not None
            and (
                only_one_expression == False
                or len(expressions) <= 1
            )
    ):
        self._consume_whitespace()

        try:
            self._try_consume(')')
        except UnderscoreCouldNotConsumeError:
            if only_one_expression and len(expressions) >= 1:
                raise UnderscoreSyntaxError(
                    'Expected \')\', got {}'.format(self._peek()),
                    self.position_in_program
                )
        else:
            break

        try:
            expressions.append(self._parse_expression(has_semi_colon=False))
        except UnderscoreIncorrectParserError:
            raise UnderscoreSyntaxError(
                'Expected name, got {}'.format(self._peek()),
                self.position_in_program
            )
        else:
            self._consume_whitespace()
            if self._peek() != ')':
                self._try_consume(',', needed=True)

    if self._peek() is None:
        raise UnderscoreSyntaxError('Expected \')\' got end of file')

    return expressions
