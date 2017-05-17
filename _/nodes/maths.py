from _.exceptions import UnderscoreTypeError
from .underscore_node import UnderscoreNode


class MathsNode(UnderscoreNode):
    def __init__(self, first_term, second_term):
        self.first_term = first_term
        self.second_term = second_term

    def run(self, memory, *args, **kwargs):
        first_value = self.first_term.run(memory)
        second_value = self.second_term.run(memory)
        return self.specific_maths(first_value, second_value)


class AdditionNode(MathsNode):
    def specific_maths(self, first_value, second_value):
        try:
            return first_value + second_value
        except TypeError:
            raise UnderscoreTypeError(
                'Could not add {} to {}.'.format(
                    first_value,
                    second_value
                )
            )


class SubtractionNode(MathsNode):
    def specific_maths(self, first_value, second_value):
        try:
            return first_value - second_value
        except TypeError:
            raise UnderscoreTypeError(
                'Could not subtract {} from {}.'.format(
                    second_value,
                    first_value
                )
            )


class MultiplicationNode(MathsNode):
    def specific_maths(self, first_value, second_value):
        try:
            return first_value * second_value
        except TypeError:
            raise UnderscoreTypeError(
                'Could not multiply {} by {}.'.format(
                    first_value,
                    second_value
                )
            )


class DivisionNode(MathsNode):
    def specific_maths(self, first_value, second_value):
        try:
            return first_value / second_value
        except TypeError:
            raise UnderscoreTypeError(
                'Could not divide {} by {}.'.format(
                    first_value,
                    second_value
                )
            )
