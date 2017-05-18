from .casting import FloatCaster, IntegerCaster, BooleanCaster, StringCaster


STANDARD_LIBRARY = {
    'float': FloatCaster(),
    'integer': IntegerCaster(),
    'boolean': BooleanCaster(),
    'string': StringCaster()
}
