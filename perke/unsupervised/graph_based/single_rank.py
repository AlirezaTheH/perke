from typing import Optional, Set

import networkx as nx

from perke.unsupervised.graph_based.text_rank import TextRank


class SingleRank(TextRank):
    """
    SingleRank keyphrase extractor

    This model is an extension of the TextRank model that uses the
    number of co-occurrences to weight edges in the graph.

    Note
    ----
    Implementation of the SingleRank model described in:

    | Xiaojun Wan and Jianguo Xiao
    | `Single Document Keyphrase Extraction Using Neighborhood
       Knowledge
       <https://www.aaai.org/Papers/AAAI/2008/AAAI08-136.pdf>`_
    | In proceedings of the NCAI, pages 855–860, 2008

    Examples
    --------
    .. literalinclude:: ../../../examples/unsupervised/graph_based/single_rank.py

    Attributes
    ----------
    graph_edges_are_weighted:
        Whether graph edges are weighted
    """

    def __init__(self, valid_pos_tags: Optional[Set[str]] = None) -> None:
        """
        Initializes SingleRank.

        Parameters
        ----------
        valid_pos_tags:
            Set of valid part of speech tags, defaults to nouns and
            adjectives. I.e. `{'NOUN', 'ADJ'}`.
        """
        super().__init__(valid_pos_tags)
        self.graph_edges_are_weighted: bool = True

    def _build_word_graph(self, window_size: int = 10) -> None:
        """
        Builds a graph representation of the text just like TextRank
        except that edges in SingleRank graph are weighted and the
        number of times two words co-occur in a window is encoded as
        edge weights.

        Parameters
        ----------
        window_size: `int`
            The size of window for connecting two words in the graph,
            defaults to `10`.
        """
        super()._build_word_graph(window_size)

    def weight_candidates(
        self,
        window_size: int = 10,
        normalize_weights: bool = False,
        **kwargs,
    ) -> None:
        """
        Weights candidates using the weighted variant of the TextRank
        formulae. Candidates are weighted by the sum of the weights of
        their words.

        Parameters
        ----------
        window_size: `int`
            The size of window for connecting two words in the graph,
            defaults to `10`.

        normalize_weights: `bool`
            Whether normalize keyphrase weight by their length, defaults
            to `False`.
        """
        # Build the word graph
        self._build_word_graph(window_size)

        # Compute the word weights using random walk
        weights = nx.pagerank(
            self.graph, alpha=0.85, tol=0.0001, weight='weight'
        )

        self._weight_candidates_with_words_weights(weights, normalize_weights)
