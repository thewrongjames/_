from _ import nodes
from _ import exceptions
from .whitespace import _surrounding_whitespace_removed

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
