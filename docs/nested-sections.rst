Nested Sections
~~~~~~~~~~~~~~~

``conficus`` has nested sections. Nested section are defined by section
names containing dots ".". In the following example, ``email`` is the
parent section and ``notify`` and ``errors`` are subsections:

.. code:: python

    >>> INI = '''
    ... [email]
    ... server = smtp.server.com
    ... 
    ... [email.notify]
    ... to = notify@home.biz
    ... subject = Notification from Ficus
    ... 
    ... [email.errors]
    ... to = admin@home.biz
    ... subject = Fatal Error Has Occurred'''
    ... 
    >>> cfg = ficus.load(INI)
    >>> 

The resulting configuration object is a dictionary, so these nested
sections can be accessed as such:

.. code:: python

    >>> cfg['email']['server']
    'smtp.server.com'
    >>> 
    >>> cfg['email']['notify']['to']
    'notify@home.biz'
    >>> 

However, you can also access the section by its full name:

.. code:: python

    >>> cfg['email.notify.to']
    'notify@home.biz'
    >>> 


