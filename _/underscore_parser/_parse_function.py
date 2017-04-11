from _ import nodes
from _ import exceptions
from ._surrounding_whitespace_removed import _surrounding_whitespace_removed

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
        returns = self._parse_expression(has_semi_colon=False)
        self._try_consume(')', needed=True)
        self._consume_whitespace()
        self._try_consume(';', needed=True)
        self._consume_whitespace()
    self._try_consume('}', needed=True)
    return nodes.TemplateFunctionNode(sections, returns)
