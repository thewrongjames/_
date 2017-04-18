from .underscore_node import UnderscoreNode

class IfNode(UnderscoreNode):
    def __init__(self, expression, if_sections, else_sections):
        self.expression = expression
        self.if_sections = if_sections
        self.else_sections = else_sections

    def run(self, memory, *args, **kwargs):
        if self.expression.run(memory, *args, **kwargs):
            for section in self.if_sections:
                section.pre_run(
                    memory=memory,
                    *args,
                    **kwargs
                )
            for section in self.if_sections:
                section.run(
                    memory=memory,
                    *args,
                    **kwargs
                )
        else:
            for section in self.else_sections:
                section.pre_run(
                    memory=memory,
                    *args,
                    **kwargs
                )
            for section in self.else_sections:
                section.run(
                    memory=memory,
                    *args,
                    **kwargs
                )
