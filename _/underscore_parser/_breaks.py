from ..nodes import ReturnNode, BreakNode, ContinueNode
from ..exceptions import UnderscoreCouldNotConsumeError
from ._whitespace import surrounding_whitespace_removed


@surrounding_whitespace_removed
def parse_return(self):
    self._try_consume('return', needed_for_this=True)
    self._consume_whitespace()
    self._try_consume('(', needed=True)
    expression_to_return = self._parse_expression(has_semi_colon=False)
    self._try_consume(')', needed=True)
    self._consume_whitespace()
    self._try_consume(';', needed=True)
    return ReturnNode(expression_to_return, self.position_in_program)

@surrounding_whitespace_removed
def parse_break_or_continue(self):
    try:
        self._try_consume('break;')
    except UnderscoreCouldNotConsumeError:
        self._try_consume('continue;', needed_for_this=True)
        return ContinueNode(self.position_in_program)
    return BreakNode(self.position_in_program)
