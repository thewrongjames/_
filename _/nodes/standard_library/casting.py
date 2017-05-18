from _.exceptions import UnderscoreTypeError, UnderscoreValueError
from ..value_node import ValueNode
from .constants import BASIC_TYPES


class _Caster:
    def __str__(self, memory):
        return self.TYPE + '_caster'

    def __call__(self, memory_from_call_location, expressions=[]):
        if len(expressions) != 1:
            raise UnderscoreTypeError(
                '{} expressions passed, {} required'.format(
                    len(expressions),
                    1
                )
            )

        value_to_cast = expressions[0].run(memory_from_call_location)
        cannot_cast_error = UnderscoreValueError(
            'could not cast {} to {}'.format(
                expressions[0],
                self.TYPE
            )
        )

        if type(value_to_cast) in BASIC_TYPES:
            try:
                return self.PYTHON_CASTER(value_to_cast)
            except ValueError:
                raise cannot_cast_error

        if not isinstance(value_to_cast, dict):
            # If it is not a basic type, and it is not a template instance, it
            # cannot be cast. (i.e. it is an uncalled function or template).
            raise cannot_cast_error

        try:
            return value_to_cast['__' + self.TYPE]({}, [])
        except UnderscoreTypeError as error:
            if error.args[0] == 'number of expressions passed does not match '\
                    'number required':
                # If their definition of the caster requires arguments the error
                # will have the above message.
                raise UnderscoreTypeError(
                    '{} method must take 0 arguments'.format('__' + self.TYPE)
                )
            # Otherwise, this is just a problem with their function that they
            # need to see.
            raise error
        except KeyError:
            # If the casting magic method is not defined, the template instance
            # cannot be cast.
            raise cannot_cast_error


class FloatCaster(_Caster):
    TYPE = 'float'
    PYTHON_CASTER = float


class IntegerCaster(_Caster):
    TYPE = 'integer'
    PYTHON_CASTER = int


class BooleanCaster(_Caster):
    TYPE = 'boolean'
    PYTHON_CASTER = bool


class StringCaster(_Caster):
    TYPE = 'string'
    PYTHON_CASTER = str
