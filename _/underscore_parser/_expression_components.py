from ..Nodes import NotNode
from ._whitespace import surrounding_whitespace_removed


@surrounding_whitespace_removed
def parse_not(self):
    self._try_consume('NOT', needed_for_this=True)
    item = self._parse_object_or_contained_expression()
    return NotNode(item)


@surrounding_whitespace_removed
def parse_bracketed_expression(self):
    self._try_consume('(', needed_for_this=True)
    expression = self._parse_expression(has_semi_colon=False)
    self._try_consume(')', needed_for_this=True)
    return expression


@surrounding_whitespace_removed
def parse_object_or_contained_expression(self):
    valid_parsers = [
        self._parse_bracketed_expression,
        self._parse_object,
    ]
    value = self._try_parsers(valid_parsers, 'object or contained expression')
    return value
