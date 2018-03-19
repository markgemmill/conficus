Automatic Coercion
~~~~~~~~~~~~~~~~~~

``conficus`` will automatically coerce ini values of the following
types:

.. code:: python

    >>> import conficus as ficus


Integers
^^^^^^^^

Numbers represented with no decimal will convert to integers:

.. code:: python

    >>> cfg = ficus.load("integer = 102")
    >>> cfg["integer"]
    102

Floats
^^^^^^

Numbers with decimals will convter to floats:

.. code:: python

    >>> cfg = ficus.load("float=10.12")
    >>> cfg['float']
    10.12

Booleans
^^^^^^^^

True/False values will convert to boolean:

.. code:: python

    >>> cfg = ficus.load("booleans=[yes, true]")
    >>> cfg['booleans']
    [True, True]

    >>> cfg = ficus.load("booleans=[no, false]")
    >>> cfg['booleans']
    [False, False ]

DateTimes
^^^^^^^^^

Date and time values will convert to a datetime:

.. code:: python

    >>> cfg = ficus.load("datetime=2017-10-12T10:12:09")
    >>> cfg["datetime"]
    datetime.datetime(2017, 10, 12, 10, 12, 9)

Dates
^^^^^

Date values will convert to datetime:

.. code:: python

    >>> cfg = ficus.load("datetime=2017-10-12")
    >>> cfg["datetime"]
    datetime.datetime(2017, 10, 12, 0, 0)

Times
^^^^^

Time values will convert to datetime:

.. code:: python

    >>> cfg = ficus.load("time=10:12:09")
    >>> cfg['time']
    datetime.datetime(1900, 1, 1, 10, 12, 9)

Lists
^^^^^

Any value that begins and ends with "[" and "]" will be viewed as a list
whose content will be split on "commas":

.. code:: python

    >>> cfg = ficus.load("single-line-list=[99, 66, 84, 9, bill]")
    >>> cfg['single-line-list']
    [99, 66, 84, 9, 'bill']

Any multiline value that ends and begins with "[" and "]" will be viewed
as a list whose contents will be split on the new line:

.. code:: python

    >>> cfg = ficus.load('''multiline-list=[Herb
    ...     Mary
    ...     John
    ...     Sarah]''')
    >>> cfg['multiline-list']
    ['Herb', 'Mary', 'John', 'Sarah']

Commas are optional, but if used they are striped:

.. code:: python

    >>> cfg = ficus.load('''multiline-list=[Herb,
    ...     Mary,
    ...     John,
    ...     Sarah]''')
    >>> cfg['multiline-list']
    ['Herb', 'Mary', 'John', 'Sarah']


Strings
^^^^^^^

Anything that does not fall into the above types is considered a string:

.. code:: python

    >>> cfg = ficus.load("string=A wealthy gentleman waved his umbrella.")
    >>> cfg['string']
    'A wealthy gentleman waved his umbrella.'


Strings can span multiple lines, but must be indented at least 3 or more spaces. 
Indented white space and new lines are not preserved:

.. code:: python

    >>> cfg = ficus.load("string='''A wealthy gentleman 
        waved his umbrella.
        '''")
    >>> cfg['string']
    A wealthy gentleman waved his umbrella.


To preserve white space to the left, pipe (|) character can be used to 
designate the left edge: 

.. code:: python

    >>> cfg = ficus.load("string='''A wealthy gentleman... 
        |    waved his umbrella.
        '''")
    >>> cfg['string']
    A wealthy gentleman...    waved his umbrella.


To preserve new lines, use the back slash (\) to designate:

.. code:: python

    >>> cfg = ficus.load("string='''A wealthy gentleman...\ 
        |    waved his umbrella.
        '''")
    >>> cfg['string']
    A wealthy gentleman...
        waved his umbrella.
