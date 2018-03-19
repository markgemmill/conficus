# -*- coding: utf-8 -*-
import alabaster

project = 'conficus'
copyright = '2018, Mark Gemmill'
author = 'Mark Gemmill'

version = '0.4.0-dev'
release = version


# -- General configuration ---------------------------------------------------


templates_path = ['templates']
source_suffix = '.rst'
master_doc = 'index'
language = None
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
html_theme = 'alabaster'
html_static_path = ['static']

html_theme_options = {
    'extra_nav_links': {
    }
}

html_sidebars =  {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
        'searchbox.html',
        'donate.html'
    ]
}

# -- Options for HTMLHelp output ---------------------------------------------
htmlhelp_basename = 'conficusdoc'


# -- Options for LaTeX output ------------------------------------------------
latex_elements = {
}
latex_documents = [
    (master_doc, 'conficus.tex', 'conficus Documentation',
     'Mark Gemmill', 'manual'),
]


# -- Options for manual page output ------------------------------------------
man_pages = [
    (master_doc, 'conficus', 'conficus Documentation',
     [author], 1)
]

# -- Options for Texinfo output ----------------------------------------------
texinfo_documents = [
    (master_doc, 'conficus', 'conficus Documentation',
     author, 'conficus', 'One line description of project.',
     'Miscellaneous'),
]

todo_include_todos =  False
