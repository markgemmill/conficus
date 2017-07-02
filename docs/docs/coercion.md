### Automatic Coercing of Values

`conficus` will automatically coerce ini values of the following types:

```python
>>> import conficus as ficus
```

#### Strings

Anything that does not fall into the below types is considered a string:

```python
>>> cfg = ficus.load("string=A wealthy gentleman waved his umbrella.")
>>> cfg['string']
'A wealthy gentleman waved his umbrella.'
```

#### Integers

Numbers represented with no decimal will convert to integers: 

```python
>>> cfg = ficus.load("integer = 102")
>>> cfg["integer"]
102
```

#### Floats
Numbers with decimals will convter to floats: 

```python
>>> cfg = ficus.load("float=10.12")
>>> cfg['float']
10.12
```

#### Booleans

True/False values will convert to boolean:

```python
>>> cfg = ficus.load("booleans=[T, t, Y, yes, true]")
>>> cfg['booleans']
[True, True, True, True, True]

>>> cfg = ficus.load("booleans=[F, f, N, no, false]")
>>> cfg['booleans']
[False, False, False, False, False]
```

#### DateTimes

Date and time values will convert to a datetime:

```python
>>> cfg = ficus.load("datetime=2017-10-12T10:12:09")
>>> cfg["datetime"]
datetime.datetime(2017, 10, 12, 10, 12, 9)
```

#### Dates

Date values will convert to datetime:

```python
>>> cfg = ficus.load("datetime=2017-10-12")
>>> cfg["datetime"]
datetime.datetime(2017, 10, 12, 0, 0)
```

#### Times
Time values will convert to datetime:

```python
>>> cfg = ficus.load("time=10:12:09")
>>> cfg['time']
datetime.datetime(1900, 1, 1, 10, 12, 9)
```

#### Lists

Any value that begins and ends with "[" and "]" will be viewed as a list whose content 
will be split on "commas":

```python
>>> cfg = ficus.load("single-line-list=[99, 66, 84, 9, bill]")
>>> cfg['single-line-list']
[99, 66, 84, 9, 'bill']
```

Any multiline value that ends and begins with "[" and "]" will be viewed as a list
whose contents will be split on the new line:

```python
>>> cfg = ficus.load('''multiline-list=[Herb
...     Mary
...     John
...     Sarah]''')
>>> cfg['multiline-list']
['Herb', 'Mary', 'John', 'Sarah']
```

Commas are optional, but if used they are striped:

```python
>>> cfg = ficus.load('''multiline-list=[Herb,
...     Mary,
...     John,
...     Sarah]''')
>>> cfg['multiline-list']
['Herb', 'Mary', 'John', 'Sarah']
```
