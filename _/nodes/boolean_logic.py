from .underscore_node import UnderscoreNode
from .limited import limited


class BooleanLogicNode(UnderscoreNode):
    FIRST_PARSER = '_parse_expression'


class AndOrOrNode(BooleanLogicNode):
    SECOND_PARSER = '_parse_and_or_or'

    def __init__(self, is_and, first_expression, second_expression):
        self.is_and = is_and
        self.first_expression = first_expression
        self.second_expression = second_expression

    def __str__(self):
        return (
            str(self.first_expression) +
            ' AND ' +
            str(self.second_expression)
        )

    @limited
    def run(self, *args, **kwargs):
        self.first_value = self.first_expression.run(*args, **kwargs)
        self.second_value = self.second_expression.run(*args, **kwargs)
        if self.is_and:
            return self.first_value and self.second_value
        return self.first_value or self.second_value\


class NotNode(BooleanLogicNode):
    SECOND_PARSER = '_parse_not'

    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return 'NOT ' + str(self.expression)

    @limited
    def run(self, *args, **kwargs):
        return not self.expression.run(*args, **kwargs)


class BooleanStatementNode(BooleanLogicNode):
    SECOND_PARSER = '_parse_comparison'

    def __init__(self, first_object, second_object):
        self.first_object = first_object
        self.second_object = second_object

    def __str__(self):
        return str(self.first_object) + self.SYMBOL + str(self.second_object)

    def _assign_values(self, *args, **kwargs):
        self.first_value = self.first_object.run(*args, **kwargs)
        self.second_value = self.second_object.run(*args, **kwargs)



class EqualityNode(BooleanStatementNode):
    SYMBOL = ' == '

    @limited
    def run(self, *args, **kwargs):
        self._assign_values(*args, **kwargs)
        try:
            return self.first_value == self.second_value
        except:
            raise _.exceptions.UnderscoreTypeError(
                'Could not compare {} and {}.'.format(
                    self.first_value,
                    self.second_value
                )
            )


class SmallerThanOrEqualToNode(BooleanStatementNode):
    SYMBOL = ' <= '

    @limited
    def run(self, *args, **kwargs):
        self._assign_values(*args, **kwargs)
        try:
            return self.first_value <= self.second_value
        except:
            raise _.exceptions.UnderscoreTypeError(
                'Could not compare {} and {}.'.format(
                    self.first_value,
                    self.second_value
                )
            )


class SmallerThanNode(BooleanStatementNode):
    SYMBOL = ' < '

    @limited
    def run(self, *args, **kwargs):
        self._assign_values(*args, **kwargs)
        try:
            return self.first_value < self.second_value
        except:
            raise _.exceptions.UnderscoreTypeError(
                'Could not compare {} and {}.'.format(
                    self.first_value,
                    self.second_value
                )
            )


class GreaterThanOrEqualToNode(BooleanStatementNode):
    SYMBOL = ' >= '

    @limited
    def run(self, *args, **kwargs):
        self._assign_values(*args, **kwargs)
        try:
            return self.first_value >= self.second_value
        except:
            raise _.exceptions.UnderscoreTypeError(
                'Could not compare {} and {}.'.format(
                    self.first_value,
                    self.second_value
                )
            )


class GreaterThanNode(BooleanStatementNode):
    SYMBOL = ' > '

    @limited
    def run(self, *args, **kwargs):
        self._assign_values(*args, **kwargs)
        try:
            return self.first_value > self.second_value
        except:
            raise _.exceptions.UnderscoreTypeError(
                'Could not compare {} and {}.'.format(
                    self.first_value,
                    self.second_value
                )
            )


class InequalityNode(BooleanStatementNode):
    SYMBOL = ' != '

    @limited
    def run(self, *args, **kwargs):
        self._assign_values(*args, **kwargs)
        try:
            return self.first_value != self.second_value
        except:
            raise _.exceptions.UnderscoreTypeError(
                'Could not compare {} and {}.'.format(
                    self.first_value,
                    self.second_value
                )
            )
