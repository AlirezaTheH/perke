import networkx as nx

from perke.unsupervised.graph_based.text_rank import TextRank


class SingleRank(TextRank):
    """
    SingleRank keyphrase extractor

    This model is an extension of the TextRank model that uses the
    number of co-occurrences to weight edges in the graph.

    Implementation of the SingleRank model described in:

    Xiaojun Wan and Jianguo Xiao.
    Single Document Keyphrase Extraction Using Neighborhood Knowledge.
    In proceedings of the NCAI, pages 855–860, 2008.

    Examples
    --------
    .. code:: python

        from perke.unsupervised.graph_based import SingleRank

        # Define the set of valid part of speech tags to occur in the model.
        valid_pos_tags = {'N', 'Ne', 'AJ', 'AJe'}

        # 1. Create a SingleRank extractor.
        extractor = SingleRank(valid_pos_tags=valid_pos_tags)

        # 2. Load the text.
        extractor.load_text(input='text or path/to/input_file',
                            word_normalization_method=None)

        # 3. Select the longest sequences of nouns and adjectives as
        #    candidates.
        extractor.select_candidates()

        # 4. Weight the candidates using the sum of their words weights that
        #    are computed using random walk. In the graph, nodes are certain
        #    parts of speech (nouns and adjectives) that are connected if
        #    they co-occur in a window of 10 words.
        extractor.weight_candidates(window=10)

        # 5. Get the 10 highest weighted candidates as keyphrases
        keyphrases = extractor.get_n_best(n=10)

    Attributes
    ----------
    graph_edges_are_weighted: `bool`
        Whether graph edges are weighted
    """

    def __init__(self, valid_pos_tags=None):
        """
        initializes SingleRank.

        Parameters
        ----------
        valid_pos_tags: `set`
            Set of valid part of speech tags, defaults to nouns and
            adjectives. I.e. `{'N', 'Ne', 'AJ', 'AJe'}`.
        """
        super().__init__(valid_pos_tags)
        self.graph_edges_are_weighted = True

    def build_word_graph(self, window_size=10):
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
        super().build_word_graph(window_size)

    def weight_candidates(self,
                          window_size=10,
                          normalize_weights=False,
                          **kwargs):
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
        self.build_word_graph(window_size)

        # Compute the word weights using random walk
        weights = nx.pagerank_scipy(self.graph,
                                    alpha=0.85,
                                    tol=0.0001,
                                    weight='weight')

        self.weight_candidates_with_words_weights(weights, normalize_weights)
