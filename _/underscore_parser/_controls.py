from _.nodes import IfNode, WhileNode
from _.exceptions import UnderscoreSyntaxError, UnderscoreCouldNotConsumeError
from ._whitespace import SurroundingWhitespaceRemover


@SurroundingWhitespaceRemover()
def parse_control(self):
    # Assign the parsers that may make up the control.
    valid_parsers = [self._parse_if, self._parse_while]

    control = self._try_parsers(valid_parsers, 'control')
    self._consume_whitespace()

    if self._peek() != ';':
        # The control must be followed by a semi colon.
        raise UnderscoreSyntaxError(
            "expected ';', got {}".format(
                self._peek() if self._peek() is not None else 'end of file',
            ),
            self.position_in_program,
        )
    # Consume the semi colon:
    self.position_in_program += 1

    return control


def parse_if(self):
    self._try_consume('if', needed_for_this=True)
    self._consume_whitespace()

    expression = self._parse_passable_expressions(only_one_expression=True)[0]

    self._try_consume('{', needed=True)
    self._consume_whitespace()
    if_sections = self._parse_sections(['}'])
    self._try_consume('}', needed=True)

    self._consume_whitespace()
    try:
        self._try_consume('else')
    except UnderscoreCouldNotConsumeError:
        else_sections = []
    else:
        self._consume_whitespace()
        self._try_consume('{', needed=True)
        self._consume_whitespace()
        else_sections = self._parse_sections(['}'])
        self._try_consume('}', needed=True)

    return IfNode(expression, if_sections, else_sections)


def parse_while(self):
    self._try_consume('while', needed_for_this=True)
    self._consume_whitespace()

    expression = self._parse_passable_expressions(only_one_expression=True)[0]

    self._try_consume('{', needed=True)
    self._consume_whitespace()
    sections = self._parse_sections(['}'])
    self._try_consume('}', needed=True)

    return WhileNode(expression, sections)
