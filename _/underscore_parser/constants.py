import string

VALID_NAME_FIRST_CHARACTER_CHARACTERS = string.ascii_letters + '_-'
VALID_NAME_NON_FIRST_CHARACTER_CHARACTERS = \
    VALID_NAME_FIRST_CHARACTER_CHARACTERS + string.digits
RESERVED_NAMES = [
    'if',
    'else',
    'while',
    'template',
    'return',
    'true',
    'false',
    'function'
]
READ_ONLY_NAMES = ['container']
