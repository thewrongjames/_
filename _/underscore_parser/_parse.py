from _.nodes import ProgramNode
from _.exceptions import UnderscoreCouldNotConsumeError, \
    UnderscoreIncorrectParserError
from ._whitespace import surrounding_whitespace_removed


@surrounding_whitespace_removed
def parse(self, memory_limit=None, time_limit=None):
    sections = self._parse_sections()
    return ProgramNode(sections, memory_limit, time_limit)


def parse_sections(self, stop_parsing_section_at=[]):
    sections = []

    while True:
        if self._peek() is None:
            break

        # This is currently only used for '}' at the end of controls, functions
        # and templates, but could potentially have more uses.
        should_stop_parsing_sections_now = False
        for item in stop_parsing_section_at:
            if self._peek(len(item)) == item:
                should_stop_parsing_sections_now = True
        if should_stop_parsing_sections_now:
            break

        starting_position = self.position_in_program

        valid_parsers = [
            self._parse_statement,
            self._parse_expression,
            self._parse_control,
            self._parse_return,
            self._parse_comment,
            self._parse_break_or_continue
        ]
        
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
