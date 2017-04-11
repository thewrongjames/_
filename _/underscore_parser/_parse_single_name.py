from _ import exceptions
from ._surrounding_whitespace_removed import _surrounding_whitespace_removed
from . import constants

@_surrounding_whitespace_removed
def _parse_single_name(self):
    name = ''

    if self._peek() is None or self._peek() not in \
            constants.VALID_NAME_FIRST_CHARACTER_CHARACTERS:
        raise exceptions.UnderscoreIncorrectParserError(
            'expected one of {}, got {}'.format(
                constants.VALID_NAME_FIRST_CHARACTER_CHARACTERS,
                self._peek() if self._peek() is not None else 'end of file',
            ),
            self.position_in_program,
        )
    # As constants.VALID_NAME_FIRST_CHARACTER_CHARACTERS is a subset
    # of constants.VALID_NAME_NON_FIRST_CHARACTER_CHARACTERS, we can
    # now move straight on to taking any non first character character,
    # because that will also take the first character.
    while self._peek() is not None and self._peek() in \
            constants.VALID_NAME_NON_FIRST_CHARACTER_CHARACTERS:
        name += self._peek()
        self._next()
    if name in self.RESERVED_NAMES:
        raise exceptions.UnderscoreIncorrectParserError(
            'name was in reserved words'
        )
    return name
