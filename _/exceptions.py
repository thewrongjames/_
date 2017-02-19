class UnderscoreError(Exception):
    """
    Base language error, the super class for all other underscore errors, for
    catching all of them.
    """

    def __init__(self, message='', character_number=None):
        if character_number is not None:
            character_message = ' at character {} (ignoring spaces)'.format(
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
