import copy
from itertools import chain
from datetime import datetime
from .parse import matcher, substituter


def coerce_single_line(value, *coercers):
    for match, convert in chain(*coercers):
        if match(value):
            return convert(value)
    # this should never return, but is here for safety
    return value # pragma: no cover


def coerce_bool(value):
    if value.lower() in ('true', 'yes', 'y', 't'):
        return True
    return False


def coerce_datetime(date_fmt):
    def _coerce_datetime(value):
        return datetime.strptime(value, date_fmt)
    return _coerce_datetime


def coerce_str(value):
    return value.strip('"')


simple_coercers = [
    (matcher(r'^(?P<value>\d+)$'), int),
    (matcher(r'^(?P<value>\d+\.\d+)$'), float),
    (matcher(r'^(?P<value>(true|false|yes|no|y|n|t|f))$'), coerce_bool),
    (matcher(r'^(?P<value>\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d)$'),
             coerce_datetime('%Y-%m-%dT%H:%M:%S')),
    (matcher(r'^(?P<value>\d{4}-\d\d-\d\d)$'),
             coerce_datetime('%Y-%m-%d')),
    (matcher(r'^(?P<value>\d\d:\d\d:\d\d)$'),
             coerce_datetime('%H:%M:%S')),
    (matcher(r'^(?P<value>("{1,3})?.*("{1,3})?) *$'), coerce_str)]


def match_single_line_list(value):
    return value.startswith('[') and value.endswith(']')


def coerce_single_line_list(value):
    value = value.lstrip('[').rstrip(']')
    if not value:
        return []
    return [coerce_single_line(v.strip(), simple_coercers) for v
            in value.split(',')]




list_coercers = [(match_single_line_list, coerce_single_line_list)]


def match_multiline_list(value):
    return value[0].startswith('[') and value[-1].endswith(']')


def match_multiline_str(value):
    return value[0].startswith('"""') and value[-1].endswith('"""')


def coerce_single_line_str(value):
    '''
    Multiline strings have two options:

        1. Preserve new lines with the back slash:

            value = """A new value \
                and something else \
                to boot.
            """

            A new value 
            and something else
            to boot.

        2. Preserve left spacing with the pipe:

            value = """A new value \
                |   it's true."""

           A new value 
              it's true.

    '''

sub_new_line = substituter(r'[\r\n]+$', '')
sub_line_ending = substituter(r'\\ *$', '\n')
sub_line_beginning = substituter(r'^ *\|', '')

def coerce_multiline(value, *coercers):

    if match_multiline_list(value):
        value[0] = value[0].lstrip('[')
        value[-1] = value[-1].rstrip(']')
        value = [v.strip().rstrip(',') for v in value]
        return [coerce_single_line(v, list_coercers, simple_coercers, *coercers)
                for v in value if v]

    elif match_multiline_str(value):
        value[0] = value[0].lstrip('"')
        value[-1] = value[-1].rstrip('"')
        # remove blank first line
        if value[0].strip() == '':
            value.pop(0)
        value = [sub_new_line(v) for v in value]
        value = [sub_line_ending(v) for v in value]
        value = [sub_line_beginning(v) for v in value]
        return ''.join(value)

    else:
        return '\n'.join(value)


def coerce(config, *coercers):

    for cfg_obj in config.walk_values():
        if cfg_obj.multiline:
            cfg_obj.end_value = coerce_multiline(cfg_obj.raw_value, *coercers)
        else:
            cfg_obj.end_value = coerce_single_line(cfg_obj.value,
                                                   list_coercers,
                                                   simple_coercers,
                                                   *coercers)
    return copy.deepcopy(config)
