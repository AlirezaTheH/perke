# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a
# full list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another
# directory, add these directories to sys.path here. If the directory is
# relative to the documentation root, use os.path.abspath to make it
# absolute, like shown here.

from os.path import dirname, join
import sys
import re

root = dirname(dirname(__file__))
sys.path.insert(0, root)

# -- Project information -----------------------------------------------

project = 'perke'
copyright = '2020-Present, Alireza Hosseini'
author = 'Alireza Hosseini'

# The short X.Y version.
with open(join(root, 'perke', 'version.py')) as f:
    version_pattern = re.compile(r'__version__\s+=\s+\'(?P<version>.*)\'')
    version = re.search(version_pattern, f.read()).group('version')

# The full version, including alpha/beta/rc tags
release = version


# -- General configuration ---------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.napoleon',
              'sphinx.ext.intersphinx']

# Napoleon configs
napoleon_use_ivar = True
napoleon_include_init_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_rtype = False

# Change the default role so we can avoid prefixing everything
# with :obj:
default_role = 'py:obj'

# Add any paths that contain templates here, relative to this directory.
# templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation
# for a list of builtin themes.
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets)
# here, relative to this directory. They are copied after the builtin
# static files, so a file named "default.css" will overwrite the builtin
# "default.css".
html_static_path = ['_static']
html_css_files = ['css/custom.css']