import time


class ProgramNode:
    def __init__(self, sections, memory_limit=None, time_limit=None):
        self.sections = sections
        self.memory_limit = memory_limit
        self.time_limit = time_limit
        self.memory = {}

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


class StatementNode:
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def run(
            self,
            memory,
            memory_limit=None,
            time_limit=None,
            start_time=None
    ):
        memory[self.name] = self.expression.run(memory)


class ValueNode:
    def __init__(self, value):
        self.value = value

    def run(self, *args, **kwargs):
        return self.value


class ReferenceNode:
    def __init__(self, name):
        self.name = name

    def run(self, memory, *args, **kwargs):
        return memory[self.name]
