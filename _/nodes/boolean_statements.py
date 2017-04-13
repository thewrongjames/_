from .underscore_node import UnderscoreNode


class BooleanStatementNode(UnderscoreNode):
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
