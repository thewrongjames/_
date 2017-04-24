from .underscore_node import UnderscoreNode
from .template_function_node import TemplateFunctionNode


class StatementNode(UnderscoreNode):
    def __init__(self, reference, expression):
        self.reference = reference
        self.expression = expression
        # Take of the last item such that running it gives you the memory
        # location you want to put the thing in.
        self.last_name = self.reference.components.pop(-1)

    def get_memory_to_write_to(self, memory):
        if self.reference.components == []:
            return memory
        memory_to_write_to = self.reference.run(memory)
        if not isinstance(memory_to_write_to, dict):
            raise _.exceptions.UnderscoreNameError(
                '{} is not a memory location'.format(self.reference.name)
            )
        return memory_to_write_to

    def pre_run(self, memory, *args, **kwargs):
        """
        Templates are assigned first.
        """
        if isinstance(self.expression, TemplateFunctionNode):
            memory_to_write_to = self.get_memory_to_write_to(memory)
            memory_to_write_to[self.last_name] = self.expression.run(
                memory=memory,
                *args,
                **kwargs
            )

    def run(self, memory, *args, **kwargs):
        if not isinstance(self.expression, TemplateFunctionNode):
            memory_to_write_to = self.get_memory_to_write_to(memory)
            memory_to_write_to[self.last_name] = self.expression.run(
                memory,
                *args,
                **kwargs
            )
