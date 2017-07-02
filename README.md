# Conficus - Python INI Configuration

![Alt url](https://img.shields.io/badge/version-v0.1.2-green.svg "v0.1.2")
![Alt url](https://img.shields.io/badge/coverage-100%25-green.svg "100% Coverage")


`conficus` is a python ini configuration utility. It reads ini-based
configuration files into a python dict. `conficus` provides automatic coercing of 
values (e.g. str -> int), nested sections, easy access and section inheritence.


### Installation

Install the `ficus` package with pip.

```bash
    pip install conficus
```


### Quick Start 

Basic usage:

```python
>>> 
>>> import conficus as ficus
>>>
>>> config = ficus.load('/Users/mgemmill/config.ini')
>>>
>>> # configuration is just a dictionary:
... 
>>> print config['app']['debug']
True
>>>
>>> # with ease of access:
... 
>>> print config['app.debug']
True

```
