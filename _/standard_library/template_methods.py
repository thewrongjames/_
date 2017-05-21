from _.exceptions import UnderscoreTypeError
from _.nodes.value_node import ValueNode
from .constants import BASIC_TYPES


class Set:
    def __init__(self, memory):
        self.memory = memory

    def __str__(self, memory):
        return 'set_method'

    def __call__(self, memory_from_call_location, expressions=[]):
        if len(expressions) != 2:
            raise UnderscoreTypeError(
                '{} expressions passed, {} required'.format(
                    len(expressions),
                    2
                )
            )
        value_to_assign_to = expressions[0].run(memory_from_call_location)
        value_to_assign = expressions[1].run(memory_from_call_location)
        if type(value_to_assign_to) not in BASIC_TYPES:
            raise UnderscoreTypeError(
                'cannot set to non-basic type'
            )
        self.memory[value_to_assign_to] = value_to_assign

        return ValueNode(None)


class Get:
    def __init__(self, memory):
        self.memory = memory

    def __str__(self, memory):
        return 'get_method'

    def __call__(self, memory_from_call_location, expressions=[]):
        if len(expressions) != 1:
            raise UnderscoreTypeError(
                '{} expressions passed, {} required'.format(
                    len(expressions),
                    1
                )
            )
        value_to_get_from = expressions[0].run(memory_from_call_location)
        if type(value_to_get_from) not in BASIC_TYPES:
            raise UnderscoreTypeError(
                'cannot get from non-basic type'
            )

        try:
            return self.memory[value_to_get_from]
        except KeyError:
            raise UnderscoreNameError(
                '{} is not assigned in this section'.format(
                    value_to_get_from
                )
            )


class Delete:
    def __init__(self, memory):
        self.memory = memory

    def __str__(self, memory):
        return 'delete_method'

    def __call__(self, memory_from_call_location, expressions=[]):
        if len(expressions) != 1:
            raise UnderscoreTypeError(
                '{} expressions passed, {} required'.format(
                    len(expressions),
                    1
                )
            )
        value_to_get_from = expressions[0].run(memory_from_call_location)
        if type(value_to_get_from) not in BASIC_TYPES:
            raise UnderscoreTypeError(
                'cannot get from non-basic type'
            )

        try:
            del(self.memory[value_to_get_from])
        except KeyError:
            raise UnderscoreNameError(
                '{} is not assigned in this section'.format(
                    value_to_get_from
                )
            )

        return ValueNode(None)
