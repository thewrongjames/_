from _ import nodes
from _ import exceptions
from ._whitespace import surrounding_whitespace_removed


@surrounding_whitespace_removed
def parse(self, memory_limit=None, time_limit=None):
    sections = self._parse_sections()
    return nodes.ProgramNode(sections, memory_limit, time_limit)


def parse_sections(self, break_at=[]):
    sections = []

    while True:
        if self._peek() is None:
            break
        should_break = False
        for item in break_at:
            if self._peek(len(item)) == item:
                should_break = True
        if should_break:
            break

        starting_position = self.position_in_program
        valid_parsers = [
            self._parse_statement,
            self._parse_expression,
            self._parse_control,
        ]
        none_worked_error = exceptions.UnderscoreCouldNotConsumeError(
            'found no parsable input'
        )
        parsed_something = False

        for parser in valid_parsers:
            try:
                sections.append(parser())
            except exceptions.UnderscoreIncorrectParserError:
                self.position_in_program = starting_position
            else:
                parsed_something = True
                break

        if not parsed_something:
            raise none_worked_error

    return sections
