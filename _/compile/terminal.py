from .compile_ import compile_


def terminal():
    """
    A limited terminal for running line by line underscore. (Memory is retained
    accross lines).
    """

    compiled = compile_('42;')
    # compiled is just a ProgramNode, so...
    memory = compiled.memory

    print('Underscore (ctrl+c to exit):')

    while True:
        # The users will ctrl+c to get out.
        try:
            line = input('_> ')
        except KeyboardInterrupt:
            break;

        try:
            compiled = compile_(line)
        except Exception as error:
            print(repr(error))
            continue

        # Such that memory is retained...
        compiled.memory = memory
        section_results = []

        for section in compiled.sections:
            try:
                pre_run_result = section.pre_run(
                    memory=memory,
                    running_underscore_standard_library=False
                )
                run_result = section.run(
                    memory=memory,
                    running_underscore_standard_library=False
                )
            except Exception as error:
                print(repr(error))
                continue
            else:
                if pre_run_result is not None:
                    section_result.append(pre_run_result)
                if run_result is not None:
                    section_results.append(run_result)

        for section_result in section_results:
            print(section_result);
