# Perke
[![tests](https://github.com/alirezatheh/perke/workflows/tests/badge.svg)](https://github.com/alirezatheh/perke/actions/workflows/tests.yaml)
[![pre-commit.ci](https://results.pre-commit.ci/badge/github/AlirezaTheH/perke/main.svg)](https://results.pre-commit.ci/latest/github/alirezatheh/perke/main)
[![PyPI Version](https://img.shields.io/pypi/v/perke)](https://pypi.python.org/pypi/perke)
[![Python Versions](https://img.shields.io/pypi/pyversions/perke)](https://pypi.org/project/perke)
[![Documentation Status](https://readthedocs.org/projects/perke/badge/?version=stable)](https://perke.readthedocs.io/en/stable/?badge=stable)

Perke is a Python keyphrase extraction package for Persian language. It
provides an end-to-end keyphrase extraction pipeline in which each component
can be easily modified or extended to develop new models.

## Installation
- The easiest way to install is from PyPI:
  ```bash
  pip install perke
  ```
  Alternatively, you can install directly from GitHub:
  ```bash
  pip install git+https://github.com/alirezatheh/perke.git
  ```
- Perke also requires a trained POS tagger model. We use
  [Hazm's](https://github.com/roshan-research/hazm) POS tagger model. You can
  easily download latest [Hazm's](https://github.com/roshan-research/hazm) POS
  tagger using the following command:
  ```bash
  python -m perke download
  ```
  Alternatively, you can use another model with same tag names and structure,
  and put it in the
  [`resources`](https://github.com/alirezatheh/perke/tree/main/perke/resources)
  directory.

## Simple Example
Perke provides a standardized API for extracting keyphrases from a text. Start
by typing the 4 lines below to use `TextRank` keyphrase extractor.


```python
from perke.unsupervised.graph_based import TextRank

# 1. Create a TextRank extractor.
extractor = TextRank()

# 2. Load the text.
extractor.load_text(input='text or path/to/input_file')

# 3. Build the graph representation of the text and weight the
#    words. Keyphrase candidates are composed of the 33 percent
#    highest weighted words.
extractor.weight_candidates(top_t_percent=0.33)

# 4. Get the 10 highest weighted candidates as keyphrases.
keyphrases = extractor.get_n_best(n=10)
```

For more in depth examples see the
[`examples`](https://github.com/alirezatheh/perke/tree/main/examples)
directory.

## Documentation
Documentation and references are available at
[Read The Docs](https://perke.readthedocs.io).

## Implemented Models
Perke currently, implements the following keyphrase extraction models:

- Unsupervised models
    - Graph-based models
        - TextRank: [article](http://www.aclweb.org/anthology/W04-3252.pdf)
          by Mihalcea and Tarau, 2004
        - SingleRank: [article](https://www.aaai.org/Papers/AAAI/2008/AAAI08-136.pdf)
          by Wan and Xiao, 2008
        - TopicRank: [article](http://aclweb.org/anthology/I13-1062.pdf)
          by Bougouin, Boudin and Daille, 2013
        - PositionRank: [article](http://www.aclweb.org/anthology/P17-1102.pdf)
          by Florescu and Caragea, 2017
        - MultipartiteRank: [article](https://www.aclweb.org/anthology/N18-2105.pdf)
          by Boudin, 2018

## Acknowledgements
Perke is inspired by [pke](https://github.com/boudinfl/pke).
