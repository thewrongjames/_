import _.exceptions
from .value_node import ValueNode


BASIC_TYPES = [int, float, bool, str, type(None)]


class Set:
    def __init__(self, memory):
        self.memory = memory

    def __call__(self, expressions=[]):
        if len(expressions) != 2:
            raise exceptions.UnderscoreTypeError(
                '{} expressions passed, {} required'.format(
                    len(expressions),
                    2
                )
            )
        value_to_assign_to = expressions[0].run(self.memory)
        value_to_assign = expressions[1].run(self.memory)
        if type(value_to_assign_to) not in BASIC_TYPES:
            raise exceptions.UnderscoreTypeError(
                'cannot set to non-basic type'
            )
        self.memory[value_to_assign_to] = value_to_assign

        return ValueNode(None)


class Get:
    def __init__(self, memory):
        self.memory = memory

    def __call__(self, expressions=[]):
        if len(expressions) != 1:
            raise exceptions.UnderscoreTypeError(
                '{} expressions passed, {} required'.format(
                    len(expressions),
                    2
                )
            )
        value_to_get_from = expressions[0].run(self.memory)
        if type(value_to_get_from) not in BASIC_TYPES:
            raise exceptions.UnderscoreTypeError(
                'cannot get from non-basic type'
            )

        try:
            return self.memory[value_to_get_from]
        except KeyError:
            raise exceptions.UnderscoreNameError(
                '{} is not assigned in this section'.format(
                    value_to_get_from
                )
            )


class Delete:
    def __init__(self, memory):
        self.memory = memory

    def __call__(self, expressions=[]):
        if len(expressions) != 1:
            raise exceptions.UnderscoreTypeError(
                '{} expressions passed, {} required'.format(
                    len(expressions),
                    2
                )
            )
        value_to_get_from = expressions[0].run(self.memory)
        if type(value_to_get_from) not in BASIC_TYPES:
            raise exceptions.UnderscoreTypeError(
                'cannot get from non-basic type'
            )

        try:
            del(self.memory[value_to_get_from])
        except KeyError:
            raise exceptions.UnderscoreNameError(
                '{} is not assigned in this section'.format(
                    value_to_get_from
                )
            )

        return ValueNode(None)
