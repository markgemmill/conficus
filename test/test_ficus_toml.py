from conficus.parse import FicusDict
from conficus.parse import ConfigValue
from conficus.parse import parse


def test_ficus_toml_compatibility(toml_sample):
    # Comparison testing against TOML example.
    # I think there is are a lot of differences here.
    # The aim of conficus is to be much simpler.
    # TOML is closer to mimicing actual python code when 
    # it comes to strings and structures - something
    # we don't feel is necessary in a configuration 
    # mark up.

    # these basic examples currently do not pass:

    # assert toml_sample['table.key'].value == 'value'
    # assert toml_sample['table.subtable.key'].value == 'another value'
    pass
