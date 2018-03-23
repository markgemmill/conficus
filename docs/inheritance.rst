Inheritence
~~~~~~~~~~~

Section's are related via dot `.` notation of there names. `[email]` would be
a parent section, whereas `[email.notify]` and `[email.errors]` would be
children sections.

Section inheritence is an option to push parent section values onto
child sections.

Section inheritance is by default off. To turn it on,
pass the ``inheritance=True`` option:

.. ipython:: python
    :okexcept:
    :okwarning:

    import conficus

    INI = """
    [email]
    server = smtp.server.com
    [email.notify]
    to = notify@home.biz
    subject = Notification from Ficus
    [email.errors]
    to = admin@home.biz
    subject = Fatal Error Has Occurred
    """

    cfg = conficus.load(INI, inheritance=True)


With inheritance turned on, our example sections ``email.errors`` and
``email.notify`` will now both contain the ``server`` configuration value:

.. ipython:: python
    :okexcept:
    :okwarning:

    # our parent section has a server option:

    cfg['email.server']

    # this option is now available on the child sections:

    cfg['email.errors.server']
    cfg['email.notify.server']
