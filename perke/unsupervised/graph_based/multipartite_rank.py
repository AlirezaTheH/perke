import math
from itertools import combinations

import networkx as nx

from perke.unsupervised.graph_based.topic_rank import TopicRank
from perke.base.types import (HierarchicalClusteringMetric,
                              HierarchicalClusteringLinkageMethod)


class MultipartiteRank(TopicRank):
    """
    MultipartiteRank keyphrase extractor

    This model encodes topical information within a multipartite graph
    structure. The model represents keyphrase candidates and topics in
    a single graph and exploits their mutually reinforcing relationship
    to improve candidate ranking.

    Implementation of the PositionRank described in:

    Florian Boudin.
    Unsupervised Keyphrase Extraction with Multipartite Graphs.
    In proceedings of NAACL, pages 667-672, 2018.

    Examples
    --------
    from perke.unsupervised.graph_based import MultipartiteRank
    from perke.base.types import (WordNormalizationMethod,
                                  HierarchicalClusteringMetric,
                                  HierarchicalClusteringLinkageMethod)

    # Define the set of valid part of speech tags to occur in the model.
    valid_pos_tags = {'N', 'Ne', 'AJ', 'AJe'}

    # 1. Create a MultipartiteRank extractor.
    extractor = MultipartiteRank(valid_pos_tags=valid_pos_tags)

    # 2. Load the text.
    extractor.load_text(
        input='text or path/to/input_file',
        word_normalization_method=WordNormalizationMethod.stemming)

    # 3. Select the longest sequences of nouns and adjectives, that do
    #    not contain punctuation marks or stopwords as candidates.
    extractor.select_candidates()

    # 4. Build the Multipartite graph and weight candidates using
    #    random walk, alpha controls the weight adjustment mechanism,
    #    see TopicRank for metric, linkage method and threshold
    #    parameters.
    extractor.weight_candidates(
        threshold=0.74,
        metric=HierarchicalClusteringMetric.jaccard,
        linkage_method=HierarchicalClusteringLinkageMethod.average,
        alpha=1.1)

    # 5. Get the 10 highest weighted candidates as keyphrases
    keyphrases = extractor.get_n_best(n=10)

    Attributes
    ----------
    topic_ids: dict
        Dict of canonical forms of candidates to to topic identifiers

    graph: nx.DiGraph
        The candidate graph
    """

    def __init__(self, valid_pos_tags=None):
        """
        Initializes  MultipartiteRank.

        Parameters
        ----------
        valid_pos_tags: set
            Set of valid part of speech tags, defaults to nouns and
            adjectives. I.e. `{'N', 'Ne', 'AJ', 'AJe'}`.
        """

        super().__init__(valid_pos_tags)
        self.topic_ids = {}
        self.graph = nx.DiGraph()

    def cluster_topics(
            self,
            threshold=0.74,
            metric=HierarchicalClusteringMetric.jaccard,
            linkage_method=HierarchicalClusteringLinkageMethod.average):
        """
        Clustering candidates into topics.

        Parameters
        ----------
        threshold: float
            The minimum similarity for clustering, defaults to `0.74`,
            i.e. more than 1/4 of normalized word overlap similarity.

        metric: str
            The hierarchical clustering metric, defaults to `'jaccard'`
            See `HierarchicalClusteringMetric` for available methods.

        linkage_method: str
            The hierarchical clustering linkage method, defaults to
            `'average'`. See HierarchicalClusteringLinkageMethod
            for available methods.
        """
        super().cluster_topics(threshold, metric, linkage_method)

        # Handle text with only one candidate
        if len(self.candidates) == 1:
            self.topic_ids[list(self.candidates)[0]] = 0
            return

        # Assign cluster identifiers to candidates
        for topic_id, topic in enumerate(self.topics):
            for c in topic:
                self.topic_ids[c] = topic_id

    def build_topic_graph(self):
        """
        Build the Multipartite graph.
        """

        # Adding the nodes to the graph
        self.graph.add_nodes_from(self.candidates.keys())

        # Pre-compute edge weights
        for node_i, node_j in combinations(self.candidates.keys(), 2):

            # Discard intra-topic edges
            if self.topic_ids[node_i] == self.topic_ids[node_j]:
                continue

            weights = []
            candidate_i = self.candidates[node_i]
            candidate_j = self.candidates[node_j]
            for p_i in candidate_i.offsets:
                for p_j in candidate_j.offsets:

                    # Compute gap
                    gap = abs(p_i - p_j)

                    # Alter gap according to candidate length
                    if p_i < p_j:
                        gap -= len(candidate_i.normalized_words) - 1
                    if p_j < p_i:
                        gap -= len(candidate_j.normalized_words) - 1

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
            Hyper-parameter that controls the strength of the weight
            adjustment, defaults to `1.1`.
        """

        weighted_edges = {}

        # Topical boosting
        for topic in self.topics:

            # Skip one candidate topics
            if len(topic) == 1:
                continue

            # Get the offsets
            offsets = [self.candidates[c].offsets[0] for c in topic]

            # Get the first occurring candidate
            first = topic[offsets.index(min(offsets))]

            # Find the nodes to which it connects
            for start, end in self.graph.edges(first):

                boosters = []
                for c in topic:
                    if c != first and self.graph.has_edge(c, end):
                        boosters.append(self.graph[c][end]['weight'])

                if boosters:
                    weighted_edges[(start, end)] = sum(boosters)

        # Update edge weights
        for nodes, boosters in weighted_edges.items():
            node_i, node_j = nodes
            position_i = 1.0 / (1 + self.candidates[node_i].offsets[0])
            position_i = math.exp(position_i)
            self.graph[node_j][node_i]['weight'] += boosters * alpha * position_i

    def weight_candidates(
            self,
            threshold=0.74,
            metric=HierarchicalClusteringMetric.jaccard,
            linkage_method=HierarchicalClusteringLinkageMethod.average,
            alpha=1.1):
        """
        Candidate weight calculation using random walk.

        Parameters
        ----------
        threshold: float
            The minimum similarity for clustering, defaults to 0.74.

        metric: str
            The hierarchical clustering metric, defaults to `'jaccard'`
            See `HierarchicalClusteringMetric` for available methods.

        linkage_method: str
            The hierarchical clustering linkage method, defaults to
            `'average'`. See HierarchicalClusteringLinkageMethod for
            available methods.

        alpha: float
            Hyper-parameter that controls the strength of the
            weight adjustment, defaults to `1.1`
        """

        # Cluster the candidates
        self.cluster_topics(threshold=threshold, linkage_method=linkage_method)

        # Build the topic graph
        self.build_topic_graph()

        if alpha > 0.0:
            self.weight_adjustment(alpha)

        # Compute the word weights using random walk
        weights = nx.pagerank_scipy(self.graph)
        for c in weights:
            self.candidates[c].weight = weights[c]