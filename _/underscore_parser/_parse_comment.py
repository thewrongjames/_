from _.nodes import CommentNode
from _.exceptions import UnderscoreSyntaxError
from ._whitespace import surrounding_whitespace_removed


@surrounding_whitespace_removed
def parse_comment(self):
    self._try_consume('#', needed_for_this=True)
    while self._peek() is not None and self._peek() != '#':
        self.position_in_program += 1
    if self._peek() is None:
        raise UnderscoreSyntaxError('expected \'#\' got end of file')
    # if self._peek() is not None, then self._peek() must be '#', so consume that.
    self.position_in_program += 1
    return CommentNode()
