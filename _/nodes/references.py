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
        return '.'.join([str(item) for item in self.components])

    def __str__(self):
        return self.name

    def run(self, memory, *args, **kwargs):
        error = _.exceptions.UnderscoreNameError(
            "'{}' is not defined in this context".format(
                '.'.join([str(item) for item in self.components])
            ),
            self.character
        )

        current_component = self.components[0]

        is_instantiation_or_call = False
        if isinstance(current_component, tuple):
            is_instantiation_or_call = True
            instance_or_call_value = TemplateInstantiateFunctionCallNode(
                current_component[0],
                self.character,
                current_component[1]
            ).run(memory=memory)

        if len(self.components) == 1:
            if is_instantiation_or_call:
                return instance_or_call_value
            try:
                return memory[current_component]
            except KeyError:
                raise error

        # Otherwise, if there is more than one component...
        new_node = ReferenceNode(
            self.components[1:],
            self.character
        )

        if is_instantiation_or_call:
            if not isinstance(instance_or_call_value, dict):
                raise _.exceptions.UnderscoreNameError(
                    '{} does not contain any names'.format(current_component),
                    self.character
                )
            return new_node.run(memory=instance_or_call_value)

        #Or, if the current one is not a node
        try:
            next_memory = memory[current_component]
        except KeyError:
            raise error
        try:
            return new_node.run(memory=next_memory)
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

    def run(self, memory, *args, **kwargs):
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
        print(isinstance(self.template_or_function, ReferenceNode))
        print(template_or_function)
        print(dir(template_or_function))
        return template_or_function(self.expressions)
