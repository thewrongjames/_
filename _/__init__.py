import os
import pickle
import time
from _.underscore_parser import UnderscoreParser


def compile_(
        program,
        memory_limit=None,
        time_limit=None,
):
    """
    Compiles underscore code (passed as a string to program) into a ProgramNode
    object which may be run (with the run method). Some errors will be found
    during compilation, and some at runtime.
    """
    program = str(program)
    parser = UnderscoreParser(program)
    compiled = parser.parse(
        memory_limit=memory_limit,
        time_limit=time_limit,
    )
    return compiled


def compile_file(directory, *args, **kwargs):
    """
    Compiles underscore code from a file at the directory passed as directory
    into a ProgramNode object which may be run (with the run method). Some
    errors will be found during compilation, and some at runtime.
    """
    with open(str(directory), 'r') as file_:
        program = file_.read()
    return compile_(program, *args, **kwargs)


def smart_compile(
        directory,
        memory_limit=None,
        time_limit=None,
        running_underscore_standard_library=False,
        force_pickle_update=False
):
    """
    Compiles underscore code, and saves a pickled version of the code alongside
    it. The next time it runs it, it attempts to parse it the same way it was
    the first time, and only searches for the parser when this fails. This will
    write over <file name before dot>.pickle, so, don't put anything important
    there.
    """
    with open(str(directory), 'r') as file_:
        program = file_.read()

    underscore_last_modified_time = os.path.getmtime(directory)
    # Start from assuming the pickle is older.
    pickle_last_modified_time = underscore_last_modified_time - 1

    file_name = str(directory).replace('\\', '/').split('/')[-1]
    directory_of_pickle = str(directory).split('.')[0] + '.pickle'

    try:
        with open(directory_of_pickle, 'rb') as pickle_file:
            unpickled_program = pickle.load(pickle_file)
        pickle_last_modified_time = os.path.getmtime(directory_of_pickle)
    except FileNotFoundError:
        # There is no pickled version.
        pickled_section_parser_list = []
    else:
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
        compiled = unpickled_program
    else:
        parser = UnderscoreParser(program)
        compiled = parser.parse(
            memory_limit=memory_limit,
            time_limit=memory_limit,
            running_underscore_standard_library=\
                running_underscore_standard_library,
            parsers_to_try_first=pickled_section_parser_list
        )

    # Write the newly compiled version to the pickle file.
    with open(str(directory_of_pickle), 'wb') as pickle_file:
        pickle.dump(compiled, pickle_file)

    return compiled
