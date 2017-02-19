def add_dictionaries(dictionary1, dictionary2):
    """
    Please note, if any of the keys are common to both values, in the dictionary
    output, the values will be those in dictionary2.
    """
    return dict(list(dictionary1.items()) + list(dictionary2.items()))
