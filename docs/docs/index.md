# Welcome To Ficus Configuration 

## Ficus 

![Alt url](https://img.shields.io/badge/version-v0.1.1-green.svg "v0.1.1")
![Alt url](https://img.shields.io/badge/coverage-100%25-green.svg "100% Coverage")


`ficus` is a python ini configuration library. It reads ini-based
configuration files into a python dict. `ficus` provides automatic coercing of 
values (e.g. str -> int), nested sections, easy access and section inheritence.

### Installation

Install the `ficus` package with pip.

    pip install ficus

### Quick Start 

Basic usage:

```python

import ficus

config = ficus.load('/Users/mgemmill/config.ini')

# prints True
print config['app']['debug']

# prints True
print config['app.debug']

```

