from _.exceptions import UnderscoreBreakError, UnderscoreContinueError, \
    UnderscoreTypeError
from .underscore_node import UnderscoreNode
from .standard_library.casting import BooleanCaster

class IfNode(UnderscoreNode):
    FIRST_PARSER = '_parse_control'

    def __init__(self, expression, if_sections, else_sections):
        self.expression = expression
        self.if_sections = if_sections
        self.else_sections = else_sections

    def run(self, memory, *args, **kwargs):
        expression_result = self.expression.run(memory, *args, **kwargs)
        if isinstance(expression_result, dict):
            # If the expression is a template instance, it needs to be casted
            # to a boolean the way its casting method defines, if it has one.
            # Otherwise it defaults to true.
            try:
                conditional = BooleanCaster()(memory, [expression_result])
            except UnderscoreTypeError:
                conditional = True
        else:
            conditional = expression_result

        if conditional:
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
    FIRST_PARSER = '_parse_control'

    def __init__(self, expression, sections):
        self.expression = expression
        self.sections = sections

    def run(self, memory, *args, **kwargs):
        expression_result = self.expression.run(memory, *args, **kwargs)
        if isinstance(expression_result, dict):
            # If the expression is a template instance, it needs to be casted
            # to a boolean the way its casting method defines, if it has one.
            # Otherwise it defaults to true.
            try:
                conditional = BooleanCaster()(memory, [expression_result])
            except UnderscoreTypeError:
                conditional = True
        else:
            conditional = expression_result

        while conditional:
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
                except UnderscoreBreakError:
                    should_break = True
                    break
                except UnderscoreContinueError:
                    should_contine = True
                    break
            if should_break: break
            if should_continue: continue


class BreakNode(UnderscoreNode):
    FIRST_PARSER = '_parse_break_or_continue'

    def __init__(self, position_in_program):
        self.position_in_program = position_in_program

    def run(self, *args, **kwargs):
        raise UnderscoreBreakError(
            'break outside of loop',
            self.position_in_program
        )


class ContinueNode(UnderscoreNode):
    FIRST_PARSER = '_parse_break_or_continue'

    def __init__(self, position_in_program):
        self.position_in_program = position_in_program

    def run(self, *args, **kwargs):
        raise UnderscoreContinueError(
            'Continue outside of loop',
            self.position_in_program
        )
