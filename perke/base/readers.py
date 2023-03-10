from os.path import dirname, join
from pathlib import Path
from typing import List

import hazm

from perke.base.data_structures import Sentence
from perke.base.types import WordNormalizationMethod


class Reader:
    """
    Base Reader

    Attributes
    ----------
    word_normalization_method:
        Word normalization method

    normalizer:
        The hazm normalizer instance

    stemmer:
        The hazm stemmer instance

    lemmatizer:
        The hazm lemmatizer instance

    pos_tagger:
        The hazm pos tagger instance
    """

    def __init__(
        self, word_normalization_method: WordNormalizationMethod
    ) -> None:
        """
        Initializes the reader.

        Parameters
        ----------
        word_normalization_method:
            Word normalization method, see
            `perke.base.types.WordNormalizationMethod` for available
            methods.
        """
        self.word_normalization_method: WordNormalizationMethod = (
            word_normalization_method
        )
        self.normalizer: hazm.Normalizer = hazm.Normalizer()
        self.stemmer: hazm.Stemmer = hazm.Stemmer()
        self.lemmatizer: hazm.Lemmatizer = hazm.Lemmatizer()
        model_filepath = join(
            dirname(dirname(__file__)), 'resources', 'postagger.model'
        )
        self.pos_tagger: hazm.POSTagger = hazm.POSTagger(model=model_filepath)


class RawTextReader(Reader):
    """
    Reader for raw text

    Attributes
    ----------
    text:
        Raw text to read sentences from
    """

    def __init__(
        self,
        input: str,
        word_normalization_method: WordNormalizationMethod,
    ) -> None:
        """
        Initializes the reader.

        Parameters
        ----------
        input:
            Input, this can be either raw text or filepath.

        word_normalization_method:
            Word normalization method, see
            `perke.base.types.WordNormalizationMethod` for available
            methods.
        """
        super().__init__(word_normalization_method)

        # If input is a filepath
        if isinstance(input, Path):
            assert input.exists()
            with open(input, encoding='utf-8') as file:
                self.text: str = file.read()

        # If input is raw text
        else:
            self.text: str = input

    def read(self) -> List[Sentence]:
        """
        Reads the input and uses hazm to preprocess.

        Returns
        -------
        List of sentences
        """
        word_normalization_method = self.word_normalization_method
        normalized_text = self.normalizer.normalize(self.text)
        sentences = []
        for sentence in hazm.sent_tokenize(normalized_text):
            words = hazm.word_tokenize(sentence)
            pos_tags = [tag for _, tag in self.pos_tagger.tag(words)]

            if word_normalization_method == 'stemming':
                normalized_words = [self.stemmer.stem(word) for word in words]

            elif word_normalization_method == 'lemmatization':
                normalized_words = [
                    self.lemmatizer.lemmatize(word) for word in words
                ]

            # No normalization
            else:
                normalized_words = words

            sentence = Sentence(words, pos_tags, normalized_words)
            sentences.append(sentence)

        return sentences
