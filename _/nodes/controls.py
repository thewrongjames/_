from _ import exceptions
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


class WhileNode(UnderscoreNode):
    def __init__(self, expression, sections):
        self.expression = expression
        self.sections = sections

    def run(self, memory, *args, **kwargs):
        while self.expression.run(memory, *args, **kwargs):
            should_break = False
            should_continue = False
            for section in self.sections:
                # As BreakNode and ContinueNode do not have a pre_run, we do not
                # need to check for their errors here.
                section.pre_run(
                    memory=memory,
                    *args,
                    **kwargs
                )
            for section in self.sections:
                try:
                    section.run(
                        memory=memory,
                        *args,
                        **kwargs
                    )
                except exceptions.UnderscoreBreakError:
                    should_break = True
                    break
                except exceptions.UnderscoreContinueError:
                    should_contine = True
                    break
            if should_break: break
            if should_continue: continue


class BreakNode(UnderscoreNode):
    def __init__(self, position_in_program):
        self.position_in_program = position_in_program

    def run(self, *args, **kwargs):
        raise exceptions.UnderscoreBreakError(
            'break outside of loop',
            self.position_in_program
        )


class ContinueNode(UnderscoreNode):
    def __init__(self, position_in_program):
        self.position_in_program = position_in_program

    def run(self, *args, **kwargs):
        raise exceptions.UnderscoreContinueError(
            'Continue outside of loop',
            self.position_in_program
        )
