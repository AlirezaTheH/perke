from dataclasses import (dataclass,
                         field)
from typing import (Literal,
                    List)


@dataclass
class Sentence:
    """
    The sentence data structure

    Attributes
    ----------
    words: `List[str]`
        List of words

    pos_tags: `List[str]`
        List of part of speech tags assigned to words

    normalized_words: `List[str]`
        List of normalized of words
    """

    words: List[str]
    pos_tags: List[str]
    normalized_words: List[str]

    @property
    def length(self):
        """
        Gets number of words

        Returns
        -------
        length: `int`
            Number of words
        """

        return len(self.words)


@dataclass
class Candidate:
    """
    The keyphrase candidate data structure

    Attributes
    ----------
    all_words: `list[list[str]]`
        Nested list of words, each words list in the list corresponds to
        one of the candidate occurrence.

    offsets: `list[list[int]]`
        List of offsets of each occurrence.

    all_pos_tags: `list[list[str]]`
        Nested list of pos tags, each pos tags list in the list
        corresponds to one of the candidate occurrence.

    normalized_words: `list[str]`
        List of normalized of words, all occurrences have the same
        list of normalized words.

    weight: `float`
        Candidate weight in weighting algorithms.
    """

    all_words: list = field(default_factory=list)
    offsets: list = field(default_factory=list)
    all_pos_tags: list = field(default_factory=list)
    normalized_words: list = field(default_factory=list)
    weight: float = 0

    @property
    def length(self) -> int:
        """
        Gets number of normalized words

        Returns
        -------
        length: `int`
            Number of normalized words
        """

        return len(self.normalized_words)

    def add_occurrence(self,
                       words: List[str],
                       offset: int,
                       pos_tags: List[str],
                       normalized_words: List[str]
                       ) -> None:
        """
        Adds a new occurrence to the candidate.

        Parameters
        ----------
        words: `list[str]`
            List of words of the occurrence

        offset: `int`
            The offset of the occurrence

        pos_tags: `list[str]`
            List of part of speech tags assigned to words of the
            occurrence

        normalized_words: `list[str]`
            List of normalized of words of the occurrence
        """
        self.all_words.append(words)
        self.offsets.append(offset)
        self.all_pos_tags.append(pos_tags)
        self.normalized_words = normalized_words
