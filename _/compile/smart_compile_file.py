import os
import pickle
from ..underscore_parser import UnderscoreParser
from .smart_compile_string import smart_compile_string


def smart_compile_file(
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
        program_string = file_.read()

    underscore_last_modified_time = os.path.getmtime(directory)
    # Start from assuming the pickle is older.
    pickle_last_modified_time = underscore_last_modified_time - 1

    file_name = str(directory).replace('\\', '/').split('/')[-1]
    directory_of_pickle = str(directory).split('.')[0] + '.pickle'

    try:
        with open(directory_of_pickle, 'rb') as pickle_file:
            unpickled_program_string = pickle_file.read()
    except FileNotFoundError:
        # There is no pickled version.
        unpickled_program_string = None
    else:
        pickle_last_modified_time = os.path.getmtime(directory_of_pickle)

    compiled, pickled = smart_compile_string(
        program_string=program_string,
        pickle_bytes_string=unpickled_program_string,
        underscore_last_modified_time=underscore_last_modified_time,
        pickle_last_modified_time=pickle_last_modified_time,
        force_pickle_update=force_pickle_update,
        memory_limit=memory_limit,
        time_limit=time_limit,
        running_underscore_standard_library=running_underscore_standard_library
    )

    # Write the newly compiled version to the pickle file.
    with open(str(directory_of_pickle), 'wb') as pickle_file:
        pickle_file.write(pickled)

    return compiled
