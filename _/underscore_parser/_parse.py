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
        parsers_to_try_first=[]
):
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

    if trying_specific_parsers:
        PARSER_METHODS = {
            '_parse_statement': self._parse_statement,
            '_parse_expression': self._parse_expression,
            '_parse_control': self._parse_control,
            '_parse_return': self._parse_return,
            '_parse_comment': self._parse_comment,
            '_parse_break_or_continue': self._parse_break_or_continue,
            '_parse_function_or_template': self._parse_function_or_template,
            '_parse_and_or_or': self._parse_and_or_or,
            '_parse_not': self._parse_not,
            '_parse_comparison': self._parse_comparison,
            '_parse_addition_or_subtraction': \
                self._parse_addition_or_subtraction,
            '_parse_term': self._parse_term,
            '_parse_reference': self._parse_reference,
            None: None
        }
        parser_methods_to_try_first = []

        for first_parser_name, second_parser_name, _ in parsers_to_try_first:
            parser_methods_to_try_first.append(
                (
                    PARSER_METHODS[first_parser_name],
                    PARSER_METHODS[second_parser_name]
                )
            )
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
                # Parsers methods to try first contains a tuple, the first one
                # beign the parser to try at the expression level, and the next
                # one for the next level down.
                sections.append(
                    parser_methods_to_try_first[index_in_specific_parsers][0](
                        second_parser=parser_methods_to_try_first[\
                            index_in_specific_parsers][1],
                        next_parsers_to_try_first=parsers_to_try_first[\
                            index_in_specific_parsers][2]
                    )
                )
            except (UnderscoreIncorrectParserError, UnderscoreSyntaxError):
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

        # If you aren't trying to parse something specific, just loop through
        # them (in order (importantly)) and see what you can parse. This needs
        # to be another if statement, as, it might have realised it can't parse
        # what it wants to just above, and if this isn't run, then it will see
        # that it couldn't parse anything and raise a could not consume error.
        if not trying_specific_parsers:
            # starting_position needs to be updated though as some of the
            # specific parsers may have worked, and may have moved it forwards.
            starting_position=self.position_in_program
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
