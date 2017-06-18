import pickle
from ..underscore_parser import UnderscoreParser
from ..nodes import ProgramNode


def smart_compile_string(
    program_string,
    pickle_bytes_string=None,
    underscore_last_modified_time=0,
    pickle_last_modified_time=0,
    force_pickle_update=False,
    memory_limit=None,
    time_limit=None,
    running_underscore_standard_library=False,
):
    """
    This takes a program string, a bytes string of a pickled program node, the
    last modified times of each, and a
    """
    pickled_section_parser_list = []

    if pickle_bytes_string is not None:
        try:
            unpickled_program = pickle.loads(pickle_bytes_string)
        except (TypeError, pickle.UnpicklingError):
            raise ValueError('invalide pickle_bytes_string')

        if not isinstance(unpickled_program, ProgramNode):
            raise ValueError('invalide pickle_bytes_string')

        def recursively_build_sections_list(node):
            try:
                sections = node.sections
            except AttributeError:
                return []
            section_list = []
            for section in node.sections:
                try:
                    second_parser = section.SECOND_PARSER
                except AttributeError:
                    second_parser = None
                section_list.append(
                    (
                        section.FIRST_PARSER,
                        second_parser,
                        recursively_build_sections_list(section)
                    )
                )
            return section_list

        # Construct a list of the parsers from the previous ProgramNode.
        pickled_section_parser_list = recursively_build_sections_list(
            unpickled_program
        )

    # If the pickle has been modified more recently than the underscore program
    # it represents, then it should be up to date, and can be used instead of
    # compiling the program.
    if (
            (pickle_last_modified_time > underscore_last_modified_time) and
            not force_pickle_update
    ):
        # This if statement can only be entered if the try statement
        # successfully got past the assignment of unpickled_program.
        return unpickled_program, pickle_bytes_string
    else:
        parser = UnderscoreParser(program_string)
        compiled = parser.parse(
            memory_limit=memory_limit,
            time_limit=memory_limit,
            running_underscore_standard_library=\
                running_underscore_standard_library,
            parsers_to_try_first=pickled_section_parser_list
        )
        return compiled, pickle.dumps(compiled)
