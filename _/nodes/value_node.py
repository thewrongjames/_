from .underscore_node import UnderscoreNode


class ValueNode(UnderscoreNode):
    def __init__(self, value):
        self.value = value

    def run(self, *args, **kwargs):
        return self.value
