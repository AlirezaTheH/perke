from collections import defaultdict

import networkx as nx

from perke.unsupervised.graph_based.single_rank import SingleRank


class PositionRank(SingleRank):
    """
    PositionRank keyphrase extractor

    This model is an unsupervised approach to extract keyphrases from 
    scholarly documents that incorporates information from all positions 
    of a word's occurrences into a biased PageRank.

    Implementation of the PositionRank described in:

    Corina Florescu and Cornelia Caragea.
    PositionRank: An Unsupervised Approach to Keyphrase Extraction from 
    Scholarly Documents.
    In proceedings of ACL, pages 1105-1115, 2017.

    Examples
    --------
    from perke.unsupervised.graph_based import PositionRank

    # Define the set of valid part of speech tags to occur in the graph.
    valid_pos_tags = {'N', 'Ne', 'AJ', 'AJe'}

    # Define the grammar for selecting the keyphrase candidates
    grammar = r'
        NP:
            <P>{<N>}<V>
        NP:
            {<DETe?|Ne?|NUMe?|AJe|PRO|CL|RESe?><DETe?|Ne?|NUMe?|AJe?|PRO|CL|RESe?>*}
            <N>}{<.*e?>
    '

    # 1. Create a PositionRank extractor.
    extractor = PositionRank(valid_pos_tags=valid_pos_tags)

    # 2. Load the text.
    extractor.load_text(input='text or path/to/input_file', 
                        word_normalization_method=None)

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

    Attributes
    ----------
    positions: defaultdict(float)
        Container the sums of word's inverse positions
    """

    def __init__(self, valid_pos_tags=None):
        """
        Initializes PositionRank.

        Parameters
        ----------
        valid_pos_tags: set
            Set of valid part of speech tags, defaults to nouns and
            adjectives. I.e. `{'N', 'Ne', 'AJ', 'AJe'}`.
        """
        super().__init__(valid_pos_tags)
        self.positions = defaultdict(float)

    def select_candidates(self, grammar=None, maximum_length=3, **kwargs):
        """
        Candidate selection heuristic using a syntactic part of speech 
        pattern for noun phrase extraction. Keyphrase candidates are 
        noun phrases that match the regular expression 
        (adjective)*(noun)+, with a given length.

        Parameters
        ----------
        grammar: str
            Grammar defining part of speech patterns of noun phrases, 
            defaults to
            `'NP:
                <P>{<N>}<V>
            NP:
                {<DETe?|Ne?|NUMe?|AJe|PRO|CL|RESe?><DETe?|Ne?|NUMe?
                |AJe?|PRO|CL|RESe?>*}
                <N>}{<.*e?>.'`

        maximum_length: int
            Maximum length in words of the candidate, defaults to `3`.
        """

        if grammar is None:
            grammar = r"""
                NP:
                    <P>{<N>}<V>
                NP:
                    {<DETe?|Ne?|NUMe?|AJe|PRO|CL|RESe?><DETe?|Ne?|NUMe?|AJe?|PRO|CL|RESe?>*}
                    <N>}{<.*e?>
            """

        # Select sequence of noun phrases with given pattern
        self.select_candidates_with_grammar(grammar=grammar)

        self.filter_candidates(maximum_length)

    def build_word_graph(self, window_size=10):
        """
        Build the graph representation of the text. In the graph, nodes
        are words that passes a parts of speech filter. Two nodes are
        connected if the words corresponding to these nodes co-occur
        within a window of contiguous tokens. The weight of an edge is
        computed based on the co-occurrence count of the two words
        within a window of successive tokens.

        Parameters
        ----------
        window_size: int
            The size of window for connecting two words in the graph,
            defaults to `10`.
        """

        # Flatten text as a sequence of only passed syntactic filter
        # (word, position) tuples
        flatten_text = []
        shift = 0
        for i, sentence in enumerate(self.sentences):
            for j, word in enumerate(sentence.normalized_words):
                if sentence.pos_tags[j] in self.valid_pos:
                    flatten_text.append((word, shift + j))

                    # Add node to the graph
                    self.graph.add_node(word)

            shift += sentence.length

        # Add edges to the graph
        for i, (first_node, first_node_position) in enumerate(flatten_text):
            for second_node, second_node_position in flatten_text[i + 1:]:
                if ((second_node_position - first_node_position) < window_size
                        and first_node != second_node):
                    if not self.graph.has_edge(first_node, second_node):
                        self.graph.add_edge(first_node, second_node, weight=0)

                    self.graph[first_node][second_node]['weight'] += 1

        # Compute the sums of the word's inverse positions
        for word, position in flatten_text:
            self.positions[word] += 1 / (position + 1)

    def weight_candidates(self,
                          window_size=10,
                          normalize_weights=False,
                          **kwargs):
        """
        Calculates candidates weights using a biased PageRank.

        Parameters
        ----------
        window_size: int
            The size of window for connecting two words in the graph,
            defaults to `10`.

        normalize_weights: bool
            Normalize keyphrase weight by their length, defaults to
            `False`.
        """

        # Build the word graph
        self.build_word_graph(window_size)

        # Normalize cumulated inverse positions
        position_sum = sum(self.positions.values())
        for word in self.positions:
            self.positions[word] /= position_sum

        # Compute the word weights using biased random walk
        weights = nx.pagerank(G=self.graph,
                              alpha=0.85,
                              tol=0.0001,
                              personalization=self.positions,
                              weight='weight')

        self.weight_candidates_with_words_weights(
            weights,
            normalize_weights,
            use_position_adjustment=False)

    def filter_candidates(self, maximum_length=3, **kwargs):
        """
        Filters the candidates with given conditions.

        Parameters
        ----------
        maximum_length: int
            Maximum length in words of the candidate, defaults to 3.
        """
        for c in list(self.candidates):
            if len(self.candidates[c].normalized_words) > maximum_length:
                del self.candidates[c]
