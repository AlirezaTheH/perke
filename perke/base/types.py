class WordNormalizationMethod:
    """
    Represents a word normalization method.
    """
    stemming = 'stemming'
    lemmatization = 'lemmatization'


class TopicHeuristic:
    """
    Represents a heuristic for selecting the best candidate for each topic.
    """
    first_occurring = 'first_occurring'
    frequent = 'frequent'


class HierarchicalClusteringLinkageMethod:
    """
    Represents a hierarchical clustering linkage method
    """
    single = 'single'
    complete = 'complete'
    average = 'average'


class HierarchicalClusteringMetric:
    """
    Represents a hierarchical clustering metric
    """
    euclidean = 'euclidean'
    seuclidean = 'seuclidean'
    jaccard = 'jaccard'
