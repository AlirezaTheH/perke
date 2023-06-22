from typing import Dict, Optional, Set

import networkx as nx

from perke.base.extractor import Extractor


class TextRank(Extractor):
    """
    TextRank keyphrase extractor

    This model builds a graph that represents the text. A graph based
    ranking algorithm is then applied to extract the phrases that are
    most important in the text.

    In this implementation, nodes are words of certain parts of speech
    (nouns and adjectives) and edges represent co-occurrence relation,
    controlled by the distance between word occurrences
    (here a window of 2 words). Nodes are weighted by the TextRank
    graph-based weighting algorithm in its unweighted variant.

    Note
    ----
    Implementation of the TextRank model for keyword extraction
    described in:

    | Rada Mihalcea and Paul Tarau
    | `TextRank: Bringing Order into Texts
      <http://www.aclweb.org/anthology/W04-3252.pdf>`_
    | In Proceedings of EMNLP, 2004

    Examples
    --------
    .. literalinclude:: ../../../examples/unsupervised/graph_based/text_rank.py

    Attributes
    ----------
    graph:
        The word graph

    graph_edges_are_weighted:
        Whether graph edges are weighted
    """

    def __init__(self, valid_pos_tags: Optional[Set[str]] = None) -> None:
        """
        Initializes TextRank.

        Parameters
        ----------
        valid_pos_tags:
            Set of valid part of speech tags, defaults to nouns and
            adjectives. I.e. `{'NOUN', 'ADJ'}`.
        """
        super().__init__(valid_pos_tags)
        self.graph: nx.Graph = nx.Graph()
        self.graph_edges_are_weighted: bool = False

    def select_candidates(self) -> None:
        """
        Selects candidates using the longest sequences of certain parts
        of speech.
        """
        # Select sequences of words with valid pos tags
        self._select_candidates_with_longest_pos_sequences(
            valid_pos_tags=self.valid_pos_tags,
        )

    def _build_word_graph(self, window_size: int = 2) -> None:
        """
        Builds a graph representation of the text in which nodes are
        words and edges represent co-occurrence relation. Syntactic
        filters can be applied to select only words with certain part
        of speech tags (noun and adjectives by default).
        Co-occurrence relations can be controlled using the distance
        between word occurrences (window) in the text.

        As the original paper does not give precise details on how the
        word graph is constructed, we make the following assumptions
        from the example given in Figure 2:
            1. Sentence boundaries **are not** taken into account.
            2. Stopwords and punctuation marks **are** considered as
               words when computing the window.

        Parameters
        ----------
        window_size:
            The size of window for connecting two words in the graph,
            defaults to `2`.
        """
        # Flatten text as a sequence of (word, is_valid) tuples
        flatten_text = []
        for sentence in self.sentences:
            for i, word in enumerate(sentence.normalized_words):
                is_valid = sentence.pos_tags[i] in self.valid_pos_tags
                flatten_text.append((word, is_valid))

                # Add node to the graph
                if is_valid:
                    self.graph.add_node(word)

        # Add edges to the graph
        for i, (first_node, first_node_is_valid) in enumerate(flatten_text):
            # Speed up things
            if not first_node_is_valid:
                continue

            for j in range(i + 1, min(i + window_size, len(flatten_text))):
                second_node, second_node_is_valid = flatten_text[j]

                if second_node_is_valid and first_node != second_node:
                    # SingleRank
                    if self.graph_edges_are_weighted:
                        if not self.graph.has_edge(first_node, second_node):
                            self.graph.add_edge(
                                first_node, second_node, weight=0.0
                            )

                        self.graph[first_node][second_node]['weight'] += 1.0

                    # TextRank
                    else:
                        self.graph.add_edge(first_node, second_node)

    def weight_candidates(
        self,
        window_size: int = 2,
        top_t_percent: Optional[float] = None,
        normalize_weights: bool = False,
    ) -> None:
        """
        Tailored candidate weighting method for TextRank. Keyphrase
        candidates are either composed of the top T-highest weighted
        words as in the original paper or extracted using the
        `select_candidates` method. Candidates are weighting using the
        sum of their (normalized?) words.

        Parameters
        ----------
        window_size:
            The size of window for connecting two words in the graph,
            defaults to `2`.

        top_t_percent:
            Percentage of top vertices to keep for phrase generation.

        normalize_weights:
            Whether normalize keyphrase weight by their length, defaults
            to `False`.
        """
        # Build the word graph
        self._build_word_graph(window_size)

        # Compute the word weights using the unweighted PageRank
        # formulae
        weights = nx.pagerank(self.graph, alpha=0.85, tol=0.0001, weight=None)

        # Generate the phrases from the T-percent top weighted words
        if top_t_percent is not None:
            # Computing the number of top keywords
            number_of_nodes = self.graph.number_of_nodes()
            to_keep = int(number_of_nodes * top_t_percent)

            # Sorting the nodes by decreasing weights
            sorted_weights = sorted(weights, key=weights.get, reverse=True)

            # Creating keyphrases from the T top words
            self._select_candidates_with_longest_keyword_sequences(
                keywords=set(sorted_weights[: int(to_keep)]),
            )

        self._weight_candidates_with_words_weights(weights, normalize_weights)

    def _weight_candidates_with_words_weights(
        self,
        weights: Dict[str, float],
        normalize_weights: bool,
        use_position_adjustment: bool = True,
    ) -> None:
        """
        Weights candidates using the sum of their words weights.

        Parameters
        ----------
        weights:
            Word weights

        normalize_weights:
            Whether normalize keyphrase weight by their length.

        use_position_adjustment:
            Whether to use candidate position to adjust weights,
            defaults to `True`.
        """
        for candidate in self.candidates.values():
            candidate.weight = sum(
                [weights.get(word, 0.0) for word in candidate.normalized_words]
            )

            if normalize_weights:
                candidate.weight /= len(candidate.normalized_words)

            if use_position_adjustment:
                candidate.weight += candidate.offsets[0] * 1e-8
