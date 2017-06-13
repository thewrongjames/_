import sys
from _ import smart_compile_file


if len(sys.argv) >= 2:
    # sys.argv[0] is the script name.
    if sys.argv[1] == 'terminal':
        # Run the terminal.
        from _ import terminal
        terminal()
    else:
        # Attempt to run the file passed to script...
        compiled = smart_compile_file(sys.argv[1])
        # Display the memory to the user.
        print(compiled.run())
