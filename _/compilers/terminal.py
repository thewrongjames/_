from .compile_ import compile_


def _get_formatted_error(error):
    return str(repr(error)).replace('(', ': ').replace('\'', '').\
        replace(',)', '').replace('"', '')


def terminal():
    """
    A limited terminal for running line by line underscore. (Memory is retained
    accross lines).
    """

    compiled = compile_('42;')
    # compiled is just a ProgramNode, so...
    memory = compiled.memory
    exit = False

    print('\nUnderscore (ctrl+c to exit):')

    while True:
        section = ''

        # Get the whole section (only run once the press enter on an empty
        # line).
        while True:
            prompt = '_> ' if len(section) == 0 else '__ '

            try:
                line = input(prompt)
            except (KeyboardInterrupt, EOFError):
                # The users will ctrl+c to get out.
                print()
                exit = True
                break
            else:
                section += line
            if len(line) == 0 or (section == line and line[-1] == ';'):
                break

        if exit:
            break

        try:
            compiled = compile_(section)
        except Exception as error:
            print(_get_formatted_error(error))
            continue

        # Such that memory is retained...
        compiled.memory = memory
        section_results = []

        for section in compiled.sections:
            try:
                pre_run_result = section.pre_run(
                    memory=memory,
                    time_limit=None,
                    memory_limit=None,
                    running_underscore_standard_library=False
                )
                run_result = section.run(
                    memory=memory,
                    time_limit=None,
                    memory_limit=None,
                    running_underscore_standard_library=False
                )
            except Exception as error:
                print(_get_formatted_error(error))
                continue
            else:
                if pre_run_result is not None:
                    section_result.append(pre_run_result)
                if run_result is not None:
                    section_results.append(run_result)

        for section_result in section_results:
            print(section_result['__display']());
