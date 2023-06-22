import logging
from collections import defaultdict
from pathlib import Path
from typing import Callable, DefaultDict, List, Optional, Set, Tuple, Union

import hazm
import nltk

from perke.base.data_structures import Candidate, Sentence
from perke.base.readers import RawTextReader
from perke.base.types import WordNormalizationMethod
from perke.utils.functions import is_alphanumeric
from perke.utils.string import punctuation_marks


class Extractor:
    """
    Base extractor, provides base functions for all extractors.

    Attributes
    ----------
    word_normalization_method:
        Word normalization method.

    sentences:
        List of sentence objects of the text

    candidates:
        Dict of canonical forms of candidates to candidates, canonical
        form of a candidate is a string joined from normalized words of
        the candidate.

    stopwords:
        Set of stopwords

    valid_pos_tags:
        Set of valid part of speech tags.
    """

    def __init__(self, valid_pos_tags: Optional[Set[str]] = None) -> None:
        """
        Initializes the extractor.

        Parameters
        ----------
        valid_pos_tags:
            Set of valid part of speech tags, defaults to nouns and
            adjectives. I.e. `{'NOUN', 'ADJ'}`.
        """
        self.word_normalization_method: Optional[str] = None
        self.sentences: List[Sentence] = []
        self.candidates: DefaultDict[str, Candidate] = defaultdict(Candidate)
        self.stopwords: Set[str] = set(hazm.stopwords_list()) | set(
            punctuation_marks
        )
        if valid_pos_tags is None:
            valid_pos_tags = {'NOUN', 'ADJ'}
        self.valid_pos_tags: Set[str] = valid_pos_tags

    def load_text(
        self,
        input: Union[str, Path],
        word_normalization_method: WordNormalizationMethod = 'stemming',
        universal_pos_tags: bool = True,
    ) -> None:
        """
        Loads the text of a document or string.

        Parameters
        ----------
        input:
            Input, this can be either raw text or filepath.

        word_normalization_method:
            Word normalization method, defaults to `'stemming'`. See
            `perke.base.types.WordNormalizationMethod` for available
            methods.

        universal_pos_tags:
            Whether to use universal part of speech tags or not,
            defaults to `True`.
        """
        # Initialize reader
        reader = RawTextReader(
            input, word_normalization_method, universal_pos_tags
        )

        # Load sentences
        self.sentences = reader.read()

        self.word_normalization_method = word_normalization_method

    def _is_redundant(
        self,
        candidate: str,
        selected_candidates: List[str],
        minimum_length: int = 1,
    ) -> bool:
        """
        Test if a candidate is redundant with respect to a list of
        already selected candidates. A candidate is considered redundant
        if it is included in another candidate that is weighted higher
        in the list.

        Parameters
        ----------
        candidate:
            The canonical form of the candidate

        selected_candidates:
            The list of already selected candidates canonical forms

        minimum_length:
            Minimum length of the candidate to be considered,
            defaults to `1`.

        Returns
        -------
        The result
        """
        # Only consider candidate with length greater than minimum
        # length
        if self.candidates[candidate].length < minimum_length:
            return False

        # Loop through the already selected candidates
        for sc in selected_candidates:
            if candidate in sc:
                return True

        return False

    def get_n_best(
        self,
        n: int = 10,
        remove_redundants: bool = False,
        normalized: bool = False,
    ) -> List[Tuple[str, float]]:
        """
        Returns the n-best candidates.

        Parameters
        ----------
        n:
            The number of candidates, defaults to `10`.

        remove_redundants:
            Whether redundant keyphrases are filtered out from the
            n-best list, defaults to `False`.

        normalized: bool
            Whether to get normalized words instead of words of first
            occurring form of candidate, defaults to `False`.

        Returns
        -------
        List of `(candidate, weight)` tuples, `candidate` can be either
        canonical form or first occurrence joined words.
        """
        # Sort candidates by descending weight
        bests = sorted(
            self.candidates,
            key=lambda c: self.candidates[c].weight,
            reverse=True,
        )

        # Remove redundant candidates
        if remove_redundants:
            # Initialize a new container for non-redundant candidates
            non_redundant_bests = []

            # Loop through the best candidates
            for c in bests:
                # Test whether candidate is redundant
                if self._is_redundant(
                    candidate=c,
                    selected_candidates=non_redundant_bests,
                ):
                    continue

                # Add the candidate otherwise
                non_redundant_bests.append(c)

                # Break computation if the n-best are found
                if len(non_redundant_bests) >= n:
                    break

            # Copy non-redundant candidates in best container
            bests = non_redundant_bests

        # Get the list of best candidate
        n_best = []
        for c in bests[: min(n, len(bests))]:
            candidate = self.candidates[c]
            if normalized:
                # (canonical form, weight) tuples
                n_best.append((c, candidate.weight))
            else:
                # (first occurrence joined words, weight) tuples
                n_best.append(
                    (' '.join(candidate.all_words[0]), candidate.weight),
                )

        if len(n_best) < n:
            logging.warning(
                'Not enough candidates to choose from '
                '({} requested, {} given).'.format(n, len(n_best))
            )

        return n_best

    def _add_candidate_occurrence(
        self,
        words: List[str],
        offset: int,
        pos_tags: List[str],
        normalized_words: List[str],
    ) -> None:
        """
        Adds a new candidate occurrence.

        Parameters
        ----------
        words:
            List of words of the occurrence

        pos_tags:
            List of part of speech tags assigned to words of the
            occurrence

        offset:
            The offset of the occurrence

        normalized_words:
            List of normalized words of the occurrence
        """
        # Build the canonical form of the candidate
        canonical_form = ' '.join(normalized_words)

        # Create candidate if not exist and add occurrence
        self.candidates[canonical_form].add_occurrence(
            words, offset, pos_tags, normalized_words
        )

    def _select_candidates_with_longest_pos_sequences(
        self,
        valid_pos_tags: Set[str],
    ) -> None:
        """
        Selects candidates with the longest sequences of given part of
        speech tags.

        Parameters
        ----------
        valid_pos_tags:
            Set of valid part of speech tags
        """
        self._select_candidates_with_longest_sequences(
            key=lambda sentence: sentence.pos_tags,
            valid_values=valid_pos_tags,
        )

    def _select_candidates_with_longest_keyword_sequences(
        self,
        keywords: Set[str],
    ) -> None:
        """
        Selects candidates with the longest sequences of given keywords.

        Parameters
        ----------
        keywords:
            Set of given keywords
        """
        self._select_candidates_with_longest_sequences(
            key=lambda sentence: sentence.normalized_words,
            valid_values=keywords,
        )

    def _select_candidates_with_longest_sequences(
        self,
        key: Callable[[Sentence], List[str]],
        valid_values: Set[str],
    ) -> None:
        """
        Selects candidates with the longest sequences of given values,
        based on `key`.

        Parameters
        ----------
        key: `(Sentence) -> list[str]`
            Function that given a sentence and returns a list

        valid_values: `set[str]`
            The valid values
        """
        # Loop through the sentences
        offset_shift = 0
        for i, sentence in enumerate(self.sentences):
            sequence_offsets = []

            # Loop through the key result
            for j, value in enumerate(key(sentence)):
                # Add candidate offset in sequence and continue if not
                # last word
                if value in valid_values:
                    sequence_offsets.append(j)
                    if j < (sentence.length - 1):
                        continue

                # Add sequence as candidate if it is not empty
                if len(sequence_offsets) > 0:
                    first = sequence_offsets[0]
                    last = sequence_offsets[-1]

                    # Add the n-gram as a new candidate occurrence
                    self._add_candidate_occurrence(
                        words=sentence.words[first : last + 1],
                        offset=offset_shift + first,
                        pos_tags=sentence.pos_tags[first : last + 1],
                        normalized_words=sentence.normalized_words[
                            first : last + 1
                        ],
                    )

                # Flush sequence offsets
                sequence_offsets = []

            offset_shift += sentence.length

    def _select_candidates_with_grammar(
        self,
        grammar: Optional[str] = None,
    ) -> None:
        """
        Selects candidates using nltk RegexpParser with a grammar
        defining noun phrases (NP).

        Parameters
        ----------
        grammar:
            grammar defining part of speech patterns of noun phrases,
            defaults to::
                r\"""
                NP:
                    {<NOUN>}<VERB>
                NP:
                    {<DET(,EZ)?|NOUN(,EZ)?|NUM(,EZ)?|ADJ(,EZ)|PRON><DET(,EZ)|NOUN(,EZ)|NUM(,EZ)|ADJ(,EZ)|PRON>*}
                    <NOUN>}{<.*(,EZ)?>
                \"""
        """
        # Initialize default grammar if none provided
        if grammar is None:
            grammar = r"""
                NP:
                    {<NOUN>}<VERB>
                NP:
                    {<DET(,EZ)?|NOUN(,EZ)?|NUM(,EZ)?|ADJ(,EZ)|PRON><DET(,EZ)|NOUN(,EZ)|NUM(,EZ)|ADJ(,EZ)|PRON>*}
                    <NOUN>}{<.*(,EZ)?>
            """

        # Initialize parser
        parser = nltk.RegexpParser(grammar)

        # Loop through the sentences
        offset_shift = 0
        for i, sentence in enumerate(self.sentences):
            # Convert sentence as list of (offset, pos) tuples
            tuples = [
                (str(j), sentence.pos_tags[j]) for j in range(sentence.length)
            ]

            # Parse sentence
            tree = parser.parse(tuples)

            # Find candidates
            for subtree in tree.subtrees():
                if subtree.label() == 'NP':
                    leaves = subtree.leaves()

                    # Get the first and last offset of the current
                    # candidate
                    first = int(leaves[0][0])
                    last = int(leaves[-1][0])

                    # Add the noun phrase to the candidate container
                    self._add_candidate_occurrence(
                        words=sentence.words[first : last + 1],
                        offset=offset_shift + first,
                        pos_tags=sentence.pos_tags[first : last + 1],
                        normalized_words=sentence.normalized_words[
                            first : last + 1
                        ],
                    )

            # Compute offset shift
            offset_shift += sentence.length

    def _filter_candidates(
        self,
        stopwords: Optional[Set[str]] = None,
        minimum_characters: int = 3,
        minimum_word_characters: int = 2,
        valid_punctuation_marks: str = '-',
        maximum_length: int = 5,
        alphanumeric_only: bool = True,
        invalid_pos_tags: Optional[Set[str]] = None,
    ) -> None:
        """
        Filters the candidates with given conditions.

        Parameters
        ----------
        stopwords:
            Set of stopwords, defaults to an empty set.

        minimum_characters:
            Minimum number of characters for a candidate, defaults to
            `3`.

        minimum_word_characters:
            Minimum number of characters for a word to be considered as
            a valid word, defaults to `2`.

        valid_punctuation_marks:
            Punctuation marks that are valid for a candidate, defaults
            to `'-'`.

        maximum_length:
            Maximum length in words of the candidate, defaults to `5`.

        alphanumeric_only:
            Filters candidates containing non-alphanumeric characters,
            defaults to `True`.

        invalid_pos_tags:
            Set of unwanted part of speech tags in candidates, defaults
            to an empty set.
        """
        if stopwords is None:
            stopwords = set()

        if invalid_pos_tags is None:
            invalid_pos_tags = set()

        # Loop through the candidates
        for c in list(self.candidates):
            # Get the candidate
            candidate = self.candidates[c]

            # Get the words from the first occurrence
            words = candidate.all_words[0]

            # Discard if words are in the stoplist
            if set(words).intersection(stopwords):
                del self.candidates[c]

            # Discard if any of pos tags are in the invalid pos tags
            elif set(candidate.all_pos_tags[0]).intersection(invalid_pos_tags):
                del self.candidates[c]

            # Discard if containing words composed of only punctuation
            elif any(
                [set(word).issubset(set(punctuation_marks)) for word in words]
            ):
                del self.candidates[c]

            # Discard short candidates
            elif len(''.join(words)) < minimum_characters:
                del self.candidates[c]

            # Discard candidates containing short words
            elif min([len(word) for word in words]) < minimum_word_characters:
                del self.candidates[c]

            # Discard candidates with long length
            elif len(candidate.normalized_words) > maximum_length:
                del self.candidates[c]

            # Discard if not containing only alphanumeric characters
            elif alphanumeric_only and not all(
                [
                    is_alphanumeric(word, valid_punctuation_marks)
                    for word in words
                ]
            ):
                del self.candidates[c]
