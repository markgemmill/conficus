import sys
import copy
from datetime import datetime
from decimal import Decimal  # noqa
from .parse import matcher, substituter
from .structs import DoubleLinkedDict


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


def coerce_none(value):
    return None


WINDOWS_PATH_REGEX = r'^(?P<value>[a-z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*)$'
UNIX_PATH_REGEX = r'^(?P<value>(/[^\0/]*)*)$'


def coerce_path():

    def _coerce_path(value):
        return Path(value)

    if sys.version_info.major >= 3 and sys.version_info.minor >= 4:
        from pathlib import Path
        return _coerce_path
    else:  # pragma: no cover
        try:
            from pathlib2 import Path
            return _coerce_path
        except Exception:
            raise Exception('pathlib module is unavailable on your system.')


coerce_float = (matcher(r'^(?P<value>\d+\.\d+)$'), float)
coerce_decimal = (matcher(r'^(?P<value>\d+\.\d+)$'), Decimal)
coerce_win_path = (matcher(WINDOWS_PATH_REGEX), coerce_path())
coerce_unx_path = (matcher(UNIX_PATH_REGEX), coerce_path())
coerce_string = (matcher(r'^(?P<value>("{1,3})?.*("{1,3})?)\s*$'), coerce_str)



def coerce_single_line(value, coercers):
    # the match object here may not always
    # return the same thing -
    # TODO: fix this - sometimes it will be a regex matcher
    # that returns a groupdict or else it might be a different
    # function....
    for match, convert in coercers.iter_values():
        m = match(value)

        if isinstance(m, dict):
            value = m.get('value', value)
        if m:
            return convert(value)
    # this should never return, but is here for safety
    return value  # pragma: no cover


def match_iterable(start_bracket, end_bracket):

    def _match_iterable(value):
        return value.startswith(start_bracket) and value.endswith(end_bracket)

    return _match_iterable


def coerce_iterable(coercers, use_tuple=False):

    def _coerce_iterable(value):
        value = value[1:-1]

        if not value and use_tuple is False:
            return []
        elif not value:
            return tuple()

        iterable = [coerce_single_line(v.strip(), coercers) for v
                    in value.split(',')]
        if use_tuple:
            iterable = tuple(iterable)

        return iterable

    return _coerce_iterable


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
    # TODO: implement this?


def build_coercers():

    coercers = DoubleLinkedDict()

    coercers['none'] = (matcher(r'^(?P<value> *)$'), coerce_none)
    coercers['int'] = (matcher(r'^(?P<value>\d+)$'), int)
    coercers['float'] = coerce_float
    coercers['bool'] = (matcher(r'^(?P<value>(true|false|yes|no))\s*$'), coerce_bool)
    coercers['datetime'] = (matcher(r'^(?P<value>\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d)\s*$'),
                            coerce_datetime('%Y-%m-%dT%H:%M:%S'))
    coercers['date'] = (matcher(r'^(?P<value>\d{4}-\d\d-\d\d)\s*$'),
                        coerce_datetime('%Y-%m-%d'))
    coercers['time'] = (matcher(r'^(?P<value>\d\d:\d\d:\d\d)\s*$'),
                        coerce_datetime('%H:%M:%S'))
    coercers['string'] = coerce_string

    match_single_line_list = match_iterable('[', ']')
    match_single_line_tuple = match_iterable('(', ')')

    coerce_single_line_list = coerce_iterable(coercers)
    coerce_single_line_tuple = coerce_iterable(coercers, use_tuple=True)

    coercers.prepend('list', (match_single_line_list, coerce_single_line_list))
    coercers.prepend('tuple', (match_single_line_tuple, coerce_single_line_tuple))

    return coercers


def coerce_multiline(value, coercers):

    sub_new_line = substituter(r'[\r\n]+$', '')
    sub_line_ending = substituter(r'\\ *$', '\n')
    sub_line_beginning = substituter(r'^ *\|', '')

    if match_multiline_list(value):
        value[0] = value[0].lstrip('[')
        value[-1] = value[-1].rstrip(']')
        value = [v.strip().rstrip(',') for v in value]
        return [coerce_single_line(v, coercers)
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


def coerce(config, **kwargs):

    simple_coercers = build_coercers()

    if kwargs.get('pathlib', False) is True:
        simple_coercers.insert_before('string', 'win_path', coerce_win_path)
        simple_coercers.insert_before('string', 'unx_path', coerce_unx_path)

    if kwargs.get('decimal', False) is True:
        simple_coercers.replace('float', coerce_decimal)

    for cfg_obj in config.walk_values():
        if cfg_obj.multiline:
            cfg_obj.end_value = coerce_multiline(cfg_obj.raw_value, simple_coercers)
        else:
            cfg_obj.end_value = coerce_single_line(cfg_obj.value,
                                                   simple_coercers)
    return copy.deepcopy(config)
