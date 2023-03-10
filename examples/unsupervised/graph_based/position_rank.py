from pathlib import Path

from perke.unsupervised.graph_based import PositionRank

# Define the set of valid part of speech tags to occur in the model.
valid_pos_tags = {'N', 'Ne', 'AJ', 'AJe'}

# Define the grammar for selecting the keyphrase candidates
grammar = r"""
    NP:
        <P>{<N>}<V>
    NP:
        {<DETe?|Ne?|NUMe?|AJe|PRO|CL|RESe?><DETe?|Ne?|NUMe?|AJe?|PRO|CL|RESe?>*}
        <N>}{<.*e?>
"""

# 1. Create a PositionRank extractor.
extractor = PositionRank(valid_pos_tags=valid_pos_tags)

# 2. Load the text.
input_filepath = Path(__file__).parent.parent.parent / 'input.txt'
extractor.load_text(input=input_filepath, word_normalization_method=None)

# 3. Select the noun phrases up to 3 words as keyphrase candidates.
extractor.select_candidates(grammar=grammar, maximum_word_number=3)

# 4. Weight the candidates using the sum of their word's weights
#    that are computed using random walk biased with the position of
#    the words in the text. In the graph, nodes are words (nouns
#    and adjectives only) that are connected if they co-occur in a
#    window of 10 words.
extractor.weight_candidates(window_size=10)

# 5. Get the 10 highest weighted candidates as keyphrases
keyphrases = extractor.get_n_best(n=10)

for i, (weight, keyphrase) in enumerate(keyphrases):
    print(f'{i+1}.\t{keyphrase}, \t{weight}')
