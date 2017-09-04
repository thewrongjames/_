from ..exceptions import UnderscoreSyntaxError, UnderscoreIncorrectParserError
from ..nodes import OperatorNode
from ._whitespace import surrounding_whitespace_removed


@surrounding_whitespace_removed
def parse_expression(
        self,
        has_semi_colon=True,
):
    """
    Parses an expression (see grammar for details). An expression consists
    of one of various other parsers, sometimes followed by a semi colon,
    (indicated by the has_semi_colon flag).
    """

    # Try to parse a not.
    starting_position = self.position_in_program
    try:
        expression = self._parse_not()
    except UnderscoreIncorrectParserError:
        self.position_in_program = starting_position
    else:
        maybe_consume_semi_colon(self, has_semi_colon)
        return expression

    # Otherwise, try to parse anything else.
    first_item = self._parse_object_or_contained_expression()

    operator_symbol = None
    for symbol_to_check in self.OPERATOR_SYMBOLS:
        if self._peek(len(symbol_to_check)) == symbol_to_check:
            operator_symbol = symbol_to_check
            break

    if operator_symbol is not None:
        self.position_in_program += len(operator_symbol)

        try:
            second_item = self._parse_object_or_contained_expression()
        except UnderscoreIncorrectParserError:
            raise UnderscoreSyntaxError(
                'expected object or contained expression after ' + \
                    operator_symbol,
                self.position_in_program
            )

        expression = OperatorNode(first_item, second_item, operator_symbol)
    else:
        expression = first_item

    maybe_consume_semi_colon(self, has_semi_colon)

    return expression


def maybe_consume_semi_colon(parser, consume_semi_colon):
    if parser._peek() != ';' and consume_semi_colon:
        raise UnderscoreSyntaxError(
            "expected ';', got {}".format(
                parser._peek() if parser._peek() is not None else 'end of file',
            ),
            parser.position_in_program,
        )
    # If it should have a semi colon, it is consumed here.
    if parser._peek() == ';' and consume_semi_colon:
        parser.position_in_program += 1
