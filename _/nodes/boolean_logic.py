from .underscore_node import UnderscoreNode


class BooleanLogicNode(UnderscoreNode):
    FIRST_PARSER = '_parse_expression'


class AndOrOrNode(BooleanLogicNode):
    SECOND_PARSER = '_parse_and_or_or'

    def __init__(self, is_and, first_expression, second_expression):
        self.is_and = is_and
        self.first_expression = first_expression
        self.second_expression = second_expression

    def run(self, memory, *args, **kwargs):
        first_value = self.first_expression.run(memory)
        second_value = self.second_expression.run(memory)
        if self.is_and:
            return first_value and second_value
        return first_value or second_value\


class NotNode(BooleanLogicNode):
    SECOND_PARSER = '_parse_not'

    def __init__(self, expression):
        self.expression = expression

    def run(self, memory, *args, **kwargs):
        return not self.expression.run(memory)


class BooleanStatementNode(BooleanLogicNode):
    SECOND_PARSER = '_parse_comparison'

    def __init__(self, first_object, second_object):
        self.first_object = first_object
        self.second_object = second_object


class EqualityNode(BooleanStatementNode):
    def run(self, memory, *args, **kwargs):
        first_value = self.first_object.run(memory)
        second_value = self.second_object.run(memory)
        try:
            return first_value == second_value
        except:
            raise _.exceptions.UnderscoreTypeError(
                'Could not compare {} and {}.'.format(
                    first_value,
                    second_value
                )
            )


class SmallerThanOrEqualToNode(BooleanStatementNode):
    def run(self, memory, *args, **kwargs):
        first_value = self.first_object.run(memory)
        second_value = self.second_object.run(memory)
        try:
            return first_value <= second_value
        except:
            raise _.exceptions.UnderscoreTypeError(
                'Could not compare {} and {}.'.format(
                    first_value,
                    second_value
                )
            )


class SmallerThanNode(BooleanStatementNode):
    def run(self, memory, *args, **kwargs):
        first_value = self.first_object.run(memory)
        second_value = self.second_object.run(memory)
        try:
            return first_value < second_value
        except:
            raise _.exceptions.UnderscoreTypeError(
                'Could not compare {} and {}.'.format(
                    first_value,
                    second_value
                )
            )


class GreaterThanOrEqualToNode(BooleanStatementNode):
    def run(self, memory, *args, **kwargs):
        first_value = self.first_object.run(memory)
        second_value = self.second_object.run(memory)
        try:
            return first_value >= second_value
        except:
            raise _.exceptions.UnderscoreTypeError(
                'Could not compare {} and {}.'.format(
                    first_value,
                    second_value
                )
            )


class GreaterThanNode(BooleanStatementNode):
    def run(self, memory, *args, **kwargs):
        first_value = self.first_object.run(memory)
        second_value = self.second_object.run(memory)
        try:
            return first_value > second_value
        except:
            raise _.exceptions.UnderscoreTypeError(
                'Could not compare {} and {}.'.format(
                    first_value,
                    second_value
                )
            )


class InequalityNode(BooleanStatementNode):
    def run(self, memory, *args, **kwargs):
        first_value = self.first_object.run(memory)
        second_value = self.second_object.run(memory)
        try:
            return first_value != second_value
        except:
            raise _.exceptions.UnderscoreTypeError(
                'Could not compare {} and {}.'.format(
                    first_value,
                    second_value
                )
            )
