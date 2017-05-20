import _.nodes.ProgramNode
from _.exceptions import UnderscoreCouldNotConsumeError, \
    UnderscoreIncorrectParserError
from ._whitespace import surrounding_whitespace_removed


@surrounding_whitespace_removed
def parse(
        self,
        memory_limit=None,
        time_limit=None,
        include_standard_library=True,
        parsers_to_try_first=[]
):
    sections = self._parse_sections(parsers_to_try_first=parsers_to_try_first)
    return ProgramNode(
        sections,
        memory_limit,
        time_limit,
        include_standard_library
    )


def parse_sections(self, stop_parsing_section_at=[], parsers_to_try_first=[]):
    sections = []
    valid_parsers = [
        self._parse_statement,
        self._parse_expression,
        self._parse_control,
        self._parse_return,
        self._parse_comment,
        self._parse_break_or_continue
    ]
    trying_specific_parsers = False
    if parsers_to_try_first:
        parser_methods = {
            '_parse_statement': self._parse_statement,
            '_parse_expression': self._parse_expression,
            '_parse_control': self._parse_control,
            '_parse_return': self._parse_return,
            '_parse_comment': self._parse_comment,
            '_parse_break_or_continue': self._parse_break_or_continue
        }
        parser_methods_to_try_first = [
            parser_methods(parser_name) for parser_name in parsers_to_try_first
        ]
        trying_specific_parsers = True
        index_in_specific_parsers = 0

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

        parsed_something = False

        if trying_specific_parsers:
            try:
                sections.append(
                    parser_methods_to_try_first[index_in_specific_parsers]
                )
            except UnderscoreIncorrectParserError:
                self.position_in_program = starting_position
                # Stop trying to parse specific parsers:
                trying_specific_parsers = False
            else:
                index_in_specific_parsers += 1
                parsed_something = True
        else:
         # If you aren't trying to parse something specific, just loop through
         # them (in order (importantly)) and see what you can parse.
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
