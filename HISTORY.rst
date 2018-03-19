Release History
---------------

v0.4.0 (2018-03-16
^^^^^^^^^^^^^^^^^^

- 

v0.3.1 (2018-03-08)
^^^^^^^^^^^^^^^^^^^

- Fixed bug with multiline string containing "=" sign.
  Enforcing a maximum of 2 blank spaces prior to an 
  option declaration. Anything 3 or more is considered and
  indented continuation of the previous line.


v0.3.0 (2018-02-16)
^^^^^^^^^^^^^^^^^^^

- added option for coercing path strings into pathlib Path objects.
- added option for coercing decimal numbers as Decimal objects, 
  instead of floats.
- updated code file/object naming and dropped use of `ficus`


v0.2.4 (2018-01-16)
^^^^^^^^^^^^^^^^^^^

-  fixed bug with parsing values that have "=" signs in them. The regex
   was too broad. Now restricting key names to [A-Za-z0-9.-\_\|]
-  empty keys now return ``None``. This:

   .. code:: ini
        
       [section]
       value =

   will now produce this:

   .. code:: python
        
        assert config['section.value'] == None


v0.2.3 (2018-01-14)
^^^^^^^^^^^^^^^^^^^

-  fixed bug with dict.get method

v0.2.2 (2018-01-14)
^^^^^^^^^^^^^^^^^^^

-  extended sequence coercion to include tuples.

v0.2.1 (2018-01-07)
^^^^^^^^^^^^^^^^^^^

-  fixed bug when coercing boolean string values that contain extra
   white space.

v0.2.0 (2017-12-31)
^^^^^^^^^^^^^^^^^^^

-  added ability to pass an environment variable name as a config\_path.

v0.1.5 (2017-07-03)
^^^^^^^^^^^^^^^^^^^

-  added documentation site

v0.1.4 (2017-07-02)
^^^^^^^^^^^^^^^^^^^

-  using readme\_renderer from PYPA to check for proper readme RST
   format. Hoping this does the trick.

v0.1.3 (2017-07-02)
^^^^^^^^^^^^^^^^^^^

-  made changes to package to attempt to get a proper long description
   to work.

v0.1.2 (2017-06-21)
^^^^^^^^^^^^^^^^^^^

-  100% code coverage with Python 2.7, 3.3, 3.4, 3.5, 3.6
-  migrated package layout to using src based on these two
   recommendations:

   -  `Testing &
      Packaging <https://hynek.me/articles/testing-packaging/>`__
   -  `Packaging a Python
      Library <https://blog.ionelmc.ro/2014/05/25/python-packaging/#id13>`__

v0.1.1 (2017-06-06)
^^^^^^^^^^^^^^^^^^^

-  initial release


