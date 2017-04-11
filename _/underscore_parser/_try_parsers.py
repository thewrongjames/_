from _ import exceptions


def _try_parsers(self, parsers, expected=None, needed=False):
    # If there is no value given to expected, this can silently return None.
    starting_position = self.position_in_program
    one_worked = False
    if expected is not None:
        if needed:
            none_worked_error = exceptions.UnderscoreSyntaxError(
                'expected {}'.format(expected),
                starting_position
            )
        else:
            none_worked_error = exceptions.UnderscoreIncorrectParserError()
    else:
        none_worked_error = None

    for parser in parsers:
        try:
            return parser()
        except exceptions.UnderscoreIncorrectParserError:
            self.position_in_program = starting_position
        else:
            one_worked = True
            break

    if not one_worked and none_worked_error is not None:
        raise none_worked_error
