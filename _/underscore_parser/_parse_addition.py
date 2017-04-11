from _ import nodes
from ._surrounding_whitespace_removed import _surrounding_whitespace_removed

@_surrounding_whitespace_removed
def _parse_addition(self):
    first_term = self._parse_term()
    self._try_consume('+', needed_for_this=True)
    second_term = self._parse_term()
    return nodes.AdditionNode(first_term, second_term)
