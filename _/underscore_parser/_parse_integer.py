from _ import nodes
from ._surrounding_whitespace_removed import _surrounding_whitespace_removed

@_surrounding_whitespace_removed
def _parse_integer(self):
    return nodes.ValueNode(int(self._parse_digits(consume_sign=True)))
