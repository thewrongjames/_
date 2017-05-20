from .underscore_node import UnderscoreNode


class CommentNode(UnderscoreNode):
    FIRST_PARSER = '_parse_comment'

    def run(self, *args, **kwargs):
        pass
