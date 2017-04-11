from _ import nodes
from ._surrounding_whitespace_removed import _surrounding_whitespace_removed

@_surrounding_whitespace_removed
def parse(self, memory_limit=None, time_limit=None):
    sections = self._parse_sections()
    return nodes.ProgramNode(sections, memory_limit, time_limit)
