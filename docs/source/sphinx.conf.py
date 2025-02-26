"""Configuration file for the Sphinx documentation builder."""

import os
import sys

# Add the project root directory to the path so Sphinx can find the modules
sys.path.insert(0, os.path.abspath('../..'))

# -- Project information -----------------------------------------------------
project = 'Git-Camus'
copyright = '2024, Evgeny Rachlenko'
author = 'Evgeny Rachlenko'

# The full version, including alpha/beta/rc tags
release = '0.1.0'


# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',  # Include documentation from docstrings
    'sphinx.ext.viewcode',  # Add links to the source code
    '