from ..nodes import ProgramNode
from ..exceptions import UnderscoreCouldNotConsumeError, \
    UnderscoreIncorrectParserError, UnderscoreSyntaxError
from ._whitespace import surrounding_whitespace_removed


@surrounding_whitespace_removed
def parse(
        self,
        memory_limit=None,
        time_limit=None,
        running_underscore_standard_library=False,
):
    sections = self._parse_sections()
    return ProgramNode(
        sections,
        memory_limit,
        time_limit,
        running_underscore_standard_library
    )


def parse_sections(self):
    sections = []
    valid_parsers = [
        self._parse_statement,
        self._parse_expression,
        self._parse_control,
        self._parse_return,
        self._parse_comment,
        self._parse_break_or_continue
    ]

    while True:
        if self._peek() is None:
            break

        if self._peek() == self.SECTIONS_END_CHARACTER:
            break

        starting_position = self.position_in_program
        parsed_something = False

        for parser in valid_parsers:
            try:
                sections.append(parser())
            except UnderscoreIncorrectParserError:
                self.position_in_program = starting_position
            else:
                parsed_something = True
                break

        if not parsed_something:
            raise UnderscoreCouldNotConsumeError(
                'encountered unparsable input',
                self.position_in_program
            )

    return sections
