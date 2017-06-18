from time import time
from ..standard_library.casting import get_casters
from .underscore_node import UnderscoreNode
from .statement_node import StatementNode
from .value_node import ValueNode
from .references import ReferenceNode, TemplateInstantiateFunctionCallNode
from .templates_and_functions import TemplateFunctionNode, ReturnNode
from .maths import AdditionNode, SubtractionNode, MultiplicationNode, \
    DivisionNode, PowerNode
from .boolean_logic import AndOrOrNode, NotNode, EqualityNode, \
    SmallerThanOrEqualToNode, SmallerThanNode, GreaterThanNode, \
    GreaterThanOrEqualToNode, InequalityNode
from .controls import IfNode, WhileNode, BreakNode, ContinueNode
from .comment_node import CommentNode

class ProgramNode:
    def __init__(
            self,
            sections,
            memory_limit=None,
            time_limit=None,
            running_underscore_standard_library=False
    ):
        self.sections = sections
        self.memory_limit = memory_limit
        self.time_which_may_be_taken = time_limit
        # To the user, time_limit refers to the amount of time the program may
        # take, but, within the program, it refers to the time by which it must
        # be finished.

        if self.time_which_may_be_taken is None:
            self.time_limit = None
        else:
            # self.time_limit is the time by which the program must be finished,
            # that is, the current time, plus the time that is allowed run for.
            self.time_limit = time() + self.time_which_may_be_taken

        self.memory = get_casters(
            time_limit=self.time_limit,
            memory_limit=self.memory_limit,
            running_underscore_standard_library=\
                running_underscore_standard_library
        )

        self.running_underscore_standard_library = \
            running_underscore_standard_library
        # running_underscore_standard_library refers to whether or not this
        # program is within the standard_library itself, because, if that is the
        # case, it needs to know to not try to import itself.
        if not running_underscore_standard_library:
            from ..standard_library.written_in_underscore import \
                WRITTEN_IN_UNDERSCORE
            for key, value in WRITTEN_IN_UNDERSCORE.items():
                self.memory[key] = value

        for section in self.sections:
            section.pre_run(
                memory=self.memory,
                memory_limit=self.memory_limit,
                time_limit=self.time_limit,
                running_underscore_standard_library=\
                    running_underscore_standard_library
            )

    def run(self):
        for section in self.sections:
            # The arguements are keyword arguments, because not all sections
            # will want all of these.
            section.run(
                memory=self.memory,
                memory_limit=self.memory_limit,
                time_limit=self.time_limit,
                running_underscore_standard_library=\
                    self.running_underscore_standard_library
            )
        return self.memory
