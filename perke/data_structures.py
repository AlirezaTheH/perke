# -*- coding: utf-8 -*-

"""
Data structures for the perke module.
"""


class Sentence(object):
    """
    The sentence data structure.

    Attributes
    ----------
    words: list
        List of words (tokens) in the sentence

    pos: list
        List of Part-Of-Speeches

    stems: list
        List of stems

    length: int
        Length (number of tokens) of the sentence

    meta: dict
        Meta-information of the sentence
    """

    def __init__(self, words):

        self.words = words
        self.pos = []
        self.stems = []
        self.length = len(words)
        self.meta = {}

    def __eq__(self, other):
        """
        Compares two sentences for equality.

        Parameters
        ----------
        other: Sentence
            The other sentence
        """

        # Test whether they are instances of different classes
        if type(self) != type(other):
            return False

        # Test whether they are of same length
        if self.length != other.length:
            return False

        # Test whether they have the same words
        if self.words != other.words:
            return False

        # Test whether they have the same PoS tags
        if self.pos != other.pos:
            return False

        # Test whether they have the same stem forms
        if self.stems != other.stems:
            return False

        # Test whether they have the same meta-information
        if self.meta != other.meta:
            return False

        # If everything is ok then they are equal
        return True


class Candidate(object):
    """
    The keyphrase candidate data structure.

    Attributes
    ----------
    surface_forms: list
        The surface forms of the candidate

    offsets: list
        The offsets of the surface forms

    sentence_ids: list
        The sentence id of each surface form

    pos_patterns: list
        The Part-Of-Speech patterns of the candidate

    lexical_form: list
        The lexical form of the candidate
    """

    def __init__(self):

        self.surface_forms = []
        self.offsets = []
        self.sentence_ids = []
        self.pos_patterns = []
        self.lexical_form = []


class Document(object):
    """
    The Document data structure.

    Attributes
    ----------
    input_file: str
        The path of the input file
    sentences: list
        The sentence container (list of Sentence)
    """

    def __init__(self):

        self.input_file = None
        self.sentences = []

    @staticmethod
    def from_sentences(sentences, **kwargs):
        """
        Populate the sentence list.

        Parameters
        ----------
        sentences: list
            Content to create the document.
        input_file: str
            Path to the input file.
        """

        # Initialize document
        doc = Document()

        # Set the input file
        doc.input_file = kwargs.get('input_file', None)

        # Loop through the parsed sentences
        for i, sentence in enumerate(sentences):

            # Add the sentence to the container
            s = Sentence(words=sentence['words'])

            # Add the POS
            s.pos = sentence['POS']

            # Add the lemmas
            s.stems = sentence['lemmas']

            # Add the meta-information
            for (k, infos) in sentence.items():
                if k not in {'POS', 'lemmas', 'words'}:
                    s.meta[k] = infos

            # Add the sentence to the document
            doc.sentences.append(s)

        return doc

    def __eq__(self, other):
        """
        Compares two documents for equality.

        Parameters
        ----------
        other: Document
            The other document
        """

        # Test whether they are instances of different classes
        if type(self) != type(other):
            return False

        # Test whether they have the same input path
        if self.input_file != other.input_file:
            return False

        # Test whether they contain the same lists of sentences
        if self.sentences != other.sentences:
            return False

        # If everything is ok then they are equal
        return True
