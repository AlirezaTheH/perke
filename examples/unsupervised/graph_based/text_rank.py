from pathlib import Path

from perke.unsupervised.graph_based import TextRank

# Define the set of valid part of speech tags to occur in the model.
valid_pos_tags = {'N', 'Ne', 'AJ', 'AJe'}

# 1. Create a TextRank extractor.
extractor = TextRank(valid_pos_tags=valid_pos_tags)

# 2. Load the text.
input_filepath = Path(__file__).parent.parent.parent / 'input.txt'
extractor.load_text(input=input_filepath, word_normalization_method=None)

# 3. Build the graph representation of the text and weight the
#    words. Keyphrase candidates are composed of the 33 percent
#    highest weighted words.
extractor.weight_candidates(window_size=2, top_t_percent=0.33)

# 4. Get the 10 highest weighted candidates as keyphrases.
keyphrases = extractor.get_n_best(n=10)

for i, (weight, keyphrase) in enumerate(keyphrases):
    print(f'{i+1}.\t{keyphrase}, \t{weight}')
