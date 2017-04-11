from _ import exceptions

def _try_consume(
        self,
        string_to_consume,
        needed=False,
        needed_for_this=False
):
    starting_position = self.position_in_program
    string_read = ''
    for character in string_to_consume:
        string_read += self._peek() if self._peek() is not None else ''
        if self._peek() != character:
            self.position_in_program = starting_position
            if needed:
                raise exceptions.UnderscoreSyntaxError(
                    'expected {}, got {}'.format(
                        string_to_consume,
                        string_read if self._peek() is not None else \
                            'end of file'
                    ),
                    starting_position
                )
            if needed_for_this:
                raise exceptions.UnderscoreIncorrectParserError
            raise exceptions.UnderscoreCouldNotConsumeError(
                'could not consume',
                string_to_consume
            )
        self.position_in_program += 1
