from _.standard_library.casting import get_casters
from _.standard_library.template_methods import get_template_methods
from _.exceptions import UnderscoreTypeError, UnderscoreReturnError, \
    UnderscoreIncorrectNumberOfArgumentsError
from .underscore_node import UnderscoreNode
from .value_node import ValueNode
from .limited import limited


class TemplateOrFunction:
    """
    This is the object that actually represents underscore templates and
    functions.
    """

    def __init__(
            self,
            sections,
            is_function,
            names,
            memory,
            time_limit,
            memory_limit,
            running_underscore_standard_library,
            *args,
            **kwargs
    ):
        self.sections = sections
        self.is_function = is_function
        self.names = names
        self.memory = memory
        self.time_limit = time_limit
        self.memory_limit = memory_limit
        self.running_underscore_standard_library = \
            running_underscore_standard_library
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return 'function' if self.is_function else 'template'

    def __repr__(self):
        return str(self)

    def __call__(self, memory_from_call_location, expressions, *args, **kwargs):
        if len(expressions) != len(self.names):
            raise UnderscoreIncorrectNumberOfArgumentsError(
                'number of expressions passed does not match number '
                'required'
            )

        internal_memory = get_casters(self.running_underscore_standard_library)
        # It doesn't need to be a deepcopy, I can use the same standard library
        # methods everywhere.
        if not self.running_underscore_standard_library:
            from _.standard_library.written_in_underscore import \
                WRITTEN_IN_UNDERSCORE
            for key, value in WRITTEN_IN_UNDERSCORE.items():
                internal_memory[key] = value
        # If this is a template, the set, get and delete methods must be added
        # to the internal memory.
        if not self.is_function:
            template_methods = get_template_methods(
                internal_memory,
                self.time_limit,
                self.memory_limit,
                self.running_underscore_standard_library
            )
            for key, value in template_methods.items():
                internal_memory[key] = value

        internal_memory['container'] = self.memory

        values_of_passed_expressions = []
        for expression in expressions:
            values_of_passed_expressions.append(
                expression.run(
                    memory_from_call_location,
                    running_underscore_standard_library=\
                        self.running_underscore_standard_library
                )
            )

        for name, value in zip(self.names, values_of_passed_expressions):
            internal_memory[name] = value

        for section in self.sections:
            # Returns don't need to be catched here as ReturnNodes don't
            # pre_run.
            section.pre_run(
                memory=internal_memory,
                time_limit=self.time_limit,
                memory_limit=self.memory_limit,
                running_underscore_standard_library=\
                    self.running_underscore_standard_library,
                *self.args,
                **self.kwargs
            )
        for section in self.sections:
            try:
                section.run(
                    memory=internal_memory,
                    time_limit=self.time_limit,
                    memory_limit=self.memory_limit,
                    running_underscore_standard_library=\
                        self.running_underscore_standard_library,
                    *self.args,
                    **self.kwargs
                )
            except UnderscoreReturnError as return_error:
                return return_error.expression_to_return.run(
                    internal_memory,
                    running_underscore_standard_library=\
                        self.running_underscore_standard_library,
                    *self.args,
                    **self.kwargs
                )
        if self.is_function:
            # If it is a function that has not already returned
            # something, it needs to return none.
            return
        return internal_memory


class TemplateFunctionNode(UnderscoreNode):
    FIRST_PARSER = '_parse_expression'
    SECOND_PARSER = '_parse_function_or_template'

    def __init__(self, sections, is_function, names):
        self.sections = sections
        self.is_function = is_function
        self.names = names

    @limited
    def run(
            self,
            memory,
            running_underscore_standard_library,
            time_limit,
            memory_limit,
            *args,
            **kwargs
    ):
        return TemplateOrFunction(
            *args,
            sections=self.sections,
            is_function=self.is_function,
            names=self.names,
            memory=memory,
            time_limit=time_limit,
            memory_limit=memory_limit,
            running_underscore_standard_library=\
                running_underscore_standard_library,
            **kwargs
        )


class ReturnNode(UnderscoreNode):
    FIRST_PARSER = '_parse_return'

    def __init__(self, expression_to_return, position_in_program):
        self.expression_to_return = expression_to_return
        self.position_in_program = position_in_program

    @limited
    def run(self, memory, *args, **kwargs):
        # The user will only ever see this error if it is outside of a function,
        # so that is the message it gives.
        raise UnderscoreReturnError(
            self.expression_to_return,
            '\'return\' outside of function',
            self.position_in_program
        )
