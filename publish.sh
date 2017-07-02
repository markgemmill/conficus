# create README.rst for docs/index.md
pandoc --from=markdown --to=rst --output=README.rst docs4/docs/index.md

# create distributions
rm dist/*
python setup.py sdist bdist_wheel

# upload distributions
twine upload --config-file setup.cfg dist/conficus-0.1.3.tar.gz
