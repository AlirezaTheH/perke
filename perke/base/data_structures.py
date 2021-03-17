class Sentence:
    """
    The sentence data structure

    Attributes
    ----------
    words: list
        List of words

    pos_tags: list
        List of part of speech tags assigned to words

    normalized_words: list
        List of normalized of words
    """

    def __init__(self, words, pos_tags, normalized_words):
        """
        Initializes the sentence.

        Parameters
        ----------
        words: list
            List of words

        pos_tags: list
            List of part of speech tags assigned to words

        normalized_words: list
            List of normalized of words
        """

        self.words = words
        self.pos_tags = pos_tags
        self.normalized_words = normalized_words

    @property
    def length(self):
        """
        Gets number of words

        Returns
        -------
        length: int
            Number of words
        """

        return len(self.words)


class Candidate:
    """
    The keyphrase candidate data structure

    Attributes
    ----------
    all_words: list
        Nested list of words, each words list in the list corresponds to
        one of the candidate occurrence.

    offsets: list
        List of offsets of each occurrence.

    all_pos_tags: list
        Nested list of pos tags, each pos tags list in the list
        corresponds to one of the candidate occurrence.

    normalized_words: list
        List of normalized of words, all occurrences have the same
        list of normalized words.

    weight: float
        Candidate weight in weighting algorithms.
    """

    def __init__(self):
        """
        Initializes the candidate.
        """

        self.all_words = []
        self.offsets = []
        self.all_pos_tags = []
        self.normalized_words = []
        self.weight = 0.

    @property
    def length(self):
        """
        Gets number of normalized words

        Returns
        -------
        length: int
            Number of normalized words
        """

        return len(self.normalized_words)

    def add_occurrence(self, words, offset, pos_tags, normalized_words):
        """
        Adds a new occurrence to the candidate.

        Parameters
        ----------
        words: list
            List of words of the occurrence

        normalized_words: list
            List of normalized of words of the occurrence

        pos_tags: list
            List of part of speech tags assigned to words of the
            occurrence

        offset: int
            The offset of the occurrence
        """
        self.all_words.append(words)
        self.offsets.append(offset)
        self.all_pos_tags.append(pos_tags)
        self.normalized_words = normalized_words
