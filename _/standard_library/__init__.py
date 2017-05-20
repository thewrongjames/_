from .casting import FloatCaster, IntegerCaster, BooleanCaster, StringCaster
from .written_in_underscore import List


STANDARD_LIBRARY = {
    'float': FloatCaster(),
    'integer': IntegerCaster(),
    'boolean': BooleanCaster(),
    'string': StringCaster(),
    'List': List
}
