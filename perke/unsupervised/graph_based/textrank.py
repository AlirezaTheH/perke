# -*- coding: utf-8 -*-

"""
TextRank keyphrase extraction model.

Implementation of the TextRank model for keyword extraction described in:

* Rada Mihalcea and Paul Tarau.
  TextRank: Bringing Order into Texts
  *In Proceedings of EMNLP*, 2004.

"""

import math
import logging

import networkx as nx

from perke.base import LoadFile


class TextRank(LoadFile):
    """
    TextRank for keyword extraction.

    This model builds a graph that represents the text. A graph based ranking
    algorithm is then applied to extract the lexical units (here the words) that
    are most important in the text.

    In this implementation, nodes are words of certain part-of-speech (nouns
    and adjectives) and edges represent co-occurrence relation, controlled by
    the distance between word occurrences (here a window of 2 words). Nodes
    are ranked by the TextRank graph-based ranking algorithm in its unweighted
    variant.

    Examples
    --------
    import perke

    # Define the set of valid Part-of-Speeches
    pos = {'N', 'Ne', 'AJ', 'AJe'}

    # 1. Create a TextRank extractor.
    extractor = perke.unsupervised.TextRank()

    # 2. Load the content of the document.
    extractor.load_document(input='path/to/input',
                            normalization=None)

    # 3. Build the graph representation of the document and rank the words.
    #    Keyphrase candidates are composed from the 33-percent
    #    highest-ranked words.
    extractor.candidate_weighting(window=2,
                                  pos=pos,
                                  top_percent=0.33)

    # 4. get the 10-highest scored candidates as keyphrases
    keyphrases = extractor.get_n_best(n=10)

    Attributes
    ----------
    graph: nx.Graph
        The word graph
    """

    def __init__(self):
        """
        Redefining initializer for TextRank.
        """

        super(TextRank, self).__init__()
        self.graph = nx.Graph()

    def candidate_selection(self, pos=None):
        """
        Candidate selection using longest sequences of PoS.

        Parameters
        ----------
        pos: set
            Set of valid POS tags, defaults to ('N', 'Ne', 'AJ', 'AJe').
        """

        if pos is None:
            pos = {'N', 'Ne', 'AJ', 'AJe'}

        # Select sequence of adjectives and nouns
        self.longest_pos_sequence_selection(valid_pos=pos)

    def build_word_graph(self, window=2, pos=None):
        """
        Build a graph representation of the document in which nodes/vertices
        are words and edges represent co-occurrence relation. Syntactic filters
        can be applied to select only words of certain Part-of-Speech.
        Co-occurrence relations can be controlled using the distance between
        word occurrences in the document.

        As the original paper does not give precise details on how the word
        graph is constructed, we make the following assumptions from the example
        given in Figure 2: 1) sentence boundaries **are not** taken into account
        and, 2) stopwords and punctuation marks **are** considered as words when
        computing the window.

        Parameters
        ----------
        window: int
            The window for connecting two words in the graph, defaults to 2.

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
                    self.graph.add_edge(node1, node2)

    def candidate_weighting(self,
                            window=2,
                            pos=None,
                            top_percent=None,
                            normalized=False):
        """
        Tailored candidate ranking method for TextRank. Keyphrase candidates
        are either composed from the T-percent highest-ranked words as in the
        original paper or extracted using the `candidate_selection()` method.
        Candidates are ranked using the sum of their (normalized?) words.

        Parameters
        ----------
        window: int
            The window for connecting two words in the graph, defaults to 2.

        pos: set
            The set of valid pos for words to be considered as nodes
            in the graph, defaults to ('N', 'Ne', 'AJ', 'AJe').

        top_percent: float
            Percentage of top vertices to keep for phrase generation.

        normalized: bool
            Normalize keyphrase score by their length, defaults to False.
        """

        if pos is None:
            pos = {'N', 'Ne', 'AJ', 'AJe'}

        # Build the word graph
        self.build_word_graph(window=window, pos=pos)

        # Compute the word scores using the unweighted PageRank formulae
        w = nx.pagerank_scipy(self.graph, alpha=0.85, tol=0.0001, weight=None)

        # Generate the phrases from the T-percent top ranked words
        if top_percent is not None:

            # Warn user as this is not the perke way of doing it
            logging.warning("Candidates are generated using {}-top".format(
                            top_percent))

            # Computing the number of top keywords
            nb_nodes = self.graph.number_of_nodes()
            to_keep = min(math.floor(nb_nodes * top_percent), nb_nodes)

            # Sorting the nodes by decreasing scores
            top_words = sorted(w, key=w.get, reverse=True)

            # Creating keyphrases from the T-top words
            self.longest_keyword_sequence_selection(top_words[:int(to_keep)])

        # Weight candidates using the sum of their word scores
        for k in self.candidates.keys():
            tokens = self.candidates[k].lexical_form
            self.weights[k] = sum([w[t] for t in tokens])
            if normalized:
                self.weights[k] /= len(tokens)

            # use position to break ties
            self.weights[k] += (self.candidates[k].offsets[0]*1e-8)
