from _ import exceptions
from ._whitespace import surrounding_whitespace_removed


@surrounding_whitespace_removed
def parse_control(self):
    raise exceptions.UnderscoreNotImplementedError
