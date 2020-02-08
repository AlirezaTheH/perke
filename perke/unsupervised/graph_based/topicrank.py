# -*- coding: utf-8 -*-

"""
TopicRank keyphrase extraction model.

Graph-based ranking approach to keyphrase extraction described in:

* Adrien Bougouin, Florian Boudin and Béatrice Daille.
  TopicRank: Graph-Based Topic Ranking for Keyphrase Extraction.
  *In proceedings of IJCNLP*, pages 543-551, 2013.

"""

import string
from itertools import combinations

import networkx as nx
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist

from perke.base import LoadFile


class TopicRank(LoadFile):
    """
    TopicRank keyphrase extraction model.

    Examples
    --------
    import perke
    import string
    import hazm

    # 1. Create a TopicRank extractor.
    extractor = pke.unsupervised.TopicRank()

    # 2. Load the content of the document.
    extractor.load_document(input='path/to/input.txt')

    # 3. Select the longest sequences of nouns and adjectives, that do
    #    not contain punctuation marks or stopwords as candidates.
    pos = {'N', 'Ne', 'AJ', 'AJe'}
    punctuations = list(string.punctuation) + ['،', '.', '٪', '×', '؛', '؟']
    stoplist += hazm.stopwords_list() + punctuations
    extractor.candidate_selection(pos=pos, stoplist=stoplist)

    # 4. Build topics by grouping candidates with HAC (average linkage,
    #    threshold of 1/4 of shared stems). Weight the topics using random
    #    walk, and select the first occuring candidate from each topic.
    extractor.candidate_weighting(threshold=0.74, method='average')

    # 5. Get the 10-highest scored candidates as keyphrases
    keyphrases = extractor.get_n_best(n=10)

    Attributes
    ----------
    graph: nx.Graph
        The word graph

    topics: list
        The topic container
    """

    def __init__(self):
        """
        Redefining initializer for TopicRank.
        """

        super(TopicRank, self).__init__()
        self.graph = nx.Graph()
        self.topics = []

    def candidate_selection(self, pos=None, stoplist=None):
        """
        Selects longest sequences of nouns and adjectives as keyphrase
        candidates.

        Parameters
        ----------
        pos: set
            Set of valid POS tags, defaults to ('N', 'Ne', 'AJ', 'AJe')

        stoplist: list
            the stoplist for filtering candidates, defaults to
            the hazm stoplist. Words that are punctuation marks from
            string.punctuation are not allowed.

        """

        # Define default pos tags set
        if pos is None:
            pos = {'N', 'Ne', 'AJ', 'AJe'}

        # Select sequence of adjectives and nouns
        self.longest_pos_sequence_selection(valid_pos=pos)

        # Initialize stoplist list if not provided
        if stoplist is None:
            stoplist = self.stoplist

        # Filter candidates containing stopwords or punctuation marks
        self.candidate_filtering(stoplist=list(string.punctuation)
                                          + ['،', '.', '×', '؛', '؟']
                                          + stoplist)

    def vectorize_candidates(self):
        """
        Vectorize the keyphrase candidates.

        Returns
        -------
        C: list
            The list of candidates.
        X: matrix
            Vectorized representation of the candidates.
        """

        # Build the vocabulary, i.e. setting the vector dimensions
        dim = set([])
        # for k, v in self.candidates.iteritems():
        # Iterate Python 2/3 compatible
        for (k, v) in self.candidates.items():
            for w in v.lexical_form:
                dim.add(w)
        dim = list(dim)

        # Vectorize the candidates Python 2/3 + sort for random issues
        C = list(self.candidates)  # .keys()
        C.sort()

        X = np.zeros((len(C), len(dim)))
        for i, k in enumerate(C):
            for w in self.candidates[k].lexical_form:
                X[i, dim.index(w)] += 1

        return C, X

    def topic_clustering(self, threshold=0.74, method='average'):
        """
        Clustering candidates into topics.

        Parameters
        ----------
        threshold: float
            The minimum similarity for clustering, defaults
            to 0.74, i.e. more than 1/4 of stem overlap similarity.

        method: str
            The linkage method, defaults to average.
        """

        # Handle document with only one candidate
        if len(self.candidates) == 1:
            self.topics.append([list(self.candidates)[0]])
            return

        # Vectorize the candidates
        candidates, X = self.vectorize_candidates()

        # Compute the distance matrix
        Y = pdist(X, 'jaccard')

        # Compute the clusters
        Z = linkage(Y, method=method)

        # Form flat clusters
        clusters = fcluster(Z, t=threshold, criterion='distance')

        # For each topic identifier
        for cluster_id in range(1, max(clusters) + 1):
            self.topics.append([candidates[j] for j in range(len(clusters))
                                if clusters[j] == cluster_id])

    def build_topic_graph(self):
        """
        Build topic graph.
        """

        # Adding the nodes to the graph
        self.graph.add_nodes_from(range(len(self.topics)))

        # Loop through the topics to connect the nodes
        for i, j in combinations(range(len(self.topics)), 2):
            self.graph.add_edge(i, j, weight=0.0)
            for c_i in self.topics[i]:
                for c_j in self.topics[j]:
                    for p_i in self.candidates[c_i].offsets:
                        for p_j in self.candidates[c_j].offsets:
                            gap = abs(p_i - p_j)
                            if p_i < p_j:
                                gap -= len(self.candidates[c_i].lexical_form) - 1
                            if p_j < p_i:
                                gap -= len(self.candidates[c_j].lexical_form) - 1
                            self.graph[i][j]['weight'] += 1.0 / gap

    def candidate_weighting(self,
                            threshold=0.74,
                            method='average',
                            heuristic=None):
        """
        Candidate ranking using random walk.

        Parameters
        ----------
        threshold: float
            The minimum similarity for clustering, defaults
            to 0.74.

        method: str
            The linkage method, defaults to average.

        heuristic: str
            The heuristic for selecting the best candidate for
            each topic, defaults to first occurring candidate. Other options
            are 'frequent' (most frequent candidate, position is used for
            ties).
        """

        # Cluster the candidates
        self.topic_clustering(threshold=threshold, method=method)

        # Build the topic graph
        self.build_topic_graph()

        # Compute the word scores using random walk
        w = nx.pagerank_scipy(self.graph, alpha=0.85, weight='weight')

        # Loop through the topics
        for i, topic in enumerate(self.topics):

            # Get the offsets of the topic candidates
            offsets = [self.candidates[t].offsets[0] for t in topic]

            # Get first candidate from topic
            if heuristic == 'frequent':

                # Get frequencies for each candidate within the topic
                freq = [len(self.candidates[t].surface_forms) for t in topic]

                # Get the indexes of the most frequent candidates
                indexes = [j for j, f in enumerate(freq) if f == max(freq)]

                # Offsets of the indexes
                indexes_offsets = [offsets[j] for j in indexes]
                most_frequent = indexes_offsets.index(min(indexes_offsets))
                self.weights[topic[most_frequent]] = w[i]

            else:
                first = offsets.index(min(offsets))
                self.weights[topic[first]] = w[i]
