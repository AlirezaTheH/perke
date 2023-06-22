import math
from itertools import combinations
from typing import Dict, Optional, Set

import networkx as nx

from perke.base.types import (
    HierarchicalClusteringLinkageMethod,
    HierarchicalClusteringMetric,
)
from perke.unsupervised.graph_based.topic_rank import TopicRank


class MultipartiteRank(TopicRank):
    """
    MultipartiteRank keyphrase extractor

    This model encodes topical information within a multipartite graph
    structure. The model represents keyphrase candidates and topics in
    a single graph and exploits their mutually reinforcing relationship
    to improve candidate ranking.

    Note
    ----
    Implementation of the MultipartiteRank described in:

    | Florian Boudin
    | `Unsupervised Keyphrase Extraction with Multipartite Graphs
      <https://www.aclweb.org/anthology/N18-2105.pdf>`_
    | In proceedings of NAACL, pages 667-672, 2018


    Examples
    --------
    .. literalinclude:: ../../../examples/unsupervised/graph_based/multipartite_rank.py


    Attributes
    ----------
    topic_ids:
        Dict of canonical forms of candidates to topic identifiers

    graph:
        The candidate graph
    """

    def __init__(self, valid_pos_tags: Optional[Set[str]] = None) -> None:
        """
        Initializes  MultipartiteRank.

        Parameters
        ----------
        valid_pos_tags:
            Set of valid part of speech tags, defaults to nouns and
            adjectives. I.e. `{'NOUN', 'ADJ'}`.
        """
        super().__init__(valid_pos_tags)
        self.topic_ids: Dict[str, int] = {}
        self.graph: nx.DiGraph = nx.DiGraph()

    def _cluster_topics(
        self,
        threshold: float = 0.74,
        metric: HierarchicalClusteringMetric = 'jaccard',
        linkage_method: HierarchicalClusteringLinkageMethod = 'average',
    ) -> None:
        """
        Clustering candidates into topics.

        Parameters
        ----------
        threshold:
            The minimum similarity for clustering, defaults to `0.74`,
            i.e. more than 1/4 of normalized word overlap similarity.

        metric:
            The hierarchical clustering metric, defaults to `'jaccard'`
            See `perke.base.types.HierarchicalClusteringMetric` for
            available methods.

        linkage_method:
            The hierarchical clustering linkage method, defaults to
            `'average'`. See
            `perke.base.types.HierarchicalClusteringLinkageMethod` for
            available methods.
        """
        super()._cluster_topics(threshold, metric, linkage_method)

        # Handle text with only one candidate
        if len(self.candidates) == 1:
            self.topic_ids[list(self.candidates)[0]] = 0
            return

        # Assign cluster identifiers to candidates
        for topic_id, topic in enumerate(self.topics):
            for c in topic:
                self.topic_ids[c] = topic_id

    def _build_candidate_graph(self) -> None:
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

    def _adjust_weights(self, alpha: float = 1.1) -> None:
        """
        Adjust edge weights for boosting some candidates.

        Parameters
        ----------
        alpha:
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
            self.graph[node_j][node_i]['weight'] += (
                boosters * alpha * position_i
            )

    def weight_candidates(
        self,
        threshold: float = 0.74,
        metric: HierarchicalClusteringMetric = 'jaccard',
        linkage_method: HierarchicalClusteringLinkageMethod = 'average',
        alpha: float = 1.1,
    ) -> None:
        """
        Candidate weight calculation using random walk.

        Parameters
        ----------
        threshold:
            The minimum similarity for clustering, defaults to `0.74`,
            i.e. more than 1/4 of normalized word overlap similarity.

        metric:
            The hierarchical clustering metric, defaults to `'jaccard'`
            See `perke.base.types.HierarchicalClusteringMetric` for
            available methods.

        linkage_method:
            The hierarchical clustering linkage method, defaults to
            `'average'`. See
            `HierarchicalClusteringLinkageMethod` for
            available methods.

        alpha:
            Hyper-parameter that controls the strength of the
            weight adjustment, defaults to `1.1`
        """
        # Cluster the candidates
        self._cluster_topics(
            threshold=threshold, linkage_method=linkage_method
        )

        # Build the candidate graph
        self._build_candidate_graph()

        if alpha > 0.0:
            self._adjust_weights(alpha)

        # Compute the word weights using random walk
        weights = nx.pagerank(self.graph)
        for c in weights:
            self.candidates[c].weight = weights[c]
