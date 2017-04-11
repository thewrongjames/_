from ._surrounding_whitespace_removed import _surrounding_whitespace_removed

@_surrounding_whitespace_removed
def _parse_object(self):
    valid_parsers = [
        self._parse_float,
        self._parse_integer,
        self._parse_boolean,
        self._parse_string,
        self._parse_none,
        self._parse_reference,
        self._parse_template,
        self._parse_function,
    ]
    return self._try_parsers(valid_parsers, 'object')
