Command-line Interface
======================
Perke’s CLI provides some helpful commands for downloading and removing
required resources. For a list of available commands, you can use the following
command:

.. code:: bash

    python -m perke --help

You can also add the ``--help`` flag to any command to see the description,
available arguments and usage.

Commands
--------
- ``download``

  Perke requires a trained POS tagger model. We use hazm's tagger model. This
  command aims to easily download latest hazm's resources (tagger and parser
  models). The downloaded resources will be put in the
  `resources <https://github.com/alirezah320/perke/tree/main/perke/resources>`_
  directory so that Perke can use them.

  .. code:: bash

      python -m perke download

- ``clear``

  Clears the
  `resources <https://github.com/alirezah320/perke/tree/main/perke/resources>`_
  directory.

  .. code:: bash

      python -m perke clear
