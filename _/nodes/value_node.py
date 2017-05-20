from .underscore_node import UnderscoreNode


class ValueNode(UnderscoreNode):
    FIRST_PARSER = '_parse_expression'

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def run(self, *args, **kwargs):
        return self.value
