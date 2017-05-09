import _
from .underscore_node import UnderscoreNode


class ReferenceNode(UnderscoreNode):
    def __init__(self, components, character):
        # components should be a list containing either strings or tuples containing
        # TemplateFunctionNodes and any expressions passed to them.
        self.components = components
        self.character = character

    @property
    def name(self):
        def make_nice(item):
            if isinstance(item, tuple):
                return str(item[0]) + '({})'.format(*item[1])
            return str(item)
        return '.'.join([make_nice(item) for item in self.components])

    def __str__(self):
        return self.name

    def run(self, memory, *args, call_memory=None, **kwargs):
        # call_memory is the original memory from the top of the chain of
        # reference nodes (if there is one), this is the memory that should be
        # passed into any TemplateInstantiateFunctionCallNode created for it to
        # evaluate the expressions in its call in. If it has not been assigned,
        # this node was not created by another ReferenceNode, and, as such,
        # call_memory should just be the memory that this node is in.
        if call_memory is None:
            call_memory = memory

        error = _.exceptions.UnderscoreNameError(
            "'{}' is not defined in this context".format(
                '.'.join([str(item) for item in self.components])
            ),
            self.character
        )

        current_component = self.components[0]

        requires_running, is_instantiation_or_call = False, False
        if isinstance(current_component, tuple):
            # current_component[0] will be the actual TemplateFunctionNode,
            # as parsed by the parser, and current_component[1] will be a list
            # of expressions to be passed to it.
            requires_running = True
            is_instantiation_or_call = True
            run_value = TemplateInstantiateFunctionCallNode(
                current_component[0],
                self.character,
                current_component[1]
            ).run(memory=memory, call_memory=call_memory)
        elif not isinstance(current_component, str):
            # If the item is both not a tuple and not a string, it has come from
            # square bracket indexing, and is an expression that must be run
            # in order to find the value that is the key. It must be run using
            # call_memory as that is from the scope that the actual reference
            # is in.
            requires_running = True
            run_value = current_component.run(memory=call_memory)

        if len(self.components) == 1:
            if requires_running and is_instantiation_or_call:
                return run_value
            try:
                return memory[current_component]
            except KeyError:
                raise error

        # Otherwise, if there is more than one component...
        new_node = ReferenceNode(
            self.components[1:],
            self.character
        )

        if requires_running:
            if not isinstance(run_value, dict):
                raise _.exceptions.UnderscoreNameError(
                    '{} does not contain any names'.format(current_component),
                    self.character
                )
            return new_node.run(
                memory=run_value,
                call_memory=memory
            )

        #Or, if the current one is not a node
        try:
            next_memory = memory[current_component]
        except KeyError:
            raise error
        try:
            return new_node.run(memory=next_memory, call_memory=memory)
        except _.exceptions.UnderscoreNameError:
            raise _.exceptions.UnderscoreNameError(
                '{} does not contain {}'.format(
                    current_component,
                    self.components[1]
                ),
                self.character
            )


class TemplateInstantiateFunctionCallNode(UnderscoreNode):
    """
    This is also used for function calls.
    """
    def __init__(self, template_or_function, character, expressions):
        # template_of_function may be a TemplateFunctionNode or a ReferenceNode.
        # character refers to the character that the program was up to when this
        # was parsed.
        self.template_or_function = template_or_function
        self.character = character
        self.expressions = expressions

    def run(self, memory, call_memory, *args, **kwargs):
        # memory is the memory location in which the most recent reference was,
        # where the template_or_function must be found if it is a ReferenceNode.
        # call_memory is the memory location in which the reference originated,
        # i.e. where the expressions that are passed need to be run.
        if isinstance(self.template_or_function, ReferenceNode):
            template_or_function = self.template_or_function.run(memory)
            if not callable(template_or_function):
                raise _.exceptions.UnderscoreValueError(
                    'reference is not callable',
                    self.character
                )
        else:
            template_or_function = self.template_or_function.run(
                *args, memory=memory, **kwargs
            )
        return template_or_function(call_memory, self.expressions)
