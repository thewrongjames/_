RUN_STRING_TESTS = False
RUN_FILE_TESTS = True

if RUN_STRING_TESTS:
    from .assignment import TestAssignment
    from .boolean_statements import TestBooleanStatements
    from .control_structures import TestControlStructures
    from .functions import TestFunctions
    from .maths import TestMaths
    from .names import TestNames
    from .references import TestReferences
    from .syntax_errors import TestSyntaxErrors
    from .templates import TestTemplates

if RUN_FILE_TESTS:
    from .file_tests import FileTests
