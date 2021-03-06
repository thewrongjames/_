from ..nodes import TemplateFunctionNode
from ..exceptions import UnderscoreCouldNotConsumeError, \
    UnderscoreIncorrectParserError, UnderscoreSyntaxError
from ._whitespace import surrounding_whitespace_removed


@surrounding_whitespace_removed
def parse_function_or_template(self, next_parsers_to_try_first):
    try:
        self._try_consume('function')
    except UnderscoreCouldNotConsumeError:
        self._try_consume('template', needed_for_this=True)
        is_function = False
    else:
        is_function = True
    names = self._parse_passable_names()
    # The above line may error, but, that is okay. Until you are past that line,
    # you do not know that you are definately in a template or function, and not
    # in, say, a name or reference that begins with 'template'.
    self._try_consume('{', needed=True)
    self._consume_whitespace()
    # If it is a function, you need to allow for parsing return.
    sections = self._parse_sections(
        ['}'],
        parsers_to_try_first=next_parsers_to_try_first
    )
    self._try_consume('}', needed=True)
    return TemplateFunctionNode(sections, is_function, names)


@surrounding_whitespace_removed
def parse_passable_names(self):
    self._try_consume('(', needed_for_this=True)
    names = []
    while self._peek() is not None:
        self._consume_whitespace()

        try:
            self._try_consume(')')
        except UnderscoreCouldNotConsumeError:
            pass
        else:
            break

        try:
            names.append(self._parse_single_name())
        except UnderscoreIncorrectParserError:
            raise UnderscoreSyntaxError(
                'expected name, got {}'.format(self.peek())
            )
        else:
            self._consume_whitespace()
            if self._peek() != ')':
                self._try_consume(',', needed=True)

    if self._peek() is None:
        raise UnderscoreSyntaxError('expected \')\', got end of file')

    return names
