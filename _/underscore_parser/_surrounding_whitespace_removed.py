def _surrounding_whitespace_removed(function):
    def decorated(self, *args, **kwargs):
        self._consume_whitespace()
        result = function(self, *args, **kwargs)
        self._consume_whitespace()
        return result

    return decorated
