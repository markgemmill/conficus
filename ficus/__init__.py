from os import path
from .parse import parse
from .coerce import coerce
from .inherit import inherit
from .readonly import ReadOnlyDict


def read_config(config_input):
    if path.exists(config_input):
        with open(config_input, 'r') as fh_:
            return fh_.readlines()
    return config_input.split('\n')


def load(config_path, inheritance=False, readonly=True):

    config = parse(read_config(config_path))

    config = coerce(config)

    if inheritance is True:
        config = inherit(config)

    if readonly is True:
        config = ReadOnlyDict(config)

    return config
