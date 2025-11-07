import conficus
from conficus.format import pprint

CFG = '''
debug = true
password = "50m3Th1NGS3Kr!T"
[numbers.integer]
value = 1

[numbers.float]
value = 2.0

[sequence.empty-list]
value = []

[sequence.empty-tuple]
value = [] 

[sequence.lists]
short = [1, 2, 3, 4]
long = ["Abagail had short hair",
   "Johnathan wore his far too long",
   "Isabelle was terribly frightened of very small horses",
   "And Henry ate the canned beans until they were all gone!"]

[datetimes.datetime]
value = 2017-05-31T10:00:00

[datetimes.date]
value = 2017-05-31

[datetimes.time]
value = 10:15:02

[strings]
short_string = "unquoted string"
string_with_spaces = " a quoted string preserves white space "
text = """This is a much longer text block
    that we want to preserve but keep
    readable in our configuration file.
    We can used this for email body
    text, and things like that."""

'''


def test_config_format():
    config = conficus.load(CFG)
    assert (
        pprint(config)
        == """[config] debug: True
[config] password: **********
[config] numbers.integer.value: 1
[config] numbers.float.value: 2.0
[config] sequence.lists.short.0: 1
[config] sequence.lists.short.1: 2
[config] sequence.lists.short.2: 3
[config] sequence.lists.short.3: 4
[config] sequence.lists.long.0: Abagail had short hair
[config] sequence.lists.long.1: Johnathan wore his far too long
[config] sequence.lists.long.2: Isabelle was terribly frightened of very small horses
[config] sequence.lists.long.3: And Henry ate the canned beans until they were all gone!
[config] datetimes.datetime.value: 2017-05-31 10:00:00
[config] datetimes.date.value: 2017-05-31
[config] datetimes.time.value: 10:15:02
[config] strings.short_string: unquoted string
[config] strings.string_with_spaces:  a quoted string preserves white space 
[config] strings.text: This is a much longer text block
    that we want to preserve but keep
    readable in our configuration file.
    We can used this for email body
    text, and things like that."""
    )
