from _ import nodes
from ._surrounding_whitespace_removed import _surrounding_whitespace_removed

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
