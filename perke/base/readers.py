from os.path import dirname, isfile, join
from typing import List, Literal

import hazm

from perke.base.data_structures import Sentence
from perke.base.types import WordNormalizationMethod


class Reader:
    """
    Base Reader

    Attributes
    ----------
    word_normalization_method: `str`
        Word normalization method

    normalizer: `hazm.Normalizer`
        The hazm normalizer instance

    stemmer: `hazm.Stemmer`
        The hazm stemmer instance

    lemmatizer: `hazm.Lemmatizer`
        The hazm lemmatizer instance

    pos_tagger: `hazm.POSTagger`
        The hazm pos tagger instance
    """

    def __init__(self,
                 word_normalization_method: Literal[WordNormalizationMethod.enums],
                 ) -> None:
        """
        Initializes the reader.

        Parameters
        ----------
        word_normalization_method: `str`
            Word normalization method, see
            `perke.base.types.WordNormalizationMethod` for available
            methods.
        """
        self.word_normalization_method = word_normalization_method
        self.normalizer = hazm.Normalizer()
        self.stemmer = hazm.Stemmer()
        self.lemmatizer = hazm.Lemmatizer()
        model_filepath = join(dirname(dirname(__file__)),
                              'resources',
                              'postagger.model')
        self.pos_tagger = hazm.POSTagger(model=model_filepath)


class RawTextReader(Reader):
    """
    Reader for raw text

    Attributes
    ----------
    text: `str`
        Raw text to read sentences from
    """

    def __init__(self,
                 input: str,
                 word_normalization_method: Literal[WordNormalizationMethod.enums],
                 ) -> None:
        """
        Initializes the reader.

        Parameters
        ----------
        input: `str`
            Input, this can be either raw text or filepath.

        word_normalization_method: `str`
            Word normalization method, see
            `perke.base.types.WordNormalizationMethod` for available
            methods.
        """
        super().__init__(word_normalization_method)

        # If input is a filepath
        if isfile(input):
            with open(input) as file:
                self.text = file.read()

        # If input is raw text
        else:
            self.text = input

    def read(self) -> List[Sentence]:
        """
        Reads the input and uses hazm to preprocess.

        Returns
        -------
        sentences: `list[Sentence]`
            List of sentences
        """
        word_normalization_method = self.word_normalization_method
        normalized_text = self.normalizer.normalize(self.text)
        sentences = []
        for sentence in hazm.sent_tokenize(normalized_text):
            words = hazm.word_tokenize(sentence)
            pos_tags = [tag for _, tag in self.pos_tagger.tag(words)]

            if word_normalization_method == WordNormalizationMethod.stemming:
                normalized_words = [self.stemmer.stem(word) for word in words]

            elif word_normalization_method == WordNormalizationMethod.lemmatization:
                normalized_words = [self.lemmatizer.lemmatize(word)
                                    for word in words]

            # No normalization
            else:
                normalized_words = words

            sentence = Sentence(words, pos_tags, normalized_words)
            sentences.append(sentence)

        return sentences
