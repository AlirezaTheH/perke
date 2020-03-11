# Perke (Persian Keyphrase Extractor)

`perke` is an **open source** python-based **keyphrase extraction** toolkit for persian language. It 
provides an end-to-end keyphrase extraction pipeline in which each component can
be easily modified or extended to develop new models.

## Installation

To pip install `perke` from github:

```bash
pip install git+https://github.com/alirezah320/perke.git
```

`perke` also requires a pos tagger model that can be obtained from 
[here](https://github.com/sobhe/hazm/releases/download/v0.5/resources-0.5.zip) and must be putted in recourses directory

`perke` only supports Python 3.7+.

## Minimal example

`perke` provides a standardized API for extracting keyphrases from a document. 
Start by typing the 5 lines below. For using another model, 
simply replace `perke.unsupervised.TopicRank` with another model 
([list of implemented models](#implemented-models)).

```python
import perke

# Initialize keyphrase extraction model, here TopicRank
extractor = perke.unsupervised.TopicRank()

# Load the content of the document, here document is expected to be in raw
# format (i.e. a simple text file) and preprocessing is carried out using hazm
extractor.load_document(input='/path/to/input.txt')

# Keyphrase candidate selection, in the case of TopicRank: sequences of nouns
# and adjectives (i.e. `(Noun|Adj)*`)
extractor.candidate_selection()

# Candidate weighting, in the case of TopicRank: using a random walk algorithm
extractor.candidate_weighting()

# N-best selection, keyphrases contains the 10 highest scored candidates as
# (keyphrase, score) tuples
keyphrases = extractor.get_n_best(n=10)
```

A detailed example is provided in the [`examples/`](examples/) directory.

## Implemented models

`perke` currently implements the following keyphrase extraction models:

* Unsupervised models
    * Graph-based models
        * TextRank: article by [Mihalcea and Tarau, 2004](http://www.aclweb.org/anthology/W04-3252.pdf)
        * SingleRank: article by [Wan and Xiao, 2008](http://www.aclweb.org/anthology/C08-1122.pdf)
        * TopicRank: article by [Bougouin et al., 2013](http://aclweb.org/anthology/I13-1062.pdf)
        * PositionRank: article by [Florescu and Caragea, 2017](http://www.aclweb.org/anthology/P17-1102.pdf)
        * MultipartiteRank: article by [Boudin, 2018](https://arxiv.org/abs/1803.08721)
