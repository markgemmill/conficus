'''
The ficus API.

ficus.init()

config = ficus.load(config_file)


'''
import re
import copy
from os import path
from itertools import chain
from datetime import datetime
from collections import OrderedDict


class FicusDict(OrderedDict):
    '''
    FicusDict is an override of standard dictionary
    to allow dot-named access to nested dictionary
    values.

    The standard nested call:

        config['parent']['child']

    can also be accessed as:

        config['parent.child']

    '''
    def __getitem__(self, key):
        if '.' not in key:
            return super(FicusDict, self).__getitem__(key)
        segments = key.split('.')
        end = self
        for seg in segments:
            end = super(FicusDict, end).__getitem__(seg)
        return end

    def __contains__(self, key):
        if '.' not in key:
            return super(FicusDict, self).__contains__(key)
        segments = key.split('.')
        end = self
        contains = False
        for seg in segments:
            contains = super(FicusDict, end).__contains__(seg)
            if not contains:
                return contains
            end = super(FicusDict, end).__getitem__(seg)
        return contains

    def values(self):
        _values = []

        def _recurse(section, v):
            for key, val in section.items():
                if isinstance(val, FicusDict):
                    _recurse(val, v)
                if isinstance(val, ConfigValue):
                    v.append(val)

        _recurse(self, _values)

        return _values


class ReadOnlyDict(FicusDict):

    def __init__(self, src):
        super(ReadOnlyDict, self).__init__(src)
        self.readonly = True

    def __setitem__(self, key, item):
        if hasattr(self, 'readonly'):
            raise TypeError('Key `{}` is read only!'.format(key))
        if isinstance(item, FicusDict):
            item = ReadOnlyDict(item)
        return super(ReadOnlyDict, self).__setitem__(key, item)

    def __delitem__(self, key):
        raise TypeError

    def clear(self):
        raise TypeError

    def pop(self, key, *args):
        raise TypeError

    def popitem(self):
        raise TypeError


def matcher(regex):
    rx = re.compile(regex, re.I)

    def _matcher(line):
        m = rx.match(line)
        if m:
            return m.groupdict()

    return _matcher


def substituter(regex, sub):
    rx = re.compile(regex, re.I)

    def _substituter(line):
        line = rx.sub(sub, line)
        return line

    return _substituter


class ConfigValue(object):

    def __init__(self, initial_value):
        self.raw_value = [initial_value]
        self.end_value = None

    def add(self, value):
        self.raw_value.append(value)

    @property
    def multiline(self):
        return len(self.raw_value) > 1

    @property
    def value(self):
        if self.multiline:
            return '\n'.join(self.raw_value)
        if self.raw_value:
            return str(self.raw_value[0])

    def __deepcopy__(self, memo):
        return self.end_value


rx_section = matcher(r'^\[(?P<section>[^\]]+)\].*$')
rx_comment = matcher(r'^ *(#|;)(?P<comment>.*)$')
rx_option = matcher(r'^ *(?P<key>\S*)( ?= ?|: )(?P<value>.*)$')
rx_multiline = matcher(r'^    *(?P<value>[^#;].*)$')
rmv_crlf = substituter(r'[\r\n]', '')


def parse_section(line, parm):
    match = rx_section(line)
    if match:
        section_name = match['section'].strip()
        section_heirarchy = section_name.split('.')
        section_dict = parm['config']
        for section in section_heirarchy:
            section_dict = section_dict.setdefault(section, FicusDict())
        parm['current_section'] = section_dict
        return None

    return line


def parse_option(line, parm):
    match = rx_option(line)
    if match:
        key = match['key'].strip()
        value = match['value']
        cv = ConfigValue(value)
        parm['current_section'][key] = cv
        parm['current_option'] = cv
        return None
    return line


def parse_multiline_opt(line, parm):
    match = rx_multiline(line)
    if match:
        if parm['current_option'] is not None:
            parm['current_option'].add(match['value'])
        return None
    return line


def parse_comment(line, parm):
    match = rx_comment(line)
    if match:
        return None
    return line


def parse_unknown(line, parm):
    return None


def parse(config_lines):
    '''
    Read the raw config file text, and parse into text only sections
    and key values.

    '''
    parsers = (parse_option,
               parse_multiline_opt,
               parse_section,
               parse_comment,
               parse_unknown)

    config = FicusDict()

    parm = {
        'config': config,
        'current_section': config,
        'current_option': None,
    }

    while config_lines:

        line = rmv_crlf(config_lines.pop(0))

        for parser in parsers:
            line = parser(line, parm)

            if line is None:
                break

    return config


def inherit(config):
    '''
    ficus.inherit pushes the configuration values of
    parent section down to its child sections.

    This can be used as a way of simplifying config usage. For example:

    [email]
    server=smtp.location.com
    user=SMTPUSR
    password=CKrit
    from=smtp@location.com

    [email.notifications]
    to=[peter@boondoggle.ca, liz@boondoggle.ca]
    subject=The Subject of Notification
    body=notification_template.txt

    [email.errors]
    to=[errors@boondoggle.ca]
    subject=[Alert] Error
    body=error_template.txt

    '''
    def _inherit(inheritable_options, section):
        # first inherit any options
        # that do not exist
        for key, val in inheritable_options.items():
            if key not in section:
                section[key] = val
        # next collect all current options
        # on the section
        section_options = {}
        for key, val in section.items():
            if not isinstance(val, FicusDict):
                section_options[key] = val
        # finally, push down the sections options
        # to all its sub-sections
        for key, val in section.items():
            if isinstance(val, FicusDict):
                _inherit(section_options, val)

    _inherit({}, config)

    return config


def coerce_single_line(value, *coercers):
    for match, convert in chain(*coercers):
        if match(value):
            return convert(value)
    return value


def coerce_bool(value):
    if value.lower() in ('true', 'yes', 'y', 't'):
        return True
    return False


def coerce_datetime(date_fmt):
    def _coerce_datetime(value):
        return datetime.strptime(value, date_fmt)
    return _coerce_datetime


simple_coercers = [
    (matcher(r'^(?P<value>\d+)$'), int),
    (matcher(r'^(?P<value>\d+\.\d+)$'), float),
    (matcher(r'^(?P<value>(true|false|yes|no|y|n|t|f))$'), coerce_bool),
    (matcher(r'^(?P<value>\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d)$'),
     coerce_datetime('%Y-%m-%dT%H:%M:%S')),
    (matcher(r'^(?P<value>\d{4}-\d\d-\d\d)$'),
     coerce_datetime('%Y-%m-%d')),
    (matcher(r'^(?P<value>\d\d:\d\d:\d\d)$'),
     coerce_datetime('%H:%M:%S'))]


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


def coerce_multiline(value, *coercers):
    if match_multiline_list(value):
        value[0] = value[0].lstrip('[')
        value[-1] = value[-1].rstrip(']')
        value = [v.strip().rstrip(',') for v in value]
        return [coerce_single_line(v, simple_coercers, list_coercers, *coercers)
                for v in value if v]
    return '\n'.join(value)


def coerce(config, *coercers):

    for cfg_obj in config.values():
        if cfg_obj.multiline:
            cfg_obj.end_value = coerce_multiline(cfg_obj.raw_value, *coercers)
        else:
            cfg_obj.end_value = coerce_single_line(cfg_obj.value,
                                                   simple_coercers,
                                                   list_coercers,
                                                   *coercers)
    return copy.deepcopy(config)


def read_config(config_input):
    if path.exists(config_input):
        with open(config_input, 'r') as fh_:
            return fh_.readlines()
    return config_input.split('\n')


def load(config_path, inheritance=False, readonly=True):

    config = parse(read_config(config_path))

    config = coerce(config)

    if inheritance is True:
        config = inherit(config)

    if readonly is True:
        config = ReadOnlyDict(config)

    return config


def format_dict(defaults):
    if not isinstance(defaults, dict):
        raise Exception('Ficus requires a dict to write to file.')

    output = []

    def _recurse(src, parent=''):
        sections = []
        values = []
        for key, val in src.items():
            if isinstance(val, dict):
                sections.append((key, val))
            else:
                values.append((key, val))

        if len(values) > 0:
            output.append('[{}]'.format(parent))

        for key, val in values:
            output.append('{} = {}'.format(key, val))

        for key, val in sections:
            _recurse(val, (parent + '.' + key).strip('.'))

    _recurse(defaults)

    return '\n'.join(output)
