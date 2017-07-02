### Section Inheritence

Section inheritence is an option to push parent section values onto child sections. Section inheritance is by default off. To turn it on, pass the `inheritance=True` option:

```python
>>> 
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
>>> # use the inheritence option:
... 
>>> cfg = ficus.load(INI, inheritence=True)
>>>
```

With inheritance turned on in our example, section `email.errors` and `email.notify` will both have the `server` configuration value added to them:

```python
>>> # our parent section has a server option:
... 
>>> cfg['email.server']
>>> 'smtp.server.com'
>>>  
>>> # this option is now available on the child sections:
>>> ...
>>> cfg['email.errors.server']
>>> 'smtp.server.com'
>>> 
>>> cfg['email.notify.server']
>>> 'smtp.server.com'
```
