from _ import nodes
from _.exceptions import UnderscoreCouldNotConsumeError, \
    UnderscoreIncorrectParserError
from ._whitespace import surrounding_whitespace_removed


@surrounding_whitespace_removed
def parse_and_or_or(self):
    first_expression = self._parse_expression(
        has_semi_colon=False,
        parsers_to_not_allow=[self._parse_and_or_or]
    )
    self._consume_whitespace()
    try:
        self._try_consume('AND')
    except UnderscoreCouldNotConsumeError:
        self._try_consume('OR', needed_for_this=True)
        is_and = False
    else:
        is_and = True
    second_expression = self._parse_expression(has_semi_colon=False)
    return nodes.AndOrOrNode(is_and, first_expression, second_expression)


@surrounding_whitespace_removed
def parse_not(self):
    self._try_consume('NOT', needed_for_this=True)
    expression = self._parse_expression(
        has_semi_colon=False,
        parsers_to_not_allow=[self._parse_and_or_or]
    )
    return nodes.NotNode(expression)


@surrounding_whitespace_removed
def parse_comparison(self):
    parsers_to_not_allow=[
        self._parse_and_or_or,
        self._parse_not,
        self._parse_comparison
    ]
    first_expression = self._parse_expression(
        has_semi_colon=False,
        parsers_to_not_allow=parsers_to_not_allow
    )
    symbols_and_nodes = (
        ('==', nodes.EqualityNode),
        ('<=', nodes.SmallerThanOrEqualToNode),
        ('<', nodes.SmallerThanNode),
        ('>=', nodes.GreaterThanOrEqualToNode),
        ('>', nodes.GreaterThanNode),
        ('!=', nodes.InequalityNode)
    )
    for symbol, node in symbols_and_nodes:
        self._consume_whitespace()
        try:
            self._try_consume(symbol)
        except UnderscoreCouldNotConsumeError:
            continue
        else:
            self._consume_whitespace()
            second_expression = self._parse_expression(
                has_semi_colon=False,
                parsers_to_not_allow=parsers_to_not_allow
            )
            return node(first_expression, second_expression)
    raise UnderscoreIncorrectParserError
