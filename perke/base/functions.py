def is_alphanumeric(word: str, valid_punctuation_marks: str = '-') -> bool:
    """
    Check if a word contains only alpha-numeric
    characters and valid punctuation marks.

    Parameters
    ----------
    word: `str`
        The given word

    valid_punctuation_marks: `str`
        Punctuation marks that are valid, defaults to `'-'`.

    Returns
    -------
    result: `bool`
        The result
    """

    for punctuation_mark in valid_punctuation_marks.split():
        word = word.replace(punctuation_mark, '')
    return word.isalnum()
