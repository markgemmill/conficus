# get rid of the original
rm README.rst

# create README.rst for docs/index.md
pandoc --from=markdown --to=rst --output=README.rst docs/docs/index.md

# at this point, we should run `python setup.py check -r -s` to 
# be sure we have the proper formatting.

# create distributions
rm dist/*
python setup.py sdist bdist_wheel

# upload distributions
#twine upload --config-file setup.cfg dist/conficus-0.1.3.tar.gz
