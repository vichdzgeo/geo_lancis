# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import pandas
import plotly.express as px
sys.path.insert(0, os.path.abspath('../../codigos/'))



sys.path.insert(0, 'C:/OSGEO4~1/apps/Python37/Scripts') # aqui se encuentra gdal calc
sys.path.insert(0, 'C:/OSGEO4~1/apps/qgis/bin')
sys.path.insert(0, 'C:/OSGEO4~1/apps/Python37/lib/site-packages') # en esta se ecuenta pyqt5.core
sys.path.insert(0, 'C:/OSGEO4~1/apps/qgis-dev/python')   #en esta se encuentra el modulo qgis
sys.path.insert(0, 'C:/OSGEO4~1/apps/qgis-dev/python/plugins')
sys.path.insert(0, 'C:/OSGEO4~1/share/proj')
sys.path.insert(0, 'C:/osgeo4~1/apps/python37/lib/site-packages/pyqt5')

sys.path.insert(0,'C:/osgeo4~1/apps/qgis-ltr/python/plugins/processing/algs/qgis') #algoritmos de processing 
#*************comentadas pero no eliminadas *****************
# sys.path.insert(0, 'C:/OSGEO4~1')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/Python37')
# sys.path.insert(0, 'C:/Program Files/MiKTeX 2.9/miktex/bin')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/Python37/lib/site-packages/numpy/.libs')

# sys.path.insert(0, 'C:/OSGEO4~1/share/gdal')
# sys.path.insert(0, 'C:/OSGEO4~1/bin')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/Python37/lib/site-packages/pythonwin')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/Python37/lib/site-packages/numpy')
#sys.path.insert(0, 'C:/OSGEO4~1/apps/qgis/python/plugins')



#***********removidas *****************#
sys.path.insert(0, 'C:/OSGEO4~1/apps/Python37/DLLs')
#sys.path.insert(0, 'C:/OSGEO4~1/bin/gdalplugins')
#sys.path.insert(0, 'C:/OSGEO4~1/apps/Python37/lib/site-packages/win32')
#sys.path.insert(0, 'C:/OSGEO4~1/apps/Python37/lib/site-packages/win32/lib')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/Python27/Scripts')
# sys.path.insert(0, 'C:/OSGEO4~1/bin;C:/WINDOWS/system32')
# sys.path.insert(0, 'C:/WINDOWS')
# sys.path.insert(0, 'C:/WINDOWS/system32/WBem')
# sys.path.insert(0, 'C:/Program Files/R/R-3.6.0/bin/x64')
# sys.path.insert(0, 'C:/OSGEO4~1/apps/Python37/lib/site-packages/pywin32_system32')
# -- Project information -----------------------------------------------------

project = 'Documentación de funciones y algoritmos en Python y QGIS para análisis espacial'
copyright = 'Licencia Creative Commons Atribución-CompartirIgual 4.0 Internacional.'
author =  'Víctor Hernández Díaz'

# The short X.Y version
version = ''
# The full version, including alpha/beta/rc tags
release = '1.0'


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'rst2pdf',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'es'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = None


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
html_sidebars = { '**': ['globaltoc.html', 'relations.html',
        'sourcelink.html', 'searchbox.html'], }
# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'Geoprocesamientoenpythonyqgisdoc'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'Geoprocesamientoenpythonyqgis.tex', 'Documentación de funciones y algoritmos en Python y Qgis para análisis espacial',
     'APC-LANCIS,UNAM', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'geoprocesamientoenpythonyqgis', 'Documentación de funciones y algoritmos en Python y Qgis para análisis espacial',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'Geoprocesamientoenpythonyqgis', 'Documentación de funciones y algoritmos en Python y Qgis para análisis espacial',
     author, 'Geoprocesamientoenpythonyqgis', 'One line description of project.',
     'Miscellaneous'),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']


# -- Extension configuration -------------------------------------------------

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'https://docs.python.org/': None}

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True
