# Perke
[![Build Status](https://travis-ci.com/AlirezaH320/perke.svg?branch=master)](https://travis-ci.com/AlirezaH320/perke)
[![PyPI Version](https://img.shields.io/pypi/v/perke)](https://pypi.python.org/pypi/perke)
[![Python Versions](https://img.shields.io/pypi/pyversions/perke)](https://pypi.org/project/perke)

`perke` is an **open source** python-based **keyphrase extraction** toolkit for 
persian language. It provides an end-to-end keyphrase extraction pipeline in 
which each component can be easily modified or extended to develop new models.

## Installation
- The easiest way to install is from PyPI:
  ```bash
  pip install perke
  ```
  Alternatively, you can install directly from the GitHub:
  ```bash
  pip install git+https://github.com/alirezah320/perke.git
  ```
- `perke` also requires a pos tagger model that can be obtained from 
  [here](https://github.com/sobhe/hazm/releases/download/v0.5/resources-0.5.zip) and 
  must be put in 
  [resources](https://github.com/alirezah320/perke/tree/master/perke/resources) 
  directory.

## Minimal example
`perke` provides a standardized API for extracting keyphrases from a document. 
Start by typing the 4 lines below. For using another model, simply replace 
`TextRank` with another model.

```python
from perke.unsupervised.graph_based import TextRank

# Define the set of valid part of speech tags to occur in the model.
valid_pos_tags = {'N', 'Ne', 'AJ', 'AJe'}

# 1. Create a TextRank extractor.
extractor = TextRank(valid_pos_tags=valid_pos_tags)

# 2. Load the text.
extractor.load_text(input='text or path/to/input_file',
                    word_normalization_method=None)

# 3. Build the graph representation of the text and weight the
#    words. Keyphrase candidates are composed from the 33 percent
#    highest weighted words.
extractor.weight_candidates(window_size=2, top_t_percent=0.33)

# 4. Get the 10 highest weighted candidates as keyphrases.
keyphrases = extractor.get_n_best(n=10)
```

Detailed examples are provided in the [examples](examples) directory.

## Implemented models
`perke` currently, implements the following keyphrase extraction models:

- Unsupervised models
    - Graph-based models
        - TextRank: article by [Mihalcea and Tarau, 2004](http://www.aclweb.org/anthology/W04-3252.pdf)
        - SingleRank: article by [Wan and Xiao, 2008](https://www.aaai.org/Papers/AAAI/2008/AAAI08-136.pdf)
        - TopicRank: article by [Bougouin et al., 2013](http://aclweb.org/anthology/I13-1062.pdf)
        - PositionRank: article by [Florescu and Caragea, 2017](http://www.aclweb.org/anthology/P17-1102.pdf)
        - MultipartiteRank: article by [Boudin, 2018](https://www.aclweb.org/anthology/N18-2105.pdf)