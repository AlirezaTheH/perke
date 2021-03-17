from perke.unsupervised.graph_based import MultipartiteRank
from perke.base.types import (WordNormalizationMethod,
                              HierarchicalClusteringMetric,
                              HierarchicalClusteringLinkageMethod)

# Define the valid parts of speech to occur in the graph
valid_pos_tags = {'N', 'Ne', 'AJ', 'AJe'}

# 1. Create a MultipartiteRank extractor.
extractor = MultipartiteRank(valid_pos_tags=valid_pos_tags)

# 2. Load the text.
extractor.load_text(
    input='input.txt',
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
for k in keyphrases:
    print(k)
