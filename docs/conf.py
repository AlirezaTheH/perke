import re
import sys
from pathlib import Path

# -- Path setup --------------------------------------------------------
root = Path(__file__).parent.parent
sys.path.insert(0, str(root))


# -- Project information -----------------------------------------------
project = 'perke'
copyright = '2020-Present, Alireza Hosseini'
author = 'Alireza Hosseini'

# The short X.Y version.
with open(root / 'perke' / 'version.py') as f:
    __version__ = re.search(
        r'__version__\s+=\s+\'(?P<version>.*)\'', f.read()
    ).group('version')
    # The short X.Y version.
    version = '.'.join(__version__.split('.')[:2])
    # The full version, including alpha/beta/rc tags.
    release = __version__


# -- General configuration ---------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'myst_parser',
    'sphinx_copybutton',
    'docs.typer_ext',
]

# Autodoc configs
autodoc_typehints = 'both'
autodoc_typehints_description_target = 'documented'

# Napoleon configs
napoleon_use_ivar = True
napoleon_include_init_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_rtype = False

# Change the default role, so we can avoid prefixing everything with
# :obj:
default_role = 'py:obj'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------
html_theme = 'furo'
html_title = "Perke's documentation"
