from ..exceptions import UnderscoreSyntaxError, UnderscoreIncorrectParserError
from ._whitespace import surrounding_whitespace_removed


@surrounding_whitespace_removed
def parse_expression(
        self,
        has_semi_colon=True,
        parsers_to_not_allow=[],
        second_parser=None,
        next_parsers_to_try_first=[]
):
    """
    Parses an expression (see grammar for details). An expression consists
    of one of various other parsers, sometimes followed by a semi colon,
    (indicated by the has_semi_colon flag). Any parsers included in the
    parsers_to_not_allow list will not be permitted to be parsed as part of the
    expression.
    """
    # Assign the parsers that may make up the expression.
    valid_parsers = [
        self._parse_and_or_or,
        self._parse_not,
        self._parse_comparison,
        self._parse_addition_or_subtraction,
        self._parse_term,
    ]

    # Remove any parsers not to be included...
    try:
        for parser_to_remove in parsers_to_not_allow:
            try:
                valid_parsers.remove(parser_to_remove)
            except ValueError:
                continue
    except TypeError:
        raise TypeError('parser_to_not_allow must be iterable.')

    # Try the second parser from the previous compiled version.
    parsed_already = False
    if second_parser is not None:
        try:
            expression = second_parser(next_parsers_to_try_first)
        except (UnderscoreIncorrectParserError, UnderscoreSyntaxError):
            pass
        else:
            parsed_already = True

    # If that doesn't work:
    if not parsed_already:
        expression = self._try_parsers(
            valid_parsers,
            'expression',
            item_to_pass=next_parsers_to_try_first
        )

    if self._peek() != ';' and has_semi_colon:
        raise UnderscoreSyntaxError(
            "expected ';', got {}".format(
                self._peek() if self._peek() is not None else 'end of file',
            ),
            self.position_in_program,
        )
    # If it should have a semi colon, it is consumed here.
    if self._peek() == ';' and has_semi_colon:
        self.position_in_program += 1
    return expression
