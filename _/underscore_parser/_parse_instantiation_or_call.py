from _ import nodes
from _ import exceptions
from ._surrounding_whitespace_removed import _surrounding_whitespace_removed

@_surrounding_whitespace_removed
def _parse_instantiation_or_call(self):
    """
    This will return either a reference node a template, or a function.
    These will be fed to a reference node which will work out what to do
    with them.
    """
    starting_position = self.position_in_program
    try:
        instantiation_or_call = self._parse_template()
    except exceptions.UnderscoreIncorrectParserError:
        try:
            instantiation_or_call = self._parse_function()
        except exceptions.UnderscoreIncorrectParserError:
            self.position_in_program = starting_position
            instantiation_or_call = nodes.ReferenceNode(
                [self._parse_single_name()],
                starting_position
            )
    # The below stuff should eventually be assigned to something.
    try:
        self._parse_passable_expressions()
    except exceptions.UnderscoreIncorrectParserError:
        self.position_in_program = starting_position
        raise
    return instantiation_or_call
