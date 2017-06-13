class UnderscoreError(Exception):
    """
    Base language error, the super class for all other underscore errors, for
    catching all of them.
    """

    def __init__(self, message='', character_number=None):
        if character_number is not None:
            character_message = ' at character {}'.format(
                character_number
            )
        else:
            character_message = ''
        super(UnderscoreError, self).__init__(message+character_message)


class UnderscoreIncorrectParserError(UnderscoreError):
    """
    Raised by parser functions that know that they are not meant to parse what
    they have been given.
    """
    pass


class UnderscoreNotImplementedError(UnderscoreIncorrectParserError):
    """
    If the parser does not exist. Of course it is not meant to parse what it has
    been given.
    """
    pass


class UnderscoreSyntaxError(UnderscoreError):
    """
    UnderscoreSyntaxErrors should be raised if the parser cannot parse the
    code, but it also cannot be anything else.
    """
    pass


class UnderscoreCouldNotConsumeError(UnderscoreError):
    """
    The error raised if a method expects to be able to consume something but
    can't.
    """
    pass


class UnderscoreNameError(UnderscoreError):
    pass


class UnderscoreValueError(UnderscoreError):
    pass


class UnderscoreTypeError(UnderscoreError):
    pass


class UnderscoreReturnError(UnderscoreError):
    """
    UnderscoreReturnError is raised when a ReturnNode is run, any containing
    functions will catch it, but, if it is not caught, the user will see it
    (they placed a return outside of a function).
    """

    def __init__(self, expression_to_return, *args, **kwargs):
        self.expression_to_return = expression_to_return
        super(UnderscoreError, self).__init__(*args, **kwargs)


class UnderscoreBreakError(UnderscoreError):
    """
    UnderscoreBreakError is raised when a BreakNode is run, any containing while
    loops will catch it, but, if it is not caught, the user will see it (they
    placed a break outside of a while loop).
    """
    pass


class UnderscoreContinueError(UnderscoreError):
    """
    UnderscoreContinueError is raised when a ContinueNode is run, any containing
    while loops will catch it, but, if it is not caught, the user will see it
    (they placed a continue outside of a while loop).
    """
    pass


class UnderscoreIncorrectNumberOfArgumentsError(UnderscoreTypeError):
    """
    This is raised whenever a template or function is called with the incorrect
    number of arguments.
    """
    pass


class  UnderscoreOutOfTimeError(UnderscoreError):
    pass


class UnderscoreOutOfMemoryError(UnderscoreError):
    pass
