from ..exceptions import UnderscoreSyntaxError, UnderscoreIncorrectParserError
from ..nodes import AdditionNode, SubtractionNode, MultiplicationNode, \
    DivisionNode, PowerNode
from ._whitespace import surrounding_whitespace_removed


def _get_item_parsers_to_exclude(self, parser_to_get_for):
    """
    Each of the parsers within an expression can parse anything beneath it in
    self.EXPRESSION_PARSERS as its first item, and, anything from it (inclusive)
    down as its second item.

    The exceptions are parse_power, which may
    parse_object_or_contained_expression for each of its items, and
    parse_object_or_contained_expression itself, which does not have a first or
    second item.

    This function takes the UnderscoreParser method, and returns the parsers it
    must exclude from parse_expression for its first item and its second item,
    in that order.
    """

    first_item_parsers_to_exclude = []
    second_item_parsers_to_exclude = []

    finished_seconds = False

    for parser in self.EXPRESSION_PARSERS:
        if parser == parser_to_get_for:
            first_item_parsers_to_exclude.append(parser)
            break

        first_item_parsers_to_exclude.append(parser)
        second_item_parsers_to_exclude.append(parser)

    if parser_to_get_for == self._parse_power:
        # For the power parsing (see above).
        first_item_parsers_to_exclude = self.EXPRESSION_PARSERS[:-1].copy()
        second_item_parsers_to_exclude = self.EXPRESSION_PARSERS[:-1].copy()

    return first_item_parsers_to_exclude, second_item_parsers_to_exclude


@surrounding_whitespace_removed
def parse_typical_sub_expression(self, symbol):
    """
    The parsing for most of the self.EXPRESSION_PARSERS is very similar, as such,
    they may all be a wrapper for this function, that just tells this function
    what symbol they use.
    """

    parser_and_node_of_symbol = {
        '+': (self._parse_addition, AdditionNode),
        '-': (self._parse_subtraction, SubtractionNode),
        '*': (self._parse_multiplication, MultiplicationNode),
        '/': (self._parse_division, DivisionNode),
        '^': (self._parse_power, PowerNode),
    }

    parser, node = parser_and_node_of_symbol[symbol]

    first_item_parsers_to_exclude, second_item_parsers_to_exclude = \
        _get_item_parsers_to_exclude(self, parser)

    first_item = self._parse_expression(
            has_semi_colon=False,
            parsers_to_not_allow=first_item_parsers_to_exclude
        )
    self._try_consume(symbol, needed_for_this=True)
    second_item = self._parse_expression(
            has_semi_colon=False,
            parsers_to_not_allow=second_item_parsers_to_exclude,
        )

    return node(first_item, second_item)


@surrounding_whitespace_removed
def parse_expression(
        self,
        has_semi_colon=True,
        parsers_to_not_allow=[],
        second_parser=None,
        next_parsers_to_try_first=[],
):
    """
    Parses an expression (see grammar for details). An expression consists
    of one of various other parsers, sometimes followed by a semi colon,
    (indicated by the has_semi_colon flag). Any parsers included in the
    parsers_to_not_allow list will not be permitted to be parsed as part of the
    expression.
    """

    # Remove any parsers not to be included...

    try:
        parsers_to_use = []
        for parser in self.EXPRESSION_PARSERS:
            if parser not in parsers_to_not_allow:
                parsers_to_use.append(parser)
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
            parsers_to_use,
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
