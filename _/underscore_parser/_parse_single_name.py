from ..exceptions import UnderscoreIncorrectParserError
from ._whitespace import surrounding_whitespace_removed


@surrounding_whitespace_removed
def parse_single_name(self):
    name = ''

    if self._peek() is None or self._peek() not in \
            self.VALID_NAME_FIRST_CHARACTER_CHARACTERS:
        raise UnderscoreIncorrectParserError(
            'expected one of {}, got {}'.format(
                self.VALID_NAME_FIRST_CHARACTER_CHARACTERS,
                self._peek() if self._peek() is not None else 'end of file',
            ),
            self.position_in_program,
        )
    # As self.VALID_NAME_FIRST_CHARACTER_CHARACTERS is a subset of
    # self.VALID_NAME_NON_FIRST_CHARACTER_CHARACTERS, we can now move straight
    # on to taking any non first character character, because that will also
    # take the first character.
    while self._peek() is not None and self._peek() in \
            self.VALID_NAME_NON_FIRST_CHARACTER_CHARACTERS:
        name += self._peek()
        self.position_in_program += 1
    if name in self.RESERVED_NAMES:
        # If the name is reserved, it is not a name. It is something like 'if'.
        raise UnderscoreIncorrectParserError()
    return name
