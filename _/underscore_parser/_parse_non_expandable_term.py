from ._surrounding_whitespace_removed import _surrounding_whitespace_removed

@_surrounding_whitespace_removed
def _parse_non_expandable_term(self):
    valid_parsers = [
        self._parse_object,
        self._parse_bracketed_expression,
    ]
    return self._try_parsers(valid_parsers, 'non expandable term')
