from _.exceptions import UnderscoreNameError, UnderscoreValueError
from .underscore_node import UnderscoreNode
from .limited import limited


class ReferenceNode(UnderscoreNode):
    FIRST_PARSER = '_parse_expression'
    SECOND_PARSER = '_parse_reference'

    def __init__(self, components, character):
        # components should be a list containing either strings or tuples
        # containing
        # TemplateFunctionNodes and any expressions passed to them.
        self.components = components
        self.character = character

    @staticmethod
    def _make_nice_string_representation(item, just_name=False):
        """
        Takes a component, and makes it look nice.

        nice, /nʌɪs/, adjective: giving pleasure or satisfaction; pleasant
        or attractive.
        """
        if isinstance(item, tuple):
            passed_values = ', '.join(str(value) for value in item[1])
            return str(item[0])
            return '{}({})'.format(item[0], passed_values)

        return str(item)

    @property
    def name(self):
        return '.'.join([self._make_nice_string_representation(item) for item \
            in self.components])

    def __repr__(self):
        return 'ReferenceNode({})'.format(self.name)

    @limited
    def run(
                self,
                memory,
                time_limit,
                memory_limit,
                running_underscore_standard_library,
                *args,
                call_memory=None,
                **kwargs
    ):
        # call_memory is the original memory from the top of the chain of
        # reference nodes (if there is one), this is the memory that should be
        # passed into any TemplateInstantiateFunctionCallNode created for it to
        # evaluate the expressions in its call in. If it has not been assigned,
        # this node was not created by another ReferenceNode, and, as such,
        # call_memory should just be the memory that this node is in.
        if call_memory is None:
            call_memory = memory

        error = UnderscoreNameError(
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
            ).run(
                memory=memory,
                call_memory=call_memory,
                time_limit=time_limit,
                memory_limit=memory_limit,
                running_underscore_standard_library=\
                    running_underscore_standard_library
            )
        elif not isinstance(current_component, str):
            # If the item is both not a tuple and not a string, it has come from
            # square bracket indexing, and is an expression that must be run
            # in order to find the value that is the key. It must be run using
            # call_memory as that is from the scope that the actual reference
            # is in.
            requires_running = True
            run_value = current_component.run(
                memory=call_memory,
                time_limit=time_limit,
                memory_limit=memory_limit,
                running_underscore_standard_library=\
                    running_underscore_standard_library
            )

        if len(self.components) == 1:
            if requires_running:
                if is_instantiation_or_call:
                    return run_value
                try:
                    return memory[run_value]
                except KeyError:
                    raise error
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
                raise UnderscoreNameError(
                    '{} does not contain any names'.format(current_component),
                    self.character
                )
            return new_node.run(
                memory=run_value,
                call_memory=memory,
                time_limit=time_limit,
                memory_limit=memory_limit,
                running_underscore_standard_library=\
                    running_underscore_standard_library
            )

        #Or, if the current one is not a node
        try:
            next_memory = memory[current_component]
        except KeyError:
            raise error
        return new_node.run(
            memory=next_memory,
            call_memory=memory,
            time_limit=time_limit,
            memory_limit=memory_limit,
            running_underscore_standard_library=\
                running_underscore_standard_library
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

    @limited
    def run(
            self,
            memory,
            call_memory,
            time_limit,
            memory_limit,
            running_underscore_standard_library,
            *args,
            **kwargs
        ):
        # memory is the memory location in which the most recent reference was,
        # where the template_or_function must be found if it is a ReferenceNode.
        # call_memory is the memory location in which the reference originated,
        # i.e. where the expressions that are passed need to be run.
        if isinstance(self.template_or_function, ReferenceNode):
            template_or_function = self.template_or_function.run(
                memory=memory,
                time_limit=time_limit,
                memory_limit=memory_limit,
                running_underscore_standard_library=\
                    running_underscore_standard_library
            )
            if not callable(template_or_function):
                raise UnderscoreValueError(
                    'reference is not callable',
                    self.character
                )
        else:
            template_or_function = self.template_or_function.run(
                *args,
                memory=memory,
                time_limit=time_limit,
                memory_limit=memory_limit,
                running_underscore_standard_library=\
                    running_underscore_standard_library,
                **kwargs
            )
        return template_or_function(
            call_memory,
            self.expressions,
            self.character
        )
