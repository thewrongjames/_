from string import whitespace


def consume_whitespace(self):
    while (self._peek() is not None and self._peek() in whitespace):
        self.position_in_program += 1


class SurroundingWhitespaceRemover:
    """
    Instances of this, used as decorators, will remove the whitespace around the
    function they are decorating, but also display that function in their
    representation.
    """
    def __init__(self, decorated_representation=''):
        self.decorated_representation = decorated_representation

    def __repr__(self):
        return 'surrounding_whitespace_removed({})'.format(
            decorated_representation
        )

    def __call__(self, function):
        self.decorated_representation = str(function)
        def decorated(self, *args, **kwargs):
            self._consume_whitespace()
            result = function(self, *args, **kwargs)
            self._consume_whitespace()
            return result

        return decorated
