Nested Sections
~~~~~~~~~~~~~~~

``conficus`` uses nested sections. Nested section are defined when section
names contain dots ".".


Here we have an ``email`` section that has two child sections ``notify`` and ``errors``.

.. include:: docs-sample.ini
    :code: ini
    :start-after: # nested-sections-sample
    :end-before: # nested-sections-end

Let's load our example file :doc:`sample-doc.ini </sample-doc>`.

.. ipython:: python
    :okexcept:
    :okwarning:

    cfg = conficus.load('docs/docs-sample.ini')

The resulting configuration object is a dictionary, so these nested
sections can be accessed as such:

.. ipython:: python
    :okexcept:
    :okwarning:

    cfg['email']['server']
    cfg['email']['notify']['to']


However, you can also access the section by its full name:

.. ipython:: python
    :okexcept:
    :okwarning:

    cfg['email.notify.to']
