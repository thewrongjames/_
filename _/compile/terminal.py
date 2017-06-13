from .compile_ import compile_


def terminal():
    """
    A limited terminal for running line by line underscore. (Memory is retained
    accross lines).
    """

    compiled = compile_('42;')
    # compiled is just a ProgramNode, so...
    memory = compiled.memory

    print('Underscore:')

    while True:
        # The users will ctrl+c to get out.
        line = input('_> ')

        try:
            compiled = compile_(line)
        except Exception as error:
            print(repr(error))
            continue

        # Such that memory is retained...
        compiled.memory = memory

        try:
            compiled.run()
        except Exception as error:
            print(repr(error))
            continue

        for section_result in compiled.section_results:
            print(section_result);
