from pathlib import Path

from perke.unsupervised.graph_based import TopicRank

# Define the set of valid part of speech tags to occur in the model.
valid_pos_tags = {'NOUN', 'ADJ'}

# 1. Create a TopicRank extractor.
extractor = TopicRank(valid_pos_tags=valid_pos_tags)

# 2. Load the text.
input_filepath = Path(__file__).parent.parent.parent / 'input.txt'
extractor.load_text(input=input_filepath, word_normalization_method='stemming')

# 3. Select the longest sequences of nouns and adjectives, that do
#    not contain punctuation marks or stopwords as candidates.
extractor.select_candidates()

# 4. Build topics by grouping candidates with HAC (average linkage,
#    jaccard distance, threshold of 1/4 of shared normalized words).
#    Weight the topics using random walk, and select the first
#    occurring candidate from each topic.
extractor.weight_candidates(
    threshold=0.74, metric='jaccard', linkage_method='average'
)

# 5. Get the 10 highest weighted candidates as keyphrases
keyphrases = extractor.get_n_best(n=10)

for i, (weight, keyphrase) in enumerate(keyphrases):
    print(f'{i + 1}.\t{keyphrase}, \t{weight}')
