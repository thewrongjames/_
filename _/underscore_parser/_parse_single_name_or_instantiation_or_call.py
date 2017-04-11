from _ import exceptions

def _parse_single_name_or_instantiation_or_call(self):
    starting_position = self.position_in_program
    try:
        return self._parse_instantiation_or_call()
    except exceptions.UnderscoreIncorrectParserError:
        self.position_in_program = starting_position
        return self._parse_single_name()
