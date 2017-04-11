from ._surrounding_whitespace_removed import _surrounding_whitespace_removed

@_surrounding_whitespace_removed
def _parse_boolean_expression(self):
    return self._parse_boolean_statement()
