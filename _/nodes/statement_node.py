from .underscore_node import UnderscoreNode
from .templates_and_functions import TemplateFunctionNode


class StatementNode(UnderscoreNode):
    FIRST_PARSER = '_parse_statement'

    def __init__(self, reference, expression):
        self.reference = reference
        self.expression = expression
        self.SECOND_PARSER = expression.SECOND_PARSER
        # Take of the last item such that running it gives you the memory
        # location you want to put the thing in.
        self.last_name = self.reference.components.pop(-1)

    def get_memory_to_write_to(
            self,
            memory,
            running_underscore_standard_library
    ):
        if self.reference.components == []:
            return memory
        memory_to_write_to = self.reference.run(
            memory,
            running_underscore_standard_library=\
                running_underscore_standard_library
        )
        if not isinstance(memory_to_write_to, dict):
            raise _.exceptions.UnderscoreNameError(
                '{} is not a memory location'.format(self.reference.name)
            )
        return memory_to_write_to

    def pre_run(
            self,
            memory,
            running_underscore_standard_library,
            *args,
            **kwargs
    ):
        """
        The statement node pre_run assigns templates first, such that they may
        be called before they have been assigned (in terms of lines through the
        code at least).
        """
        if isinstance(self.expression, TemplateFunctionNode):
            memory_to_write_to = self.get_memory_to_write_to(
                memory,
                running_underscore_standard_library=\
                    running_underscore_standard_library
            )
            memory_to_write_to[self.last_name] = self.expression.run(
                memory=memory,
                running_underscore_standard_library=\
                    running_underscore_standard_library,
                *args,
                **kwargs
            )

    def run(self, memory, running_underscore_standard_library, *args, **kwargs):
        if not isinstance(self.expression, TemplateFunctionNode):
            memory_to_write_to = self.get_memory_to_write_to(
                memory,
                running_underscore_standard_library=\
                    running_underscore_standard_library
            )
            memory_to_write_to[self.last_name] = self.expression.run(
                memory,
                running_underscore_standard_library=\
                    running_underscore_standard_library,
                *args,
                **kwargs
            )
