import _
from time import time
from _.standard_library.casting import CASTERS
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
        self.time_limit = time_limit
        self.memory = CASTERS.copy()
        # It doesn't need to be a deepcopy, I can use the same standard library
        # methods everywhere.
        self.running_underscore_standard_library = \
            running_underscore_standard_library
        # running_underscore_standard_library refers to whether or not this
        # program is within the standard_library itself, because, if that is the
        # case, it needs to know to not try to import itself.

        if not running_underscore_standard_library:

            from _.standard_library.written_in_underscore import \
                WRITTEN_IN_UNDERSCORE
            for key, value in WRITTEN_IN_UNDERSCORE.items():
                self.memory[key] = value

        self.pre_run_start_time = time()


        
        for section in self.sections:
            section.pre_run(
                memory=self.memory,
                memory_limit=self.memory_limit,
                time_limit=self.time_limit,
                start_time = self.pre_run_start_time,
                running_underscore_standard_library=\
                    running_underscore_standard_library
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
                running_underscore_standard_library=\
                    self.running_underscore_standard_library
            )
        return self.memory
