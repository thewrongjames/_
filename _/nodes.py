import time
from copy import deepcopy
from .exceptions import UnderscoreNameError, UnderscoreValueError
from .utilities import add_dictionaries


class ProgramNode:
    def __init__(self, sections, memory_limit=None, time_limit=None):
        self.sections = sections
        self.memory_limit = memory_limit
        self.time_limit = time_limit
        self.memory = {}
        self.templates = {}
        self.pre_run_start_time = time.time()
        for section in self.sections:
            section.pre_run(
                memory=self.memory,
                templates=self.templates,
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
                templates=self.templates,
                memory_limit=self.memory_limit,
                time_limit=self.time_limit,
                start_time=time.time(),
            )
        return add_dictionaries(self.templates, self.memory)


class UnderscoreNode:
    def pre_run(*args, **kwargs):
        pass


class StatementNode(UnderscoreNode):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def pre_run(self, templates, memory, *args, **kwargs):
        if isinstance(self.expression, TemplateNode):
            templates[self.name] = self.expression.run(
                templates=templates,
                memory=memory,
                *args,
                **kwargs
            )

    def run(self, memory, templates, *args, **kwargs):
        """
        This will assign only non-template values to names. Template values will
        already have been assigned in the pre_run. If the name is the name of a
        template, that template will be removed from memory. Note that that will
        only happen at the point at which this assignment does. The consequence
        of this is that if you assign a name to, say, a string, and then a
        template, before the assignement to string, that name will represent the
        template, and after the string assignment, it will represent the string,
        even after the assignement to the template, because that has already
        been run.
        """
        if not isinstance(self.expression, TemplateNode):
            memory[self.name] = deepcopy(
                self.expression.run(
                    memory,
                    templates,
                    *args,
                    **kwargs
                )
            )
            if self.name in templates:
                del templates[self.name]


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

    def run(self, memory, templates, *args, **kwargs):
        all_memory = add_dictionaries(templates, memory)
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
                self.character).run(memory=memory, templates=templates)

        if len(self.names) == 1:
            if template_call_value is not None:
                return template_call_value
            try:
                return all_memory[current_name]
            except KeyError:
                raise error

        # Otherwise, if there is more than one name...
        new_node = ReferenceNode(
            self.names[1:],
            self.character + len(current_name) + 1 # +1 for the . between names.
        )

        if template_call_value is not None:
            if not isinstance(template_call_value, dict):
                raise UnderscoreNameError(
                    '{} does not contain any names'.format(current_name),
                    self.character
                )
            return new_node.run(memory=template_call_value, templates={})

        #Or, if the current one is not a node
        try:
            next_memory = all_memory[current_name]
        except KeyError:
            raise error
        try:
            return new_node.run(memory=next_memory, templates={})
        except UnderscoreNameError:
            raise UnderscoreNameError(
                '{} does not contain {}'.format(current_name, self.names[1]),
                self.character
            )





        # split_name = self.names
        # if len(split_name) > 1:
        #     try:
        #         next_memory = all_memory[split_name[0]]
        #     except KeyError:
        #         raise error
        #
        # if '(' in split_name[0]:
        #     template_reference_node = ReferenceNode(
        #         split_name[0].split('(')[0],
        #         self.character
        #     )
        #     template_call_node = TemplateCallNode(
        #         template_reference_node,
        #         self.character
        #     )
        #     template_call_value = template_call_node.run(
        #         memory=memory,
        #         templates=templates
        #     )
        #     if len(split_name) == 1:
        #         # This is the last single name
        #         return template_call_value
        #     # But, if this is not the last item...
        #     if not isinstance(template_call_value, dict):
        #         raise UnderscoreNameError(
        #             '{} does not contain any names'.format(split_name[0])
        #         )
        #     next_memory = template_call_value
        #
        # if len(split_name) == 1:
        #     try:
        #         print(self.name)
        #         return all_memory[self.name]
        #     except KeyError:
        #         raise error
        #
        # new_node = ReferenceNode(
        #     '.'.join(split_name[1:]),
        #     self.character + len(split_name[0]) + 1
        # )
        # return new_node.run(all_memory=next_memory)


class TemplateNode(UnderscoreNode):
    def __init__(self, sections, returns=None):
        self.sections = sections
        self.internal_memory = {}
        self.internal_templates = {}
        self.returns = returns

    def __str__(self):
        return self.__repr__()

    def run(self, memory, templates, *args, **kwargs):
        def template():
            container_memory = add_dictionaries(templates, memory)
            self.internal_memory = {
                'container': container_memory
            }
            for section in self.sections:
                section.pre_run(
                    memory=self.internal_memory,
                    templates=self.internal_templates,
                    *args,
                    **kwargs
                )
            for section in self.sections:
                section.run(
                    memory=self.internal_memory,
                    templates=self.internal_templates,
                    *args,
                    **kwargs
                )
            final_memory = add_dictionaries(
                self.internal_templates,
                self.internal_memory
            )
            if self.returns is not None:
                node = self.returns
                return node.run(
                    memory=self.internal_memory,
                    templates=self.internal_templates,
                    *args,
                    **kwargs
                )
            return final_memory
        return template


class TemplateCallNode(UnderscoreNode):
    def __init__(self, template, character):
        # Template may be a TemplateNode or a ReferenceNode
        self.template = template
        self.character = character

    def run(self, memory, templates, *args, **kwargs):
        if isinstance(self.template, ReferenceNode):
            template = self.template.run(memory, templates)
            if not callable(template):
                raise UnderscoreValueError(
                    'reference is not callable',
                    self.character
                )
        else:
            template = self.template.run(
                *args, memory=memory, templates=templates, **kwargs
            )
        return template()
