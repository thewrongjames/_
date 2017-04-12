from _ import nodes
from _ import exceptions
from ._whitespace import surrounding_whitespace_removed


@surrounding_whitespace_removed
def parse_function(self):
    try:
        self._try_consume('function')
    except exceptions.UnderscoreCouldNotConsumeError:
        raise exceptions.UnderscoreIncorrectParserError()
    names = self._parse_passable_names()
    # The above line may error, but, that is okay. Until you are past that line,
    # you do not know that you are definately in a template, and not in, say, a
    # name or reference that begins with 'template'
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
        returns = self._parse_expression(has_semi_colon=False)
        self._try_consume(')', needed=True)
        self._consume_whitespace()
        self._try_consume(';', needed=True)
        self._consume_whitespace()
    self._try_consume('}', needed=True)
    return nodes.TemplateFunctionNode(sections, returns, names)


@surrounding_whitespace_removed
def parse_template(self):
    try:
        self._try_consume('template')
    except exceptions.UnderscoreCouldNotConsumeError:
        raise exceptions.UnderscoreIncorrectParserError()
    names = self._parse_passable_names()
    # The above line may error, but, that is okay. Until you are past that line,
    # you do not know that you are definately in a template, and not in, say, a
    # name or reference that begins with 'template'
    self._try_consume('{', needed=True)
    self._consume_whitespace()
    sections = self._parse_sections(['}'])
    self._try_consume('}', needed=True)
    return nodes.TemplateFunctionNode(sections, None, names)


@surrounding_whitespace_removed
def parse_passable_names(self):
    try:
        self._try_consume('(')
    except exceptions.UnderscoreCouldNotConsumeError:
        raise exceptions.UnderscoreIncorrectParserError
    names = []
    while self._peek() is not None:
        self._consume_whitespace()

        try:
            self._try_consume(')')
        except exceptions.UnderscoreCouldNotConsumeError:
            pass
        else:
            break

        try:
            names.append(self._parse_single_name())
        except exceptions.UnderscoreIncorrectParserError:
            raise exceptions.UnderscoreSyntaxError(
                'Expected name, got {}'.format(self.peek())
            )
        else:
            self._consume_whitespace()
            if self._peek() != ')':
                self._try_consume(',', needed=True)

    if self._peek() is None:
        raise exceptions.UnderscoreSyntaxError('Expected \')\' got end of file')

    return names
