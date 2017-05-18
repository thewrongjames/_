from _.exceptions import UnderscoreTypeError, UnderscoreReturnError
from .underscore_node import UnderscoreNode
from .value_node import ValueNode
from .standard_library import STANDARD_LIBRARY
from .standard_library.template_methods import Set, Get, Delete


class TemplateFunctionNode(UnderscoreNode):
    def __init__(self, sections, is_function, names):
        self.sections = sections
        self.is_function = is_function
        self.names = names

    def __str__(self):
        return self.__repr__()

    def run(self, memory, *args, **kwargs):
        class TemplateOrFunction:
            def __init__(
                    self,
                    sections,
                    is_function,
                    names,
                    memory,
                    *args,
                    **kwargs
            ):
                self.sections = sections
                self.is_function = is_function
                self.names = names
                self.memory = memory
                self.args = args
                self.kwargs = kwargs

            def __str__(self):
                return 'function' if self.is_function else 'template'

            def __call__(self, memory_from_call_location, expressions=[]):
                if len(expressions) != len(self.names):
                    raise UnderscoreTypeError(
                        'number of expressions passed does not match number '
                        'required'
                    )

                internal_memory = STANDARD_LIBRARY.copy()
                # It doesn't need to be a deepcopy, I can use the same standard library
                # methods everywhere.
                internal_memory['container'] = self.memory

                # If this is a template, the standard methods must be added to
                # the internal memory.
                if not self.is_function:
                    internal_memory['set'] = Set(internal_memory)
                    internal_memory['get'] = Get(internal_memory)
                    internal_memory['delete'] = Delete(internal_memory)

                values_of_passed_expressions = []
                for expression in expressions:
                    values_of_passed_expressions.append(
                        expression.run(memory_from_call_location)
                    )

                for name, value in zip(self.names, values_of_passed_expressions):
                    internal_memory[name] = value

                for section in self.sections:
                    # Returns don't need to be catched here as ReturnNodes don't
                    # pre_run.
                    section.pre_run(
                        memory=internal_memory,
                        *self.args,
                        **self.kwargs
                    )
                for section in self.sections:
                    try:
                        section.run(
                            memory=internal_memory,
                            *self.args,
                            **self.kwargs
                        )
                    except UnderscoreReturnError as return_error:
                        return return_error.expression_to_return.run(
                            internal_memory,
                            *self.args,
                            **self.kwargs
                        )
                if self.is_function:
                    return ValueNode(None)
                return internal_memory
        return TemplateOrFunction(
            self.sections,
            self.is_function,
            self.names,
            memory,
            *args,
            **kwargs
        )


class ReturnNode(UnderscoreNode):
    def __init__(self, expression_to_return, position_in_program):
        self.expression_to_return = expression_to_return
        self.position_in_program = position_in_program

    def run(self, memory, *args, **kwargs):
        # The user will only ever see this error if it is outside of a function,
        # so that is the message it gives.
        raise UnderscoreReturnError(
            self.expression_to_return,
            '\'return\' outside of function',
            self.position_in_program
        )
