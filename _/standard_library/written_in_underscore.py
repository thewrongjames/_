import os
from ..compilers import compile_file


List = compile_file(
    os.path.dirname(__file__) + '/written_in_underscore/list._',
    running_underscore_standard_library=True
).run()['List']


WRITTEN_IN_UNDERSCORE = {
    'List': List
}
