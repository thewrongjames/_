from string import whitespace


def consume_whitespace(self):
    while (self._peek() is not None and self._peek() in whitespace):
        self.position_in_program += 1


def surrounding_whitespace_removed(function):
    def decorated(self, *args, **kwargs):
        self._consume_whitespace()
        result = function(self, *args, **kwargs)
        self._consume_whitespace()
        return result

    return decorated
