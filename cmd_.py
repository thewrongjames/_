import sys
from _ import compile_file, terminal

# This is a command line interface for underscore.

if len(sys.argv) <= 1:
    # sys.argv[0] is the script name.
    # Run the terminal.
    terminal()
else:
    # If there are any arguments passed, attempt to compile_file the first one.
    compiled = compile_file(sys.argv[1])
    # Display the memory to the user.
    print(compiled.run())
