Installation
============
Perke is a Python package, which means you need to download and install Python
from `python.org <https://www.python.org/downloads>`_ if you haven't already.
Once you have Python installed, follow bellow steps:

- The easiest way to install is from PyPI:

  .. code:: bash

      pip install perke


  Alternatively, you can install directly from GitHub:

  .. code:: bash

      pip install git+https://github.com/alirezatheh/perke.git

- Perke also requires a trained POS tagger model. We use
  `hazm's <https://github.com/sobhe/hazm>`_ tagger model. You can download this
  model using the following command:

  .. code:: bash

      python -m perke download

  Alternatively, you can use another model with same tag names and structure,
  and put it in the
  `resources <https://github.com/alirezatheh/perke/tree/main/perke/resources>`_
  directory.
