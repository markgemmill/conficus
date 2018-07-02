###### FOLLOW ALL STEPS #######

### 1. ###
# first run version and update the version number in all the
# official locations.
#   setup.py
#   setup.cfg

### 2. ###
# then make sure we update all the other locations where the 
# version number resides.
#   HISTORY.md
#   Documentation

### 3. ###
# Make sure there is a version folder for the documentation
# on thebitsilo.com/dev/conficus/${VERSION}

### 4. ###
# Then run this script:
# . publish.sh

VERSION=`version`

echo "##############################"
echo "PUBLISHING CONFICUS v${VERSION}"
echo "##############################"

# get rid of the original
# rm README.rst
# rm HISTORY.md

# create README.rst for docs/index.md
# pandoc --from=markdown --to=rst --output=README.rst docs/docs/index.md
# copy release-history.md from docs/release-history.md
# cp docs/docs/release-history.md HISTORY.md

# at this point, we should run `python setup.py check -r -s` to 
# be sure we have the proper formatting.
python setup.py check -r -s

#
# create distributions
#
echo "##############################"
echo "CREATING DISTRIBUTION FOR ${VERSION}"
echo "##############################"
rm dist/*
python setup.py sdist bdist_wheel

#
# upload distributions
#
echo "##################################"
echo "UPLOADING CONFICUS ${VERSION} TO PYPI...."
echo "##################################"
twine upload --config-file setup.cfg dist/conficus-${VERSION}.tar.gz
twine upload --config-file setup.cfg dist/conficus-${VERSION}-py2.py3-none-any.whl

#
# generate documentation
#
# echo "##################################"
# echo "UPDATING CONFICUS ${VERSION} DOCUMENTATION...."
# echo "##################################"
# cd docs
# rmdir -rf ./site
# mkdir site
# 
# mkdocs build
# 
# echo "#######################################"
# echo "SYNCING CONFICUS ${VERSION} WEBSITE...."
# echo "#######################################"
# rsync -r --delete ./site/ aedilis@web591.webfaction.com:webapps/thebitsilo_www/dev/conficus/current/
# 
# # return to starting directory
# cd ..
