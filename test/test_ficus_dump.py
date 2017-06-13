import ficus
from collections import OrderedDict
from datetime import datetime


default_config = OrderedDict({
    'section': {
        'value': 'hello',
        'subsection': {
            'value': 'goodbye',
            'three': {
                'repeat': datetime(2017, 5, 28, 10, 10, 10)
            }
        }
    },
    'section.two': {
        'value': 2
    }
})


def test_dump_section():
    ini = ficus.format_dict(default_config)

    assert ini == ('[section]\n'
                   'value = hello\n'
                   '[section.subsection]\n'
                   'value = goodbye\n'
                   '[section.subsection.three]\n'
                   'repeat = 2017-05-28 10:10:10\n'
                   '[section.two]\n'
                   'value = 2')
