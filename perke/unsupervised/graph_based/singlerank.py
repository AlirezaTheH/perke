# -*- coding: utf-8 -*-

"""
SingleRank keyphrase extraction model.

Simple extension of the TextRank model described in:

* Xiaojun Wan and Jianguo Xiao.
  CollabRank: Towards a Collaborative Approach to Single-Document Keyphrase
  Extraction.
  *In proceedings of the COLING*, pages 969-976, 2008.
"""

import networkx as nx

from perke.unsupervised.graph_based.textrank import TextRank


class SingleRank(TextRank):
    """
    SingleRank keyphrase extraction model.

    This model is an extension of the TextRank model that uses the number of
    co-occurrences to weigh edges in the graph.

    Examples
    --------
    import perke

    # define the set of valid Part-of-Speeches
    pos = {'N', 'Ne', 'AJ', 'AJe'}

    # 1. Create a SingleRank extractor.
    extractor = pke.unsupervised.SingleRank()

    # 2. Load the content of the document.
    extractor.load_document(input='path/to/input',
                            normalization=None)

    # 3. Select the longest sequences of nouns and adjectives as candidates.
    extractor.candidate_selection(pos=pos)

    # 4. Weight the candidates using the sum of their word's scores that are
    #    computed using random walk. In the graph, nodes are words of
    #    certain part-of-speech (nouns and adjectives) that are connected if
    #    they occur in a window of 10 words.
    extractor.candidate_weighting(window=10,
                                  pos=pos)

    # 5. Get the 10-highest scored candidates as keyphrases
    keyphrases = extractor.get_n_best(n=10)

    """

    def __init__(self):
        """
        Redefining initializer for SingleRank.
        """

        super(SingleRank, self).__init__()

    def build_word_graph(self, window=10, pos=None):
        """
        Build a graph representation of the document in which nodes/vertices
        are words and edges represent co-occurrence relation. Syntactic filters
        can be applied to select only words of certain Part-of-Speech.
        Co-occurrence relations can be controlled using the distance (window)
        between word occurrences in the document.

        The number of times two words co-occur in a window is encoded as *edge
        weights*. Sentence boundaries **are not** taken into account in the
        window.

        Parameters
        ----------
        window: int
            The window for connecting two words in the graph, defaults to 10.

        pos: set
            The set of valid pos for words to be considered as nodes
            in the graph, defaults to ('N', 'Ne', 'AJ', 'AJe').
        """

        if pos is None:
            pos = {'N', 'Ne', 'AJ', 'AJe'}

        # Flatten document as a sequence of (word, pass_syntactic_filter) tuples
        text = [(word, sentence.pos[i] in pos) for sentence in self.sentences
                for i, word in enumerate(sentence.stems)]

        # Add nodes to the graph
        self.graph.add_nodes_from([word for word, valid in text if valid])

        # Add edges to the graph
        for i, (node1, is_in_graph1) in enumerate(text):

            # Speed up things
            if not is_in_graph1:
                continue

            for j in range(i + 1, min(i + window, len(text))):
                node2, is_in_graph2 = text[j]
                if is_in_graph2 and node1 != node2:
                    if not self.graph.has_edge(node1, node2):
                        self.graph.add_edge(node1, node2, weight=0.0)
                    self.graph[node1][node2]['weight'] += 1.0

    def candidate_weighting(self, window=10, pos=None, normalized=False, **kwargs):
        """
        Keyphrase candidate ranking using the weighted variant of the
        TextRank formulae. Candidates are scored by the sum of the scores of
        their words.

        Parameters
        ----------
        window: int
            The window for connecting two words in the graph, defaults to 10.

        pos: set
            The set of valid pos for words to be considered as nodes
            in the graph, defaults to ('N', 'Ne', 'AJ', 'AJe').

        normalized: bool
            Normalize keyphrase score by their length, defaults to False.
        """

        if pos is None:
            pos = {'N', 'Ne', 'AJ', 'AJe'}

        # Build the word graph
        self.build_word_graph(window=window, pos=pos)

        # Compute the word scores using random walk
        w = nx.pagerank_scipy(self.graph,
                              alpha=0.85,
                              tol=0.0001,
                              weight='weight')

        # Loop through the candidates
        for k in self.candidates.keys():
            tokens = self.candidates[k].lexical_form
            self.weights[k] = sum([w[t] for t in tokens])
            if normalized:
                self.weights[k] /= len(tokens)

            # use position to break ties
            self.weights[k] += (self.candidates[k].offsets[0] * 1e-8)
