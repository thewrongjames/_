import _.exceptions
from .value_node import ValueNode


BASIC_TYPES = [int, float, bool, str, type(None)]


class Set:
    def run(self, memory, *args, **kwargs):
        class SetMethod:
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

        return SetMethod(memory)


class Get:
    def run(self, memory, *args, **kwargs):
        class GetMethod:
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

        return SetMethod(memory)


class Delete:
    def run(self, memory, *args, **kwargs):
        class DeleteMethod:
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

        return SetMethod(memory)
