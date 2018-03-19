if [ "$1" = "build" ]
then
    # cp ./documentation/index.rst README.rst
    sphinx-build -b html -a ./docs/ ./docs/_build
fi

if [ "$1" = "serve" ]
then
    sphinx-autobuild -b html -a --open-browser ./docs ./docs/_build
fi
