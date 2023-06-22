from collections import defaultdict
from typing import DefaultDict, Optional, Set

import networkx as nx

from perke.unsupervised.graph_based.single_rank import SingleRank


class PositionRank(SingleRank):
    """
    PositionRank keyphrase extractor

    This model is an unsupervised approach to extract keyphrases from
    scholarly documents that incorporates information from all positions
    of a word's occurrences into a biased PageRank.

    Note
    ----
    Implementation of the PositionRank described in:

    | Corina Florescu and Cornelia Caragea
    | `PositionRank: An Unsupervised Approach to Keyphrase Extraction
      from Scholarly Documents
      <http://www.aclweb.org/anthology/P17-1102.pdf>`_
    | In proceedings of ACL, pages 1105-1115, 2017

    Examples
    --------
    .. literalinclude:: ../../../examples/unsupervised/graph_based/position_rank.py

    Attributes
    ----------
    positions:
        Dict of normalized word to the sums of word's inverse positions
    """

    def __init__(self, valid_pos_tags: Optional[Set[str]] = None) -> None:
        """
        Initializes PositionRank.

        Parameters
        ----------
        valid_pos_tags:
            Set of valid part of speech tags, defaults to nouns and
            adjectives. I.e. `{'NOUN', 'NOUN,EZ', 'ADJ', 'ADJ,EZ'}`.
        """
        if valid_pos_tags is None:
            valid_pos_tags = {'NOUN', 'NOUN,EZ', 'ADJ', 'ADJ,EZ'}
        super().__init__(valid_pos_tags)
        self.positions: DefaultDict[str, float] = defaultdict(float)

    def select_candidates(
        self,
        grammar: Optional[str] = None,
        maximum_length: int = 3,
        **kwargs,
    ) -> None:
        """
        Candidate selection heuristic using a syntactic part of speech
        pattern for noun phrase extraction. Keyphrase candidates are
        noun phrases that match the regular expression
        (adjective)*(noun)+, with a given length.

        Parameters
        ----------
        grammar:
            Grammar defining part of speech patterns of noun phrases,
            defaults to::
                r\"""
                NP:
                    {<NOUN>}<VERB>
                NP:
                    {<DET(,EZ)?|NOUN(,EZ)?|NUM(,EZ)?|ADJ(,EZ)|PRON><DET(,EZ)|NOUN(,EZ)|NUM(,EZ)|ADJ(,EZ)|PRON>*}
                    <NOUN>}{<.*(,EZ)?>
                \"""
        maximum_length: `int`
            Maximum length in words of the candidate, defaults to `3`.
        """
        if grammar is None:
            grammar = r"""
                NP:
                    {<NOUN>}<VERB>
                NP:
                    {<DET(,EZ)?|NOUN(,EZ)?|NUM(,EZ)?|ADJ(,EZ)|PRON><DET(,EZ)|NOUN(,EZ)|NUM(,EZ)|ADJ(,EZ)|PRON>*}
                    <NOUN>}{<.*(,EZ)?>
            """

        # Select sequence of noun phrases with given pattern
        self._select_candidates_with_grammar(grammar=grammar)

        self._filter_candidates(maximum_length)

    def _build_word_graph(self, window_size: int = 10) -> None:
        """
        Build the graph representation of the text. In the graph, nodes
        are words that passes a parts of speech filter. Two nodes are
        connected if the words corresponding to these nodes co-occur
        within a window of contiguous tokens. The weight of an edge is
        computed based on the co-occurrence count of the two words
        within a window of successive tokens.

        Parameters
        ----------
        window_size:
            The size of window for connecting two words in the graph,
            defaults to `10`.
        """
        # Flatten text as a sequence of only passed syntactic filter
        # (word, position) tuples
        flatten_text = []
        shift = 0
        for i, sentence in enumerate(self.sentences):
            for j, word in enumerate(sentence.normalized_words):
                if sentence.pos_tags[j] in self.valid_pos_tags:
                    flatten_text.append((word, shift + j))

                    # Add node to the graph
                    self.graph.add_node(word)

            shift += sentence.length

        # Add edges to the graph
        for i, (first_node, first_node_position) in enumerate(flatten_text):
            for second_node, second_node_position in flatten_text[i + 1 :]:
                if (
                    second_node_position - first_node_position
                ) < window_size and first_node != second_node:
                    if not self.graph.has_edge(first_node, second_node):
                        self.graph.add_edge(first_node, second_node, weight=0)

                    self.graph[first_node][second_node]['weight'] += 1

        # Compute the sums of the word's inverse positions
        for word, position in flatten_text:
            self.positions[word] += 1 / (position + 1)

    def weight_candidates(
        self,
        window_size: int = 10,
        normalize_weights: bool = False,
        **kwargs,
    ) -> None:
        """
        Calculates candidates weights using a biased PageRank.

        Parameters
        ----------
        window_size:
            The size of window for connecting two words in the graph,
            defaults to `10`.

        normalize_weights:
            Normalize keyphrase weight by their length, defaults to
            `False`.
        """
        # Build the word graph
        self._build_word_graph(window_size)

        # Normalize cumulated inverse positions
        position_sum = sum(self.positions.values())
        for word in self.positions:
            self.positions[word] /= position_sum

        # Compute the word weights using biased random walk
        weights = nx.pagerank(
            self.graph,
            alpha=0.85,
            tol=0.0001,
            personalization=self.positions,
            weight='weight',
        )

        self._weight_candidates_with_words_weights(
            weights,
            normalize_weights,
            use_position_adjustment=False,
        )

    def _filter_candidates(self, maximum_length: int = 3, **kwargs) -> None:
        """
        Filters the candidates with given conditions.

        Parameters
        ----------
        maximum_length:
            Maximum length in words of the candidate, defaults to 3.
        """
        for c in list(self.candidates):
            if len(self.candidates[c].normalized_words) > maximum_length:
                del self.candidates[c]
