from _ import nodes
from _ import exceptions
from ._whitespace import surrounding_whitespace_removed


@surrounding_whitespace_removed
def parse_boolean_expression(self):
    return self._parse_boolean_statement()


@surrounding_whitespace_removed
def parse_boolean_statement(self):
    first_expression = self._parse_expression(
        has_semi_colon=False,
        parsers_to_not_allow=[self._parse_boolean_expression]
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
        except exceptions.UnderscoreCouldNotConsumeError:
            continue
        else:
            self._consume_whitespace()
            second_expression = self._parse_expression(
                has_semi_colon=False,
                parsers_to_not_allow=[self._parse_boolean_expression]
            )
            return node(first_expression, second_expression)
    raise exceptions.UnderscoreIncorrectParserError
