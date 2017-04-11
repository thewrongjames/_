import string

def _consume_whitespace(self):
    while (self._peek() is not None and self._peek() in string.whitespace):
        self._next()
