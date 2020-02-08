# -*- coding: utf-8 -*-

"""
Multipartite graph keyphrase extraction model.

Graph-based ranking approach to keyphrase extraction described in:

* Florian Boudin.
  Unsupervised Keyphrase Extraction with Multipartite Graphs.
  *In proceedings of NAACL*, pages 667-672, 2018.

"""

import math
from itertools import combinations

import networkx as nx
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist

from perke.unsupervised.graph_based.topicrank import TopicRank


class MultipartiteRank(TopicRank):
    """
    Multipartite graph keyphrase extraction model.

    Examples
    --------

    import perke
    import string
    import hazm

    # 1. Create a MultipartiteRank extractor.
    extractor = pke.unsupervised.MultipartiteRank()

    # 2. Load the content of the document.
    extractor.load_document(input='path/to/input.txt')

    # 3. Select the longest sequences of nouns and adjectives, that do
    #    not contain punctuation marks or stopwords as candidates.
    pos = {'N', 'Ne', 'AJ', 'AJe'}
    punctuations = list(string.punctuation) + ['،', '.', '٪', '×', '؛', '؟']
    stoplist += hazm.stopwords_list() + punctuations
    extractor.candidate_selection(pos=pos, stoplist=stoplist)

    # 4. Build the Multipartite graph and rank candidates using random walk,
    #    alpha controls the weight adjustment mechanism, see TopicRank for
    #    threshold/method parameters.
    extractor.candidate_weighting(alpha=1.1,
                                  threshold=0.74,
                                  method='average')

    # 5. Get the 10-highest scored candidates as keyphrases
    keyphrases = extractor.get_n_best(n=10)

    Attributes
    ----------
    topic_identifiers: dict
        A container for linking candidates to topic identifiers

    graph: nx.DiGraph
        Redefine the graph as a directed graph
    """

    def __init__(self):
        """
        Redefining initializer for MultipartiteRank.
        """

        super(MultipartiteRank, self).__init__()

        self.topic_identifiers = {}
        self.graph = nx.DiGraph()

    def topic_clustering(self,
                         threshold=0.74,
                         method='average'):
        """
        Clustering candidates into topics.

        Parameters
        ----------
            threshold: float
                The minimum similarity for clustering,
                defaults to 0.74, i.e. more than 1/4 of stem overlap
                similarity.
            method: str
                The linkage method, defaults to average.
        """

        # Handle document with only one candidate
        if len(self.candidates) == 1:
            candidate = list(self.candidates)[0]
            self.topics.append([candidate])
            self.topic_identifiers[candidate] = 0
            return

        # Vectorize the candidates
        candidates, X = self.vectorize_candidates()

        # Compute the distance matrix
        Y = pdist(X, 'jaccard')
        Y = np.nan_to_num(Y)

        # Compute the clusters
        Z = linkage(Y, method=method)

        # Form flat clusters
        clusters = fcluster(Z, t=threshold, criterion='distance')

        # For each cluster id
        for cluster_id in range(1, max(clusters) + 1):
            self.topics.append([candidates[j] for j in range(len(clusters))
                                if clusters[j] == cluster_id])

        # Assign cluster identifiers to candidates
        for i, cluster_id in enumerate(clusters):
            self.topic_identifiers[candidates[i]] = cluster_id - 1

    def build_topic_graph(self):
        """
        Build the Multipartite graph.
        """

        # Adding the nodes to the graph
        self.graph.add_nodes_from(self.candidates.keys())

        # Pre-compute edge weights
        for node_i, node_j in combinations(self.candidates.keys(), 2):

            # Discard intra-topic edges
            if self.topic_identifiers[node_i] == self.topic_identifiers[node_j]:
                continue

            weights = []
            for p_i in self.candidates[node_i].offsets:
                for p_j in self.candidates[node_j].offsets:

                    # Compute gap
                    gap = abs(p_i - p_j)

                    # Alter gap according to candidate length
                    if p_i < p_j:
                        gap -= len(self.candidates[node_i].lexical_form) - 1
                    if p_j < p_i:
                        gap -= len(self.candidates[node_j].lexical_form) - 1

                    weights.append(1.0 / gap)

            # Add weighted edges
            if weights:
                # node_i -> node_j
                self.graph.add_edge(node_i, node_j, weight=sum(weights))
                # node_j -> node_i
                self.graph.add_edge(node_j, node_i, weight=sum(weights))

    def weight_adjustment(self, alpha=1.1):
        """
        Adjust edge weights for boosting some candidates.

        Parameters
        ----------
        alpha: float
            Hyper-parameter that controls the strength of the
            weight adjustment, defaults to 1.1.
        """

        # weighted_edges = defaultdict(list)
        weighted_edges = {}

        # Find the sum of all first positions
        norm = sum([s.length for s in self.sentences])

        # Topical boosting
        for variants in self.topics:

            # Skip one candidate topics
            if len(variants) == 1:
                continue

            # Get the offsets
            offsets = [self.candidates[v].offsets[0] for v in variants]

            # Get the first occurring variant
            first = variants[offsets.index(min(offsets))]

            # Find the nodes to which it connects -- Python 2/3 compatible
            # for start, end in self.graph.edges_iter(first):
            for start, end in self.graph.edges(first):

                boosters = []
                for v in variants:
                    if v != first and self.graph.has_edge(v, end):
                        boosters.append(self.graph[v][end]['weight'])

                if boosters:
                    weighted_edges[(start, end)] = np.sum(boosters)

        # Update edge weights -- Python 2/3 compatible
        # for nodes, boosters in weighted_edges.iteritems():
        for nodes, boosters in weighted_edges.items():
            node_i, node_j = nodes
            position_i = 1.0 / (1 + self.candidates[node_i].offsets[0])
            position_i = math.exp(position_i)
            self.graph[node_j][node_i]['weight'] += (boosters * alpha * position_i)

    def candidate_weighting(self,
                            threshold=0.74,
                            method='average',
                            alpha=1.1):
        """
        Candidate weight calculation using random walk.

        Parameters
        ----------
        threshold: float
            The minimum similarity for clustering,
            defaults to 0.25

        method: str
            The linkage method, defaults to average

        alpha: float
            Hyper-parameter that controls the strength of the
            weight adjustment, defaults to 1.1
        """

        # Cluster the candidates
        self.topic_clustering(threshold=threshold, method=method)

        # Build the topic graph
        self.build_topic_graph()

        if alpha > 0.0:
            self.weight_adjustment(alpha)

        # Compute the word scores using random walk
        self.weights = nx.pagerank_scipy(self.graph)
