from typing import Literal

#:
WordNormalizationMethod = Literal['stemming', 'lemmatization', None]
#:
TopicHeuristic = Literal['first_occurring', 'frequent']
#:
HierarchicalClusteringLinkageMethod = Literal['single', 'complete', 'average']
#:
HierarchicalClusteringMetric = Literal['euclidean', 'seuclidean', 'jaccard']
