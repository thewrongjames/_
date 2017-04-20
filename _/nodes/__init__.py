import time
import _
from .underscore_node import UnderscoreNode
from .statement_node import StatementNode
from .value_node import ValueNode
from .references import ReferenceNode, TemplateInstantiateFunctionCallNode
from .template_function_node import TemplateFunctionNode
from .maths import AdditionNode, SubtractionNode, MultiplicationNode, \
    DivisionNode
from .boolean_statements import EqualityNode, SmallerThanOrEqualToNode, \
    SmallerThanNode, GreaterThanNode, GreaterThanOrEqualToNode, InequalityNode
from .controls import IfNode, WhileNode

class ProgramNode:
    def __init__(self, sections, memory_limit=None, time_limit=None):
        self.sections = sections
        self.memory_limit = memory_limit
        self.time_limit = time_limit
        self.memory = {}
        self.pre_run_start_time = time.time()
        for section in self.sections:
            section.pre_run(
                memory=self.memory,
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
                memory_limit=self.memory_limit,
                time_limit=self.time_limit,
                start_time=time.time(),
            )
        return self.memory
