# -*- coding: utf-8 -*-

"""Base classes for the pke module."""

from collections import defaultdict
import string
import os
import logging
import codecs
from six import string_types

from nltk import RegexpParser
import hazm

from perke.data_structures import Candidate, Document
from perke.readers import RawTextReader


from builtins import str

ISO_to_language = {'en': 'english', 'pt': 'portuguese', 'fr': 'french',
                   'es': 'spanish', 'it': 'italian', 'nl': 'dutch',
                   'de': 'german'}

escaped_punctuation = {'-lrb-': '(', '-rrb-': ')', '-lsb-': '[', '-rsb-': ']',
                       '-lcb-': '{', '-rcb-': '}'}


class LoadFile(object):
    """
    The LoadFile class that provides base functions.

    Attributes
    ----------
    input_file: str
        Path to the input file

    normalization: str
        Word normalization method

    sentences: list
        Sentence container (list of Sentence objects)

    candidates: defaultdict(Candidate)
        Keyphrase candidates container (dict of Candidate objects)

    weights: dict
        Weight container (can be either word or candidate weights)

    stoplist: list
        List of stopwords
    """

    def __init__(self):

        self.input_file = None
        self.normalization = None
        self.sentences = []
        self.candidates = defaultdict(Candidate)
        self.weights = {}
        self.stoplist = None

    def load_document(self, input, **kwargs):
        """
        Loads the content of a document/string/stream.

        Parameters
        ----------
        input: str
            Input

        encoding: str
            Encoding of the raw file.

        normalization: str
            Word normalization method, defaults to
            'stemming'. Other possible values are 'lemmatization' or 'None'
            for using word surface forms instead of stems/lemmas.
        """

        # Initialize document
        doc = Document()

        if isinstance(input, string_types):

            # If input is an input file
            if os.path.isfile(input):

                parser = RawTextReader()
                encoding = kwargs.get('encoding', 'utf-8')
                with codecs.open(input, 'r', encoding=encoding) as file:
                    text = file.read()
                doc = parser.read(text=text, path=input, **kwargs)

            # If input is a string
            else:
                parser = RawTextReader()
                doc = parser.read(text=input, **kwargs)

        elif getattr(input, 'read', None):
            parser = RawTextReader()
            doc = parser.read(text=input.read(), **kwargs)

        else:
            logging.error('Cannot process {}'.format(type(input)))

        # Set the input file
        self.input_file = doc.input_file

        # Set the sentences
        self.sentences = doc.sentences

        # Initialize the stoplist
        self.stoplist = hazm.stopwords_list()

        # word normalization
        self.normalization = kwargs.get('normalization', 'stemming')
        if self.normalization == 'stemming':
            self.apply_stemming()
        elif self.normalization is None:
            for i, sentence in enumerate(self.sentences):
                self.sentences[i].stems = sentence.words

    def apply_stemming(self):
        """
        Populates the stem containers of sentences.
        """

        stemmer = hazm.Stemmer()

        # Iterate throughout the sentences
        for i, sentence in enumerate(self.sentences):
            self.sentences[i].stems = [stemmer.stem(w) for w in sentence.words]

    def is_redundant(self, candidate, prev, minimum_length=1):
        """
        Test if one candidate is redundant with respect to a list of already
        selected candidates. A candidate is considered redundant if it is
        included in another candidate that is ranked higher in the list.

        Parameters
        ----------
        candidate: str
            the lexical form of the candidate

        prev: list
            the list of already selected candidates (lexical forms)

        minimum_length: int
            minimum length (in words) of the candidate
            to be considered, defaults to 1
        """

        # Get the tokenized lexical form from the candidate
        candidate = self.candidates[candidate].lexical_form

        # Only consider candidate greater than one word
        if len(candidate) < minimum_length:
            return False

        # Get the tokenized lexical forms from the selected candidates
        prev = [self.candidates[u].lexical_form for u in prev]

        # Loop through the already selected candidates
        for prev_candidate in prev:
            for i in range(len(prev_candidate) - len(candidate) + 1):
                if candidate == prev_candidate[i:i + len(candidate)]:
                    return True
        return False

    def get_n_best(self, n=10, redundancy_removal=False, stemming=False):
        """
        Returns the n-best candidates given the weights.

        Parameters
        ----------
        n: int
            The number of candidates, defaults to 10.

        redundancy_removal: bool
            Whether redundant keyphrases are
            filtered out from the n-best list, defaults to False.

        stemming: bool
            Whether to extract stems or surface forms
            (first occurring form of candidate), default to False.
        """

        # Sort candidates by descending weight
        best = sorted(self.weights, key=self.weights.get, reverse=True)

        # Remove redundant candidates
        if redundancy_removal:

            # Initialize a new container for non redundant candidates
            non_redundant_best = []

            # Loop through the best candidates
            for candidate in best:

                # Test wether candidate is redundant
                if self.is_redundant(candidate, non_redundant_best):
                    continue

                # Add the candidate otherwise
                non_redundant_best.append(candidate)

                # Break computation if the n-best are found
                if len(non_redundant_best) >= n:
                    break

            # Copy non redundant candidates in best container
            best = non_redundant_best

        # Get the list of best candidates as (lexical form, weight) tuples
        n_best = [(u, self.weights[u]) for u in best[:min(n, len(best))]]

        # Replace with surface forms if no stemming
        if not stemming:
            n_best = [(' '.join(self.candidates[u].surface_forms[0]),
                       self.weights[u]) for u in best[:min(n, len(best))]]

        if len(n_best) < n:
            logging.warning(
                'Not enough candidates to choose from '
                '({} requested, {} given)'.format(n, len(n_best)))

        # Return the list of best candidates
        return n_best

    def add_candidate(self, words, stems, pos, offset, sentence_id):
        """
        Add a keyphrase candidate to the candidates container.

        Parameters
        ----------
        words: list
            The words (surface form) of the candidate

        stems: list
            The stemmed words of the candidate.

        pos: list)
            The Part-Of-Speeches of the words in the candidate.

        offset: int
            The offset of the first word of the candidate.

        sentence_id: int
            The sentence id of the candidate.
        """

        # Build the lexical (canonical) form of the candidate using stems
        lexical_form = ' '.join(stems)

        # Add/update the surface forms
        self.candidates[lexical_form].surface_forms.append(words)

        # Add/update the lexical_form
        self.candidates[lexical_form].lexical_form = stems

        # Add/update the POS patterns
        self.candidates[lexical_form].pos_patterns.append(pos)

        # Add/update the offsets
        self.candidates[lexical_form].offsets.append(offset)

        # Add/update the sentence ids
        self.candidates[lexical_form].sentence_ids.append(sentence_id)

    def ngram_selection(self, n=3):
        """Select all the n-grams and populate the candidate container.

        Args:
            n (int): the n-gram length, defaults to 3.
        """

        # loop through the sentences
        for i, sentence in enumerate(self.sentences):

            # limit the maximum n for short sentence
            skip = min(n, sentence.length)

            # compute the offset shift for the sentence
            shift = sum([s.length for s in self.sentences[0:i]])

            # generate the ngrams
            for j in range(sentence.length):
                for k in range(j + 1, min(j + 1 + skip, sentence.length + 1)):
                    # add the ngram to the candidate container
                    self.add_candidate(words=sentence.words[j:k],
                                       stems=sentence.stems[j:k],
                                       pos=sentence.pos[j:k],
                                       offset=shift + j,
                                       sentence_id=i)

    def longest_pos_sequence_selection(self, valid_pos=None):
        self.longest_sequence_selection(
            key=lambda s: s.pos, valid_values=valid_pos)

    def longest_keyword_sequence_selection(self, keywords):
        self.longest_sequence_selection(
            key=lambda s: s.stems, valid_values=keywords)

    def longest_sequence_selection(self, key, valid_values):
        """
        Select the longest sequences of given POS tags as candidates.

        Parameters
        ----------
        key: func
            function that given a sentence return an iterable

        valid_values: set
            The set of valid values, defaults to None.
        """

        # Loop through the sentences
        for i, sentence in enumerate(self.sentences):

            # Compute the offset shift for the sentence
            shift = sum([s.length for s in self.sentences[0:i]])

            # Container for the sequence (defined as list of offsets)
            seq = []

            # Loop through the tokens
            for j, value in enumerate(key(self.sentences[i])):

                # Add candidate offset in sequence and continue if not last word
                if value in valid_values:
                    seq.append(j)
                    if j < (sentence.length - 1):
                        continue

                # Add sequence as candidate if non empty
                if seq:
                    # Add the ngram to the candidate container
                    self.add_candidate(words=sentence.words[seq[0]:seq[-1] + 1],
                                       stems=sentence.stems[seq[0]:seq[-1] + 1],
                                       pos=sentence.pos[seq[0]:seq[-1] + 1],
                                       offset=shift + seq[0],
                                       sentence_id=i)

                # Flush sequence container
                seq = []

    def grammar_selection(self, grammar=None):
        """
        Select candidates using nltk RegexpParser with a grammar defining
        noun phrases (NP).

        Parameters
        ----------
        grammar: str
            grammar defining POS patterns of NPs.
        """

        # Initialize default grammar if none provided
        if grammar is None:
            grammar = r"""
                NP:
                    <P>{<N>}<V>
                NP:
                    {<DETe?|Ne?|NUMe?|AJe|PRO|CL|RESe?><DETe?|Ne?|NUMe?|AJe?|PRO|CL|RESe?>*}
                    <N>}{<.*e?>
            """

        # Initialize chunker
        chunker = RegexpParser(grammar)

        # Loop through the sentences
        for i, sentence in enumerate(self.sentences):

            # Compute the offset shift for the sentence
            shift = sum([s.length for s in self.sentences[0:i]])

            # Convert sentence as list of (offset, pos) tuples
            tuples = [(str(j), sentence.pos[j]) for j in range(sentence.length)]

            # Parse sentence
            tree = chunker.parse(tuples)

            # Find candidates
            for subtree in tree.subtrees():
                if subtree.label() == 'NP':
                    leaves = subtree.leaves()

                    # Get the first and last offset of the current candidate
                    first = int(leaves[0][0])
                    last = int(leaves[-1][0])

                    # Add the NP to the candidate container
                    self.add_candidate(words=sentence.words[first:last + 1],
                                       stems=sentence.stems[first:last + 1],
                                       pos=sentence.pos[first:last + 1],
                                       offset=shift + first,
                                       sentence_id=i)

    @staticmethod
    def _is_alphanum(word, valid_punctuation_marks='-'):
        """
        Check if a word is valid, i.e. it contains only alpha-numeric
        characters and valid punctuation marks.

        Parameters
        ----------
        word: string
            A word

        valid_punctuation_marks: str
            Punctuation marks that are valid
            for a candidate, defaults to '-'.
        """
        for punct in valid_punctuation_marks.split():
            word = word.replace(punct, '')
        return word.isalnum()

    def candidate_filtering(self,
                            stoplist=None,
                            minimum_length=3,
                            minimum_word_size=2,
                            valid_punctuation_marks='-',
                            maximum_word_number=5,
                            only_alphanum=True,
                            pos_blacklist=None):
        """
        Filter the candidates containing strings from the stoplist. Only
        keep the candidates containing alpha-numeric characters (if the
        non_latin_filter is set to True) and those length exceeds a given
        number of characters.

        Parameters
        ----------
        stoplist: list
            List of strings, defaults to None.

        minimum_length: int
            Minimum number of characters for a
            candidate, defaults to 3.

        minimum_word_size: int
            Minimum number of characters for a
            token to be considered as a valid word, defaults to 2.

        valid_punctuation_marks: str
            Punctuation marks that are valid
            for a candidate, defaults to '-'.

        maximum_word_number: int
            Maximum length in words of the
            candidate, defaults to 5.

        only_alphanum: bool
            Filter candidates containing non
            alpha-numeric characters, defaults to True.

        pos_blacklist: list
            List of unwanted Part-Of-Speeches in
            candidates, defaults to [].
        """

        if stoplist is None:
            stoplist = []

        if pos_blacklist is None:
            pos_blacklist = []

        punctuation = list(string.punctuation) + ['،', '.', '×', '؛', '؟']

        # Loop through the candidates
        for k in list(self.candidates):

            # Get the candidate
            v = self.candidates[k]

            # Get the words from the first occurring surface form
            words = v.surface_forms[0]

            # Discard if words are in the stoplist
            if set(words).intersection(stoplist):
                del self.candidates[k]

            # Discard if tags are in the pos_blacklist
            elif set(v.pos_patterns[0]).intersection(pos_blacklist):
                del self.candidates[k]

            # Discard if containing tokens composed of only punctuation
            elif any([set(u).issubset(set(punctuation)) for u in words]):
                del self.candidates[k]

            # discard candidates composed of 1-2 characters
            elif len(''.join(words)) < minimum_length:
                del self.candidates[k]

            # Discard candidates containing small words (1-character)
            elif min([len(u) for u in words]) < minimum_word_size:
                del self.candidates[k]

            # Discard candidates composed of more than 5 words
            elif len(v.lexical_form) > maximum_word_number:
                del self.candidates[k]

            # Discard if not containing only alpha-numeric characters
            if only_alphanum and k in self.candidates:
                if not all([self._is_alphanum(w, valid_punctuation_marks)
                            for w in words]):
                    del self.candidates[k]

