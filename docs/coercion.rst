Coercion
~~~~~~~~

``conficus`` will automatically coerce basic types such integers, booleans and dates. Flat lists of basic types will also be converted automatically.

In the examples below we use :doc:`sample-doc.ini <sample-doc>`.


.. ipython:: python
    :okexcept:
    :okwarning:
    :supress:

    from pathlib import Path
    pth = Path('.').resolve()
    print('CWD: {}'.format(pth))


    .. include:: ../test/samples/docs-sample.ini
        :code: text


.. ipython:: python
    :okexcept:
    :okwarning:

    import conficus
    cfg = conficus.load('test/samples/docs-sample.ini')


Integers
^^^^^^^^

Numbers represented with no decimal will convert to integers:

.. include:: ../test/samples/docs-sample.ini
    :code: ini
    :start-after: # coerce-integer
    :end-before: # coerce-float

.. ipython:: python
    :okexcept:
    :okwarning:

    cfg["integer"]

Floats
^^^^^^

Numbers with decimals will convter to floats:

.. include:: ../test/samples/docs-sample.ini
    :code: ini
    :start-after: # coerce-float
    :end-before:  # coerce-boolean

.. ipython:: python
    :okexcept:
    :okwarning:

    cfg['float']


Booleans
^^^^^^^^

True/False values will convert to `boolean`:

.. include:: ../test/samples/docs-sample.ini
    :code: ini
    :start-after: # coerce-boolean
    :end-before: # coerce-dates

.. ipython:: python
    :okexcept:
    :okwarning:

    cfg['boolean-yes']

    cfg['boolean-no']

    cfg['boolean-true']

    cfg['boolean-false']


Dates and Times
^^^^^^^^^^^^^^^


.. include:: ../test/samples/docs-sample.ini
    :code: ini
    :start-after: # coerce-dates
    :end-before: # coerce-list-1


Dates
-----

Date values will convert to `datetime`:

.. ipython:: python
    :okexcept:
    :okwarning:

    cfg["date"]

Times
-----

Time values will convert to `datetime`:

.. ipython:: python
    :okexcept:
    :okwarning:

    cfg['time']


DateTimes
---------

Date and time values will convert to a `datetime`:

.. ipython:: python
    :okexcept:
    :okwarning:

    cfg["date-and-time"]


Lists
^^^^^

Any value that begins and ends with "[" and "]" will be viewed as a list
whose content will be split on "commas":

.. include:: ../test/samples/docs-sample.ini
    :code: ini
    :start-after: # coerce-list-1
    :end-before: # coerce-list-2


.. ipython:: python
    :okexcept:
    :okwarning:

    cfg['single-line-list']

Any multiline value that ends and begins with "[" and "]" will be viewed
as a list whose contents will be split on the new line:

.. include:: ../test/samples/docs-sample.ini
    :code: ini
    :start-after: # coerce-list-2
    :end-before: # coerce-list-3

.. ipython:: python
    :okexcept:
    :okwarning:

    cfg['multiline-list-no-commas']

Commas are optional, but if used they are striped:

.. include:: ../test/samples/docs-sample.ini
    :code: ini
    :start-after: # coerce-list-3
    :end-before: # coerce-list-4

.. ipython:: python
    :okexcept:
    :okwarning:

    cfg['multiline-list-with-commas']

Tuples
^^^^^^

Values that begin  with ``(`` and end with ``)`` are converted
to a `tuple` in the same way as a `list` above.

.. include:: ../test/samples/docs-sample.ini
    :code: ini
    :start-after: # coerce-tuple-1
    :end-before: # coerce-tuple-2

.. ipython:: python
    :okexcept:
    :okwarning:

    cfg['single-line-tuple']


.. include:: ../test/samples/docs-sample.ini
    :code: ini
    :start-after: # coerce-tuple-2
    :end-before: # coerce-tuple-end

.. ipython:: python
    :okexcept:
    :okwarning:

    cfg['multiline-tuple']

Strings
^^^^^^^

Anything that does not fall into the above types is considered a string:

.. include:: ../test/samples/docs-sample.ini
    :code: ini
    :start-after: # coerce-string-1
    :end-before: # coerce-string-2

.. ipython:: python
    :okexcept:
    :okwarning:

    cfg['string']


Strings can span multiple lines, but must be indented at least 3 or
more spaces. Indented white space and new lines are not preserved:

.. include:: ../test/samples/docs-sample.ini
    :code: ini
    :start-after: # coerce-string-2
    :end-before: # coerce-string-3

.. ipython:: python
    :okexcept:
    :okwarning:

    cfg['string-multiline']



To preserve new lines, use the back slash (\\) to designate the right edge:

.. include:: ../test/samples/docs-sample.ini
    :code: ini
    :start-after: # coerce-string-3
    :end-before: # coerce-string-4

.. ipython:: python
    :okexcept:
    :okwarning:

    cfg['string-multiline-preserve-new-lines']


To preserve white space to the left, pipe (|) character can be used to
designate the left edge:

.. include:: ../test/samples/docs-sample.ini
    :code: ini
    :start-after: # coerce-string-4
    :end-before: # coerce-string-end

.. ipython:: python
    :okexcept:
    :okwarning:

    cfg['string-multiline-preserve-space']



Optional Conversions
^^^^^^^^^^^^^^^^^^^^

Decimals
--------

If the `use_decimal=True` option is passed to
the `load` function, decimal numbers will be converted to
python `Decimal` type instead of `float`:


.. include:: ../test/samples/docs-sample.ini
    :code: ini
    :start-after: # coerce-float
    :end-before:  # coerce-boolean


.. ipython:: python
    :okexcept:
    :okwarning:

    cfg = conficus.load('test/samples/docs-sample.ini', use_decimal=True)
    cfg['float']


Paths
-----

If the ``use_pathlib=True`` option is pass to the ``load`` function,
file and directory paths will be converted to ``pathlib`` Path
objects.


.. include:: ../test/samples/docs-sample.ini
    :code: ini
    :start-after: # coerce-paths
    :end-before:  # coerce-paths-end


.. ipython:: python
    :okexcept:
    :okwarning:

    cfg = conficus.load('test/samples/docs-sample.ini', use_pathlib=True)
    cfg['unix-file-path']
    cfg['windows-file-path']
