from _ import nodes
from _ import exceptions
from ._surrounding_whitespace_removed import _surrounding_whitespace_removed

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
