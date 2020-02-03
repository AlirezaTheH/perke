# -*- coding: utf-8 -*-

"""
Readers for the perke module.
"""
import os

import hazm

from perke.data_structures import Document
from perke.utils import char_offsets


class Reader(object):
    def read(self, path):
        raise NotImplementedError


class RawTextReader(Reader):
    """
    Reader for raw text
    """

    def __init__(self):
        pass

    def read(self, text, **kwargs):
        """
        Read the input file and use hazm to pre-process.

        Parameters
        ----------
            text: str
                Raw text to pre-process.
        """

        normalizer = hazm.Normalizer()
        normalized_text = normalizer.normalize(text)

        lemmatizer = hazm.Lemmatizer()
        model_path = os.path.join(os.path.dirname(__file__), 'resources/postagger.model')
        tagger = hazm.POSTagger(model=model_path)
        sentences = []
        for sentence_id, sentence in enumerate(hazm.sent_tokenize(normalized_text)):
            tokens = hazm.word_tokenize(sentence)
            sentences.append({
                "words": tokens,
                "lemmas": [lemmatizer.lemmatize(token) for token in tokens],
                "POS": [tagged_token[1] for tagged_token in tagger.tag(tokens)],
                "char_offsets": char_offsets(normalized_text, sentence, tokens)
            })

        doc = Document.from_sentences(sentences,
                                      input_file=kwargs.get('input_file', None),
                                      **kwargs)

        return doc
