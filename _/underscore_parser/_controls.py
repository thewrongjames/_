from _ import exceptions
from ._whitespace import surrounding_whitespace_removed


@surrounding_whitespace_removed
def parse_control(self):
    # Assign the parsers that may make up the control.
    valid_parsers = [self._parse_if, self._parse_while]

    control = self._try_parsers(valid_parsers, 'control')

    if self._peek() != ';':
        # The control must be followed by a semi colon.
        raise exceptions.UnderscoreSyntaxError(
            "expected ';', got {}".format(
                self._peek() if self._peek() is not None else 'end of file',
            ),
            self.position_in_program,
        )
    # Consume the semi colon:
    self.position_in_program += 1

    return control


def parse_if(self):
    raise exceptions.UnderscoreNotImplementedError


def parse_while(self):
    raise exceptions.UnderscoreNotImplementedError
