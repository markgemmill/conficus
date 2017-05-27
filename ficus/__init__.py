import re
from functools import wraps
from collections import OrderedDict


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

    def skip_null(func):
        @wraps(func)
        def _skip_null(line, cur_sec, cur_opt, cfg_dct, document):
            if line is None:
                return line, cur_sec, cur_opt
            return func(line, cur_sec, cur_opt, cfg_dct, document)
        return _skip_null

    @skip_null
    def _parse_section(line, cur_sec, cur_opt, cfg_dct, document):
        match = rx_section(line)
        if match:
            section_name = match['section'].strip()
            section_heirarchy = section_name.split('.')
            section_dict = cfg_dct
            for section in section_heirarchy:
                section_dict = section_dict.setdefault(section, OrderedDict())
            cfg_dct[section_name] = section_dict
            document.append(('section', line, section_name, section_dict))
            return None, section_dict, cur_opt
        # if this is not a match, return values
        return line, cur_sec, cur_opt

    @skip_null
    def _parse_option(line, cur_sec, cur_opt, cfg_dct, document):
        match = rx_option(line)
        if match:
            key = match['key'].strip()
            value = match['value']
            cur_sec[key] = value
            return None, cur_sec, key
        return line, cur_sec, cur_opt

    @skip_null
    def _parse_multiline_opt(line, cur_sec, cur_opt, cfg_dct, document):
        match = rx_multiline(line)
        if match:
            value = cur_sec.get(cur_opt, None)
            if value is None:
                raise Exception('Invalid indentation at: {}'.format(line))
            if not isinstance(value, list):
                value = [value]
                cur_sec[cur_opt] = value
            value.append(line.lstrip())
            return None, cur_sec, cur_opt
        return line, cur_sec, cur_opt

    @skip_null
    def _parse_comment(line, cur_sec, cur_opt, cfg_dct, document):
        match = rx_comment(line)
        if match:
            comment = match['comment'].rstrip()
            document.append(('comment', line, None, None))
            return None, cur_sec, cur_opt
        return line, cur_sec, cur_opt

    @skip_null
    def _parse_unknown(line, cur_sec, cur_opt, cfg_dct, document):
        line = line if line is None else line.rstrip()
        document.append((None, line, None, None))
        return line, cur_sec, cur_opt

    parsers = (_parse_option,
               _parse_multiline_opt,
               _parse_section,
               _parse_comment,
               _parse_unknown)

    cfg_dct = OrderedDict()
    cfg_lst = []
    cur_sec = cfg_dct
    cur_opt = None
    line_index = 0

    while config_lines:

        line = rmv_crlf(config_lines.pop(0))
        line_index += 1

        print '-'*60
        print line_index, line

        for parser in parsers:

            print line_index, parser, '`{}`'.format(line)
            print line_index, cur_opt, cur_sec

            line, cur_sec, cur_opt = parser(line, cur_sec, cur_opt, cfg_dct, cfg_lst)

            if line is None:
                print line_index, 'parsed', cur_opt, cur_sec
                break

    print cfg_dct

    return cfg_lst, cfg_dct
