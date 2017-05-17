RUN_STRING_TESTS = True
RUN_FILE_TESTS = True

if RUN_STRING_TESTS:
    from .assignment import TestAssignment
    from .boolean_logic import TestBooleanStatements, TestBooleanExpressions
    from .control_structures import TestControlStructures
    from .functions import TestFunctions
    from .maths import TestMaths
    from .names import TestNames
    from .references import TestReferences
    from .syntax_errors import TestSyntaxErrors
    from .templates import TestTemplates
    from .comments import TestComments

if RUN_FILE_TESTS:
    from .file_tests import FileTests
