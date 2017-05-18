from _.exceptions import UnderscoreTypeError
from .underscore_node import UnderscoreNode
from .value_node import ValueNode


class MathsNode(UnderscoreNode):
    def __init__(self, first_term, second_term):
        self.first_term = first_term
        self.second_term = second_term

    def run(self, memory, *args, **kwargs):
        first_value = self.first_term.run(memory)
        second_value = self.second_term.run(memory)
        return self._specific_maths(first_value, second_value)

    def _try_magic_methods(self, first_value, second_value):
        could_not_add_error = UnderscoreTypeError(
            'could not {} {} {} {}'.format(
                self.VERB,
                self.first_term,
                self.PREPOSITION,
                self.second_term
            )
        )
        if (
                not isinstance(first_value, dict) and
                not isinstance(second_value, dict)
        ):
            # If neither of the values were template instances, there are no
            # magic methods to call.
            raise could_not_add_error
        try:
            return first_value[self.MAGIC_METHOD_NAME]({}, [ValueNode(\
                second_value), ValueNode(False)])
        except (TypeError, KeyError):
            try:
                return second_value[self.MAGIC_METHOD_NAME]({}, [ValueNode(\
                    first_value), ValueNode(True)])
            except KeyError:
                raise could_not_add_error
            except TypeError:
                if isinstance(second_value, dict):
                    raise UnderscoreTypeError(
                        'incorrectly defined {} method (it must take two '
                        'arguments)'.format(self.MAGIC_METHOD_NAME)
                    )
                raise could_not_add_error


class AdditionNode(MathsNode):
    MAGIC_METHOD_NAME = '__addition'
    VERB = 'add'
    PREPOSITION = 'to'

    def _specific_maths(self, first_value, second_value):
        try:
            return first_value + second_value
        except TypeError:
            return self._try_magic_methods(first_value, second_value)


class SubtractionNode(MathsNode):
    MAGIC_METHOD_NAME = '__subtraction'
    VERB = 'subtract'
    PREPOSITION = 'from'

    def _specific_maths(self, first_value, second_value):
        try:
            return first_value - second_value
        except TypeError:
            return self._try_magic_methods(first_value, second_value)


class MultiplicationNode(MathsNode):
    MAGIC_METHOD_NAME = '__multiplication'
    VERB = 'multiply'
    PREPOSITION = 'by'

    def _specific_maths(self, first_value, second_value):
        try:
            return first_value * second_value
        except TypeError:
            return self._try_magic_methods(first_value, second_value)


class DivisionNode(MathsNode):
    MAGIC_METHOD_NAME = '__division'
    VERB = 'divide'
    PREPOSITION = 'by'

    def _specific_maths(self, first_value, second_value):
        try:
            return first_value / second_value
        except TypeError:
            return self._try_magic_methods(first_value, second_value)

class PowerNode(MathsNode):
    MAGIC_METHOD_NAME = '__power'
    VERB = 'raise'
    PREPOSITION = 'to'

    def _specific_maths(self, first_value, second_value):
        try:
            return first_value ** second_value
        except TypeError:
            return self._try_magic_methods(first_value, second_value)
