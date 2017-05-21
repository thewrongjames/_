from _.nodes import ProgramNode
from _.exceptions import UnderscoreCouldNotConsumeError, \
    UnderscoreIncorrectParserError
from ._whitespace import surrounding_whitespace_removed


@surrounding_whitespace_removed
def parse(
        self,
        memory_limit=None,
        time_limit=None,
        running_underscore_standard_library=False,
        parsers_to_try_first=[]
):
    print(4, parsers_to_try_first)
    sections = self._parse_sections(parsers_to_try_first=parsers_to_try_first)
    return ProgramNode(
        sections,
        memory_limit,
        time_limit,
        running_underscore_standard_library
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
    # Smart compiling stuff:
    trying_specific_parsers = bool(parsers_to_try_first)
    print(parsers_to_try_first)
    if trying_specific_parsers:
        print(0)
        PARSER_METHODS = {
            '_parse_statement': self._parse_statement,
            '_parse_expression': self._parse_expression,
            '_parse_control': self._parse_control,
            '_parse_return': self._parse_return,
            '_parse_comment': self._parse_comment,
            '_parse_break_or_continue': self._parse_break_or_continue
        }
        parser_methods_to_try_first = []
        for parser_name, contained_parsers_to_try_first in \
                parsers_to_try_first:
            parser_methods_to_try_first.append(
                (PARSER_METHODS[parser_name], contained_parsers_to_try_first)
            )
        index_in_specific_parsers = 0
        print(parser_methods_to_try_first)
    print(1)

    while True:
        if self._peek() is None:
            print(5)
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
            print(2)
            try:
                # parser_methods_to_try_first[index] is a tuple containing the
                # parser to try now, and then a list of parsers to try within
                # that later on.
                print(parser_methods_to_try_first, index_in_specific_parsers)
                sections.append(
                    parser_methods_to_try_first[index_in_specific_parsers][0]()
                )
            except UnderscoreIncorrectParserError:
                self.position_in_program = starting_position
                # If it failed to parse it, stop trying to parse specific
                # parsers:
                trying_specific_parsers = False
            else:
                if (
                        index_in_specific_parsers >=
                        len(parser_methods_to_try_first) - 1
                ):
                    # The list of specific parsers has run out, but, perhaps
                    # they have added something on the end.
                    trying_specific_parsers = False
                else:
                    index_in_specific_parsers += 1
                parsed_something = True
        else:
            print(3)
         # If you aren't trying to parse something specific, just loop through
         # them (in order (importantly)) and see what you can parse.
            for parser in valid_parsers:
                print(parser)
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
