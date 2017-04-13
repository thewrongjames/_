import time
from .exceptions import UnderscoreNameError, UnderscoreValueError, \
    UnderscoreTypeError


class ProgramNode:
    def __init__(self, sections, memory_limit=None, time_limit=None):
        self.sections = sections
        self.memory_limit = memory_limit
        self.time_limit = time_limit
        self.memory = {}
        self.pre_run_start_time = time.time()
        for section in self.sections:
            section.pre_run(
                memory=self.memory,
                memory_limit=self.memory_limit,
                time_limit=self.time_limit,
                start_time = self.pre_run_start_time
            )
        self.pre_run_time_taken = time.time() - self.pre_run_start_time
        if self.time_limit is not None:
            self.time_limit -= self.pre_run_time_taken

    def run(self):
        for section in self.sections:
            # The arguements are keyword arguments, because not all sections
            # will want all of these.
            section.run(
                memory=self.memory,
                memory_limit=self.memory_limit,
                time_limit=self.time_limit,
                start_time=time.time(),
            )
        return self.memory


class UnderscoreNode:
    def pre_run(*args, **kwargs):
        pass


class StatementNode(UnderscoreNode):
    def __init__(self, reference, expression):
        self.reference = reference
        self.expression = expression
        # Take of the last item such that running it gives you the memory
        # location you want to put the thing in.
        self.last_name = self.reference.names.pop(-1)

    def get_memory_to_write_to(self, memory):
        if self.reference.names == []:
            return memory
        memory_to_write_to = self.reference.run(memory)
        if not isinstance(memory_to_write_to, dict):
            raise UnderscoreNameError(
                '{} is not a memory location'.format(self.reference.name)
            )
        return memory_to_write_to

    def pre_run(self, memory, *args, **kwargs):
        """
        Templates are assigned first.
        """
        if isinstance(self.expression, TemplateFunctionNode):
            memory_to_write_to = self.get_memory_to_write_to(memory)
            memory_to_write_to[self.last_name] = self.expression.run(
                memory=memory,
                *args,
                **kwargs
            )

    def run(self, memory, *args, **kwargs):
        if not isinstance(self.expression, TemplateFunctionNode):
            memory_to_write_to = self.get_memory_to_write_to(memory)
            memory_to_write_to[self.last_name] = self.expression.run(
                memory,
                *args,
                **kwargs
            )


class ValueNode(UnderscoreNode):
    def __init__(self, value):
        self.value = value

    def run(self, *args, **kwargs):
        return self.value


class ReferenceNode(UnderscoreNode):
    def __init__(self, names, character):
        # Names should be a list containing either strings or tuples containing
        # TemplateFunctionNodes and any expressions passed to them.
        self.names = names
        self.character = character

    @property
    def name(self):
        return '.'.join([str(item) for item in self.names])

    def __str__(self):
        return self.name

    def run(self, memory, *args, **kwargs):
        error = UnderscoreNameError(
            "the name '{}' is not defined".format(
                '.'.join([str(item) for item in self.names])
            ),
            self.character
        )

        current_name = self.names[0]
        # Current name may be a TemplateFunctionNode or a ReferenceNode though.

        is_instantiation_or_call = False
        if isinstance(current_name, tuple):
            is_instantiation_or_call = True
            instance_or_call_value = TemplateInstantiateFunctionCallNode(\
                current_name[0], self.character, current_name[1]).run(memory=\
                memory)

        if len(self.names) == 1:
            if is_instantiation_or_call:
                return instance_or_call_value
            try:
                return memory[current_name]
            except KeyError:
                raise error

        # Otherwise, if there is more than one name...
        new_node = ReferenceNode(
            self.names[1:],
            self.character
        )

        if is_instantiation_or_call:
            if not isinstance(instance_or_call_value, dict):
                raise UnderscoreNameError(
                    '{} does not contain any names'.format(current_name),
                    self.character
                )
            return new_node.run(memory=instance_or_call_value)

        #Or, if the current one is not a node
        try:
            next_memory = memory[current_name]
        except KeyError:
            raise error
        try:
            return new_node.run(memory=next_memory)
        except UnderscoreNameError:
            raise UnderscoreNameError(
                '{} does not contain {}'.format(current_name, self.names[1]),
                self.character
            )


class TemplateFunctionNode(UnderscoreNode):
    """
    A function has returns=something.
    """
    def __init__(self, sections, returns, names):
        self.sections = sections
        self.returns = returns
        self.names = names

    def __str__(self):
        return self.__repr__()

    def run(self, memory, *args, **kwargs):
        class TemplateOrFunction:
            def __init__(
                    self,
                    sections,
                    returns,
                    names,
                    memory,
                    *args,
                    **kwargs
            ):
                self.sections = sections
                self.returns = returns
                self.names = names
                self.memory = memory
                self.args = args
                self.kwargs = kwargs

            def __call__(self, expressions=[]):
                if len(expressions) != len(self.names):
                    raise UnderscoreTypeError(
                        'number of expressions passed does not match number '
                        'required'

                    )
                internal_memory = {
                    'container': self.memory
                }
                values = [expression.run() for expression in expressions]
                for name, value in zip(self.names, values):
                    internal_memory[name] = value
                for section in self.sections:
                    section.pre_run(
                        memory=internal_memory,
                        *self.args,
                        **self.kwargs
                    )
                for section in self.sections:
                    section.run(
                        memory=internal_memory,
                        *self.args,
                        **self.kwargs
                    )
                if self.returns is not None:
                    return self.returns.run(
                        memory=internal_memory,
                        *self.args,
                        **self.kwargs
                    )
                return internal_memory
        return TemplateOrFunction(
            self.sections,
            self.returns,
            self.names,
            memory,
            *args,
            **kwargs
        )


class TemplateInstantiateFunctionCallNode(UnderscoreNode):
    """
    This is also used for function calls.
    """
    def __init__(self, template_or_function, character, expressions):
        # template_of_function may be a TemplateFunctionNode or a ReferenceNode.
        # character refers to the character that the program was up to when this
        # was parsed.
        self.template_or_function = template_or_function
        self.character = character
        self.expressions = expressions

    def run(self, memory, *args, **kwargs):
        if isinstance(self.template_or_function, ReferenceNode):
            template_or_function = self.template_or_function.run(memory)
            if not callable(template_or_function):
                raise UnderscoreValueError(
                    'reference is not callable',
                    self.character
                )
        else:
            template_or_function = self.template_or_function.run(
                *args, memory=memory, **kwargs
            )
        return template_or_function(self.expressions)


class MathNode(UnderscoreNode):
    def __init__(self, first_term, second_term):
        self.first_term = first_term
        self.second_term = second_term

    def run(self, memory, *args, **kwargs):
        first_value = self.first_term.run(memory)
        second_value = self.second_term.run(memory)
        return self.specific_maths(first_value, second_value)


class AdditionNode(MathNode):
    def specific_maths(self, first_value, second_value):
        try:
            return first_value + second_value
        except TypeError:
            raise UnderscoreTypeError(
                'Could not add {} to {}.'.format(
                    first_value,
                    second_value
                )
            )


class SubtractionNode(MathNode):
    def specific_maths(self, first_value, second_value):
        try:
            return first_value - second_value
        except TypeError:
            raise UnderscoreTypeError(
                'Could not subtract {} from {}.'.format(
                    second_value,
                    first_value
                )
            )


class MultiplicationNode(MathNode):
    def specific_maths(self, first_value, second_value):
        try:
            return first_value * second_value
        except TypeError:
            raise UnderscoreTypeError(
                'Could not multiply {} by {}.'.format(
                    first_value,
                    second_value
                )
            )


class DivisionNode(MathNode):
    def specific_maths(self, first_value, second_value):
        try:
            return first_value / second_value
        except TypeError:
            raise UnderscoreTypeError(
                'Could not divide {} by {}.'.format(
                    first_value,
                    second_value
                )
            )


class BooleanStatementNode(UnderscoreNode):
    def __init__(self, first_object, second_object):
        self.first_object = first_object
        self.second_object = second_object


class EqualityNode(BooleanStatementNode):
    def run(self, memory, *args, **kwargs):
        first_value = self.first_object.run(memory)
        second_value = self.second_object.run(memory)
        try:
            return first_value == second_value
        except:
            raise UnderscoreTypeError(
                'Could not compare {} and {}.'.format(
                    first_value,
                    second_value
                )
            )


class SmallerThanOrEqualToNode(BooleanStatementNode):
    def run(self, memory, *args, **kwargs):
        first_value = self.first_object.run(memory)
        second_value = self.second_object.run(memory)
        try:
            return first_value <= second_value
        except:
            raise UnderscoreTypeError(
                'Could not compare {} and {}.'.format(
                    first_value,
                    second_value
                )
            )


class SmallerThanNode(BooleanStatementNode):
    def run(self, memory, *args, **kwargs):
        first_value = self.first_object.run(memory)
        second_value = self.second_object.run(memory)
        try:
            return first_value < second_value
        except:
            raise UnderscoreTypeError(
                'Could not compare {} and {}.'.format(
                    first_value,
                    second_value
                )
            )


class GreaterThanOrEqualToNode(BooleanStatementNode):
    def run(self, memory, *args, **kwargs):
        first_value = self.first_object.run(memory)
        second_value = self.second_object.run(memory)
        try:
            return first_value >= second_value
        except:
            raise UnderscoreTypeError(
                'Could not compare {} and {}.'.format(
                    first_value,
                    second_value
                )
            )


class GreaterThanNode(BooleanStatementNode):
    def run(self, memory, *args, **kwargs):
        first_value = self.first_object.run(memory)
        second_value = self.second_object.run(memory)
        try:
            return first_value > second_value
        except:
            raise UnderscoreTypeError(
                'Could not compare {} and {}.'.format(
                    first_value,
                    second_value
                )
            )


class InequalityNode(BooleanStatementNode):
    def run(self, memory, *args, **kwargs):
        first_value = self.first_object.run(memory)
        second_value = self.second_object.run(memory)
        try:
            return first_value != second_value
        except:
            raise UnderscoreTypeError(
                'Could not compare {} and {}.'.format(
                    first_value,
                    second_value
                )
            )
