# -*- coding: utf-8 -*-

"""
Useful functions for the pke module.
"""


def char_offsets(text, sentence, tokens):
    """
    Calculates begin and end index of tokens of a sentence in a text

    Parameters
    ----------
    text: str
        The given text

    sentence: str
        The given sentences

    tokens: list
        List of tokens of the sentence

    Returns
    -------
        offsets: list
            List of tuples of begins and ends

    """
    sentence_index = text.index(sentence)
    offsets = []
    so_far = 0
    for i, token in enumerate(tokens):
        token_index = sentence_index + so_far + i
        so_far += len(token)
        offsets.append((token_index, token_index + len(token)))
    return offsets
