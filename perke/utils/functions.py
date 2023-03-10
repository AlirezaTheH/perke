def is_alphanumeric(word: str, valid_punctuation_marks: str = '-') -> bool:
    """
    Check if a word contains only alphanumeric
    characters and valid punctuation marks.

    Parameters
    ----------
    word:
        The given word

    valid_punctuation_marks:
        Punctuation marks that are valid, defaults to `'-'`.

    Returns
    -------
    The result
    """
    for punctuation_mark in valid_punctuation_marks.split():
        word = word.replace(punctuation_mark, '')
    return word.isalnum()
