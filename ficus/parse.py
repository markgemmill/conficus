import re
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
