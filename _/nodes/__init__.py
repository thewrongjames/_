import _
from time import time
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
            include_standard_library=True
    ):
        self.sections = sections
        self.memory_limit = memory_limit
        self.time_limit = time_limit
        # include_standard_library should almost always be True. Turning it off
        # removes access to casters and also the Set, Get, and Delete methods
        # amoungst other things. It should only be turned off when methods to
        # be in the standard library themselves are being run.
        if include_standard_library:
            import _.standard_library.STANDARD_LIBRARY
            self.memory = STANDARD_LIBRARY.copy()
            # It doesn't need to be a deepcopy, I can use the same standard library
            # methods everywhere.
        self.pre_run_start_time = time()
        for section in self.sections:
            section.pre_run(
                memory=self.memory,
                memory_limit=self.memory_limit,
                time_limit=self.time_limit,
                start_time = self.pre_run_start_time,
                include_standard_library=include_standard_library
            )
        self.pre_run_time_taken = time() - self.pre_run_start_time
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
                start_time=time(),
                include_standard_library=include_standard_library
            )
        return self.memory
