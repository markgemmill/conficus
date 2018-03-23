# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    = -b html -a
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = conficus
SOURCEDIR     = docs
BUILDDIR      = docs/_build
SPHINXAUTOBUILD = sphinx-autobuild

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

serve:
	@$(SPHINXAUTOBUILD) --open-browser "$(SOURCEDIR)" "$(BUILDDIR)" -b html -a

build:
	@$(SPHINXBUILD) $(SPHINXOPTS)  "$(SOURCEDIR)" "$(BUILDDIR)"


# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: build
