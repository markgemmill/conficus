Conficus v0.5.0
===================

Python INI Configuration
^^^^^^^^^^^^^^^^^^^^^^^^


|version-badge| |coverage-badge|

``conficus`` is a python ini configuration utility. It reads ini and toml based
configuration files into a python dict. ``conficus`` provides automatic
coercing of values (e.g. str -> int), nested sections, easy access and
section inheritance.

v0.5.0 drops support for all python versions less that 3.6. The next minor version
will also drop it's custom ini support solely for toml format.


Installation
~~~~~~~~~~~~

Install the ``ficus`` package with pip.

.. code:: bash

        pip install conficus

Quick Start
~~~~~~~~~~~

Basic usage:

.. ipython::

    In [1]: import conficus

Configurations can be loaded from a file path string:

.. ipython:: python

    config = conficus.load('/Users/mgemmill/config.ini')

Or from path stored in an environment variable:

.. ipython:: python

    config = conficus.load('ENV_VAR_CONFIG_PATH')


Or from a raw string:

.. ipython:: python

    config = conficus.load('config_option = true')


.. ipython:: python
    :suppress:

    config = conficus.load('test/samples/docs-sample.ini')


The configuration is a dictionary. This raw config:

.. include:: ../test/samples/docs-sample.ini
    :code: ini
    :start-after: # intro-example
    :end-before: # intro-example-end


Is accessible as standard dictionary keys:

.. ipython:: python

    config['app']['debug']


Or as a single string key:

.. ipython:: python

    config['app.debug']

Recognized types will automatically be converted from their string. In the
above examples the configuration value of ``yes`` is converted to ``True``.


Topics
^^^^^^

.. toctree::
   :maxdepth: 2

   coercion
   nested-sections
   inheritance
   release-history


.. |version-badge| image:: https://img.shields.io/badge/version-v0.5.0-green.svg
.. |coverage-badge| image:: https://img.shields.io/badge/coverage-100%25-green.svg

