import sys
from time import time
from functools import wraps
from _.exceptions import UnderscoreOutOfMemoryError, UnderscoreOutOfTimeError


def limited(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        memory = kwargs.get('memory')
        time_limit = kwargs.get('time_limit')
        memory_limit = kwargs.get('memory_limit')

        if memory is not None and memory_limit is not None:
            if sys.getsizeof(memory) > memory_limit:
                raise UnderscoreOutOfMemoryError

        if time_limit is not None:
            if time() > time_limit:
                raise UnderscoreOutOfTimeError

        return function(*args, **kwargs)

    return wrapper
