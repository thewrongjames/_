from _.exceptions import UnderscoreTypeError, UnderscoreNameError
from _.nodes.value_node import ValueNode
from .constants import BASIC_TYPES


class Set:
    def __init__(self, memory, running_underscore_standard_library):
        self.memory = memory
        self.running_underscore_standard_library = \
            running_underscore_standard_library

    def __str__(self):
        return 'set_method'

    def __repr__(self):
        return str(self)

    def __call__(self, memory_from_call_location, expressions, character):
        if len(expressions) != 2:
            raise UnderscoreTypeError(
                '{} expressions passed, {} required'.format(
                    len(expressions),
                    2
                ),
                character
            )
        value_to_assign_to = expressions[0].run(
            memory_from_call_location,
            running_underscore_standard_library=\
                self.running_underscore_standard_library
        )
        value_to_assign = expressions[1].run(
            memory_from_call_location,
            running_underscore_standard_library=\
                self.running_underscore_standard_library
        )
        if type(value_to_assign_to) not in BASIC_TYPES:
            raise UnderscoreTypeError(
                'cannot set to non-basic type',
                character
            )
        self.memory[value_to_assign_to] = value_to_assign

        return ValueNode(None)


class Get:
    def __init__(self, memory, running_underscore_standard_library):
        self.memory = memory
        self.running_underscore_standard_library = \
            running_underscore_standard_library

    def __str__(self):
        return 'get_method'

    def __repr__(self):
        return str(self)

    def __call__(self, memory_from_call_location, expressions, character):
        if len(expressions) != 1:
            raise UnderscoreTypeError(
                '{} expressions passed, {} required'.format(
                    len(expressions),
                    1
                ),
                character
            )
        value_to_get_from = expressions[0].run(
            memory_from_call_location,
            running_underscore_standard_library=\
                self.running_underscore_standard_library
        )
        if type(value_to_get_from) not in BASIC_TYPES:
            raise UnderscoreTypeError(
                'cannot get from non-basic type',
                character
            )

        try:
            return self.memory[value_to_get_from]
        except KeyError:
            raise UnderscoreNameError(
                '{} is not assigned in this section'.format(
                    value_to_get_from
                ),
                character
            )


class Delete:
    def __init__(self, memory, running_underscore_standard_library):
        self.memory = memory
        self.running_underscore_standard_library = \
            running_underscore_standard_library

    def __str__(self):
        return 'delete_method'

    def __repr__(self):
        return str(self)

    def __call__(self, memory_from_call_location, expressions, character):
        if len(expressions) != 1:
            raise UnderscoreTypeError(
                '{} expressions passed, {} required'.format(
                    len(expressions),
                    1
                ),
                character
            )
        value_to_get_from = expressions[0].run(
            memory_from_call_location,
            running_underscore_standard_library=\
                self.running_underscore_standard_library
        )
        if type(value_to_get_from) not in BASIC_TYPES:
            raise UnderscoreTypeError(
                'cannot get from non-basic type',
                character
            )

        try:
            del(self.memory[value_to_get_from])
        except KeyError:
            raise UnderscoreNameError(
                '{} is not assigned in this section'.format(
                    value_to_get_from
                ),
                character
            )

        return ValueNode(None)
