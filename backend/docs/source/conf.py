# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

print(sys.path)
sys.path.insert(0, os.path.abspath("../../.."))
print(sys.path)
path = sys.path[0]


def print_directory_structure(path, indent=0):
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        print(" " * indent + item)
        if os.path.isdir(item_path):
            print_directory_structure(item_path, indent + 4)


print_directory_structure(path)


project = "VOCData"
copyright = "2024, Luka Gerlach"
author = "Luka Gerlach"
release = "0.0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",  # include docstrings
    "pydata_sphinx_theme",  # nice theme
    "sphinx.ext.viewcode",  # Add links to source code
]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

nbsphinx_allow_errors = True
html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
