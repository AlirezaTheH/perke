from perke.utils.enum import Enum


class WordNormalizationMethod(Enum):
    """
    Represents a word normalization method.
    """

    stemming = 'stemming'
    lemmatization = 'lemmatization'


class TopicHeuristic(Enum):
    """
    Represents a heuristic for selecting the best candidate for each
    topic.
    """

    first_occurring = 'first_occurring'
    frequent = 'frequent'


class HierarchicalClusteringLinkageMethod(Enum):
    """
    Represents a hierarchical clustering linkage method.
    """

    single = 'single'
    complete = 'complete'
    average = 'average'


class HierarchicalClusteringMetric(Enum):
    """
    Represents a hierarchical clustering metric.
    """

    euclidean = 'euclidean'
    seuclidean = 'seuclidean'
    jaccard = 'jaccard'
