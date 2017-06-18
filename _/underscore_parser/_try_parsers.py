from ..exceptions import UnderscoreIncorrectParserError, UnderscoreSyntaxError


def try_parsers(self, parsers, expected=None, needed=False, item_to_pass=None):
    # If there is no value given to expected, this can silently return None.
    starting_position = self.position_in_program
    one_worked = False
    if expected is not None:
        if needed:
            none_worked_error = UnderscoreSyntaxError(
                'expected {}'.format(expected),
                starting_position
            )
        else:
            none_worked_error = UnderscoreIncorrectParserError()
    else:
        none_worked_error = None

    for parser in parsers:
        try:
            if item_to_pass is not None:
                return parser(item_to_pass)
            else:
                return parser()
        except UnderscoreIncorrectParserError:
            self.position_in_program = starting_position
        else:
            one_worked = True
            break

    if not one_worked and none_worked_error is not None:
        raise none_worked_error
