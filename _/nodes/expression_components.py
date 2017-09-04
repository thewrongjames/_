from ..exceptions import UnderscoreTypeError
from .underscore_node import UnderscoreNode
from .value_node import ValueNode
from .limited import limited


class OperatorNode(UnderscoreNode):
    SYMBOL_DATA = {
        'AND': {
            'python_method_name': '__and__',
            'magic_method_name': '__and',
            'verb': 'boolean and',
            'preposition': 'and'
        },
        'OR': {
            'python_method_name': '__or__',
            'magic_method_name': '__or',
            'verb': 'boolean or',
            'preposition': 'and'
        },
        '==': {
            'python_method_name': '__eq__',
            'magic_method_name': '__equal',
            'verb': 'check if',
            'preposition': 'is equal to'
        },
        '<=': {
            'python_method_name': '__le__',
            'magic_method_name': '__less_than_or_equal_to',
            'verb': 'check if',
            'preposition': 'is less than or equal to'
        },
        '<': {
            'python_method_name': '__lt__',
            'magic_method_name': '__less_than',
            'verb': 'check if',
            'preposition': 'is less than'
        },
        '>=': {
            'python_method_name': '__ge__',
            'magic_method_name': '__greater_than_or_equal_to',
            'verb': 'check if',
            'preposition': 'is greater than or equal to'
        },
        '>': {
            'python_method_name': '__gt__',
            'magic_method_name': '__greater_than',
            'verb': 'check if',
            'preposition': 'is greater than'
        },
        '!=': {
            'python_method_name': '__ne__',
            'magic_method_name': '__not_equal_to',
            'verb': 'check if',
            'preposition': 'is not equal to'
        },
        '+': {
            'python_method_name': '__add__',
            'magic_method_name': '__addition',
            'verb': 'add',
            'preposition': 'to'
        },
        '-': {
            'python_method_name': '__sub__',
            'magic_method_name': '__subtraction',
            'verb': 'subtract',
            'preposition': 'from'
        },
        '*': {
            'python_method_name': '__mul__',
            'magic_method_name': '__multiplication',
            'verb': 'multiply',
            'preposition': 'by'
        },
        '/': {
            'python_method_name': '__truediv__',
            'magic_method_name': '__division',
            'verb': 'divide',
            'preposition': 'by'
        },
        '^': {
            'python_method_name': '__pow__',
            'magic_method_name': '__power',
            'verb': 'raise',
            'preposition': 'to'
        }
    }

    def __init__(self, first_item, second_item, symbol):
        self.first_item = first_item
        self.second_item = second_item
        self.symbol = symbol

    def __str__(self):
        return str(self.first_item) + self.symbol + str(self.second_item)

    @limited
    def run(self, memory, *args, **kwargs):
        # This could be cleaned up by making everything templates. Somehow.
        first_value = self.first_item.run(memory, *args, **kwargs)
        second_value = self.second_item.run(memory, *args, **kwargs)
        try:
            return getattr(
                first_value,
                self.SYMBOL_DATA[self.symbol]['python_method_name']
            )(second_value)
        except (TypeError, AttributeError):
            return self._try_magic_methods(first_value, second_value)

    def _try_magic_methods(self, first_value, second_value):
        verb = self.SYMBOL_DATA[self.symbol]['verb']
        preposition = self.SYMBOL_DATA[self.symbol]['preposition']
        magic_method_name = self.SYMBOL_DATA[self.symbol]['magic_method_name']

        could_not_perform_operation_error = UnderscoreTypeError(
            'could not {} {} {} {}, as the operation is not defined'.format(
                verb,
                self.first_item,
                preposition,
                self.second_item
            )
        )
        if (
                not isinstance(first_value, dict) and
                not isinstance(second_value, dict)
        ):
            # If neither of the values were template instances, there are no
            # magic methods to call.
            raise could_not_perform_operation_error
        try:
            return first_value[magic_method_name]({}, [ValueNode(\
                second_value), ValueNode(False)])
        except (TypeError, KeyError):
            try:
                return second_value[magic_method_name]({}, [ValueNode(\
                    first_value), ValueNode(True)])
            except KeyError:
                raise could_not_perform_operation_error
            except TypeError:
                if isinstance(second_value, dict):
                    raise UnderscoreTypeError(
                        'incorrectly defined {} method (it must take two '
                        'arguments)'.format(magic_method_name)
                    )
                raise could_not_perform_operation_error


class NotNode(UnderscoreNode):
    def __init__(self, item):
        self.item = item

    def __str__(self):
        return 'NOT ' + str(self.item)

    @limited
    def run(self, *args, **kwargs):
        # Pretty sure python not works on everything. All the basic types that
        # this can be running on at least. But, this too could be improved by
        # having everything be templates.
        return not self.item.run(*args, **kwargs)
