from ._surrounding_whitespace_removed import _surrounding_whitespace_removed

@_surrounding_whitespace_removed
def _parse_term(self):
    valid_parsers = [
        self._parse_multiplication,
        self._parse_division,
        self._parse_non_expandable_term,
    ]
    return self._try_parsers(valid_parsers, 'term')
