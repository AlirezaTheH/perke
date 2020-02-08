import perke

# Initialize keyphrase extraction model, here TopicRank
extractor = perke.unsupervised.TopicRank()

# Load the content of the document, here document is expected to be in raw
# format (i.e. a simple text file) and preprocessing is carried out using hazm
extractor.load_document(input='input.txt')

# Keyphrase candidate selection, in the case of TopicRank: sequences of nouns
# and adjectives (i.e. `(Noun|Adj)*`)
extractor.candidate_selection()

# Candidate weighting, in the case of TopicRank: using a random walk algorithm
extractor.candidate_weighting()

# N-best selection, keyphrases contains the 10 highest scored candidates as
# (keyphrase, score) tuples
keyphrases = extractor.get_n_best(n=10)
for k in keyphrases:
    print(k)
