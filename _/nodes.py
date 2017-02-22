import time
from copy import deepcopy
from .exceptions import UnderscoreNameError, UnderscoreValueError


class ProgramNode:
    def __init__(self, sections, memory_limit=None, time_limit=None):
        self.sections = sections
        self.memory_limit = memory_limit
        self.time_limit = time_limit
        self.memory = {}
        self.pre_run_start_time = time.time()
        for section in self.sections:
            section.pre_run(
                memory=self.memory,
                memory_limit=self.memory_limit,
                time_limit=self.time_limit,
                start_time = self.pre_run_start_time
            )
        self.pre_run_time_taken = time.time() - self.pre_run_start_time
        if self.time_limit is not None:
            self.time_limit -= self.pre_run_time_taken

    def run(self):
        for section in self.sections:
            # The arguements are keyword arguments, because not all sections
            # will want all of these.
            section.run(
                memory=self.memory,
                memory_limit=self.memory_limit,
                time_limit=self.time_limit,
                start_time=time.time(),
            )
        return self.memory


class UnderscoreNode:
    def pre_run(*args, **kwargs):
        pass


class StatementNode(UnderscoreNode):
    def __init__(self, reference, expression):
        self.reference = reference
        self.expression = expression
        # Take of the last item such that running it gives you the memory
        # location you want to put the thing in.
        self.last_name = self.reference.names.pop(-1)

    def get_memory_to_write_to(self, memory):
        if self.reference.names == []:
            return memory
        memory_to_write_to = self.reference.run(memory)
        if not isinstance(memory_to_write_to, dict):
            raise UnderscoreNameError(
                '{} is not a memory location'.format(self.reference.name)
            )
        return memory_to_write_to

    def pre_run(self, memory, *args, **kwargs):
        """
        Templates are assigned first.
        """
        memory_to_write_to = self.get_memory_to_write_to(memory)
        if isinstance(self.expression, TemplateNode):
            memory_to_write_to[self.last_name] = self.expression.run(
                memory=memory,
                *args,
                **kwargs
            )

    def run(self, memory, *args, **kwargs):
        memory_to_write_to = self.get_memory_to_write_to(memory)
        if not isinstance(self.expression, TemplateNode):
            memory_to_write_to[self.last_name] = self.expression.run(
                memory,
                *args,
                **kwargs
            )


class ValueNode(UnderscoreNode):
    def __init__(self, value):
        self.value = value

    def run(self, *args, **kwargs):
        return self.value


class ReferenceNode(UnderscoreNode):
    def __init__(self, names, character):
        # Names should be a list containing either strings of TemplateNodes.
        self.names = names
        self.character = character

    @property
    def name(self):
        return '.'.join([str(item) for item in self.names])

    def run(self, memory, *args, **kwargs):
        error = UnderscoreNameError(
            "the name '{}' is not defined".format(
                '.'.join([str(item) for item in self.names])
            ),
            self.character
        )

        current_name = self.names[0]
        # Current name may be a TemplateNode or a ReferenceNode though.

        template_call_value = None
        if isinstance(current_name, (TemplateNode, ReferenceNode)):
            template_call_value = TemplateCallNode(current_name, \
                self.character).run(memory=memory)

        if len(self.names) == 1:
            if template_call_value is not None:
                return template_call_value
            try:
                return memory[current_name]
            except KeyError:
                raise error

        # Otherwise, if there is more than one name...
        new_node = ReferenceNode(
            self.names[1:],
            self.character
        )

        if template_call_value is not None:
            if not isinstance(template_call_value, dict):
                raise UnderscoreNameError(
                    '{} does not contain any names'.format(current_name),
                    self.character
                )
            return new_node.run(memory=template_call_value)

        #Or, if the current one is not a node
        try:
            next_memory = memory[current_name]
        except KeyError:
            raise error
        try:
            return new_node.run(memory=next_memory)
        except UnderscoreNameError:
            raise UnderscoreNameError(
                '{} does not contain {}'.format(current_name, self.names[1]),
                self.character
            )


class TemplateNode(UnderscoreNode):
    def __init__(self, sections, returns=None):
        self.sections = sections
        self.internal_memory = {}
        self.returns = returns

    def __str__(self):
        return self.__repr__()

    def run(self, memory, *args, **kwargs):
        def template():
            self.internal_memory = {
                'container': memory
            }
            for section in self.sections:
                section.pre_run(
                    memory=self.internal_memory,
                    *args,
                    **kwargs
                )
            for section in self.sections:
                section.run(
                    memory=self.internal_memory,
                    *args,
                    **kwargs
                )
            if self.returns is not None:
                node = self.returns
                return node.run(
                    memory=self.internal_memory,
                    *args,
                    **kwargs
                )
            return self.internal_memory
        return template


class TemplateCallNode(UnderscoreNode):
    def __init__(self, template, character):
        # Template may be a TemplateNode or a ReferenceNode
        self.template = template
        self.character = character

    def run(self, memory, *args, **kwargs):
        if isinstance(self.template, ReferenceNode):
            template = self.template.run(memory)
            if not callable(template):
                raise UnderscoreValueError(
                    'reference is not callable',
                    self.character
                )
        else:
            template = self.template.run(
                *args, memory=memory, **kwargs
            )
        return template()
