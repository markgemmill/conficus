'''
The ficus API.

ficus.init()

config = ficus.load(config_file)


'''
import re
from functools import wraps
from collections import OrderedDict


class FicusDict(OrderedDict):
    '''
    FicusDict is an override of standard dictionary 
    to allow dot-named access to nested dictionary 
    values, so this call:

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


def read_config(file_path):
    with open(file_path) as fh_:
        return fh_.readlines()


class ConfigValue(object):

    def __init__(self, full_name, raw_value):
        self.full_name = full_name
        self.raw_value = raw_value
        self._split_name(full_name)
        self.multiline = [] 

    @property
    def is_multiline(self):
        return len(self.multiline) > 0

    def _split_name(self, full_name):
        segments = full_name.split('.')
        self.name = segments[-1]
        self.section = '.'.join(segments[:-1])

    def add_multiline(self, value):
        # we don't know if a value is multiline until it is parsed.
        if not self.multiline:
            self.multiline.append(self.raw_value)
        self.multiline.append(value)

    @property
    def value(self):
        return self.raw_value
         

def parse_raw(config_lines):
    '''
    Read the raw config file text, and parse into text only sections
    and key values.

    '''
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
            cv = ConfigValue(key, value)
            parm['current_section'][key] = cv
            parm['current_option'] = cv
            return None
        return line

    def parse_multiline_opt(line, parm):
        match = rx_multiline(line)
        if match:
            if parm['current_option'] is None:
                raise Exception('Invalid indentation at: {}'.format(line))
            parm['current_option'].add_multiline(match['value'])
            return None
        return line

    def parse_comment(line, parm):
        match = rx_comment(line)
        if match:
            return None
        return line

    def parse_unknown(line, parm):
        return None

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


def push_inheritence(config):
    def _inherit(options, section):
        # first inherit any options
        # that do not exist
        for key, val in options.items():
            if key not in section:
                section[key] = val
        # next collect all current options
        # on the section
        section_options = {} 
        for key, val in section.items():
            if isinstance(val, ConfigValue):
                section_options[key] = val
        # finally, push down the sections options
        # to all its sub-sections
        for key, val in section.items():
            if isinstance(val, FicusDict):
                _inherit(section_options, val)

    _inherit({}, config)


# string
# integer
# float
# url
# path
# multiline handling
# list

